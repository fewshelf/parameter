# core/rules/engine.py
from typing import List, Dict
from .packs.ads_marketing import ADS_MARKETING_PACK
# from .packs.general_safety import GENERAL_SAFETY_PACK
# ...

PACKS = {
    "ads_marketing": ADS_MARKETING_PACK,
    # "general_safety": GENERAL_SAFETY_PACK,
}

def run_rulepacks(text: str, profiles: List[str]):
    all_findings = []
    for p in profiles:
        pack = PACKS.get(p)
        if not pack:
            continue
        all_findings.extend(pack.run(text))
    return all_findings
