import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

SYSTEM_PROMPT = """
You are a fact-checking assistant.

Return ONLY valid JSON with this exact schema:
{
  "credibility_score": number between 0 and 1,
  "verdict": string,
  "reasons": array of strings,
  "disclaimer": string
}

Do NOT use markdown.
Do NOT wrap in ```json.
"""


def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

def check_credibility(headline, image_file=None):
    user_content = [{"type": "text", "text": f"Headline: {headline}"}]

    if image_file:
        user_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encode_image(image_file)}"
            }
        })

    response = client.chat.completions.create(
        model="qwen/qwen2.5-vl-72b-instruct",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
    )

    return response.choices[0].message.content
