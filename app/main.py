# app/main.py
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.rules.engine import run_rulepacks
from core.llm.policy_engine import LLMPolicyEngine
from core.engine.decision_engine import decide
from db import get_org_config, save_evaluation

app = FastAPI()
llm_engine = LLMPolicyEngine(client=...)  # plug your LLM client

class CheckRequest(BaseModel):
    text: str
    profiles: Optional[List[str]] = None
    options: Optional[dict] = None

@app.post("/v1/check")
async def check_text(payload: CheckRequest, x_api_key: str = Header(...)):
    org = get_org_config(x_api_key)
    if not org:
        raise HTTPException(status_code=401, detail="Invalid API key")

    profiles = payload.profiles or org.default_profiles

    # 1) Rules
    rule_matches = run_rulepacks(payload.text, profiles)

    # 2) LLM
    llm_result = await llm_engine.analyze(
        text=payload.text,
        rule_matches=[m.__dict__ for m in rule_matches],
        profiles=profiles
    )

    # 3) Decision
    decision = decide(
        text=payload.text,
        rule_matches=rule_matches,
        llm_result=llm_result,
        org_config=org.config
    )

    # 4) Persist
    save_evaluation(
        org_id=org.id,
        text=payload.text,
        profiles=profiles,
        decision=decision
    )

    return decision
