from model.predictor import predictor
from scoring.frame_scoring import frame_scoring
from scoring.video_scoring import video_scoring
from video_processing.frame_extractor import frame_extractor
from video_processing.frame_selector import frame_selector

import ffmpeg
import os


def prediction(video_full_path):


    filename = os.path.basename(video_full_path)
    video_name = os.path.splitext(filename)[0]

    video_dir = os.path.dirname(video_full_path)


    blur_threshold = 130
    dup_threshold = 10
    model = "../backend/model/vit_kvasir.onnx"
    mode="all"
    n=10
    target_fps=10
    max_frames=10000
    input_file=video_full_path

    conf_threshold = 0.70

    if input_file.endswith(".avi"):
        new_input_file = os.path.join(video_dir, f'{video_name}.mp4')

        (
            ffmpeg
            .input(input_file)
            .output(new_input_file, vcodec='libx264', acodec='aac')
            .run(overwrite_output=True)
        )
    else:
        new_input_file = input_file


    extractor = frame_extractor()
    frames = extractor.extract_frames(new_input_file, mode, n, target_fps, max_frames)

    selector = frame_selector()
    final_frames,cleaned_frames= selector.select_frames(frames,video_name, blur_threshold, dup_threshold)

    model_predictor = predictor()
    output = model_predictor.predict(cleaned_frames, model,video_name)

    frame_scorer = frame_scoring()
    result = frame_scorer.compute_stats(video_name,conf_threshold)

    video_scorer = video_scoring()
    top_label,top_conf = video_scorer.average_confidence(video_name)


    return top_label,top_conf


# if __name__ == "__main__":
#     prediction()