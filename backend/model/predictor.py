from PIL import Image
import numpy as np
import os
import torch
from typing import List
from torchvision import transforms
import torch
import onnxruntime as ot
import time
import json


class predictor:

    def __init__(self, model_path: str):
        self.session = ot.InferenceSession(model_path)

    # def preprocess(self,cleaned_frames):

    #     mean = [0.485, 0.456, 0.406]
    #     std = [0.229, 0.224, 0.225]

    #     transform = transforms.Compose([
    #         transforms.Resize((224,224)),
    #         transforms.ToTensor(),
    #         transforms.Normalize(mean=mean, std=std)
    #     ])

    #     all_tensors = []
        
    #     frames = sorted(os.listdir(cleaned_frames))
    #     for frame in frames:
    #         try:
    #             frame_path = os.path.join(cleaned_frames, frame)
    #             frame = Image.open(frame_path)
    #         except Exception:
    #             continue

    #         rgb_frame = frame.convert("RGB")
            
    #         tensor_frame = transform(rgb_frame)

    #         all_tensors.append(tensor_frame)
        
    #     valid_frames = len(all_tensors)
    #     batch_tensor = torch.stack(all_tensors)

    #     return batch_tensor

    def preprocess(self, frame_input):
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]

        transform = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])

        all_tensors = []
        
        if isinstance(frame_input, str):
            # Original disk-based path (unchanged behaviour)
            frames = sorted(os.listdir(frame_input))
            for frame in frames:
                try:
                    frame_path = os.path.join(frame_input, frame)
                    frame_pil = Image.open(frame_path)
                except Exception:
                    continue

                rgb_frame = frame_pil.convert("RGB")
                tensor_frame = transform(rgb_frame)
                all_tensors.append(tensor_frame)
        else:
            # NEW IN-MEMORY PATH (BGR np arrays from selector)
            # This exactly replicates what the old PIL + PNG path did (same tensor values)
            for frame_bgr in frame_input:
                try:
                    rgb_frame = Image.fromarray(frame_bgr)  # uint8 BGR values interpreted as RGB → identical to old behaviour
                    tensor_frame = transform(rgb_frame)
                    all_tensors.append(tensor_frame)
                except Exception:
                    continue
        
        batch_tensor = torch.stack(all_tensors)
        return batch_tensor



    # def predict(self,cleaned_frames,video_name):

    #     class_names = {0: 'dyed-lifted-polyps', 
    #             1: 'dyed-resection-margins', 
    #             2: 'esophagitis', 
    #             3: 'normal-cecum', 
    #             4: 'normal-pylorus', 
    #             5: 'normal-z-line', 
    #             6: 'polyps', 
    #             7: 'ulcerative-colitis'}

    #     batch_tensor = self.preprocess(cleaned_frames)

    #     batch_numpy = batch_tensor.numpy().astype(np.float32)

    #     input_name = self.session.get_inputs()[0].name

    #     start_time = time.time()

    #     outputs = self.session.run(
    #         None,
    #         {input_name: batch_numpy}
    #     )

    #     end_time = time.time()

    #     inference_time = (end_time - start_time)*1000

    #     logits = outputs[0]

    #     exp_vals = np.exp(logits - np.max(logits,axis=1,keepdims=True))
    #     exp_vals = exp_vals/np.sum(exp_vals,axis=1,keepdims=True)

    #     probs = []
    #     for j in range(len(exp_vals)):
    #         probabilities = {name: float(exp_vals[j][i]) for i,name in class_names.items() }
    #         probs.append(probabilities)

    #     frame_probs = []
    #     p=0
    #     frames = sorted(os.listdir(cleaned_frames))

    #     for frame in frames:
    #         while p<len(probs):
    #             best_label = max(probs[p], key=probs[p].get)
    #             confidence = probs[p][best_label]
    #             frame_probs.append([frame,best_label,confidence])
    #             p += 1
    #             break
        

    #     backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #     video_dir = os.path.join(backend_dir,"outputs", video_name)
    #     with open(f"{video_dir}/frame_scores.jsonl","w") as file:

    #         for frame_prob,prob in zip(frame_probs,probs):
    #             entry = {
    #                 "frame": frame_prob[0],
    #                 "label" : frame_prob[1],
    #                 "confidence": frame_prob[2],
    #                 "probabilities" : prob
    #             }

    #             file.write(json.dumps(entry) + "\n")

        

    #     return frame_probs


    def predict(self, frame_input, video_name, frame_names: List[str] = None):
        class_names = {0: 'dyed-lifted-polyps', 
                1: 'dyed-resection-margins', 
                2: 'esophagitis', 
                3: 'normal-cecum', 
                4: 'normal-pylorus', 
                5: 'normal-z-line', 
                6: 'polyps', 
                7: 'ulcerative-colitis'}

        batch_tensor = self.preprocess(frame_input)

        batch_numpy = batch_tensor.numpy().astype(np.float32)

        input_name = self.session.get_inputs()[0].name

        start_time = time.time()

        outputs = self.session.run(
            None,
            {input_name: batch_numpy}
        )

        end_time = time.time()

        inference_time = (end_time - start_time)*1000

        logits = outputs[0]

        exp_vals = np.exp(logits - np.max(logits,axis=1,keepdims=True))
        exp_vals = exp_vals/np.sum(exp_vals,axis=1,keepdims=True)

        probs = []
        for j in range(len(exp_vals)):
            probabilities = {name: float(exp_vals[j][i]) for i,name in class_names.items() }
            probs.append(probabilities)

        frame_probs = []
        p=0

        # Choose correct list of frame names
        if frame_names is None:
            # backward compatibility (old path mode)
            if isinstance(frame_input, str):
                frames = sorted(os.listdir(frame_input))
            else:
                frames = []
        else:
            frames = frame_names

        for frame in frames:
            while p < len(probs):
                best_label = max(probs[p], key=probs[p].get)
                confidence = probs[p][best_label]
                frame_probs.append([frame, best_label, confidence])
                p += 1
                break

        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_dir = os.path.join(backend_dir,"outputs", video_name)
        with open(f"{video_dir}/frame_scores.jsonl","w") as file:

            for frame_prob,prob in zip(frame_probs,probs):
                entry = {
                    "frame": frame_prob[0],
                    "label" : frame_prob[1],
                    "confidence": frame_prob[2],
                    "probabilities" : prob
                }

                file.write(json.dumps(entry) + "\n")
        
        return frame_probs