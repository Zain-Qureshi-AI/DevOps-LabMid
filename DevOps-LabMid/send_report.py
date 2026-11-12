import json
import os
from pathlib import Path
import requests

report = json.loads(
    Path("ci-test-report.json").read_text(encoding="utf-8")
)

token = os.environ["REPORT_TOKEN"]
receiver_url = os.environ["RECEIVER_URL"]

response = requests.post(
    receiver_url,
    json=report,
    headers={"X-Report-Token": token},
    timeout=30
)

response.raise_for_status()

print("Report successfully delivered to receiver!")