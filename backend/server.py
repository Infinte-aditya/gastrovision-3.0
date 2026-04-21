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
        top_label, top_conf, heatmap_results  = prediction(file_path)

        return {
            "file": file.filename,
            "label": top_label,
            "confidence": top_conf,
            "heatmap_paths": [r["save_path"] for r in heatmap_results]

        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        pass







