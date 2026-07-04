import subprocess
import os
import stat
from core.auditor import BaseAuditor

class LinuxAuditor(BaseAuditor):
    def run_audit(self):
        print("[*] Starting Linux CIS Benchmark Audit...")
        
        for rule in self.rules:
            audit_type = rule.get('audit_type')
            rule_id = rule.get('rule_id')
            title = rule.get('title')
            severity = rule.get('severity')
            remediation = rule.get('remediation')
            
            if audit_type == "shell":
                self._audit_shell(rule_id, title, severity, rule.get('check_command'), rule.get('expected_output'), remediation)
            elif audit_type == "file_permission":
                self._audit_file_permission(rule_id, title, severity, rule.get('target_path'), rule.get('expected_permissions'), remediation)
            else:
                # Fallback / Placeholder for unsupported types
                self.add_result(rule_id, title, severity, "SKIPPED", "N/A", "N/A", remediation)

    def _audit_shell(self, rule_id, title, severity, command, expected, remediation):
        try:
            # Runs the shell command and captures stdout
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            actual = result.stdout.strip()
            
            status = "PASS" if expected in actual else "FAIL"
            self.add_result(rule_id, title, severity, status, actual, expected, remediation)
        except Exception as e:
            self.add_result(rule_id, title, severity, "ERROR", str(e), expected, remediation)

    def _audit_file_permission(self, rule_id, title, severity, path, expected_perms, remediation):
        if not os.path.exists(path):
            self.add_result(rule_id, title, severity, "FAIL", "File does not exist", expected_perms, remediation)
            return

        # Fetch file octal permissions (e.g., '0755')
        file_stat = os.stat(path)
        actual_perms = oct(file_stat.st_mode & 0o7777)[2:] # strips '0o' prefix
        
        status = "PASS" if actual_perms == expected_perms else "FAIL"
        self.add_result(rule_id, title, severity, status, actual_perms, expected_perms, remediation)

    def _get_linux_distro(self):
        """Detects whether the system is Ubuntu, Debian, RHEL, CentOS, etc."""
        try:
            with open("/etc/os-release", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        return line.strip().split("=")[1].replace('"', '')
        except Exception:
            return "generic"