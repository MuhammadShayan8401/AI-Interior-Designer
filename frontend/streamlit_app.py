import streamlit as st
import requests
import base64
import uuid
from io import BytesIO
from pathlib import Path
from PIL import Image

# ── Config ────────────────────────────────────────────────────────────────────
API_URL = "https://holmes-lights-euro-happening.trycloudflare.com"   
MAX_UPLOAD_MB = 10

ROOM_TYPES = [
    "living room", "bedroom", "kitchen", "bathroom",
    "dining room", "home office", "nursery", "studio apartment",
]

STYLES = [
    "modern", "minimalist", "scandinavian", "industrial", "bohemian",
    "mid-century modern", "traditional", "japandi", "coastal", "art deco",
]

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interior Designer",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "results" not in st.session_state:
    st.session_state.results = None
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}


# ── Helpers ───────────────────────────────────────────────────────────────────
def b64_to_pil(b64: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(b64)))


def check_api_health() -> tuple[bool, dict]:
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return r.status_code == 200, r.json()
    except Exception as e:
        return False, {"error": str(e)}


def send_feedback(image_index: int, rating: int, seed: int, style: str, room_type: str):
    try:
        requests.post(f"{API_URL}/feedback", data={
            "session_id": st.session_state.session_id,
            "image_index": image_index,
            "rating": rating,
            "seed": seed,
            "style": style,
            "room_type": room_type,
        }, timeout=5)
    except Exception:
        pass  # non-critical


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 Design Controls")

    if st.button("🔌 Check API connection", use_container_width=True):
        ok, info = check_api_health()
        if ok:
            gpu = info.get("gpu", False)
            device = info.get("device", "unknown")
            st.success(f"Connected ✓  \n{'GPU: ' + device if gpu else '⚠️ CPU only (slow)'}")
        else:
            st.error(
                "Cannot reach API.\n\n"
                "1. Make sure Cell 8 is running in Colab\n"
                "2. Paste the new tunnel URL in `API_URL`\n\n"
                f"Error: {info.get('error', 'unknown')}"
            )

    st.divider()

    room_type = st.selectbox("Room type", ROOM_TYPES, index=0)
    style = st.selectbox("Design style", STYLES, index=0)
    density = st.select_slider(
        "Furniture density",
        options=["minimal", "moderate", "dense"],
        value="moderate",
    )

    st.divider()

    num_images = st.slider("Variations to generate", 1, 4, 3)
    strength = st.slider(
        "Transformation strength",
        min_value=0.3, max_value=0.9, value=0.6, step=0.05,
        help="Low = stays close to original layout. High = more creative.",
    )

    st.divider()

    with st.expander("📊 Feedback stats"):
        if st.button("Load stats"):
            try:
                r = requests.get(f"{API_URL}/feedback/summary", timeout=5)
                s = r.json()
                st.metric("Total ratings", s.get("total", 0))
                st.metric("👍 Like rate", f"{s.get('like_rate_pct', 0)}%")
                if s.get("by_style"):
                    st.write("By style:", s["by_style"])
            except Exception as e:
                st.error(f"Could not load: {e}")

    st.caption(f"Session: `{st.session_state.session_id}`")

    if st.button("🗑 Clear results", use_container_width=True):
        st.session_state.results = None
        st.session_state.feedback_given = {}
        st.rerun()


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">AI Interior Designer</div>
    <div class="hero-sub">
        Upload a room photo. Get AI-redesigned interiors in seconds.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a room photo",
    type=["jpg", "jpeg", "png", "webp"],
    help=f"JPG / PNG / WEBP · Max {MAX_UPLOAD_MB}MB · Best results with well-lit, wide-angle room shots",
)

if uploaded_file and uploaded_file.size > MAX_UPLOAD_MB * 1024 * 1024:
    st.error(f"File too large ({uploaded_file.size / 1e6:.1f}MB). Max is {MAX_UPLOAD_MB}MB.")
    uploaded_file = None

# ── Preview + Generate ────────────────────────────────────────────────────────
if uploaded_file:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("**Original room**")
        st.image(Image.open(uploaded_file), use_container_width=True)

    with col_right:
        st.markdown("**Settings**")
        st.markdown(f"""
        | | |
        |---|---|
        | Room | `{room_type}` |
        | Style | `{style}` |
        | Density | `{density}` |
        | Variations | `{num_images}` |
        | Strength | `{strength}` |
        """)

        generate_clicked = st.button(
            "✨ Generate designs",
            use_container_width=True,
            type="primary",
        )

        if generate_clicked:
            if "YOUR_CLOUDFLARE_URL_HERE" in API_URL:
                st.error("Update `API_URL` in `frontend/streamlit_app.py` with your Colab tunnel URL first.")
            else:
                progress = st.progress(0, text="Starting pipeline...")
                status = st.empty()

                try:
                    uploaded_file.seek(0)
                    status.info("📤 Uploading image...")
                    progress.progress(10, text="Uploading...")

                    files = {"image": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                    data = {
                        "room_type": room_type,
                        "style": style,
                        "density": density,
                        "num_images": num_images,
                        "strength": strength,
                    }

                    status.info("🧠 Running segmentation + depth analysis...")
                    progress.progress(30, text="Analysing room...")

                    resp = requests.post(
                        f"{API_URL}/generate",
                        files=files,
                        data=data,
                        timeout=300,
                    )

                    progress.progress(80, text="Decoding results...")
                    result = resp.json()

                    if result.get("success"):
                        progress.progress(100, text="Done!")
                        status.success("Generated successfully!")
                        st.session_state.results = result
                        st.session_state.feedback_given = {}
                        st.rerun()
                    else:
                        progress.empty()
                        status.error(f"Pipeline error: {result.get('error', 'Unknown')}")
                        if "trace" in result:
                            with st.expander("Full traceback"):
                                st.code(result["trace"])

                except requests.exceptions.Timeout:
                    progress.empty()
                    status.error("⏱ Timed out. The model may still be loading — try again in 30s.")
                except requests.exceptions.ConnectionError:
                    progress.empty()
                    status.error("🔌 Connection refused. Is Cell 8 running in Colab?")
                except Exception as e:
                    progress.empty()
                    status.error(f"Unexpected error: {e}")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results
    settings = r.get("settings", {})

    st.divider()
    st.markdown("### Generated designs")

    # Description + prompt
    st.caption(f"🎨 {r.get('description', '')}")
    with st.expander("📝 View full prompt"):
        st.code(r.get("prompt", ""), language=None)

    # Furniture detected
    if r.get("furniture_detected"):
        badges = "  ".join(
            f"`{f}`" for f in r["furniture_detected"]
        )
        st.markdown(f"**Detected furniture:** {badges}")

    st.markdown("")

    # Generated images grid
    cols = st.columns(len(r["generated_images"]), gap="medium")
    for i, (col, b64) in enumerate(zip(cols, r["generated_images"])):
        with col:
            gen_img = b64_to_pil(b64)
            st.image(gen_img, caption=f"Variation {i+1}", use_container_width=True)

            # Download
            buf = BytesIO()
            gen_img.save(buf, format="PNG")
            st.download_button(
                "⬇ Download",
                data=buf.getvalue(),
                file_name=f"interior_{settings.get('style', 'design')}_v{i+1}.png",
                mime="image/png",
                key=f"dl_{i}",
                use_container_width=True,
            )

            # Feedback
            fb_key = f"{st.session_state.session_id}_{i}"
            if fb_key not in st.session_state.feedback_given:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("👍", key=f"like_{i}", use_container_width=True):
                        send_feedback(i, 1, r["seeds"][i], settings.get("style", ""), settings.get("room_type", ""))
                        st.session_state.feedback_given[fb_key] = "liked"
                        st.rerun()
                with c2:
                    if st.button("👎", key=f"dislike_{i}", use_container_width=True):
                        send_feedback(i, -1, r["seeds"][i], settings.get("style", ""), settings.get("room_type", ""))
                        st.session_state.feedback_given[fb_key] = "disliked"
                        st.rerun()
            else:
                fb = st.session_state.feedback_given[fb_key]
                st.markdown(
                    "✅ Liked" if fb == "liked" else "❌ Disliked",
                    help="Feedback recorded"
                )

    # Pipeline internals
    st.divider()
    with st.expander("🔬 Pipeline internals"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Segmentation mask**")
            st.image(b64_to_pil(r["segmentation_mask"]), use_container_width=True)
            st.caption("SegFormer (ADE20K) — detects furniture + room structure")
        with c2:
            st.markdown("**Depth map**")
            st.image(b64_to_pil(r["depth_map"]), use_container_width=True)
            st.caption("MiDaS small — estimates distance/depth per pixel")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 35px 0;
    margin-top: 60px;
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
    border-top: 1px solid rgba(255,255,255,0.15);
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
">
    AI Interior Designer · SegFormer · MiDaS · Stable Diffusion v1.5 · FastAPI · Streamlit
</div>
""", unsafe_allow_html=True)