import os
import ffmpeg
from math import floor
import json
from datetime import datetime

def extract_frames(input_file, output_dir, mode="all", n=10, target_fps=2, max_frames=10000):

    full_path = os.path.join(output_dir,input_file[:6],"frames") 
    if not (os.path.exists(full_path)):
        os.makedirs(full_path)


    stream = ffmpeg.input(input_file)

    if mode == "fixed_fps":
        stream = stream.filter('fps',fps=target_fps)
    elif mode == "every_n_frames":
        stream = stream.filter('select',f'not(mod(n,{n}))')
        stream = stream.filter('setpts', 'N/FRAME_RATE/TB')
    elif mode == "every_n_seconds":
        stream = stream.filter('fps',fps=f'1/{n}')



    output_pattern = os.path.join(full_path,f"{input_file[:6]}_frame_%06d.png")

    stream = ffmpeg.output(stream, output_pattern, vframes=max_frames)
    ffmpeg.run(stream, overwrite_output=True)

    created_files = [f for f in os.listdir(full_path) if f.endswith(".png")]

    with open(f"{full_path}/frame_manifest.jsonl", "a") as file:
        for i in range(1, len(created_files)+1):

            frame_filename = f"{input_file[:6]}_frame{i:06d}.png"

            entry = {
                frame_filename: {
                    "timestamp" : datetime.now().strftime("%H:%M:%S.%f"),
                    "confidence": 1
                }
            }

            file.write(json.dumps(entry) + "\n")


def find_metadata(input_file):

    probe = ffmpeg.probe(input_file)
    
    #print(probe)
    print("duration: ",probe['format']['duration'])
    print("number of frames: ",probe['streams'][0]['nb_frames'])

if __name__ == "__main__":
    extract_frames("sample.mp4",'output_videos', mode="every_n_seconds")
    find_metadata("sample.mp4")
