from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    prompt = f"You are a friendly AI companion. Respond to the user as a supportive friend.\nUser: {req.message}\nAI:"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.8
    )
    text = response.choices[0].message.content
    # Simple mood detection
    mood = "neutral"
    if any(word in req.message.lower() for word in ["sad", "depressed", "unhappy"]):
        mood = "sad"
    elif any(word in req.message.lower() for word in ["happy", "good", "excited"]):
        mood = "happy"
    return {"text": text, "mood": mood}
