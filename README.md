# 🏠 AI Interior Designer

> Upload a room photo → get AI-redesigned interiors in any style, instantly.

**Pipeline:** Room photo → SegFormer (segmentation) → MiDaS (depth) → Prompt Builder → Stable Diffusion img2img → Output

---

## Project Structure

```
AI-Interior-Designer/
│
├── backend/
│   ├── app.py                  ← FastAPI entry point
│   ├── models/
│   │   ├── segmentation.py     ← SegFormer (ADE20K)
│   │   ├── depth.py            ← MiDaS depth estimation
│   │   ├── diffusion.py        ← Stable Diffusion img2img
│   │   └── prompts.py          ← Dynamic prompt builder
│   ├── routes/
│   │   ├── generate.py         ← POST /generate
│   │   └── feedback.py         ← POST /feedback, GET /feedback/summary
│   ├── utils/
│   │   └── image_utils.py      ← base64, resize, validate, save
│   └── uploads/                ← saved uploads + feedback.json
│
├── frontend/
│   ├── streamlit_app.py        ← Streamlit UI
│   └── styles.css              ← Custom styling
│
├── colab_runner.ipynb          ← Colab backend launcher
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1 — Run backend on Google Colab (GPU)

1. Open [colab.research.google.com](https://colab.research.google.com)
2. Upload `colab_runner.ipynb`
3. Set runtime: **Runtime → Change runtime type → T4 GPU**
4. Run all 4 cells in order
5. Cell 4 prints your public URL: `https://xxxx.trycloudflare.com`

No accounts or tokens needed — Cloudflare Tunnel is free and instant.

### 2 — Configure frontend

Open `frontend/streamlit_app.py` and update line 10:

```python
API_URL = "https://xxxx.trycloudflare.com"  # your Colab URL
```

### 3 — Run Streamlit

```bash
pip install streamlit requests Pillow
streamlit run frontend/streamlit_app.py
```

Visit [http://localhost:8501](http://localhost:8501)

---

## API Reference

### `GET /health`
Check server status and GPU availability.

### `POST /generate`
Run the full pipeline.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `image` | file | required | Room photo (JPG/PNG/WEBP ≤ 10MB) |
| `room_type` | string | living room | bedroom, kitchen, bathroom... |
| `style` | string | modern | minimalist, japandi, industrial... |
| `density` | string | moderate | minimal / moderate / dense |
| `num_images` | int | 3 | Variations to generate (1–4) |
| `strength` | float | 0.6 | SD strength (0.3–0.9) |

**Response:**
```json
{
  "success": true,
  "prompt": "...",
  "furniture_detected": ["sofa", "coffee table", "lamp"],
  "segmentation_mask": "<base64>",
  "depth_map": "<base64>",
  "generated_images": ["<base64>", ...],
  "seeds": [123, 456, 789],
  "settings": { "room_type": "...", "style": "...", ... }
}
```

### `POST /feedback`
Submit a rating for a generated image.

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Frontend session ID |
| `image_index` | int | Which variation (0-indexed) |
| `rating` | int | 1 (👍) or -1 (👎) |
| `seed` | int | Seed of rated image |

### `GET /feedback/summary`
Returns aggregate stats including like rate and breakdown by style.

---

## Models

| Model | Task | Source |
|-------|------|--------|
| `nvidia/segformer-b2-finetuned-ade-512-512` | Semantic segmentation | HuggingFace |
| `intel-isl/MiDaS` (small) | Depth estimation | torch.hub |
| `runwayml/stable-diffusion-v1-5` | Image generation | HuggingFace |

---

## Tips for Best Results

- Use well-lit, wide-angle room photos (like real estate listings)
- Strength 0.5–0.65 gives the best redesign while keeping layout
- Living rooms and bedrooms produce the most consistent results
- The URL changes every Colab session — update `API_URL` each time

---

## Limitations

- Generation takes 30–90s on T4 GPU, longer on CPU
- Colab free tier disconnects after ~12h idle
- SD v1.5 is general-purpose, not interior-design-specific
- Segmentation is less accurate on dark or cluttered rooms
