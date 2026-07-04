import os
import yaml
from abc import ABC, abstractmethod

class BaseAuditor(ABC):
    def __init__(self, config_path):
        self.config_path = config_path
        self.rules = []
        self.results = []
        self.load_rules()

    def load_rules(self):
        """Loads rules from the specified YAML configuration file."""
        if not os.path.exists(self.config_path):
            print(f"[-] Configuration file not found: {self.config_path}")
            return
            
        with open(self.config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            self.rules = config_data.get('rules', [])
            print(f"[+] Loaded {len(self.rules)} rules from configuration.")

    @abstractmethod
    def run_audit(self):
        """Each OS auditor must implement its own execution logic."""
        pass

    def add_result(self, rule_id, title, severity, status, actual, expected, remediation):
        """Appends the audit result of a specific rule."""
        self.results.append({
            "rule_id": rule_id,
            "title": title,
            "severity": severity,
            "status": status,          # "PASS" or "FAIL"
            "actual_value": actual,
            "expected_value": expected,
            "remediation": remediation
        })