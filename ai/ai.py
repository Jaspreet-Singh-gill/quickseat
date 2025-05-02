import requests
import cv2
import numpy as np
from collections import deque
from ultralytics import YOLO

# Configuration
VIDEO_SOURCE = 'http://100.71.9.85:8080/video'
ENTRY_API_URL = 'http://192.168.198.63:8000/person_in'
EXIT_API_URL = 'http://192.168.198.63:8000/person_out'
DIST_THRESHOLD = 50
DISAPPEAR_FRAMES = 15  # frames after which a person is considered gone
X_MOVEMENT_THRESHOLD = 50  # Horizontal movement threshold (adjust as necessary)
MAX_HISTORY = 10

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Open video
cap = cv2.VideoCapture(VIDEO_SOURCE)

# Tracking
track_history = {}     # {id: deque of (x, y)}
last_seen = {}         # {id: frame_index}
track_status = {}      # {id: 'entry'/'exit'}
next_id = 0
frame_index = 0

# API calls
def on_entry(track_id):
    print(f"[ENTRY] Person {track_id}")
    try:
        requests.get(ENTRY_API_URL)
    except Exception as e:
        print("Entry API Error:", e)

def on_exit(track_id):
    print(f"[EXIT] Person {track_id}")
    try:
        requests.get(EXIT_API_URL)
    except Exception as e:
        print("Exit API Error:", e)

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_index += 1
    results = model(frame, classes=[0])
    detections = results[0].boxes.xyxy.cpu().numpy()
    centers = []

    for box in detections:
        x1, y1, x2, y2 = map(int, box[:4])
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
        centers.append((cx, cy))

    matched_ids = set()

    # Match or assign new IDs
    for center in centers:
        matched_id = None
        for tid, history in track_history.items():
            if euclidean(center, history[-1]) < DIST_THRESHOLD:
                matched_id = tid
                break

        if matched_id is None:
            matched_id = next_id
            track_history[matched_id] = deque(maxlen=MAX_HISTORY)
            next_id += 1

        track_history[matched_id].append(center)
        last_seen[matched_id] = frame_index
        matched_ids.add(matched_id)

    # Check for disappeared IDs and evaluate entry/exit
    for tid in list(track_history.keys()):
        if tid not in matched_ids and (frame_index - last_seen.get(tid, 0)) > DISAPPEAR_FRAMES:
            history = track_history[tid]
            if len(history) >= 5:
                # Calculate horizontal movement (left-right movement)
                x_movement = history[-1][0] - history[0][0]

                # If the person has moved horizontally enough
                if x_movement < -X_MOVEMENT_THRESHOLD:  # Moving left (entry)
                    if tid not in track_status:  # Ensure entry is counted only once
                        on_entry(tid)
                        track_status[tid] = 'entry'
                elif x_movement > X_MOVEMENT_THRESHOLD:  # Moving right (exit)
                    if tid not in track_status:  # Ensure exit is counted only once
                        on_exit(tid)
                        track_status[tid] = 'exit'

    # Draw visualization
    for tid, history in track_history.items():
        if history:
            cx, cy = history[-1]
            color = (0, 255, 0) if tid not in track_status else (255, 0, 0)
            label = f"ID {tid}"
            if tid in track_status:
                label += f" ({track_status[tid]})"
            cv2.circle(frame, (cx, cy), 5, color, -1)
            cv2.putText(frame, label, (cx + 5, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Draw Entry and Exit counts on frame
    cv2.putText(frame, f"Entries: {sum(1 for status in track_status.values() if status == 'entry')}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Exits: {sum(1 for status in track_status.values() if status == 'exit')}", (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Entry/Exit Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
