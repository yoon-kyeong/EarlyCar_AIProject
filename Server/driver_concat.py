import argparse
import cv2
import numpy as np
import os.path as osp
import headpose
import time
from ultralytics import YOLO
from gtts import gTTS
from playsound import playsound

def main(args):
    filename = args["input_file"]

    sound_interval = 5
    last_sound_time = time.time()

    if filename is None:
        isVideo = False
        cap = cv2.VideoCapture(0)
        cap.set(3, args['wh'][0])
        cap.set(4, args['wh'][1])
    else:
        isVideo = True
        cap = cv2.VideoCapture(filename)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name, ext = osp.splitext(filename)
        out = cv2.VideoWriter(args["output_file"], fourcc, fps, (width, height))

    # Pose Detection Initialization
    hpd = headpose.HeadposeDetection(args["landmark_type"], args["landmark_predictor"])

    # YOLOv5 Initialization
    model = YOLO('phone_v5.pt')

    count = 0
    tilt_counter = 0  # Variable to count the tilt direction
    max_tilt_counter = 20  # Threshold to determine the tilt direction

    while(cap.isOpened()):
        # Frame capture
        print('\rframe: %d' % count, end='')
        ret, frame = cap.read()

        if isVideo:
            frame, angles = hpd.process_image(frame)
            if frame is None:
                break
            else:
                out.write(frame)
        else:
            frame = cv2.flip(frame, 1)
            frame, angles = hpd.process_image(frame)

            if angles is not None:
                # Extract pitch, yaw, and roll angles
                pitch = angles[0]
                yaw = angles[1]
                roll = angles[2]

                # Check if the person is looking right or left
                if yaw > 15:
                    tilt_counter += 1  # Increase counter if looking right
                    if tilt_counter > max_tilt_counter:
                        if time.time() - last_sound_time >= sound_interval:
                            text = "Don't Look Right"  # Display text on the screen when looking right
                            playsound("look.mp3")
                            last_sound_time = time.time()

                elif yaw < -15:
                    tilt_counter += 1  # Increase counter if looking left
                    if tilt_counter > max_tilt_counter:
                        if time.time() - last_sound_time >= sound_interval:
                            text = "Don't Look Left"  # Display text on the screen when looking left
                            playsound("look.mp3")
                            last_sound_time = time.time()
                else:
                    tilt_counter = 0  # Reset the counter if not looking sideways
                    text = ""  # No significant tilt

                # Display text on webcam frame
                cv2.putText(frame, text, (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Run YOLOv5 on the frame to detect phones
            results = model(frame)
            for result in results:
                uniq, cnt = np.unique(result.boxes.cls.cpu().numpy(), return_counts=True)
                uniq_cnt_dict = dict(zip(uniq, cnt))

                print('\n{class num:counts} =', uniq_cnt_dict, '\n')

                for c in result.boxes.cls:
                    if int(c) == 0:
                        # Draw bounding box for phone
                        box = result.boxes.xyxy[0].cpu().numpy().astype(int)
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

                        if time.time() - last_sound_time >= sound_interval:
                            playsound("phone.mp3")
                            last_sound_time = time.time()

            # Display summarized frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        count += 1

    # Cleanup
    cap.release()
    if isVideo:
        out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar='FILE', dest='input_file', default=None, help='Input video. If not given, web camera will be used.')
    parser.add_argument('-o', metavar='FILE', dest='output_file', default=None, help='Output video.')
    parser.add_argument('-wh', metavar='N', dest='wh', default=[720, 480], nargs=2, help='Frame size.')
    parser.add_argument('-lt', metavar='N', dest='landmark_type', type=int, default=1, help='Landmark type.')
    parser.add_argument('-lp', metavar='FILE', dest='landmark_predictor',
                        default='model/shape_predictor_68_face_landmarks.dat', help="Landmark predictor data file.")
    args = vars(parser.parse_args())
    main(args)
