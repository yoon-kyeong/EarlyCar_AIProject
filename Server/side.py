import numpy as np
import cv2
from ultralytics import YOLO
from gtts import gTTS
from IPython.display import Audio
import time
from playsound import playsound

model = YOLO('side.pt') 

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
                if int(c) == 0 and (box[2] - box[0]) >= 100:
                    if time.time() - last_sound_time >= sound_interval:
                        playsound("side.mp3") 
                        last_sound_time = time.time()
        time.sleep(0.1)

    else:
        break

cap.release()
cv2.destroyAllWindows()