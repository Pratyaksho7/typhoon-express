from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import json

from ai import check_credibility

app = FastAPI()

# ✅ ENABLE CORS (GitHub Pages → Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check (REQUIRED by Render)
@app.get("/")
def health():
    return {"status": "FastAPI backend running"}

# ✅ Main API
@app.post("/check")
async def check_news(
    headline: str = Form(...),
    image: UploadFile | None = None
):
    raw_result = check_credibility(headline, image)

    # Clean AI response
    cleaned_result = (
        raw_result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(cleaned_result)
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_output": raw_result
        }
