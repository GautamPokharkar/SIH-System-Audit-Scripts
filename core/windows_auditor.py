import subprocess
from core.auditor import BaseAuditor
import platform

is_windows_11 = int(platform.version().split('.')[2]) >= 22000

# winreg is a Windows-only built-in module. We check if it can be imported safely.
try:
    import winreg
except ImportError:
    winreg = None

class WindowsAuditor(BaseAuditor):
    def run_audit(self):
        print("[*] Starting Windows 11 CIS Benchmark Audit...")
        
        for rule in self.rules:
            audit_type = rule.get('audit_type')
            rule_id = rule.get('rule_id')
            title = rule.get('title')
            severity = rule.get('severity')
            remediation = rule.get('remediation')
            
            if audit_type == "registry" and winreg:
                self._audit_registry(rule_id, title, severity, rule, remediation)
            elif audit_type == "powershell":
                self._audit_powershell(rule_id, title, severity, rule.get('check_command'), str(rule.get('expected_value')), remediation)
            else:
                self.add_result(rule_id, title, severity, "SKIPPED", "N/A", "N/A", remediation)

    def _audit_registry(self, rule_id, title, severity, rule, remediation):
        # Maps string representation to actual winreg HIVE constant
        hive_map = {
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
        }
        
        hive = hive_map.get(rule.get('registry_hive'))
        path = rule.get('registry_path')
        key_name = rule.get('key_name')
        expected = rule.get('expected_value')

        try:
            # Opens registry key and queries its value
            registry_key = winreg.OpenKey(hive, path, 0, winreg.KEY_READ)
            actual, _ = winreg.QueryValueEx(registry_key, key_name)
            winreg.CloseKey(registry_key)
            
            status = "PASS" if actual == expected else "FAIL"
            self.add_result(rule_id, title, severity, status, str(actual), str(expected), remediation)
        except FileNotFoundError:
            self.add_result(rule_id, title, severity, "FAIL", "Registry key/value not found", str(expected), remediation)
        except Exception as e:
            self.add_result(rule_id, title, severity, "ERROR", str(e), str(expected), remediation)

    def _audit_powershell(self, rule_id, title, severity, command, expected, remediation):
        try:
            # Safely executes custom PowerShell blocks
            ps_command = f"powershell -Command \"{command}\""
            result = subprocess.run(ps_command, shell=True, capture_output=True, text=True)
            actual = result.stdout.strip()
            
            status = "PASS" if expected in actual else "FAIL"
            self.add_result(rule_id, title, severity, status, actual, expected, remediation)
        except Exception as e:
            self.add_result(rule_id, title, severity, "ERROR", str(e), expected, remediation)