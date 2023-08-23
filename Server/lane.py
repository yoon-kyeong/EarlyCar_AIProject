import cv2
import numpy as np
import time
import playsound

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255):
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        color = color3
    else:
        color = color1
    cv2.fillPoly(mask, vertices, color)
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def draw_lines(img, lines, color=[0, 0, 255], thickness=2):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines

def weighted_img(img, initial_img, α=1, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)

def get_fitline(img, f_lines):
    lines = np.squeeze(f_lines)
    if len(lines.shape) == 1:
        lines = np.expand_dims(lines, axis=0)

    if len(lines) == 0:
        return []

    lines = lines.reshape(lines.shape[0]*2, 2)
    rows, cols = img.shape[:2]
    output = cv2.fitLine(lines, cv2.DIST_L2, 0, 0.01, 0.01)

    if output is None:
        return []

    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x), img.shape[0]-1
    x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x), int(img.shape[0]/2+100)

    result = [x1, y1, x2, y2]
    return result

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10):
    if len(lines) == 4:
        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

def play_center_sound():
    playsound.playsound('center.mp3')

cap = cv2.VideoCapture(0)
last_sound_time = time.time()
sound_interval = 5

while cap.isOpened():
    success, image = cap.read()

    if success:
        height, width = image.shape[:2]
        gray_img = grayscale(image)
        blur_img = gaussian_blur(gray_img, 3)
        canny_img = canny(blur_img, 70, 210)
        vertices = np.array([[(50, height), (width//2-45, height//2+60), (width//2+45, height//2+60), (width-50, height)]], dtype=np.int32)
        ROI_img = region_of_interest(canny_img, vertices)
        line_arr = hough_lines(ROI_img, 1, np.pi/180, 30, 10, 20)

        if line_arr is not None:
            temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
            draw_lines(temp, line_arr)

            line_arr = np.squeeze(line_arr)
            if len(line_arr.shape) == 1:
                line_arr = np.expand_dims(line_arr, axis=0)

            slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3], line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi
            line_arr = line_arr[np.abs(slope_degree) < 160]
            slope_degree = slope_degree[np.abs(slope_degree) < 160]
            line_arr = line_arr[np.abs(slope_degree) > 95]
            slope_degree = slope_degree[np.abs(slope_degree) > 95]
            L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]
            if len(L_lines) != 0:
                L_lines = L_lines[:, None]
            if len(R_lines) != 0:
                R_lines = R_lines[:, None]
            left_fit_line = get_fitline(image, L_lines)
            right_fit_line = get_fitline(image, R_lines)
            draw_fit_line(temp, left_fit_line)
            draw_fit_line(temp, right_fit_line)

            result = weighted_img(temp, image)
            cv2.imshow('result', result)

            if len(left_fit_line) != 4 and len(right_fit_line) != 4:
                if time.time()-last_sound_time >= sound_interval:
                    play_center_sound()
                    last_sound_time = time.time()
            

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
