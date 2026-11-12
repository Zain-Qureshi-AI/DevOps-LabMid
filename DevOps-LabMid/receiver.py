from flask import Flask, request, jsonify
from pathlib import Path
import json
import os

receiver = Flask(__name__)

REPORT_PATH = Path(__file__).resolve().parent / "testreport.json"


@receiver.route("/report", methods=["POST"])
def receive_report():
    expected_token = os.environ.get("REPORT_TOKEN")

    if not expected_token:
        return jsonify({"error": "Receiver token not configured"}), 503

    supplied_token = request.headers.get("X-Report-Token")

    if supplied_token != expected_token:
        return jsonify({"error": "Unauthorized"}), 401

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    required = [
        "repository", "branch", "commit_sha",
        "run_id", "timestamp", "tests"
    ]

    if not all(field in report for field in required):
        return jsonify({"error": "Missing required report fields"}), 400

    if "total" not in report and "total_count" not in report:
        return jsonify({"error": "Missing total count"}), 400
    if "passed" not in report and "passed_count" not in report:
        return jsonify({"error": "Missing passed count"}), 400
    if "failed" not in report and "failed_count" not in report:
        return jsonify({"error": "Missing failed count"}), 400
    if "status" not in report and "overall_status" not in report:
        return jsonify({"error": "Missing status"}), 400

    temp_path = REPORT_PATH.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )
    temp_path.replace(REPORT_PATH)

    commit_sha = report.get("commit_sha", "unknown")
    status = report.get("overall_status") or report.get("status", "unknown")
    total = report.get("total_count", report.get("total", 0))
    passed = report.get("passed_count", report.get("passed", 0))
    failed = report.get("failed_count", report.get("failed", 0))

    print("\n========================================")
    print("Test report received and saved!")
    print(f"Commit SHA:   {commit_sha}")
    print(f"Status:       {status}")
    print(f"Test Counts:  Total: {total}, Passed: {passed}, Failed: {failed}")
    print(f"Saved To:     {REPORT_PATH}")
    print("========================================\n", flush=True)

    return jsonify({"message": "Report saved"}), 200


if __name__ == "__main__":
    receiver.run(host="0.0.0.0", port=5001)
