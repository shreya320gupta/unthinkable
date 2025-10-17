import os
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")


app = FastAPI(title="Gemini Code Review Assistant Backend")

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini model details
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"

# Request body model
class CodeReviewRequest(BaseModel):
    code: str
    source: str = "Pasted Code"

@app.get("/")
def root():
    return {"message": "Gemini Code Review Assistant API is running."}


@app.post("/review")
def review_code(request: CodeReviewRequest):
    """Accept code as text and return AI-generated review."""
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code content cannot be empty.")
    
    system_prompt = (
        "You are a professional senior software engineer performing a code review. "
        "Provide a structured, actionable review that includes:\n"
        "1. Summary of what the code does\n"
        "2. Major issues or bugs\n"
        "3. Style and readability improvements\n"
        "4. Performance or security concerns\n"
        "Use clear Markdown formatting (headings, bullet points, and code blocks where relevant)."
    )

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Review the following code (source: {request.source}):\n\n---\n{request.code}\n---"
                    }
                ]
            }
        ],
    }

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        candidate = data.get("candidates", [{}])[0]
        text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        if not text:
            raise HTTPException(status_code=502, detail="Empty response from Gemini API.")

        # Optional: extract sources
        sources = []
        grounding_metadata = candidate.get("groundingMetadata", {})
        for attr in grounding_metadata.get("groundingAttributions", []):
            web = attr.get("web", {})
            if web.get("uri") and web.get("title"):
                sources.append({"title": web["title"], "uri": web["uri"]})

        return {"review": text, "sources": sources}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Gemini API request failed: {e}")
