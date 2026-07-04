import platform
import sys
import os

# Import the core auditor engines
from core.linux_auditor import LinuxAuditor
from core.windows_auditor import WindowsAuditor
from core.report_engine import ReportEngine

def main():
    print("="*50)
    print(" SIH 2024 - OS Security Audit & Compliance Tool ")
    print("="*50)

    # 1. Automatic OS Detection
    current_os = platform.system()
    print(f"[*] Detected Operating System: {current_os}")

    # 2. Route to the correct configuration and auditor
    if current_os == "Linux":
        config_file = "configs/linux_cis.yaml"
        auditor = LinuxAuditor(config_file)
    elif current_os == "Windows":
        config_file = "configs/windows_cis.yaml"
        auditor = WindowsAuditor(config_file)
    else:
        print(f"[-] Unsupported Operating System: {current_os}")
        sys.exit(1)

    # Sanity check to ensure the YAML file exists before running
    if not os.path.exists(config_file):
        print(f"[-] Error: Could not find configuration file at {config_file}")
        print("[-] Please ensure the 'configs/' directory contains your YAML rules.")
        sys.exit(1)

    # 3. Execute the Audit
    print("[*] Initiating audit engine...\n")
    auditor.run_audit()

    # 4. Process and Display Results in the Terminal
    print("\n" + "="*50)
    print(" AUDIT SUMMARY ")
    print("="*50)
    
    passed = 0
    failed = 0
    skipped_or_error = 0

    for result in auditor.results:
        status = result.get('status')
        rule_id = result.get('rule_id')
        title = result.get('title')

        # ANSI Escape codes for terminal colors
        if status == "PASS":
            passed += 1
            color = "\033[92m" # Green
        elif status == "FAIL":
            failed += 1
            color = "\033[91m" # Red
        else:
            skipped_or_error += 1
            color = "\033[93m" # Yellow
            
        reset = "\033[0m"
        
        # Print the formatted result line
        print(f"{color}[{status}] {rule_id}: {title}{reset}")

    # 5. Final Tally
    print("\n[*] Final Tally:")
    print(f"    Total Checks : {len(auditor.results)}")
    print(f"    Passed       : {passed}")
    print(f"    Failed       : {failed}")
    print(f"    Other        : {skipped_or_error}")
    print("="*50)


    # 6. Generate Reports
    print("\n[*] Generating Audit Reports...")
    reporter = ReportEngine(auditor.results)
    reporter.export_csv()
    reporter.export_json()
    print("="*50)

if __name__ == "__main__":
    main()