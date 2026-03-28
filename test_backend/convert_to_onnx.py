from transformers import ViTForImageClassification
from optimum.onnxruntime import ORTModelForImageClassification
import os

# Define output path
output_dir = os.path.abspath(os.path.dirname(__file__))  # backend/ directory
output_path = os.path.join(output_dir, 'vit_kvasir.onnx')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the ViT model
model = ViTForImageClassification.from_pretrained('mmuratarat/kvasir-v2-classifier')

# Convert to ONNX
ort_model = ORTModelForImageClassification.from_pretrained('mmuratarat/kvasir-v2-classifier', export=True)

# Save the ONNX model
ort_model.save_pretrained(output_dir)

print(f"ONNX model saved to {output_path}")