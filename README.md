# PUKHTANA 🏔 — The Living Pashtoon Encyclopedia
### AI-Powered Pashtoon History & Culture Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?logo=google)](https://ai.google.dev)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-gold)](LICENSE)

> *"که سر ورکوم که سر اخلم — زه پښتون يم ددې ملک"*  
> *"Whether I give my head or take another's — I am a Pashtoon of this land"*  
> — Khushal Khan Khattak

**Pukhtana** is an open-source, AI-powered platform preserving and celebrating Pashtoon history for 50M+ diaspora worldwide. Built with FastAPI + Gemini AI.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📜 **Interactive Timeline** | 2,500 years of Pashtoon history — click any event for AI deep-dive |
| 🤖 **AI Historian** | Chat with "Ustaz Ahmad" — powered by Gemini 2.0 Flash |
| 🪪 **Identity Card Generator** | Enter your name & tribe — AI generates your personal ancestral story |
| 📖 **Poetry Corner** | Rahman Baba, Khushal Khan, Nazo Tokhi with AI literary analysis |
| ⚖️ **Pashtunwali Explorer** | All 9 codes of honor with AI historical stories |
| 🏔 **Tribe Profiles** | 12+ major tribes with AI-generated comprehensive histories |
| 📅 **On This Day** | Daily AI-generated Pashtoon historical events |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Free Gemini API key from [Google AI Studio](https://aistudio.google.com) (no credit card)

### Installation

```bash
# Clone
git clone https://github.com/yourusername/pukhtana.git
cd pukhtana

# Install backend
pip install -r backend/requirements.txt

# Set your API key
export GEMINI_API_KEY="your_key_here"

# Run
python backend/main.py
```

Then open `http://localhost:8000` in your browser.

### Frontend Only (No Backend)
Open `frontend/index.html` directly in your browser and enter your Gemini API key in the banner.

---

## 🏗️ Architecture

```
pukhtana/
├── backend/
│   ├── main.py          # FastAPI app — all AI endpoints
│   └── requirements.txt
├── frontend/
│   └── index.html       # Full SPA — cinematic dark gold UI
└── README.md
```

**Stack:**
- **Backend**: FastAPI + Python (Gemini 2.0 Flash API)
- **Frontend**: Pure HTML/CSS/JS (no framework, zero dependencies)
- **AI**: Google Gemini 2.0 Flash (free tier, 1500 req/day)
- **Hosting**: GitHub Pages (frontend) + any free Python host (backend)

---

## 🌐 API Endpoints

```
GET  /api/health          — Server status
GET  /api/timeline        — Full 2,500-year timeline data
GET  /api/poetry          — All poets and poems
GET  /api/pashtunwali     — Pashtunwali code data
GET  /api/tribes          — Tribes overview
GET  /api/today           — On This Day in Pashtoon History (AI)
GET  /api/wisdom          — Random Pashto proverb

POST /api/chat            — AI Historian chat
POST /api/identity        — Generate personal identity card
POST /api/tribe-deep-dive — Full AI tribe profile

GET  /api/pashtunwali/{code}        — AI story for a Pashtunwali value
GET  /api/poetry/{poet}/explain/{n} — AI poem analysis
GET  /api/battle/{battle_name}      — AI battle narrative
```

---

## 🤝 Contributing

This is a community project for the Pashtoon diaspora. Contributions welcome!

- 📝 Add more historical events to the timeline
- 🌍 Add Pashto language translations  
- 🏔 Add more tribe profiles and histories
- 📖 Add more poets and poems
- 🗺️ Add interactive maps

---

## 📄 License

MIT License — Free for the community, forever.

---

*Built by a proud Pashtoon AI Engineer · د پښتنو دپاره*
