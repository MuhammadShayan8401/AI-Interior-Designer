"""
models/diffusion.py
Stable Diffusion img2img pipeline for room redesign.
Uses runwayml/stable-diffusion-v1-5 with DPM-Solver scheduler.
"""

import random
import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler

MODEL_ID = "runwayml/stable-diffusion-v1-5"

# ── Singleton loader ──────────────────────────────────────────────────────────
_pipe = None


def load_diffusion_model():
    global _pipe
    if _pipe is None:
        print("[Diffusion] Loading Stable Diffusion (this may take ~2 min)...")
        _pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            safety_checker=None,
            requires_safety_checker=False,
        )
        _pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            _pipe.scheduler.config
        )
        if torch.cuda.is_available():
            _pipe = _pipe.to("cuda")
            _pipe.enable_attention_slicing()
        print("[Diffusion] Model loaded.")
    return _pipe


# ── Main function ─────────────────────────────────────────────────────────────
def run_diffusion(
    image: Image.Image,
    prompt: str,
    negative_prompt: str,
    strength: float = 0.6,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: int = None,
) -> tuple[Image.Image, int]:
    """
    Args:
        image:             Input PIL Image (will be resized to 512x512)
        prompt:            Positive text prompt
        negative_prompt:   Negative text prompt
        strength:          How much to transform the image (0.3–0.9)
        guidance_scale:    Classifier-free guidance scale
        num_inference_steps: Denoising steps (more = better quality, slower)
        seed:              Random seed for reproducibility (None = random)
    Returns:
        result_image: Generated PIL Image
        seed_used:    The seed that was used (useful for frontend display)
    """
    pipe = load_diffusion_model()

    if seed is None:
        seed = random.randint(0, 2**32 - 1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    generator = torch.Generator(device=device).manual_seed(seed)

    img = image.convert("RGB").resize((512, 512))

    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=img,
        strength=strength,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        generator=generator,
    )

    return result.images[0], seed


def run_diffusion_batch(
    image: Image.Image,
    prompt: str,
    negative_prompt: str,
    strength: float = 0.6,
    num_images: int = 3,
) -> tuple[list[Image.Image], list[int]]:
    """
    Generate multiple variations using different random seeds.
    Returns list of images and the seeds used.
    """
    images, seeds = [], []
    for _ in range(num_images):
        seed = random.randint(0, 2**32 - 1)
        img, used_seed = run_diffusion(
            image, prompt, negative_prompt, strength=strength, seed=seed
        )
        images.append(img)
        seeds.append(used_seed)
    return images, seeds
