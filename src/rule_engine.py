import re
from typing import List, Dict, Any

class Rule:
    def __init__(self, action: str, msg: str, regex: str, severity: str = "medium", src_ip: str = None, dst_ip: str = None, whitelist: List[str] = None):
        self.action = action
        self.msg = msg
        self.regex = regex
        self.severity = severity
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.whitelist = whitelist or []

    def match(self, log: str, src_ip: str = None, dst_ip: str = None) -> bool:
        if self.src_ip and self.src_ip != src_ip:
            return False
        if self.dst_ip and self.dst_ip != dst_ip:
            return False
        if src_ip and src_ip in self.whitelist:
            return False
        return re.search(self.regex, log, re.IGNORECASE) is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "msg": self.msg,
            "regex": self.regex,
            "severity": self.severity,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "whitelist": self.whitelist
        }

class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    @classmethod
    def from_dicts(cls, rule_dicts: List[Dict[str, Any]]):
        rules = [Rule(**rd) for rd in rule_dicts]
        return cls(rules)

    def process_log(self, log: str, src_ip: str = None, dst_ip: str = None) -> List[Dict[str, Any]]:
        alerts = []
        for rule in self.rules:
            if rule.match(log, src_ip, dst_ip):
                alerts.append(rule.to_dict())
        return alerts

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def remove_rule(self, idx: int):
        if 0 <= idx < len(self.rules):
            self.rules.pop(idx)

    def list_rules(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.rules]
