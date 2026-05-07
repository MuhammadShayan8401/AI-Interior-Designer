"""
routes/generate.py
POST /generate — Full pipeline endpoint.
Accepts an image + design parameters, returns generated images.
"""

import traceback
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from models.segmentation import run_segmentation
from models.depth import run_depth
from models.diffusion import run_diffusion_batch
from models.prompts import build_prompt, describe_prompt
from utils.image_utils import (
    bytes_to_pil,
    resize_for_model,
    pil_to_b64,
    validate_image_bytes,
    save_upload,
)

router = APIRouter()


@router.post("")
async def generate(
    image: UploadFile = File(...),
    room_type: str = Form("living room"),
    style: str = Form("modern"),
    density: str = Form("moderate"),
    num_images: int = Form(3),
    strength: float = Form(0.6),
):
    """
    Run the full interior design pipeline.

    - **image**: Room photo (JPG/PNG/WEBP, max 10MB)
    - **room_type**: bedroom | living room | kitchen | bathroom | dining room | home office | nursery | studio apartment
    - **style**: modern | minimalist | scandinavian | industrial | bohemian | mid-century modern | traditional | japandi | coastal | art deco
    - **density**: minimal | moderate | dense
    - **num_images**: Number of variations to generate (1–4)
    - **strength**: SD transformation strength (0.3–0.9)
    """
    try:
        # ── 1. Validate & load image ──────────────────────────────────────────
        raw = await image.read()
        validate_image_bytes(raw, image.filename or "upload.jpg")
        pil_img = bytes_to_pil(raw)

        # Save original upload
        save_upload(raw, image.filename or "upload.jpg")

        # Resize for model input
        pil_resized = resize_for_model(pil_img)

        # ── 2. Segmentation ───────────────────────────────────────────────────
        mask_img, furniture = run_segmentation(pil_resized)

        # ── 3. Depth estimation ───────────────────────────────────────────────
        depth_img = run_depth(pil_resized)

        # ── 4. Build prompts ──────────────────────────────────────────────────
        prompt, negative_prompt = build_prompt(room_type, style, density, furniture)
        description = describe_prompt(room_type, style, density, furniture)

        # ── 5. Generate images ────────────────────────────────────────────────
        num_images = max(1, min(4, num_images))  # clamp 1–4
        strength = max(0.3, min(0.9, strength))  # clamp 0.3–0.9

        gen_images, seeds = run_diffusion_batch(
            pil_resized, prompt, negative_prompt,
            strength=strength,
            num_images=num_images
        )

        # ── 6. Encode outputs ─────────────────────────────────────────────────
        return JSONResponse({
            "success": True,
            "description": description,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "furniture_detected": furniture,
            "segmentation_mask": pil_to_b64(mask_img),
            "depth_map": pil_to_b64(depth_img),
            "generated_images": [pil_to_b64(img) for img in gen_images],
            "seeds": seeds,
            "settings": {
                "room_type": room_type,
                "style": style,
                "density": density,
                "strength": strength,
                "num_images": num_images,
            }
        })

    except ValueError as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=400)

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }, status_code=500)
