import cv2
import numpy as np
from PIL import Image
from typing import List, Union, Literal
import os
import imagehash
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir,"..","outputs")


def remove_blurry(frames: List[str], video: str, blur_threshold: int):

    video_path = os.path.join(output_path,video,"frames")
    
    frame_arr = []
    frame_var = []
    frame_score = []
    count = 0

    for frame in frames:
        full_path = os.path.join(video_path,frame)
        img = cv2.imread(full_path)
        if img is None:
            print(f"Skipping frame {frame} : could not read the file")
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        variance = int(cv2.Laplacian(gray, cv2.CV_64F).var())
        if variance > blur_threshold:
            frame_var.append(variance)
            frame_arr.append(img)
            frame_score.append([frame,img,variance])
            count += 1

    return frame_arr,frame_var, blur_threshold, count, frame_score
        

def remove_duplicates(frames: List[np.ndarray],video,dup_threshold):

    seen_hashes = set()
    kept_frames = []
    frame_score_dup = []

    for name,frame,score in frames:
        # full_path = os.path.join(cleaned_frames_path,frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        hash_value = imagehash.dhash(img)
        is_dup = False
        for seen in seen_hashes:
            if abs(seen - hash_value) < dup_threshold:   
                is_dup = True                 
                break
        if not is_dup:
            seen_hashes.add(hash_value)
            kept_frames.append(frame)
            frame_score_dup.append([name,frame,score])


    return kept_frames,frame_score_dup
        

def select_frames(frames: List[str], video_name, blur_threshold, dup_threshold):
    max_frames = 1000
    video_dir = os.path.join("..","outputs",output_video)
    cleaned_frames = os.path.join(video_dir,"cleaned_frames")

    if not os.path.exists(cleaned_frames):
        os.makedirs(cleaned_frames)



    img_arr,var_arr,blur_threshold,count,frame_score = remove_blurry(frames,video_name,blur_threshold)

    final_frames,frame_score_dup = remove_duplicates(frame_score, video_name, dup_threshold)

    if len(final_frames) > max_frames:
        return final_frames[:max_frames]
    
    metadata_path = os.path.join(video_dir,"cleaned_metadata.json")

    qual_arr=[]
    final_frames_arr=[]
    for file_name,img,score in frame_score_dup:
        qual_arr.append([file_name,score])
        final_frames_arr.append(file_name)

        cleaned_frames_path = os.path.join(cleaned_frames,file_name)
        cv2.imwrite(cleaned_frames_path,img)


    with open(metadata_path,"w") as file:

        entry = {
            "selected_frames": final_frames_arr,
            "stats": {
                "total_input": len(frames),
                "blurry_removed": len(frames) - len(img_arr),
                "duplicates_removed" : len(img_arr) - len(final_frames),
                "final_selected" : len(final_frames),
                "average_blur_score" : np.mean(var_arr)
            },
            "quality_scores" : qual_arr
        }

        file.write(json.dumps(entry))

    

    return final_frames
    
if __name__ == "__main__":

    list_frames = []
    output_video = "cosmos"
    video_dir = os.path.join("..","outputs",output_video)
    frame_dir = os.path.join(video_dir,"frames")

    frames = os.listdir(frame_dir)

    for i in frames:
        if i[-4:] == ".png":
            list_frames.append(i)

    select_frames(frames,output_video,130,10)

