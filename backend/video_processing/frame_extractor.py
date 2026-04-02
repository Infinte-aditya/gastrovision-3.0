import os
import ffmpeg
from math import floor
import json
from datetime import datetime as dt
import datetime
import shutil


def extract_frames(input_file, output_dir, mode="all", n=10, target_fps=10, max_frames=10000):

    video_name = os.path.splitext(os.path.basename(input_file))[0]

    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(backend_dir,"outputs", video_name, "frames")

    if os.path.exists(full_path):
        shutil.rmtree(full_path)
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

    with open(f"{backend_dir}/outputs/{video_name}/frame_manifest.jsonl", "a") as file:
        for i in range(1, len(created_files)+1):

            frame_filename = f"{input_file[:6]}_frame{i:06d}.png"

            entry = {
                frame_filename: {
                    "timestamp" : dt.now().strftime("%H:%M:%S.%f"),
                    "confidence": 1
                }
            }

            file.write(json.dumps(entry) + "\n")

    with open(f"{backend_dir}/outputs/{video_name}/video_metadata.json", "w") as file:

        probe = ffmpeg.probe(input_file)

        duration_secs = float(probe['streams'][0].get('duration', probe['format']['duration']))
        duration_hhmmss = str(datetime.timedelta(seconds=int(duration_secs)))

        frame_rate = probe['streams'][0]['avg_frame_rate']
        if '/' in frame_rate:
            num, den = frame_rate.split('/')
            actual_fps = float(num)/float(den)
        else:
            actual_fps = float(frame_rate)

        if mode == "all":
            nof = probe['streams'][0]['nb_frames']
        elif mode == "fixed_fps":
            nof = int(probe['streams'][0]['nb_frames'])/(actual_fps/target_fps)
        elif mode == "every_n_frames":
            nof = int(probe['streams'][0]['nb_frames'])/n
        elif mode == "every_n_seconds":
            nof = float(probe['format']['duration'])/n
      
        entry = {

            "resolution: ": f"{probe['streams'][0]['width']} x {probe['streams'][0]['height']}",
            "frame rate": actual_fps,
            "codec name": probe['streams'][0]['codec_name'],
            "bit rate": probe['streams'][0]['bit_rate'],
            "duration_formatted": duration_hhmmss,
            "duration: ": probe['format']['duration'],
            "number of frames: ": nof
        }

        file.write(json.dumps(entry))

if __name__ == "__main__":
    extract_frames("cosmos.mp4",'output_videos', mode="every_n_seconds")
    # find_metadata("sample.mp4")
