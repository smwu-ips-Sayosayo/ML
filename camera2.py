import cv2
import math
from ultralytics import YOLO
import mediapipe as mp

# YOLO 모델 불러오기 (로컬 경로 사용)
model = YOLO('snack.pt')

# Mediapipe 손 인식 초기화
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

# 손가락 인덱스 비교
compareIndex = [[4, 6], [6, 8], [10, 12], [14, 16], [18, 20]]

# 손가락 4개 접혀있을 때 "Grap" 표시
gesture = [
    [False, False, False, False, "Grap"]
]

# 비디오 캡처 초기화
def process_stream(frame):
    h, w, c = frame.shape
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)

    # Mediapipe 결과 디버깅 출력
    if results.multi_hand_landmarks:
        print("Mediapipe Hand Landmarks detected")
    else:
        print("No Hand Landmarks detected")

    # YOLO 객체 검출
    yolo_results = model(frame)

    # 손 인식 및 바운딩 박스 그리기
    overlapping_objects = set()
    recognized_objects = []
    hand_present = False

    if results.multi_hand_landmarks:
        hand_present = True
        for handLms in results.multi_hand_landmarks:
            # 바운딩 박스 좌표 초기화
            x_min, y_min = w, h
            x_max, y_max = 0, 0

            for lm in handLms.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)

            # 손과 겹치는 객체 검출
            for result in yolo_results[0].boxes:
                x1, y1, x2, y2 = map(int, result.xyxy[0])
                conf = result.conf[0]
                cls = int(result.cls[0])
                if x1 < x_max and x2 > x_min and y1 < y_max and y2 > y_min:
                    overlapping_objects.add(model.names[cls])
                    recognized_objects.append(model.names[cls])

    # 겹치는 객체들을 가로로 나열하여 표시
    if overlapping_objects:
        label = "grab: " + ", ".join(overlapping_objects)
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return overlapping_objects
    else:
        return ','.join(recognized_objects)

