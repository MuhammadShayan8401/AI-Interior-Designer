# 🏠 AI Interior Designer

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-orange.svg)
![Stable Diffusion](https://img.shields.io/badge/Stable%20Diffusion-v1.5-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

> ✨ AI-powered interior redesign system that transforms room images into modern, aesthetic interiors using multi-model generative AI.

---

## 🚀 Live Demo Flow

```
Upload Room Image → SegFormer → MiDaS → Prompt Engine → Stable Diffusion → AI Designs
```

---

## 🧠 Project Overview

This project is a **multi-modal AI system** that understands and redesigns interior spaces using computer vision and generative models.

It combines:

* 🧩 Scene segmentation (SegFormer)
* 📏 Depth estimation (MiDaS)
* 🎨 Prompt engineering layer
* 🖼️ Image generation (Stable Diffusion)
* 📊 Feedback learning loop

---

## ✨ Features

### ⚡ Core Features

* Upload room images (JPG / PNG / WEBP)
* AI-generated interior redesigns
* Multiple design variations (1–4)
* Real-time generation pipeline

### 🧠 AI Capabilities

* Furniture detection (sofa, table, bed, etc.)
* Depth-aware spatial understanding
* Context-aware prompt generation

### 🎨 UI Features

* Midjourney-style grid gallery
* Hover zoom + glow effects
* One-click image download
* Like / dislike feedback system

### 📊 Analytics

* Feedback tracking system
* Style-based performance stats
* Session-based logging

---

## 🏗️ System Architecture

```
Room Image
   ↓
SegFormer (Segmentation)
   ↓
MiDaS (Depth Estimation)
   ↓
Prompt Builder (AI Context Engine)
   ↓
Stable Diffusion (Image Generation)
   ↓
Streamlit UI (Gallery + Feedback)
```

---

## 📁 Project Structure

```
AI-Interior-Designer/
│
├── backend/
│   ├── app.py
│   ├── models/
│   │   ├── segmentation.py
│   │   ├── depth.py
│   │   ├── diffusion.py
│   │   └── prompts.py
│   ├── routes/
│   │   ├── generate.py
│   │   └── feedback.py
│   └── utils/
│       └── image_utils.py
│
├── frontend/
│   ├── streamlit_app.py
│   └── styles.css
│
├── colab_runner.ipynb
├── requirements.txt
└── README.md
```

---

## ⚙️ Quick Start

### 1️⃣ Run Backend (Colab GPU)

1. Open Google Colab
2. Upload `colab_runner.ipynb`
3. Enable GPU (T4 recommended)
4. Run all cells
5. Copy generated URL:

```
https://xxxx.trycloudflare.com
```

---

### 2️⃣ Configure Frontend

```python
API_URL = "https://xxxx.trycloudflare.com"
```

---

### 3️⃣ Run Streamlit App

```bash
pip install streamlit requests pillow
streamlit run frontend/streamlit_app.py
```

Open:

```
http://localhost:8501
```

---

## 📡 API Endpoints

### 🔹 GET /health

Returns system status + GPU info

---

### 🔹 POST /generate

Generates interior designs

| Field      | Type   | Description                |
| ---------- | ------ | -------------------------- |
| image      | file   | Room image                 |
| room_type  | string | bedroom, kitchen, etc      |
| style      | string | modern, japandi, etc       |
| density    | string | minimal / moderate / dense |
| num_images | int    | 1–4 outputs                |
| strength   | float  | creativity level           |

---

### 🔹 POST /feedback

Stores user ratings for improvement

---

### 🔹 GET /feedback/summary

Returns analytics dashboard stats

---

## 🧠 AI Models Used

| Model                 | Task              |
| --------------------- | ----------------- |
| SegFormer (ADE20K)    | Room segmentation |
| MiDaS (Small)         | Depth estimation  |
| Stable Diffusion v1.5 | Image generation  |

---

## 🎯 Best Results Tips

* Use bright, clean room images
* Wide-angle shots work best
* Strength 0.5–0.65 gives realistic output
* Living rooms & bedrooms perform best

---

## ⚠️ Limitations

* Colab session resets after inactivity
* Tunnel URL changes every run
* Model is not fine-tuned for interiors
* CPU mode is slow

---

## 🔮 Future Improvements

* Fine-tuned interior diffusion model
* User authentication system
* Saved design history (DB integration)
* Prompt editor UI
* Docker deployment

---

## 🧩 Tech Stack

* Streamlit
* FastAPI
* PyTorch
* Stable Diffusion
* HuggingFace Transformers
* OpenCV
* Cloudflare Tunnel

---

## 👨‍💻 Author

**Muhammad Shayan Ahmed**
AI + Full Stack Developer

---

⭐ If you like this project, consider starring the repo!
