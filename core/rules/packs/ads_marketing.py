# core/rules/packs/ads_marketing.py
from .base import Rule, RulePack

rules = [
    Rule(
        code="AD_GUARANTEED_OUTCOME",
        pattern=r"\b(guaranteed|guarantee|no risk|zero risk)\b",
        message="Absolute guarantee / no risk language is not allowed."
    ),
    Rule(
        code="AD_HEALTH_CURE",
        pattern=r"\b(cures?|cured|permanently heals?|permanent cure)\b",
        message="Unproven cure/medical guarantee claims are not allowed.",
        severity="HIGH"
    ),
]

ADS_MARKETING_PACK = RulePack("ads_marketing", rules)
