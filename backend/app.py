"""
AI Interior Designer — FastAPI Backend Entry Point
Run locally:  uvicorn backend.app:app --reload
Run in Colab: see colab_runner.ipynb
"""

import os
import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes.generate import router as generate_router
from routes.feedback import router as feedback_router

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Interior Designer API",
    description="Room redesign pipeline: Segmentation → Depth → Stable Diffusion",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files statically (optional, useful for debugging)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(generate_router, prefix="/generate", tags=["Generate"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "gpu": torch.cuda.is_available(),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    }


@app.get("/", tags=["Health"])
async def root():
    return {"message": "AI Interior Designer API is running. Visit /docs for API reference."}
