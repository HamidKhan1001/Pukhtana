from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_KEY)

app = FastAPI(title="PUKHTANA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
Respond in 2-4 paragraphs. Be dramatic, historically accurate, and speak with the pride of an elder telling stories around a fire."""


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []


class IdentityRequest(BaseModel):
    name: str
    tribe: str
    region: str


@app.get("/")
def root():
    return {"status": "PUKHTANA API running", "routes": ["/api/chat", "/api/identity"]}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not GEMINI_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in .env")
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM
        )
        # Build history for multi-turn
        history_parts = []
        for h in (req.history or [])[-10:]:
            role = "user" if h.get("role") == "user" else "model"
            history_parts.append({"role": role, "parts": [h.get("content", "")]})

        chat_session = model.start_chat(history=history_parts)
        response = chat_session.send_message(req.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/identity")
async def identity(req: IdentityRequest):
    if not GEMINI_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in .env")
    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        prompt = f"""Create a proud Pashtoon identity profile for:
Name: {req.name} | Tribe: {req.tribe} | Region: {req.region}

Return ONLY valid JSON (no markdown, no backticks, no extra text):
{{
  "tribal_legacy": "2-3 sentences on the {req.tribe} tribe's greatest historical achievements",
  "ancestral_warriors": "Name 1-2 famous historical figures from the {req.tribe} tribe and their deeds",
  "pashtunwali_spirit": "Which of the 9 Pashtunwali values best defines the {req.tribe} tribe and one line why",
  "ancient_homeland": "The original homeland and 1-sentence origin story of the {req.tribe}",
  "historical_moment": "One specific historical event where the {req.tribe} tribe shaped Pashtoon or world history",
  "message_from_ancestors": "A powerful, moving 2-3 sentence message as if your ancestors are speaking directly to {req.name} today in 2025"
}}"""
        response = model.generate_content(prompt)
        import json, re
        text = response.text.strip()
        # Strip markdown fences
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            data = json.loads(m.group(0))
            return data
        raise HTTPException(status_code=500, detail="Could not parse JSON from Gemini response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
