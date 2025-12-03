# core/rules/packs/ads_marketing.py
from core.rules.base import Rule, RulePack

rules = [

    # --- Absolute guarantees / no-risk claims ---
    Rule(
        code="AD_GUARANTEED_OUTCOME",
        pattern=r"\b(guaranteed?|money[- ]back guarantee|100% (success|results)|"
                r"you can’t lose|you cannot lose|will (always|definitely) work)\b",
        message="Absolute guarantee of outcome is generally not compliant.",
        severity="HIGH"
    ),
    Rule(
        code="AD_NO_RISK",
        pattern=r"\b(no risk|zero risk|risk[- ]free|safe and guaranteed)\b",
        message="No-risk claims are typically not compliant.",
        severity="MEDIUM"
    ),

    # --- Financial promise / unrealistic earnings ---
    Rule(
        code="AD_FAST_RICHES",
        pattern=r"\b(make \$?\d{3,}[kK]?\s*(per (day|week|month)|in \d+ (days?|weeks?|months?))|"
                r"become a millionaire (overnight|in (30|60|90) days))\b",
        message="Unrealistic or unsubstantiated income/wealth claims.",
        severity="HIGH"
    ),
    Rule(
        code="AD_PASSIVE_INCOME_PROMISE",
        pattern=r"\b(passive income (for life|forever)|income while you sleep with no effort)\b",
        message="Strong earning claims implying no effort or risk.",
        severity="MEDIUM"
    ),

    # --- Health / medical cure claims ---
    Rule(
        code="AD_HEALTH_DISEASE_CURE",
        pattern=r"\b(cures?|heals?|eliminates?|reverses?) (cancer|diabetes|depression|anxiety|"
                r"alzheimer'?s|hiv|aids|autism|heart disease)\b",
        message="Disease cure or reversal claims typically require strict substantiation/regulation.",
        severity="HIGH"
    ),
    Rule(
        code="AD_HEALTH_PERMANENT_RESULTS",
        pattern=r"\b(permanently (clear|remove|erase) (acne|wrinkles?|fat|cellulite)|"
                r"permanent(ly)? (weight loss|hair growth))\b",
        message="Permanent health/appearance claims are often non-compliant.",
        severity="MEDIUM"
    ),
    Rule(
        code="AD_HEALTH_UNQUALIFIED_ADVICE",
        pattern=r"\b(stop taking your medication|you don’t need a doctor anymore)\b",
        message="Discouraging medical supervision or medication without context.",
        severity="HIGH"
    ),

    # --- Weight loss / body image ---
    Rule(
        code="AD_WEIGHT_LOSS_FAST",
        pattern=r"\b(lose \d{2,} ?(kg|lbs|pounds) in (a week|7 days|10 days|14 days|a month)|"
                r"drop \d{2,} ?(kg|lbs) (instantly|overnight))\b",
        message="Aggressive fast weight-loss claims are often non-compliant.",
        severity="MEDIUM"
    ),

    # --- Social proof exaggeration / fake stats ---
    Rule(
        code="AD_FAKE_EVERYONE_DOES_IT",
        pattern=r"\b(everyone (uses|is using) this|"
                r"all my clients (achieve|get) these results)\b",
        message="Broad, absolute social proof statements without substantiation.",
        severity="LOW"
    ),

    # --- Limited-time / scarcity (potentially manipulative) ---
    Rule(
        code="AD_FAKE_SCARCITY",
        pattern=r"\b(only \d+ spots left forever|never available again|"
                r"last chance ever to (join|buy))\b",
        message="Strong ‘never again’ scarcity language that can be misleading.",
        severity="LOW"
    ),

]

ADS_MARKETING_PACK = RulePack("ads_marketing", rules)
