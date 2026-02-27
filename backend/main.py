from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"

app = FastAPI(title="PUKHTANA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM = """You are Ustaz Ahmad, a deeply knowledgeable and proud Pashtoon historian and cultural elder.
You speak with authority, warmth, and immense pride about Pashtoon civilization.
You know everything about:
- Ancient origins: Bani Israel theory, Qais Abdur Rashid, Gandharan civilization
- Empires: Hotaki (1709), Durrani (1747), connections to Mughal and Safavid courts
- Warriors: Ahmad Shah Durrani (Baba), Mirwais Hotak, Khushal Khan Khattak, Sher Shah Suri, Mahmud Hotak
- Anglo-Afghan Wars: 1st (1839-42), 2nd (1878-80), 3rd (1919) and their outcomes
- Pashtunwali: Melmastia, Nanawatai, Badal, Nang, Tureh, Sabat, Isteqamat, Namus, Ghayrat
- Geography: Khyber Pakhtunkhwa, Kandahar, Kabul, Peshawar, Khyber Pass, Waziristan, Swat, FATA
- Tribes: Durrani, Ghilzai, Yusufzai, Afridi, Khattak, Wazir, Mahsud, Mohmand, Kakar, Shinwari, Bangash, Orakzai
- Poetry: Rahman Baba (mystic), Khushal Khan Khattak (warrior-poet), Nazo Tokhi (founding poetess), Ghani Khan
- Culture: Attan dance, Jirga system, Hujra guest house, Pashto and Dari languages, Pakol, tribal music
- Modern: Khan Abdul Ghaffar Khan (Frontier Gandhi), Khudai Khidmatgar, 1947 partition, Durand Line controversy
Respond in 2-4 paragraphs. Be dramatic, historically accurate, and speak with the pride of an elder telling stories around a fire.
"""

IDENTITY_SYSTEM = """You are generating a proud Pashtoon identity profile.
Return JSON only. No markdown fences. No commentary outside JSON.
Be historically grounded, concise, and emotionally powerful.
"""

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class IdentityRequest(BaseModel):
    name: str
    tribe: str
    region: str


def get_model(system_instruction: Optional[str] = None):
    if not GEMINI_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in .env")
    try:
        if system_instruction:
            return genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=system_instruction
            )
        return genai.GenerativeModel(model_name=MODEL_NAME)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Gemini model: {str(e)}")


def raise_gemini_error(e: Exception):
    msg = str(e)

    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        raise HTTPException(
            status_code=429,
            detail="AI Historian is temporarily unavailable because the Gemini free quota is exhausted. Please try again later."
        )

    if "API key not valid" in msg or "API_KEY_INVALID" in msg:
        raise HTTPException(status_code=401, detail="Invalid Gemini API key in .env")

    raise HTTPException(status_code=500, detail=msg)


def clean_json_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0).strip()

    return text


@app.get("/")
def root():
    return {
        "status": "PUKHTANA API running",
        "model": MODEL_NAME,
        "routes": ["/api/chat", "/api/identity"]
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "key_loaded": bool(GEMINI_KEY)
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        model = get_model(SYSTEM)

        history_parts = []
        for h in (req.history or [])[-10:]:
            content = str(h.get("content", "")).strip()
            if not content:
                continue

            role = "user" if h.get("role") == "user" else "model"
            history_parts.append({
                "role": role,
                "parts": [content]
            })

        chat_session = model.start_chat(history=history_parts)
        response = chat_session.send_message(req.message.strip())

        return {"response": response.text}
    except HTTPException:
        raise
    except Exception as e:
        raise_gemini_error(e)


@app.post("/api/identity")
async def identity(req: IdentityRequest):
    try:
        model = get_model(IDENTITY_SYSTEM)

        prompt = f"""Create a proud Pashtoon identity profile for:
Name: {req.name}
Tribe: {req.tribe}
Region: {req.region}

Return ONLY valid JSON:
{{
  "tribal_legacy": "2-3 sentences on the {req.tribe} tribe's greatest historical achievements",
  "ancestral_warriors": "Name 1-2 famous historical figures from the {req.tribe} tribe and their deeds",
  "pashtunwali_spirit": "Which of the 9 Pashtunwali values best defines the {req.tribe} tribe and one line why",
  "ancient_homeland": "The original homeland and 1-sentence origin story of the {req.tribe}",
  "historical_moment": "One specific historical event where the {req.tribe} tribe shaped Pashtoon or world history",
  "message_from_ancestors": "A powerful, moving 2-3 sentence message as if your ancestors are speaking directly to {req.name} today"
}}"""

        response = model.generate_content(prompt)
        cleaned = clean_json_text(response.text)
        data = json.loads(cleaned)

        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Could not parse JSON from Gemini response")
    except HTTPException:
        raise
    except Exception as e:
        raise_gemini_error(e)