# Source_Code/detect_parking.py
import os
import pickle
import cv2

WIDTH, HEIGHT = 107, 48
THRESH = 900

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "Assets")

# Pickle file for parking positions
pkl_path = os.path.join(ASSETS, "CarParkPos.pkl")
with open(pkl_path, "rb") as f:
    posList = pickle.load(f)

# Video file
video_candidates = ["carPark.mp4", "CarPark.mp4"]
video_path = None
for name in video_candidates:
    p = os.path.join(ASSETS, name)
    if os.path.exists(p):
        video_path = p
        break

def analyze_frame(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    slot_status = []
    for idx, pos in enumerate(posList, start=1):
        x, y = pos
        imgCrop = imgDilate[y:y+HEIGHT, x:x+WIDTH]
        count = cv2.countNonZero(imgCrop)
        status = "available" if count < THRESH else "occupied"
        slot_status.append({"slot_number": f"S{idx}", "status": status, "count": int(count)})
    return slot_status

# Function for Django to call
def analyze_parking():
    """
    Returns list of dicts: [{'slot_number': 'S1', 'status': 'available'}, ...]
    Uses first frame of video or dummy if no video.
    """
    if video_path:
        cap = cv2.VideoCapture(video_path)
        success, img = cap.read()
        cap.release()
        if success:
            return analyze_frame(img)
    # fallback: return all available if no video
    return [{"slot_number": f"S{idx}", "status": "available", "count": 0} for idx in range(1, len(posList)+1)]

# Only run video window if executed directly
if __name__ == "__main__":
    if not video_path:
        print("No video found")
        exit(1)
    cap = cv2.VideoCapture(video_path)
    while True:
        success, img = cap.read()
        if not success:
            print("End of video")
            break
        slots = analyze_frame(img)
        for idx, pos in enumerate(posList, start=1):
            x, y = pos
            status = slots[idx-1]["status"]
            color = (0,255,0) if status=="available" else (0,0,255)
            thickness = 4 if status=="available" else 2
            cv2.rectangle(img, pos, (x+WIDTH, y+HEIGHT), color, thickness)
        free = sum(1 for s in slots if s["status"]=="available")
        cv2.putText(img, f"Free: {free}/{len(posList)}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
        cv2.imshow("Parking Detection", img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
