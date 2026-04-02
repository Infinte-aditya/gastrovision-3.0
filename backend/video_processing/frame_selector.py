import cv2
import numpy as np
from PIL import Image
from typing import List, Union, Literal
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir,"..","outputs","cosmos","frames")


def remove_blurry(frames: List[str], video: str, threshold: int):

    video_path = os.path.join(output_path,video,"frames")
    
    frame_arr = []
    frame_var = []
    count = 0

    for frame in frames:
        full_path = os.path.join(video_path,frame)
        img = cv2.imread(full_path)
        if img is None:
            print(f"Skipping frame {frame} : could not read the file")
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        variance = int(cv2.Laplacian(gray, cv2.CV_64F).var())
        if variance > threshold:
            frame_var.append(variance)
            frame_arr.append(img)
            count += 1

    return frame_arr,frame_var, threshold, count
        

    
if __name__ == "__main__":

    list_frames = []
    output_video = "cosmos"
    frame_dir = os.path.join("..","outputs",output_video,"frames")
    frames = os.listdir(frame_dir)

    for i in frames:
        if i[-4:] == ".png":
            list_frames.append(i)

    img_arr,var_arr,threshold,count = remove_blurry(list_frames,"cosmos",130)
    print(count)

