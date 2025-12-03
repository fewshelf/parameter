# core/engine/decision_engine.py
from typing import Any, Dict, List

from core.rules.base import RuleMatch

SEVERITY_WEIGHT = {
    "LOW": 0.2,
    "MEDIUM": 0.5,
    "HIGH": 0.9,
}


def aggregate_rule_risk(matches: List[RuleMatch]) -> float:
    if not matches:
        return 0.0
    return max(SEVERITY_WEIGHT.get(m.severity, 0.5) for m in matches)


def decide(
    text: str,
    rule_matches: List[RuleMatch],
    llm_result: Dict[str, Any],
    org_config: Dict[str, Any],
) -> Dict[str, Any]:
    rule_risk = aggregate_rule_risk(rule_matches)
    llm_overall_risk = float(llm_result.get("risk_scores", {}).get("overall", 0.0))

    overall_risk = max(rule_risk, llm_overall_risk)

    block_th = org_config.get("block_threshold", 0.8)
    review_th = org_config.get("review_threshold", 0.4)

    if overall_risk >= block_th:
        verdict = "BLOCK"
    elif overall_risk >= review_th:
        verdict = "REVIEW"
    else:
        verdict = "ALLOW"

    issues = []

    # include rule-based issues
    for m in rule_matches:
        issues.append(
            {
                "source": "rule",
                "code": m.code,
                "message": m.message,
                "severity": m.severity,
                "profile": m.profile,
                "span": [m.start, m.end],
            }
        )

    # include LLM issues
    for issue in llm_result.get("issues", []):
        issues.append(
            {
                "source": "llm",
                **issue,
            }
        )

    return {
        "verdict": verdict,
        "scores": {
            "overall": overall_risk,
            "rule_risk": rule_risk,
            "llm_risk": llm_overall_risk,
            "llm_scores": llm_result.get("risk_scores", {}),
        },
        "issues": issues,
        "rewrite": llm_result.get("suggested_rewrite", text),
        "llm_verdict_hint": llm_result.get("verdict_hint"),
        "llm_explanation": llm_result.get("explanation", ""),
    }
