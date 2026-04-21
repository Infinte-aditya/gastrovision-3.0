"""
visualization/heatmap.py
========================
Attention Rollout heatmap generator for GastroVision 3.0.

Architecture: google/vit-base-patch16-224-in21k (finetuned, your weights)
Technique:    Attention Rollout (Abnar & Zuidema, 2020)
              — the standard explainability method for Vision Transformers.
              Grad-CAM is NOT used here because ViT has no convolutional
              feature maps; attention rollout operates on the transformer's
              own attention weights instead.

Inference path (ONNX) is untouched — this module is a separate,
on-demand visualization tool called per-frame when a doctor requests
a heatmap. It loads the PyTorch model once and caches it.

Usage:
    from visualization.heatmap import HeatmapGenerator

    gen = HeatmapGenerator(pth_path="backend/model/vit_model_final.pth")
    result = gen.generate(frame_input="path/to/frame.jpg",
                          target_class="ulcerative-colitis",
                          confidence=0.94)

    overlay  = result["overlay_image"]   # PIL.Image  — save or display
    raw_map  = result["raw_heatmap"]     # np.ndarray 224×224 float32
    metadata = result["metadata"]
"""

import time
import warnings
from pathlib import Path
from typing import Union

import cv2
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
from torchvision import transforms
from transformers import ViTForImageClassification
from transformers import ViTConfig


warnings.filterwarnings("ignore", category=UserWarning)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class HeatmapGenerationError(Exception):
    """Raised when attention rollout cannot be computed for a frame."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_COLORMAP = cv2.COLORMAP_JET          # red-hot for lesions (clinical standard)
_IMAGENET_MEAN = [0.5, 0.5, 0.5]     # matches your training normalisation
_IMAGENET_STD  = [0.5, 0.5, 0.5]

_CLASS_NAMES = {
    "dyed-lifted-polyps":    0,
    "dyed-resection-margins": 1,
    "esophagitis":            2,
    "normal-cecum":           3,
    "normal-pylorus":         4,
    "normal-z-line":          5,
    "polyps":                 6,
    "ulcerative-colitis":     7,
}

_TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=_IMAGENET_MEAN, std=_IMAGENET_STD),
])


def _load_frame(frame_input: Union[str, Path, np.ndarray, Image.Image]) -> Image.Image:
    """Accept PIL, NumPy HWC, or file path — always return RGB PIL.Image."""
    if isinstance(frame_input, (str, Path)):
        img = Image.open(frame_input)
    elif isinstance(frame_input, np.ndarray):
        if frame_input.ndim == 2:                        # grayscale
            frame_input = np.stack([frame_input] * 3, axis=-1)
        elif frame_input.shape[2] == 4:                  # RGBA
            frame_input = frame_input[:, :, :3]
        img = Image.fromarray(frame_input.astype(np.uint8))
    elif isinstance(frame_input, Image.Image):
        img = frame_input
    else:
        raise HeatmapGenerationError(
            f"Unsupported frame type: {type(frame_input)}. "
            "Expected str, Path, np.ndarray, or PIL.Image."
        )
    return img.convert("RGB")


def _attention_rollout(attention_weights: list[torch.Tensor],
                       discard_ratio: float = 0.9) -> np.ndarray:
    """
    Attention Rollout (Abnar & Zuidema, 2020).

    Parameters
    ----------
    attention_weights : list of tensors, each shape [1, num_heads, seq_len, seq_len]
                        One tensor per transformer layer (12 layers for ViT-base).
    discard_ratio     : float — fraction of lowest attention values to zero out
                        before rollout. Higher = sharper, more focused heatmap.
                        0.9 is the recommended clinical default.

    Returns
    -------
    np.ndarray of shape (14, 14), float32, values in [0, 1].
    The spatial attention map for the CLS token over the 196 patch positions.
    """
    # ViT-base-patch16-224: image_size=224, patch_size=16 → 14×14 = 196 patches
    # seq_len = 196 patches + 1 CLS token = 197
    rollout = torch.eye(attention_weights[0].shape[-1])  # identity [197, 197]

    for attn in attention_weights:
        # attn: [1, 12, 197, 197] — average over heads
        attn_avg = attn.squeeze(0).mean(dim=0)            # [197, 197]

        # Discard the lowest-attention tokens (noise suppression)
        flat = attn_avg.view(-1)
        threshold = torch.quantile(flat, discard_ratio)
        attn_avg = torch.where(attn_avg < threshold,
                               torch.zeros_like(attn_avg),
                               attn_avg)

        # Add residual connection (identity) then re-normalise rows
        attn_avg = attn_avg + torch.eye(attn_avg.shape[0])
        attn_avg = attn_avg / attn_avg.sum(dim=-1, keepdim=True).clamp(min=1e-6)

        # Accumulate rollout
        rollout = torch.matmul(attn_avg, rollout)

    # CLS token (row 0) attends to all 196 patches (columns 1:)
    mask = rollout[0, 1:]                                  # [196]
    mask = mask.reshape(14, 14).numpy().astype(np.float32) # [14, 14]

    # Normalise to [0, 1]
    mask -= mask.min()
    denom = mask.max()
    if denom > 1e-8:
        mask /= denom

    return mask


def _upsample_and_colorise(mask_14x14: np.ndarray,
                            original_frame: Image.Image,
                            alpha: float = 0.5) -> tuple[np.ndarray, np.ndarray]:
    """
    Upsample the 14×14 attention map to 224×224, apply JET colormap,
    and blend with the original frame.

    Returns
    -------
    overlay    : np.ndarray [H, W, 3] uint8 — blended result
    heatmap_224: np.ndarray [H, W, 3] uint8 — raw coloured heatmap
    """
    h, w = original_frame.size[1], original_frame.size[0]

    # Bicubic upsampling (smoother than bilinear for attention maps)
    heatmap_224 = cv2.resize(mask_14x14, (w, h),
                             interpolation=cv2.INTER_CUBIC)

    # Clip any overshoot from bicubic, then scale to uint8
    heatmap_224 = np.clip(heatmap_224, 0.0, 1.0)
    heatmap_uint8 = (heatmap_224 * 255).astype(np.uint8)

    # Apply JET colormap (blue=low, red=high attention — clinical standard)
    coloured = cv2.applyColorMap(heatmap_uint8, _COLORMAP)   # BGR
    coloured_rgb = cv2.cvtColor(coloured, cv2.COLOR_BGR2RGB)

    # Blend with original
    frame_np = np.array(original_frame.resize((w, h))).astype(np.float32)
    overlay = (frame_np * (1 - alpha) + coloured_rgb.astype(np.float32) * alpha)
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    return overlay, coloured_rgb


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class HeatmapGenerator:
    """
    Generates Attention Rollout heatmaps for GastroVision frames.

    The PyTorch model is loaded once on __init__ and reused across
    all generate() calls — no per-frame model reload.

    Parameters
    ----------
    pth_path      : path to your vit_model_final.pth weights file
    num_labels    : number of output classes (default 8 for Kvasir)
    discard_ratio : attention noise suppression (default 0.9)
    device        : "cpu" | "cuda" | "auto" (default "auto")
    """
    

    def __init__(self,
                 pth_path: Union[str, Path],
                 num_labels: int = 8,
                 discard_ratio: float = 0.9,
                 device: str = "auto"):

        self.discard_ratio = discard_ratio

        # Device selection
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        # Load ViT-base with your finetuned weights
        # output_attentions=True is the key flag — makes all 12 layers
        # return their attention matrices alongside logits
        config = ViTConfig.from_pretrained("google/vit-base-patch16-224-in21k")
        config.output_attentions = True
        config.num_labels = num_labels

        self._model = ViTForImageClassification.from_pretrained(
            "google/vit-base-patch16-224-in21k",
            config=config,
            ignore_mismatched_sizes=True,
            force_download=True,   # ← ADD THIS

        )

        state_dict = torch.load(pth_path,
                                map_location=self.device,
                                weights_only=True)
        self._model.load_state_dict(state_dict)
        self._model.eval()
        self._model.to(self.device)

        print("vit encoder config:", self._model.vit.encoder.layer[0].attention.attention.query.weight.shape)
        print("encoder output_attentions:", self._model.vit.encoder.config.output_attentions)


        print(f"[HeatmapGenerator] ready — device: {self.device}")

    # ------------------------------------------------------------------

    # ADD this method to HeatmapGenerator class:
    
    def _get_attention_via_hooks(self, tensor):
        attentions = []
        hooks = []

        def make_hook(module):
            def hook(mod, input, output):
                # Recompute attention scores from the query/key projections
                # input[0] is the hidden states: [1, 197, 768]
                hidden = input[0]
                num_heads = mod.num_attention_heads
                head_dim = mod.attention_head_size

                q = mod.query(hidden)  # [1, 197, 768]
                k = mod.key(hidden)

                # Reshape to [1, num_heads, 197, head_dim]
                def reshape(x):
                    b, seq, _ = x.shape
                    x = x.view(b, seq, num_heads, head_dim)
                    return x.permute(0, 2, 1, 3)

                q = reshape(q)
                k = reshape(k)

                scale = head_dim ** -0.5
                scores = torch.matmul(q, k.transpose(-2, -1)) * scale  # [1, heads, 197, 197]
                attn = torch.softmax(scores, dim=-1)
                attentions.append(attn.detach().cpu())

            return hook

        for layer in self._model.vit.encoder.layer:
            h = layer.attention.attention.register_forward_hook(make_hook(layer.attention.attention))
            hooks.append(h)

        with torch.no_grad():
            outputs = self._model(pixel_values=tensor)

        for h in hooks:
            h.remove()

        return outputs, attentions

    def generate(self,
             frame_input: Union[str, Path, np.ndarray, Image.Image],
             target_class: str = None,
             confidence: float = None,
             alpha: float = 0.5) -> dict:
        """
        Generate an Attention Rollout heatmap for a single frame.

        Parameters
        ----------
        frame_input  : file path, np.ndarray (HWC), or PIL.Image
        target_class : class label string (e.g. "ulcerative-colitis").
                    If None, uses the model's own argmax prediction.
        confidence   : pass-through from ONNX predictor output, stored
                    in metadata only — does not affect the heatmap.
        alpha        : heatmap blend strength [0=original, 1=pure heatmap]
                    Default 0.5 is the clinical sweet spot.

        Returns
        -------
        dict with keys:
            overlay_image  : PIL.Image   — final visualised frame
            raw_heatmap    : np.ndarray  — 14×14 float32 attention map
            superimposed   : np.ndarray  — 224×224 uint8 RGB overlay
            metadata       : dict        — method, class, confidence, timing
        """
        t_start = time.perf_counter()

        # 1. Load and validate frame
        try:
            pil_frame = _load_frame(frame_input)
        except Exception as e:
            raise HeatmapGenerationError(f"Failed to load frame: {e}") from e

        # 2. Preprocess (same transform as predictor)
        tensor = _TRANSFORM(pil_frame).unsqueeze(0).to(self.device)  # [1,3,224,224]

        # 3. Forward pass via hooks (clean, no debug, no output_attentions=True hack)
        try:
            outputs, attn_cpu = self._get_attention_via_hooks(tensor)
        except Exception as e:
            raise HeatmapGenerationError(f"Model forward pass failed: {e}") from e

        # 4. Resolve target class
        logits = outputs.logits                              # [1, 8]
        pred_idx = int(logits.argmax(dim=-1).item())
        id2label = {v: k for k, v in _CLASS_NAMES.items()}
        pred_class = id2label[pred_idx]

        if target_class is not None and target_class not in _CLASS_NAMES:
            raise HeatmapGenerationError(
                f"Unknown target_class '{target_class}'. "
                f"Valid options: {list(_CLASS_NAMES.keys())}"
            )
        used_class = target_class if target_class is not None else pred_class

        # 5. Compute confidence from logits if not supplied
        if confidence is None:
            probs = torch.softmax(logits, dim=-1).squeeze(0)
            idx = _CLASS_NAMES.get(used_class, pred_idx)
            confidence = float(probs[idx].item())

        # 6. Attention Rollout (attn_cpu already returned on CPU by the hook)
        raw_map_14x14 = _attention_rollout(attn_cpu, self.discard_ratio)

        # 7. Upsample + colorise + blend
        superimposed, heatmap_rgb = _upsample_and_colorise(
            raw_map_14x14, pil_frame, alpha=alpha
        )

        overlay_pil = Image.fromarray(superimposed)

        elapsed_ms = (time.perf_counter() - t_start) * 1000

        return {
            "overlay_image": overlay_pil,           # PIL.Image — save/display
            "raw_heatmap":   raw_map_14x14,         # [14,14] float32 — debug
            "superimposed":  superimposed,           # [H,W,3] uint8 ndarray
            "metadata": {
                "method":              "attention_rollout",
                "target_class":        used_class,
                "predicted_class":     pred_class,
                "confidence":          round(confidence, 4),
                "discard_ratio":       self.discard_ratio,
                "alpha":               alpha,
                "generation_time_ms":  round(elapsed_ms, 1),
                "device":              str(self.device),
            }
        }

    # ------------------------------------------------------------------

    def generate_batch(self,
                       frame_dir: Union[str, Path],
                       frame_results: list[dict],
                       output_dir: Union[str, Path],
                       alpha: float = 0.5,
                       top_n: int = None) -> list[dict]:
        """
        Convenience method: generate heatmaps for ranked frames from
        frame_scoring output and save them to disk.

        Parameters
        ----------
        frame_dir     : directory containing the extracted frame images
        frame_results : list of dicts from frame_scoring.compute_stats()
                        (ranked_frames list — each has 'frame', 'label',
                        'confidence', 'rank')
        output_dir    : directory to save overlay images
        alpha         : blend strength (default 0.5)
        top_n         : if set, only process the top-N ranked frames.
                        Useful for demo: pass top_n=5 to heatmap only the
                        most confident frames.

        Returns
        -------
        list of dicts — one per frame, with save path + metadata
        """
        frame_dir  = Path(frame_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        frames_to_process = frame_results
        if top_n is not None:
            frames_to_process = frame_results[:top_n]

        results = []
        for entry in frames_to_process:
            frame_name = entry["frame"]
            frame_path = frame_dir / frame_name
            label      = entry.get("label")
            conf       = entry.get("confidence")
            rank       = entry.get("rank", "?")

            if not frame_path.exists():
                print(f"[HeatmapGenerator] skipping {frame_name} — file not found")
                continue

            try:
                result = self.generate(
                    frame_input=frame_path,
                    target_class=label,
                    confidence=conf,
                    alpha=alpha,
                )

                # Save overlay as PNG
                stem = Path(frame_name).stem
                save_path = output_dir / f"{stem}_heatmap.png"
                result["overlay_image"].save(save_path)

                results.append({
                    "frame":     frame_name,
                    "rank":      rank,
                    "save_path": str(save_path),
                    "metadata":  result["metadata"],
                })

                print(
                    f"[HeatmapGenerator] rank {rank:>3} | "
                    f"{frame_name} | "
                    f"{result['metadata']['target_class']} "
                    f"({result['metadata']['confidence']:.2%}) | "
                    f"{result['metadata']['generation_time_ms']:.0f}ms"
                )

            except HeatmapGenerationError as e:
                print(f"[HeatmapGenerator] ERROR on {frame_name}: {e}")
                continue

        return results