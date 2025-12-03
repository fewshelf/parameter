# core/rules/base.py
from typing import List, Dict, Any
import re

class RuleMatch:
    def __init__(self, code: str, message: str, start: int, end: int, severity: str, profile: str):
        self.code = code
        self.message = message
        self.start = start
        self.end = end
        self.severity = severity
        self.profile = profile

class Rule:
    def __init__(self, code: str, pattern: str, message: str, severity: str = "MEDIUM"):
        self.code = code
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.message = message
        self.severity = severity

    def apply(self, text: str, profile: str) -> List[RuleMatch]:
        matches = []
        for m in self.regex.finditer(text):
            matches.append(
                RuleMatch(
                    code=self.code,
                    message=self.message,
                    start=m.start(),
                    end=m.end(),
                    severity=self.severity,
                    profile=profile
                )
            )
        return matches

class RulePack:
    def __init__(self, name: str, rules: List[Rule]):
        self.name = name
        self.rules = rules

    def run(self, text: str) -> List[RuleMatch]:
        findings = []
        for r in self.rules:
            findings.extend(r.apply(text, self.name))
        return findings
