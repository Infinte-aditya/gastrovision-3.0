# Gastrointestinal Disease Prediction System - Project Context

## Overview

This project focuses on building an end-to-end system for detecting gastrointestinal (GI) diseases from endoscopic video data using deep learning. The system processes videos, extracts meaningful frames, predicts disease classes, and provides visual explanations to assist clinical interpretation.

## Problem Context

Endoscopic procedures generate large volumes of video data that must be manually reviewed by medical professionals. This process is time-consuming, error-prone, and depends heavily on expertise. Subtle differences between disease classes further increase diagnostic complexity.

## Solution Overview

The system is designed as a modular pipeline:

Video → Frame Extraction → Frame Selection → Model Prediction → Visualization → Scoring → Output

Key capabilities:

- Automated frame extraction from videos
- Removal of blurry and duplicate frames
- Disease prediction & classification using deep learning models
- Heatmap-based explainability
- Bounding box localization
- Desktop-based visualization (PyQt)

## Dataset & Model Details

- Dataset: Hyper-Kvasir
- Initial approach: Pretrained models for baseline prediction
- Final model: Fine-tuned Vision Transformer (ViT Base Patch16-224)
- Dataset: Hyper-Kvasir (reduced to 8 relevant classes)
- Accuracy achieved: ~94%
- Classes used: 8 selected GI conditions 
dyed-lifted-polyps
dyed-resection-margins
esophagitis
normal-cecum
normal-pylorus
normal-z-line
polyps
ulcerative-colitis
- Inference: ONNX Runtime (~0.2 sec/frame)

## Key Features

- Configurable frame extraction (FPS, intervals)
- Frame quality filtering (blur+duplicates)
- Structured outputs (JSON metadata + frame manifest)
- ONNX-based optimized inference
- Heatmap visualization (Grad-CAM)
- Bounding box localization
- PyQt-based user interface

## System Pipeline

Video → Frame Extraction → Frame Selection → Model Prediction → Visualization → Scoring → Output

## Deployment

- Backend: Python + FastAPI
- Frontend: PyQt6
- Model Runtime: ONNX Runtime (GPU optimized)
- Database: PostgreSQL (Docker-based optional for product based production grade environment, provsions made)

---

## Sprint-Based Development

### Sprint I: Video Processing & Frame Selection Pipeline

- Built full pipeline without AI model
- Implemented frame extraction with configurable parameters
- Removed blurry frames (Laplacian method)
- Removed duplicate frames (perceptual hashing)
- Generated metadata (JSON)
- Organized output structure

Outcome:
Clean, structured, high-quality frame dataset ready for model use

---

### Sprint II: Pretrained Model Integration

- Integrated pretrained model using ONNX Runtime
- Implemented prediction pipeline
- Added confidence scoring
- Introduced Grad-CAM heatmaps
- Built frame ranking system

Outcome:
End-to-end working system (video → prediction → visualization)

---

### Sprint III: Fine-Tuned Model & Optimization

- Fine-tuned Vision Transformer on Hyper-Kvasir
- Achieved ~94% accuracy
- Improved heatmaps (smoothing + thresholding)
- Added bounding box extraction
- Optimized inference (batching + frame skipping)
- Integrated frontend with backend

Outcome:
Fully functional, optimized, and interpretable system

---

## Final System Capabilities

- Accept endoscopic video input
- Extract and filter frames
- Predict GI diseases
- Highlight affected regions
- Display results via UI
- Support clinical decision-making

---

## Goal

To develop a reliable, efficient, and interpretable AI-based system that assists healthcare professionals in diagnosing gastrointestinal diseases from endoscopic data.