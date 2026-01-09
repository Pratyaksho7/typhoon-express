from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import json

from ai import check_credibility

app = FastAPI()

# CORS (allow frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check")
async def check_news(
    headline: str = Form(...),
    image: UploadFile | None = None
):
    # Get raw AI output (string)
    raw_result = check_credibility(headline, image)

    # Remove markdown formatting if present
    cleaned_result = (
        raw_result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Convert string JSON → real JSON
    try:
        parsed_result = json.loads(cleaned_result)
        return parsed_result
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_output": raw_result
        }
