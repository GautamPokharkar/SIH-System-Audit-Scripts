import csv
import json
import os
from datetime import datetime

class ReportEngine:
    def __init__(self, results, output_dir="reports"):
        self.results = results
        self.output_dir = output_dir
        # Create a unique timestamp for the report filename
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure the reports directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_csv(self):
        """Exports the audit results to a CSV file."""
        filename = os.path.join(self.output_dir, f"audit_report_{self.timestamp}.csv")
        
        if not self.results:
            print("[-] No results to export.")
            return

        # Extract headers from the first result dictionary keys
        headers = self.results[0].keys()

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.results)
            
        print(f"[+] CSV Report successfully generated: {filename}")

    def export_json(self):
        """Exports the audit results to a JSON file."""
        filename = os.path.join(self.output_dir, f"audit_report_{self.timestamp}.json")
        
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(self.results, file, indent=4)
            
        print(f"[+] JSON Report successfully generated: {filename}")