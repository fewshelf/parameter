# core/llm/policy_engine.py
import json
from typing import Any, Dict, List

from openai import OpenAI


MASTER_PROMPT = """
You are ComplianceGPT, an enterprise-level AI content compliance analyst.

Your job is to assess text for regulatory, safety, privacy, brand, and advertising compliance risks.

You MUST follow these rules:
1. ALWAYS output valid minified JSON following the schema I will provide.
2. NO extra commentary. NO prose. Only JSON.
3. Base your reasoning on:
   - The text provided.
   - The rule_matches (these are signals, not final verdicts).
   - The compliance profiles activated (e.g., "general_safety", "ads_marketing", "privacy_light").

4. Evaluate the text across these risk areas:
   - Regulatory risk (laws, health claims, financial claims)
   - Safety risk (violence, hate, harassment, self-harm)
   - Privacy risk (PII, minors, sensitive data)
   - Brand risk (tone, misleading claims, extremism, low-quality content)

5. Produce:
   - risk_scores (0.0 to 1.0)
   - a verdict_hint ("ALLOW", "REVIEW", "BLOCK")
   - issues[] (list of risks with severity)
   - suggested_rewrite (a safer, compliant version)
   - explanation (short summary)

6. VERY IMPORTANT:
   - Your JSON MUST include every key even if empty.
   - If content contains a serious violation (e.g., minors, violence, medical cure claims), severity HIGH.

7. DO NOT hallucinate rules. Use general industry standards only.

JSON schema you MUST strictly follow:
{
  "risk_scores": {
    "regulatory": float,
    "safety": float,
    "privacy": float,
    "brand": float,
    "overall": float
  },
  "verdict_hint": "ALLOW | REVIEW | BLOCK",
  "issues": [
    {
      "category": "string",
      "message": "string",
      "severity": "LOW | MEDIUM | HIGH"
    }
  ],
  "suggested_rewrite": "string",
  "explanation": "string"
}

Return ONLY JSON.
"""


class LLMPolicyEngine:
    def __init__(self, model: str = "gpt-4.1"):
        self.client = OpenAI()
        self.model = model

    async def analyze(
        self,
        text: str,
        rule_matches: List[Dict[str, Any]],
        profiles: List[str]
    ) -> Dict[str, Any]:
        """
        Returns dict:
        {
          "risk_scores": {...},
          "verdict_hint": "...",
          "issues": [...],
          "suggested_rewrite": "...",
          "explanation": "..."
        }
        """
        try:
            user_content = {
                "text": text,
                "rule_matches": rule_matches,
                "profiles": profiles,
            }

            response = await self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": MASTER_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": json.dumps(user_content),
                    },
                ],
                response_format={"type": "json_object"},
            )

            # responses.create returns a structured object; extract the text
            content = response.output[0].content[0].text
            result = json.loads(content)
        except Exception as e:
            # Fail-safe: if LLM fails, return neutral, ALLOW
            result = {
                "risk_scores": {
                    "regulatory": 0.0,
                    "safety": 0.0,
                    "privacy": 0.0,
                    "brand": 0.0,
                    "overall": 0.0,
                },
                "verdict_hint": "REVIEW",
                "issues": [
                    {
                        "category": "system_error",
                        "message": f"LLM policy engine error: {str(e)}",
                        "severity": "MEDIUM",
                    }
                ],
                "suggested_rewrite": text,
                "explanation": "LLM engine failed; defaulting to REVIEW.",
            }

        # sanity-fill missing keys
        result.setdefault("risk_scores", {})
        rs = result["risk_scores"]
        for k in ["regulatory", "safety", "privacy", "brand", "overall"]:
            rs.setdefault(k, 0.0)
        result.setdefault("verdict_hint", "REVIEW")
        result.setdefault("issues", [])
        result.setdefault("suggested_rewrite", text)
        result.setdefault("explanation", "")

        return result
