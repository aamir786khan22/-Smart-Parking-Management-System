import pickle
import os

pkl_path = os.path.join("Assets", "CarParkPos.pkl")

if os.path.exists(pkl_path):
    with open(pkl_path, "rb") as f:
        posList = pickle.load(f)
    print("Vacant Slot Coordinates:", posList)
else:
    print("No CarParkPos.pkl found. Run ParkingSpacePicker.py first.")
