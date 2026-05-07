# 🏠 AI Interior Designer

🚀 **Live Demo:**
urlTry AI Interior Designer[https://ai-interior-designer-eurhnj66zzjm4zzhxuggkh.streamlit.app/](https://ai-interior-designer-eurhnj66zzjm4zzhxuggkh.streamlit.app/)

---

## ✨ Overview

AI Interior Designer is a full-stack AI SaaS prototype that transforms room photos into redesigned interiors using state-of-the-art deep learning models.

**Pipeline:**
Room Image → SegFormer (Segmentation) → MiDaS (Depth Estimation) → Prompt Builder → Stable Diffusion (Img2Img) → Final Design

---

## 🧠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-orange)
![Status](https://img.shields.io/badge/Status-Live-success)

---

## 🏗️ Architecture

```
Frontend (Streamlit)
        ↓
FastAPI Backend (Colab / Cloudflare Tunnel)
        ↓
────────────────────────────
SegFormer → Scene Understanding
MiDaS → Depth Mapping
Prompt Builder → AI Prompt Engineering
Stable Diffusion → Image Generation
────────────────────────────
        ↓
Generated Interior Designs
```

---

## 📂 Project Structure

```
AI-Interior-Designer/
│
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── utils/
│   └── uploads/
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

## 🚀 Features

* 🖼 Upload room image
* 🎨 AI redesign in multiple styles
* 🏠 Room type customization
* 📦 Furniture density control
* 🔥 Multiple variations generation
* 👍 Feedback system (like/dislike)
* 📊 Live analytics dashboard
* ⚡ GPU-powered generation via Colab

---

## ⚙️ Quick Start

### 1️⃣ Run Backend (Google Colab)

* Open Colab
* Upload `colab_runner.ipynb`
* Enable GPU (T4)
* Run all cells
* Copy generated Cloudflare URL

---

### 2️⃣ Setup Frontend

Update:

```python
API_URL = "https://your-colab-url.trycloudflare.com"
```

---

### 3️⃣ Run Streamlit App

```bash
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

---

## 🧪 API Endpoints

### GET `/health`

Check system status

### POST `/generate`

Generate AI interior designs

### POST `/feedback`

Submit user ratings

### GET `/feedback/summary`

Analytics dashboard

---

## 🤖 AI Models Used

| Model                 | Task               |
| --------------------- | ------------------ |
| SegFormer             | Scene segmentation |
| MiDaS                 | Depth estimation   |
| Stable Diffusion v1.5 | Image generation   |

---

## 📊 Best Practices

* Use bright, clean room images
* Optimal strength: 0.5 – 0.65
* Works best on living rooms & bedrooms

---

## ⚠️ Limitations

* Colab session resets every ~12 hours
* First generation may be slow (model loading)
* Free GPU has performance limits

---

## 🚀 Deploy

### Streamlit Cloud

[![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

* Repo: `AI-Interior-Designer`
* Main file: `frontend/streamlit_app.py`

---

## 💡 Author

**Muhammad Shayan Ahmed**

AI + Full Stack Developer | Computer Science Student

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub and share it!
