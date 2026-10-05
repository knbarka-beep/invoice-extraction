"""Method 2: low-cost LLM (Gemini flash-lite, free tier).

Run from the repo root: py -m methods.method2_gemini
"""
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from methods.llm_common import run
from methods.method1_rules import ROOT

MODELS = ["gemini-3.1-flash-lite-preview", "gemini-flash-lite-latest"]  # fallback order on 503/429

load_dotenv(ROOT / ".env", encoding="utf-8-sig")  # utf-8-sig: the file may start with a BOM
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def call(prompt):
    for model in MODELS:
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
        except errors.APIError as e:
            if e.code in (429, 503) and model != MODELS[-1]:
                continue
            raise
        finally:
            time.sleep(5)  # free-tier rate limit
        um = resp.usage_metadata
        return resp.text, {
            "model": model,
            "input_tokens": um.prompt_token_count,
            "output_tokens": (um.candidates_token_count or 0) + (um.thoughts_token_count or 0),
        }


if __name__ == "__main__":
    run("method2_gemini", call)
