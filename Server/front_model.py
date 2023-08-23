import numpy as np
import cv2
from ultralytics import YOLO
from gtts import gTTS
from IPython.display import Audio
import time
from playsound import playsound

'''
- 0: car
- 1: green light
- 2: pedestriangreen light
- 3: pedestrianred light
- 4: red light
- 5: unprotected left turn
'''

model = YOLO('road_v5.pt') 

# webcam 사용
cap = cv2.VideoCapture(0)

sound_interval = 5 
last_sound_time = time.time()

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv5 Inference", annotated_frame)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
            
        for result in results:
            uniq, cnt = np.unique(result.boxes.cls.cpu().numpy(), return_counts=True)  
            uniq_cnt_dict = dict(zip(uniq, cnt))
            print('\n{class num:counts} =', uniq_cnt_dict,'\n')
            for c, box in zip(result.boxes.cls, result.boxes.xyxy):
                if 2 in result.boxes.cls and (box[2] - box[0]) >= 100: #비보호 우회전 
                    if time.time() - last_sound_time >= sound_interval:
                        playsound("pedgreenlight.mp3")
                        last_sound_time = time.time()
                if 5 in result.boxes.cls and 0 not in result.boxes.cls and 1 in result.boxes.cls: #비보호 좌회전 
                    if time.time() - last_sound_time >= sound_interval:
                        playsound("turnleft.mp3")
                        last_sound_time = time.time()
                time.sleep(0.1)
                if 0 in result.boxes.cls: #비보호 좌회전 불가 
                    if 5 in result.boxes.cls and 1 in result.boxes.cls:
                        if time.time() - last_sound_time >= sound_interval:
                            playsound("cant_turn_left.mp3")
                            last_sound_time = time.time()
                    elif 4 in result.boxes.cls and (box[2] - box[0]) >= 100: #빨간불 정지 
                        playsound("redlight.mp3")
                        last_sound_time = time.time() 
                    else: #차간 거리 유지 
                        if (box[2] - box[0]) >= 150: 
                            if time.time() - last_sound_time >= sound_interval:
                                playsound("frontcar.mp3")
                                last_sound_time = time.time()
                    time.sleep(0.1)
                elif 1 in result.boxes.cls:  
                    if 3 in result.boxes.cls:
                        playsound("turnright.mp3")
                        last_sound_time = time.time()
                    elif time.time() - last_sound_time >= sound_interval:
                        playsound("greenlight.mp3")
                        last_sound_time = time.time()
                time.sleep(0.1)
                
        time.sleep(0.1)

    else:
        break

cap.release()
cv2.destroyAllWindows()