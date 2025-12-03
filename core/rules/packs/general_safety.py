# core/rules/packs/general_safety.py
from core.rules.base import Rule, RulePack

rules = [

    # --- Hate / Harassment / Slurs (sample – expand privately) ---
    Rule(
        code="GS_HATE_RACE_ETHNICITY",
        pattern=r"\b(nigg\w*|chink\w*|spic\w*|kike\w*|wetback\w*|paki\w*)\b",
        message="Contains racial/ethnic slurs that violate hate-speech and brand-safety policies.",
        severity="HIGH"
    ),
    Rule(
        code="GS_HATE_RELIGION",
        pattern=r"\b(kill all (muslims?|jews?|christians?)|exterminate (muslims?|jews?|christians?))\b",
        message="Incitement to violence against religious groups.",
        severity="HIGH"
    ),
    Rule(
        code="GS_HARASSMENT_DIRECT",
        pattern=r"\b(you are (worthless|useless|disgusting|a failure)|nobody (likes|wants) you)\b",
        message="Direct harassment / demeaning language towards a person.",
        severity="MEDIUM"
    ),

    # --- Self-harm / Suicide ---
    Rule(
        code="GS_SELF_HARM_IDEATION",
        pattern=r"\b(i (want to|wanna|will) (kill myself|end my life|die)|"
                r"thinking about suicide|considering suicide|i can’t go on)\b",
        message="Mentions of self-harm or suicidal ideation.",
        severity="HIGH"
    ),
    Rule(
        code="GS_SELF_HARM_INSTRUCTION",
        pattern=r"\b(how (do i|to) kill myself|best way to commit suicide)\b",
        message="Requests for instructions or methods of self-harm.",
        severity="HIGH"
    ),

    # --- Violence / Threats ---
    Rule(
        code="GS_VIOLENT_THREAT_DIRECT",
        pattern=r"\b(i (will|am going to) (kill|shoot|stab|beat) (you|him|her|them))\b",
        message="Direct threat of violence against a person.",
        severity="HIGH"
    ),
    Rule(
        code="GS_VIOLENT_MASS_HARM",
        pattern=r"\b(shoot up (the )?(school|office|place)|massacre|"
                r"bomb (the )?(building|place|school|office))\b",
        message="Mentions of mass violence or attacks.",
        severity="HIGH"
    ),

    # --- Sexual explicit / minors (text-only, high-level) ---
    Rule(
        code="GS_SEX_EXPLICIT_GENERIC",
        pattern=r"\b(porn(?!ography class)|pornographic|hardcore sex|explicit sex|sex tape)\b",
        message="Sexually explicit content that may be inappropriate for general audiences.",
        severity="MEDIUM"
    ),
    Rule(
        code="GS_SEX_MINOR",
        pattern=r"\b(sex with (a )?(minor|child|kid|underage)|"
                r"13[- ]year[- ]old (girl|boy) (sex|naked|nude))\b",
        message="Sexual content involving minors is strictly prohibited.",
        severity="HIGH"
    ),

    # --- Extremism / Terror Praise ---
    Rule(
        code="GS_EXTREMISM_PRAISE",
        pattern=r"\b(i (support|love|admire) (isis|al[- ]qaeda|nazis?|hitler)|"
                r"(isis|al[- ]qaeda) (are|is) (heroes?|great))\b",
        message="Apparent praise or support for extremist or terrorist organizations.",
        severity="HIGH"
    ),
]

GENERAL_SAFETY_PACK = RulePack("general_safety", rules)
