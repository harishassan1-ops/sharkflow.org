import os
from typing import Dict, Any
from dotenv import load_dotenv
from models import IngestRecord, AIResult
import random

load_dotenv()

USE_OPENAI = False  # flip to True to enable real LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def run_ai_enrichment(rec: IngestRecord) -> AIResult:
    if not USE_OPENAI or not OPENAI_API_KEY:
        # Safe deterministic-ish stub for local testing
        sentiment = random.choice(["positive", "neutral", "negative"])
        category = "general"
        risk_score = round(random.random(), 3)
        return AIResult(sentiment=sentiment, category=category, risk_score=risk_score, extra={})
    else:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = f"""Classify and score this record.
        
        Name: {rec.name}
        Email: {rec.email}
        Phone: {rec.phone}
        Notes: {rec.notes}
        
        Return JSON with:
        - sentiment (positive|neutral|negative)
        - category (string)
        - risk_score (0..1 float)
        """
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2
        )
        # Very basic extraction from text output
        text = resp.output_text
        import json, re
        try:
            data = json.loads(re.search(r"\{[\s\S]*\}", text).group(0))
        except Exception:
            data = {"sentiment":"neutral","category":"general","risk_score":0.5}
        return AIResult(
            sentiment=data.get("sentiment"),
            category=data.get("category"),
            risk_score=float(data.get("risk_score", 0.5)),
            extra=data
        )
