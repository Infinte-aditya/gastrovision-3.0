import os
import ffmpeg
from model.predictor import predictor
from scoring.frame_scoring import frame_scoring
from scoring.video_scoring import video_scoring
from video_processing.frame_extractor import frame_extractor
from video_processing.frame_selector import frame_selector
from visualization.heatmap import HeatmapGenerator
from threading import Thread



MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "vit_model_fp32.onnx")
GLOBAL_PREDICTOR = predictor(MODEL_PATH)
GLOBAL_FRAME_SCORER = frame_scoring()
GLOBAL_VIDEO_SCORER = video_scoring()
GLOBAL_HEATMAP_GEN = HeatmapGenerator(
    pth_path=os.path.join(os.path.dirname(__file__), "model", "vit_best.pth")
)


def prediction(video_full_path):
    filename = os.path.basename(video_full_path)
    video_name = os.path.splitext(filename)[0]
    video_dir = os.path.dirname(video_full_path)

    # Config parameters
    blur_threshold = 130
    dup_threshold = 10
    conf_threshold = 0.70

    # Convert .avi to .mp4 if needed
    if video_full_path.endswith(".avi"):
        new_input_file = os.path.join(video_dir, f'{video_name}.mp4')
        (
            ffmpeg
            .input(video_full_path)
            .output(new_input_file, vcodec='libx264', crf=23, preset='ultrafast')
            .run(overwrite_output=True, quiet=True)
        )
    else:
        new_input_file = video_full_path

    # Step 1: Extraction
    extractor = frame_extractor()
    frames = extractor.extract_frames(new_input_file, "every_n_frames", 5, 10, 10000)

    # # Step 2: Selection (blur/duplicate removal)
    # selector = frame_selector()
    # _, cleaned_frames = selector.select_frames(frames, video_name, blur_threshold, dup_threshold)

    selector = frame_selector()
    frame_names, kept_frames, cleaned_frames = selector.select_frames(frames, video_name, blur_threshold, dup_threshold)

    # # Step 3: Prediction
    # # predictor.predict() signature: (self, cleaned_frames, model, video_name)

    # GLOBAL_PREDICTOR.predict(cleaned_frames, video_name)
    GLOBAL_PREDICTOR.predict(kept_frames, video_name, frame_names=frame_names)


    # # Step 4: Scoring
    # frame_scorer = frame_scoring()
    # scoring_result = frame_scorer.compute_stats(video_name, conf_threshold)
    # ranked = scoring_result["ranked_frames"]

    # video_scorer = video_scoring()
    # top_label, top_conf = video_scorer.average_confidence(video_name)

    frame_scorer = GLOBAL_FRAME_SCORER
    scoring_result = frame_scorer.compute_stats(video_name, conf_threshold)
    ranked = scoring_result["ranked_frames"]

    video_scorer = GLOBAL_VIDEO_SCORER
    top_label, top_conf = video_scorer.average_confidence(video_name)

    # gen = HeatmapGenerator(pth_path=os.path.join(os.path.dirname(__file__), "model", "vit_model_fp32.pth"))

    # heatmap_dir = os.path.join(os.path.dirname(__file__), "outputs", video_name, "heatmaps")
    # heatmap_results = gen.generate_batch(
    #     frame_dir=cleaned_frames,
    #     frame_results=ranked,
    #     output_dir=heatmap_dir,
    #     top_n=5
    # )

    heatmap_dir = os.path.join(os.path.dirname(__file__), "outputs", video_name, "heatmaps")
    # heatmap_results = GLOBAL_HEATMAP_GEN.generate_batch(
    #     frame_dir=cleaned_frames,
    #     frame_results=ranked,
    #     output_dir=heatmap_dir,
    #     top_n=5
    # )

    heatmap_results = []

    def run_heatmap():
        results = GLOBAL_HEATMAP_GEN.generate_batch(
            frame_dir=cleaned_frames,
            frame_results=ranked,
            output_dir=heatmap_dir,
            top_n=5
        )
        heatmap_results.extend(results)

    heatmap_thread = Thread(target=run_heatmap, daemon=True)
    heatmap_thread.start()



    return top_label, top_conf #, heatmap_results  