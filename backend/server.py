from fastapi import FastAPI, UploadFile, File
import uvicorn
from main import prediction
from pydantic import BaseModel
import shutil
import os


class VideoInput(BaseModel):
    video: str

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello"}

@app.post("/predict")
async def predict_video(file: UploadFile= File(...)):

    file_path = os.path.join(UPLOAD_DIR,file.filename)

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    try:
        # top_label, top_conf, heatmap_results  = prediction(file_path)

        # return {
        #     "file": file.filename,
        #     "label": top_label,
        #     "confidence": top_conf,
        #     "heatmap_paths": [r["save_path"] for r in heatmap_results]

        # }

        top_label, top_conf = prediction(file_path)
        return {
            "file": file.filename,
            "label": top_label,
            "confidence": top_conf
        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        pass



# Add new endpoint to server.py:
@app.get("/heatmaps/{video_name}")
def get_heatmaps(video_name: str):
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    heatmap_dir = os.path.join(backend_dir, "outputs", video_name, "heatmaps")
    if not os.path.exists(heatmap_dir):
        return {"heatmap_paths": []}
    paths = sorted([
        os.path.join(heatmap_dir, f)
        for f in os.listdir(heatmap_dir)
        if f.endswith(".png")
    ])
    return {"heatmap_paths": paths}