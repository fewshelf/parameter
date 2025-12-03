# app/main.py
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from core.rules.engine import run_rulepacks
from core.llm.policy_engine import LLMPolicyEngine
from core.engine.decision_engine import decide
from db import get_org_config, save_evaluation


app = FastAPI(
    title="ComplianceGPT Text API",
    version="0.1.0",
)

llm_engine = LLMPolicyEngine()


class CheckRequest(BaseModel):
    text: str
    profiles: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None


@app.post("/v1/check")
async def check_text(
    payload: CheckRequest,
    x_api_key: str = Header(..., alias="X-API-Key"),
):
    org = get_org_config(x_api_key)
    if not org:
        raise HTTPException(status_code=401, detail="Invalid API key")

    profiles = payload.profiles or org.default_profiles

    # 1) run rules
    rule_matches = run_rulepacks(payload.text, profiles)

    # 2) LLM analysis
    llm_result = await llm_engine.analyze(
        text=payload.text,
        rule_matches=[m.to_dict() for m in rule_matches],
        profiles=profiles,
    )

    # 3) decision
    decision = decide(
        text=payload.text,
        rule_matches=rule_matches,
        llm_result=llm_result,
        org_config=org.config,
    )

    # 4) persist (in-memory for now)
    save_evaluation(
        org_id=org.id,
        text=payload.text,
        profiles=profiles,
        decision=decision,
    )

    return {
        "verdict": decision["verdict"],
        "scores": decision["scores"],
        "issues": decision["issues"],
        "rewrite": decision["rewrite"],
        "meta": {
            "llm_verdict_hint": decision["llm_verdict_hint"],
            "llm_explanation": decision["llm_explanation"],
            "profiles": profiles,
        },
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
