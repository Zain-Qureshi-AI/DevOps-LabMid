import json
import os
import sys
from pathlib import Path
import requests


def send_report():
    report_file = Path("ci-test-report.json")
    if not report_file.exists():
        print(f"Error: {report_file} does not exist.")
        sys.exit(1)

    try:
        report = json.loads(report_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading {report_file}: {e}")
        sys.exit(1)

    receiver_url = os.environ.get("RECEIVER_URL", "").strip()
    report_token = os.environ.get("REPORT_TOKEN", "").strip()

    if not receiver_url:
        print("Error: RECEIVER_URL environment variable is not configured.")
        sys.exit(1)

    if not report_token:
        print("Error: REPORT_TOKEN environment variable is not configured.")
        sys.exit(1)

    # Normalize receiver_url to append /report if omitted
    clean_url = receiver_url.rstrip("/")
    if not clean_url.endswith("/report"):
        endpoint_url = f"{clean_url}/report"
    else:
        endpoint_url = clean_url

    print(f"Sending test report to {endpoint_url}...")
    headers = {
        "Content-Type": "application/json",
        "X-Report-Token": report_token
    }

    try:
        response = requests.post(
            endpoint_url,
            json=report,
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            print("Report successfully delivered to receiver!")
            print(f"Receiver response: {response.text}")
        elif response.status_code == 401:
            print("Authentication error (HTTP 401): Invalid or unauthorized REPORT_TOKEN.")
            sys.exit(1)
        elif response.status_code == 503:
            print("Receiver error (HTTP 503): Receiver token not configured on server.")
            sys.exit(1)
        else:
            print(f"Receiver returned HTTP {response.status_code}: {response.text}")
            sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error reaching receiver at {endpoint_url}: {e}")
        sys.exit(1)
    except requests.exceptions.Timeout as e:
        print(f"Timeout error reaching receiver at {endpoint_url}: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error sending report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    send_report()
