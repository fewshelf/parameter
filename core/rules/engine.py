# core/rules/engine.py
from typing import List
from core.rules.base import RuleMatch
from core.rules.packs.general_safety import GENERAL_SAFETY_PACK
from core.rules.packs.ads_marketing import ADS_MARKETING_PACK
from core.rules.packs.privacy_light import PRIVACY_LIGHT_PACK

PACKS = {
    "general_safety": GENERAL_SAFETY_PACK,
    "ads_marketing": ADS_MARKETING_PACK,
    "privacy_light": PRIVACY_LIGHT_PACK,
}

def run_rulepacks(text: str, profiles: List[str]) -> List[RuleMatch]:
    all_findings = []
    for p in profiles:
        pack = PACKS.get(p)
        if not pack:
            continue
        all_findings.extend(pack.run(text))
    return all_findings
