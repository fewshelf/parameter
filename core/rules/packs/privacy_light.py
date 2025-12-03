# core/rules/packs/privacy_light.py
from core.rules.base import Rule, RulePack

rules = [

    # --- Email addresses ---
    Rule(
        code="PR_EMAIL",
        pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}",
        message="Contains what appears to be an email address (personal identifier).",
        severity="MEDIUM"
    ),

    # --- Phone numbers (very broad, US-biased) ---
    Rule(
        code="PR_PHONE",
        pattern=r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
        message="Contains what appears to be a phone number.",
        severity="MEDIUM"
    ),

    # --- SSN-like pattern (US) ---
    Rule(
        code="PR_SSN_US",
        pattern=r"\b\d{3}-\d{2}-\d{4}\b",
        message="Contains a number formatted like a US Social Security Number.",
        severity="HIGH"
    ),

    # --- Credit card-like sequences (broad; expect false positives) ---
    Rule(
        code="PR_CREDIT_CARD",
        pattern=r"\b(?:\d[ -]*?){13,16}\b",
        message="Contains a long digit sequence that may be a payment card number.",
        severity="HIGH"
    ),

    # --- Dates of birth (MM/DD/YYYY or DD/MM/YYYY – crude) ---
    Rule(
        code="PR_DOB",
        pattern=r"\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12]\d|3[01])[/-](19|20)\d{2}\b",
        message="Contains a date that may be a date of birth.",
        severity="MEDIUM"
    ),

    # --- Explicit age statements (potential minors) ---
    Rule(
        code="PR_MINOR_AGE_SELF",
        pattern=r"\b(i am|i'm)\s*(?:\d{1,2})\b",
        message="Explicit self-disclosed age; may indicate a minor.",
        severity="MEDIUM"
    ),
    Rule(
        code="PR_MINOR_AGE_OTHER",
        pattern=r"\b(my|our) (son|daughter|child|kid) is\s*(?:\d{1,2})\b",
        message="Explicit age of a child; may be sensitive personal data.",
        severity="LOW"
    ),

    # --- Physical address indicators (very high-level) ---
    Rule(
        code="PR_ADDRESS_INDICATOR",
        pattern=r"\b(\d{1,5}\s+[A-Za-z0-9.\s]+(street|st\.|road|rd\.|avenue|ave\.|boulevard|blvd\.|lane|ln\.))\b",
        message="Looks like a street address (physical location).",
        severity="MEDIUM"
    ),
]

PRIVACY_LIGHT_PACK = RulePack("privacy_light", rules)
