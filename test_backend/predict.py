from PIL import Image
import numpy as np
import onnxruntime as ort
from transformers import ViTImageProcessor
import os

# Load image processor
processor = ViTImageProcessor.from_pretrained('mmuratarat/kvasir-v2-classifier')

# Load ONNX model
onnx_model_path = os.path.join(os.path.dirname(__file__), 'vit_kvasir.onnx')
if not os.path.exists(onnx_model_path):
    raise FileNotFoundError(f"ONNX model not found at {onnx_model_path}")
session = ort.InferenceSession(onnx_model_path)

# Class labels (Kvasir v2)
labels = [
    'dyed-lifted-polyps',
    'dyed-resection-margins',
    'esophagitis',
    'normal-cecum',
    'normal-pylorus',
    'normal-z-line',
    'polyps',
    'ulcerative-colitis'
]

def predict(image_path):
    try:
        # Open and preprocess image
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="np")
        pixel_values = inputs['pixel_values'].astype(np.float32)

        # Run ONNX inference
        outputs = session.run(None, {'pixel_values': pixel_values})[0]
        predicted_class = np.argmax(outputs, axis=1)[0]
        label = labels[predicted_class]

        return {"status": "success", "prediction": label}
    except Exception as e:
        return {"status": "error", "message": str(e)}