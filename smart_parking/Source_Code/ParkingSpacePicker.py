import cv2
import pickle
import os

width, height = 107, 48
img_path = "Assets/carParkImg.png"
pkl_path = "Assets/CarParkPos.pkl"

# Load existing positions
if os.path.exists(pkl_path):
    with open(pkl_path, 'rb') as f:
        posList = pickle.load(f)
else:
    posList = []

def mouseClick(events, x, y, flags, params):
    global posList
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        posList = [pos for pos in posList if not (pos[0] < x < pos[0]+width and pos[1] < y < pos[1]+height)]
    
    with open(pkl_path, 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Image not found at", img_path)
        break

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cv2.destroyAllWindows()

print("Saving to:", pkl_path)
