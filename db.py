# 
from dataclasses import dataclass, field
from typing import Dict, List, Any
import time
import uuid


@dataclass
class OrgConfig:
    id: str
    name: str
    api_key: str
    default_profiles: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)


# In-memory single org for now
_ORG = OrgConfig(
    id="org_demo",
    name="Demo Org",
    api_key="demo-key-123",  # replace with env / real store
    default_profiles=["general_safety", "ads_marketing", "privacy_light"],
    config={
        "block_threshold": 0.8,
        "review_threshold": 0.4,
    },
)

_EVALS: List[Dict[str, Any]] = []


def get_org_config(api_key: str) -> OrgConfig | None:
    if api_key == _ORG.api_key:
        return _ORG
    return None


def save_evaluation(org_id: str, text: str, profiles: List[str], decision: Dict[str, Any]) -> None:
    _EVALS.append(
        {
            "id": str(uuid.uuid4()),
            "org_id": org_id,
            "text": text,
            "profiles": profiles,
            "decision": decision,
            "created_at": time.time(),
        }
    )
