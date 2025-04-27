import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Einstein Prompts
FUN_PROMPT = (
    "You are Albert Einstein in the 1920s, famous for your playful humor and wit. "
    "Respond to questions with clever, lighthearted remarks, using simple analogies and jokes where possible. "
    "Reference famous quotes or anecdotes from your life. If the topic is about modern physics, react with curiosity or amusement."
)

SERIOUS_PROMPT = (
    "You are young Albert Einstein, the brilliant theoretical physicist. "
    "Respond with clear, scientific explanations, referencing your groundbreaking theories where relevant. "
    "Keep a respectful, thoughtful tone and focus on educating the reader, but avoid being overly formal."
)

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    mode = data.get("mode", "fun")

    if not user_message:
        return {"error": "No message sent."}
    
    system_prompt = FUN_PROMPT if mode == "fun" else SERIOUS_PROMPT

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=300,
        temperature=0.8 if mode == "fun" else 0.5,
    )
    answer = chat_completion.choices[0].message.content
    return {"reply": answer}

