"""
routes/feedback.py
POST /feedback       — Submit thumbs up/down for a generated image
GET  /feedback/summary — Aggregate stats
GET  /feedback/all     — Full feedback log (for debugging/export)
"""

import json
import time
from pathlib import Path
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

router = APIRouter()

# ── Storage ───────────────────────────────────────────────────────────────────
# In-memory store + optional JSON persistence to uploads/feedback.json
FEEDBACK_FILE = Path(__file__).parent.parent / "uploads" / "feedback.json"
_feedback: list[dict] = []


def _load_feedback():
    """Load persisted feedback from disk on startup."""
    global _feedback
    if FEEDBACK_FILE.exists():
        try:
            _feedback = json.loads(FEEDBACK_FILE.read_text())
        except Exception:
            _feedback = []


def _save_feedback():
    """Persist feedback to disk."""
    try:
        FEEDBACK_FILE.parent.mkdir(exist_ok=True)
        FEEDBACK_FILE.write_text(json.dumps(_feedback, indent=2))
    except Exception:
        pass  # Non-critical — still works in-memory


_load_feedback()


# ── Routes ────────────────────────────────────────────────────────────────────
@router.post("")
async def submit_feedback(
    session_id: str = Form(...),
    image_index: int = Form(...),
    rating: int = Form(...),      # 1 = thumbs up, -1 = thumbs down
    seed: int = Form(0),
    room_type: str = Form(""),
    style: str = Form(""),
):
    """
    Submit feedback for a generated image.

    - **session_id**: Unique session identifier from the frontend
    - **image_index**: Which generated image (0-indexed)
    - **rating**: 1 (👍) or -1 (👎)
    - **seed**: The seed used to generate the image
    - **room_type**: Optional — logged for analytics
    - **style**: Optional — logged for analytics
    """
    if rating not in (1, -1):
        return JSONResponse(
            {"success": False, "error": "rating must be 1 or -1"}, status_code=400
        )

    entry = {
        "session_id": session_id,
        "image_index": image_index,
        "rating": rating,
        "seed": seed,
        "room_type": room_type,
        "style": style,
        "timestamp": time.time(),
    }
    _feedback.append(entry)
    _save_feedback()

    return JSONResponse({
        "success": True,
        "message": "Feedback recorded. Thank you!",
        "total_feedback": len(_feedback),
    })


@router.get("/summary")
async def feedback_summary():
    """Return aggregate feedback stats."""
    total = len(_feedback)
    likes = sum(1 for f in _feedback if f["rating"] == 1)
    dislikes = total - likes
    like_rate = round(likes / total * 100, 1) if total > 0 else 0

    # Break down by style
    style_counts: dict[str, dict] = {}
    for f in _feedback:
        s = f.get("style") or "unknown"
        if s not in style_counts:
            style_counts[s] = {"likes": 0, "dislikes": 0}
        if f["rating"] == 1:
            style_counts[s]["likes"] += 1
        else:
            style_counts[s]["dislikes"] += 1

    return JSONResponse({
        "total": total,
        "likes": likes,
        "dislikes": dislikes,
        "like_rate_pct": like_rate,
        "by_style": style_counts,
    })


@router.get("/all")
async def feedback_all():
    """Return full feedback log (for export/debugging)."""
    return JSONResponse({"feedback": _feedback, "total": len(_feedback)})


@router.delete("/clear")
async def clear_feedback():
    """Clear all feedback (admin use)."""
    global _feedback
    _feedback = []
    _save_feedback()
    return JSONResponse({"success": True, "message": "All feedback cleared."})
