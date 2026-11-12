import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Look for pytest json output: check test-report.json then pytest-results.json
source = Path("test-report.json")
if not source.exists():
    source = Path("pytest-results.json")

if not source.exists():
    raise SystemExit("Pytest report missing: neither test-report.json nor pytest-results.json was found")

data = json.loads(source.read_text(encoding="utf-8"))

tests = []

for test in data.get("tests", []):
    outcome = test.get("outcome", "unknown")
    failure = None

    for phase in ("setup", "call", "teardown"):
        details = test.get(phase, {})
        if details.get("outcome") == "failed":
            longrepr = details.get("longrepr", "Test failed")
            failure = str(longrepr) if longrepr is not None else "Test failed"
            outcome = "failed"
            break

    tests.append({
        "name": test.get("nodeid"),
        "result": outcome,
        "failure_message": failure
    })

passed = sum(t["result"] == "passed" for t in tests)
failed = sum(t["result"] == "failed" for t in tests)
total = len(tests)

summary = data.get("summary", {})
overall_success = (
    failed == 0
    and total >= 3
    and summary.get("failed", 0) == 0
    and summary.get("errors", 0) == 0
    and summary.get("collected", 0) == total
    and all(t["result"] == "passed" for t in tests)
)

status = "passed" if overall_success else "failed"

report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "local"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "total": total,
    "total_count": total,
    "passed": passed,
    "passed_count": passed,
    "failed": failed,
    "failed_count": failed,
    "status": status,
    "overall_status": status
}

Path("ci-test-report.json").write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
