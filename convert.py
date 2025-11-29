import os
import cv2

print('Processing...')

input_file = 'video.mp4'
output_path = './frames/'

if not os.path.exists(output_path):
    os.makedirs(output_path)

cap = cv2.VideoCapture(input_file)

width = 640
height = 360

frame_num = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    resized = cv2.resize(frame, (width, height))

    rgba = cv2.cvtColor(resized, cv2.COLOR_BGR2RGBA)
    rgba[(rgba[:, :, 0] == 0) & (rgba[:, :, 1] == 0) & (rgba[:, :, 2] == 0)] = [0, 0, 0, 0]

    cv2.imwrite(os.path.join(output_path, f'{frame_num:04d}.png'), rgba)

    frame_num += 1

cap.release()

print('Done!')