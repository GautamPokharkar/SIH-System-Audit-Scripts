import tkinter as tk
from tkinter import scrolledtext, messagebox
import platform
import os
import threading

# Import core modules
from core.linux_auditor import LinuxAuditor
from core.windows_auditor import WindowsAuditor
from core.report_engine import ReportEngine

class AuditDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("SIH 2024 - OS Security Auditor")
        self.root.geometry("600x450")
        self.root.configure(padx=20, pady=20)

        # Header
        self.header_label = tk.Label(root, text="System Integrity & Compliance Scanner", font=("Helvetica", 14, "bold"))
        self.header_label.pack(pady=(0, 10))

        # OS Detection Label
        self.current_os = platform.system()
        self.os_label = tk.Label(root, text=f"Detected OS: {self.current_os}", fg="blue")
        self.os_label.pack(pady=(0, 10))

        # Run Button
        self.run_btn = tk.Button(root, text="Run Security Audit", bg="#4CAF50", fg="white", 
                                 font=("Helvetica", 12, "bold"), command=self.start_audit_thread)
        self.run_btn.pack(fill=tk.X, pady=10)

        # Console Output Area
        self.console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg="black", fg="white", font=("Courier", 10))
        self.console.pack(fill=tk.BOTH, expand=True)
        self.log_to_console("System Ready. Waiting to start audit...\n")

    def log_to_console(self, message):
        """Safely inserts text into the GUI console."""
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END) # Auto-scroll to bottom

    def start_audit_thread(self):
        """Runs the audit in a background thread to prevent GUI freezing."""
        self.run_btn.config(state=tk.DISABLED, text="Auditing...")
        self.console.delete(1.0, tk.END)
        self.log_to_console("[*] Initiating Audit Engine...")
        
        # Start thread
        threading.Thread(target=self.execute_audit, daemon=True).start()

    def execute_audit(self):
        if self.current_os == "Linux":
            config_file = "configs/linux_cis.yaml"
            auditor = LinuxAuditor(config_file)
        elif self.current_os == "Windows":
            config_file = "configs/windows_cis.yaml"
            auditor = WindowsAuditor(config_file)
        else:
            self.log_to_console("[-] Unsupported OS.")
            self.reset_button()
            return

        if not os.path.exists(config_file):
            self.log_to_console(f"[-] Error: Missing {config_file}")
            self.reset_button()
            return

        # Run the backend logic
        auditor.run_audit()

        # Display results in GUI
        passed, failed = 0, 0
        for res in auditor.results:
            status = res.get('status')
            rule = res.get('rule_id')
            if status == "PASS":
                passed += 1
            elif status == "FAIL":
                failed += 1
            self.log_to_console(f"[{status}] {rule}")

        self.log_to_console(f"\n[*] Audit Complete. Passed: {passed} | Failed: {failed}")

        # Generate Reports
        self.log_to_console("[*] Generating CSV and JSON reports...")
        reporter = ReportEngine(auditor.results)
        reporter.export_csv()
        reporter.export_json()
        
        self.log_to_console("[+] Reports saved in the 'reports/' directory.")
        self.reset_button()
        messagebox.showinfo("Audit Complete", "Security audit finished and reports generated successfully.")

    def reset_button(self):
        """Re-enables the run button after execution."""
        self.run_btn.config(state=tk.NORMAL, text="Run Security Audit")

if __name__ == "__main__":
    root = tk.Tk()
    app = AuditDashboard(root)
    root.mainloop()