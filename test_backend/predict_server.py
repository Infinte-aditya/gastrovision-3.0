from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from predict import predict
import shutil
from PIL import Image
import io

app = FastAPI()

# Allow CORS for Express server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary directory for images
TEMP_DIR = "temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/predict")
async def predict_endpoint(image: UploadFile = File(...)):
    try:
        # Validate file
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=422, detail="File must be an image (JPEG/PNG)")
        
        # Save uploaded image temporarily
        image_path = os.path.join(TEMP_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Verify image integrity
        try:
            with Image.open(image_path) as img:
                img.verify()  # Check if image is valid
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid image file: {str(e)}")

        # Get prediction
        result = predict(image_path)

        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    finally:
        # Clean up
        if os.path.exists(image_path):
            os.remove(image_path)