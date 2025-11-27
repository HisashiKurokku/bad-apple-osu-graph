import cv2
import os
import json
import svgwrite
from skimage import measure
from scipy.interpolate import splprep, splev
import numpy as np

INPUT_DIR = "frames"           
OUTPUT_DIR = "svg_frames"     
TARGET_W = 640.86                 
TARGET_H = 360

os.makedirs(OUTPUT_DIR, exist_ok=True)

def png_to_svg_path(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    img = cv2.resize(img, (int(TARGET_W), int(TARGET_H)))
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    contours = measure.find_contours(thresh, 0.3)

    path_commands = []

    for contour in contours:
        contour = contour.astype(int)
        if len(contour) < 2:
            continue

        cmd = f"M{contour[0][1]},{contour[0][0]}"
        for y, x in contour[1:]:
            cmd += f" L{x},{y}"

        path_commands.append(cmd)

    return " ".join(path_commands)

def convert_all():
    frames = sorted(os.listdir(INPUT_DIR))

    for i, file in enumerate(frames):
        if not file.endswith(".png"):
            continue

        frame_path = os.path.join(INPUT_DIR, file)

        d_path = png_to_svg_path(frame_path)

        json_data = { "path": d_path }

        out_name = f"frame_{i:04d}.json"
        with open(os.path.join(OUTPUT_DIR, out_name), "w") as f:
            json.dump(json_data, f)

    print("Done.")

if __name__ == "__main__":
    convert_all()
