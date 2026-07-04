# Enterprise Cross-Platform Compliance & Auto-Remediation Engine (SIH 2024)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Compliance](https://img.shields.io/badge/Compliance-CIS_Benchmarks-red.svg)](https://www.cisecurity.org/cis-benchmarks)

An advanced, automated configuration assessment, compliance auditing, and **active remediation tool** built for the **Smart India Hackathon (SIH) 2024 (Problem ID: SIH1679)**. This utility scans **Windows 10/11** and multiple Linux distributions (**Ubuntu/Debian/RHEL**) to evaluate system integrity against standard **CIS Benchmarks** and optionally fixes misconfigurations autonomously.

---

## 📌 Problem Statement & Context
While traditional audit scripts merely generate long, passive text logs of vulnerabilities, security operations teams need tools that reduce the time-to-remediation. Built during SIH 2024, this project transitions from a passive auditor into an active hardening tool. 

It implements a **Data-Driven Architecture** that decouples systemic detection/remediation commands from the core codebase using structured YAML schemas.

---

## ✨ Key Features

* **Distro & Version Awareness:** Automatically queries host environmental metadata to distinguish between Linux flavours (`/etc/os-release` parsing for Ubuntu vs. RHEL) and Windows iterations (build version parsing for Windows 10 vs. 11) to safely execute target-specific checks.
* **Automated Hardening (Auto-Remediation):** Features a safe remediation pipeline. If a check fails, the tool can execute predefined, isolated commands (e.g., registry writes, config substitutions using `sed`) to instantly enforce compliance.
* **Data-Driven Rule Engine:** Entirely extensible YAML schema. Security policies can be scaled, modified, or updated globally by system administrators without altering the underlying engine logic.
* **Asynchronous Desktop GUI:** Implements a multi-threaded execution framework using Python's `threading` module to run heavy system queries seamlessly without locking the Tkinter dashboard UI.
* **Dual-Format Reporting:** Generates timestamped compliance reports in both `CSV` (for spreadsheet analytics) and `JSON` (for direct integration into SIEM tools like Splunk or ELK pipelines).

---

## 🛠️ Repository Architecture

```text
Project-OS-Audit/
│
├── configs/                  # Data-driven compliance benchmarks
│   ├── windows_cis.yaml      # Multi-version Windows Registry/PS rules
│   └── linux_cis.yaml        # Distro-specific (Ubuntu/RHEL) shell rules
│
├── core/                     # Modular backend architecture
│   ├── __init__.py
│   ├── auditor.py            # Base abstract auditor class (holds shared remediation engine)
│   ├── linux_auditor.py      # Linux-specific execution engine with distro filtering
│   ├── windows_auditor.py    # Windows registry & version-aware scanner
│   └── report_engine.py      # Timestamped data reporting pipeline
│
├── gui/                      # Desktop dashboard layer
│   └── dashboard.py          # Multithreaded Tkinter interface with "Scan" & "Fix" pipelines
│
├── reports/                  # Git-ignored local audit output directory
├── main.py                   # Command-line entry execution point
├── requirements.txt          # Python external dependency manifests
└── README.md                 # Project documentation
```
## 🛠️ Future Roadmap
To transition this from a hackathon prototype to an enterprise-ready product, the next development phases include:
- [ ] **Role-Based Access Control (RBAC):** Implementing secure login for administrators to restrict who can trigger the "Auto-Remediation" fixes.
- [ ] **Agent-Server Architecture:** Converting the standalone tool into a lightweight agent that reports back to a centralized web-based dashboard.
- [ ] **Cloud Configuration Scanning:** Expanding the YAML rule schema to audit AWS, Azure, and GCP IAM policies alongside local OS configurations.
---

