Cross-Platform OS Security Auditor (SIH 2024)
An automated configuration assessment and compliance auditing tool built for Smart India Hackathon (SIH) 2024 (Problem ID: SIH1679). This utility scans both Windows 11 and Linux (Ubuntu/RHEL) operating systems to evaluate system integrity, user access controls, and network security policies against standard CIS (Center for Internet Security) Benchmarks.

📌 Problem Statement & Context
Manual security audits of enterprise systems are tedious, error-prone, and slow. During SIH 2024, our team was tasked with creating an automated, low-overhead solution that gives system administrators instant visibility into their system's compliance stance without requiring deep coding knowledge.

This tool achieves that by separating the auditing engine logic from the compliance rules, leveraging a data-driven YAML architecture.

✨ Key Features
Data-Driven Rule Engine: Security checks are defined entirely in modular YAML schemas. Rules can be updated, added, or deleted without modifying a single line of Python code.

Automatic OS Detection: Cross-platform orchestration engine autonomously detects the host operating system (platform.system) and routes execution to specialized sub-engines.

Multi-Vector Audit Capabilities:

Linux: Executes system shell diagnostics and validates native octal file permissions (chmod/chown).

Windows 11: Performs deep registry hives (HKEY_LOCAL_MACHINE/HKEY_CURRENT_USER) validation and triggers customized PowerShell scripts safely via subprocess pipelines.

Asynchronous Desktop GUI: Built with an active asynchronous threading architecture using tkinter to prevent interface freezing during heavy system execution.

Dual-Format Reporting Engine: Automatically compiles audit metrics into timestamped CSV and JSON compliance trails ready to be ingested by SIEM tools like Splunk or ELK.

🛠️ Architecture & Tech Stack
Language: Python 3.8+

Libraries Used: PyYAML (Data Parsing), tkinter (User Interface), subprocess / winreg (OS Level Interactions)

Design Pattern: Object-Oriented Programming (OOP) utilizing abstract base classes and polymorphic runtime execution.

Repository Structure
Plaintext
Project-OS-Audit/
│
├── configs/                  # Data-driven compliance benchmarks
│   ├── windows_cis.yaml      # Windows 11 Registry/PowerShell rules
│   └── linux_cis.yaml        # Linux Shell/File permission rules
│
├── core/                     # Modular backend architecture
│   ├── __init__.py
│   ├── auditor.py            # Base abstract auditor class
│   ├── linux_auditor.py      # Linux-specific execution sub-engine
│   ├── windows_auditor.py    # Windows-specific registry & PS scanner
│   └── report_engine.py      # Timestamped data reporting pipeline
│
├── gui/                      # Desktop dashboard layer
│   └── dashboard.py          # Multithreaded Tkinter interface
│
├── reports/                  # Git-ignored local audit output directory
├── main.py                   # Command-line entry execution point
├── requirements.txt          # Python external dependency manifests
└── README.md                 # Project documentation
🚀 Installation & Usage
1. Clone the repository
Bash
git clone https://github.com/gautampokharkar/sih-os-security-auditor.git
cd sih-os-security-auditor
2. Install dependencies
Bash
pip install -r requirements.txt
3. Execution Options
Run via Command Line Interface (CLI):

Bash
python main.py
Run via Desktop Graphical User Interface (GUI):

Bash
python -m gui.dashboard