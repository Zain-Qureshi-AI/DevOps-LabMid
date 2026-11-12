# University DevOps Lab Midterm Project — Evidence & Submission Report

**Course**: DevOps Lab Midterm Examination / Project  
**Project Title**: Automated Assignment Submission Portal & Continuous Integration / Continuous Delivery (CI/CD) Pipeline  
**Student Name**: [Insert Student Name, e.g., Muhammad Zain / Ali Ahmed]  
**Registration Number**: [Insert Registration Number, e.g., FA23-BAI-001]  
**Class / Section**: [Insert Section / Degree Program]  
**Instructor / Supervisor**: [Insert Course Instructor / Lab Engineer Name]  
**Submission Date**: November 12, 2026  
**Repository Name**: `DevOps-LabMid`  

---

## 1. Verified Project & Submission Links

| Component | URL / Location | Status |
|-----------|----------------|--------|
| **GitHub Repository** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid` | Active / Public |
| **Default Branch** | `main` | Clean / Verified |
| **GitHub Actions Pipeline** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions` | Active |
| **Live GitHub Pages Showcase** | `https://zain-qureshi-ai.github.io/Devops-LabMid/` | **Verified Live (HTTP 200)** |
| **Demo 1 Workflow Run (Baseline Pass)** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43202359149` | **Succeeded (Green)** |
| **Demo 1 Webhook Delivery Run** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43206713910` | **Succeeded (Green)** |
| **Demo 2 Workflow Run (Deliberate Defect)** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43208600634` | **Failed as Expected (Red)** |
| **Demo 3 Workflow Run (Restored & Verified)**| `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43208916556` | **Succeeded (Green)** |
| **Active ngrok Forwarding Tunnel** | `https://colony-clambake-snipping.ngrok-free.dev/report` | **Verified Live (HTTP 200)** |
| **Local Project Path** | `C:\DevOps LabMid\DevOps-LabMid` | Clean |

---

## 2. Requirements Compliance Checklist

- [x] **Flask Web Application**: Form supporting Student Name, Registration Number, Assignment Title, and Submission URL.
- [x] **Input Validation**: Rejection of empty required fields and URL validation using `urllib.parse`.
- [x] **Automatic Database Initialization**: SQLite database (`submissions.db`) and table creation triggered automatically when needed.
- [x] **Display Stored Submissions**: Dynamic rendering of saved assignment submissions in reverse chronological order.
- [x] **Pytest Automated Tests**: 3 comprehensive test cases running on isolated temporary database fixtures:
  - `test_valid_submission` (PASSED)
  - `test_missing_registration_number` (PASSED)
  - `test_invalid_url` (PASSED)
- [x] **GitHub Actions Workflow**: Runs on `ubuntu-latest`, Python 3.11, triggered on `push`, `pull_request`, and `workflow_dispatch`.
- [x] **Non-destructive Failure Handling**: Uses `continue-on-error: true` on pytest with an explicit `Check Test Result` enforcement step so reports are always generated and delivered even on failure.
- [x] **Structured JSON Report Generation**: `generate_report.py` produces `ci-test-report.json` with repository, branch, commit SHA, run ID, timestamp, and per-test breakdown.
- [x] **GitHub Actions Artifacts**: `DevOps-Test-Reports` uploaded containing both `test-report.json` and `ci-test-report.json`.
- [x] **Local Webhook Receiver**: `receiver.py` on `localhost:5001` validates `X-Report-Token`, displays commit SHA, status, and test counts, and writes `testreport.json`.
- [x] **Live ngrok Integration**: Secure HTTPS webhook forwarding to local receiver verified live with HTTP 200.
- [x] **GitHub Pages Showcase (Bonus)**: Static demo portal conditionally deployed only from `main` on passing tests; preserved on failed runs. Verified live at `https://zain-qureshi-ai.github.io/Devops-LabMid/`.
- [x] **Email Notification (Bonus)**: `send_email.py` formats an HTML test summary with attached JSON report; skips gracefully when secrets are unset.

---

## 3. Verified Pass → Fail → Fix Demonstration Summary

The university requires 3 distinct workflow demonstration runs with real evidence:

```
[Demo 1: Baseline Pass]  ───▶ Commit 43b1f85  ───▶ Run #43202359149 & #43206713910  ───▶ All Tests Pass (3/3), Pages Deployed, Webhook HTTP 200
[Demo 2: Defect Fail]    ───▶ Commit a049182  ───▶ Run #43208600634                 ───▶ 1 Test Failed (2/3), Pages Skipped, Failure Webhook HTTP 200
[Demo 3: Fix Restored]   ───▶ Commit 4988bff  ───▶ Run #43208916556                 ───▶ All Tests Pass (3/3), Pages Redeployed, Green Status
```

### Demonstration Details

| Demonstration | Target Code State | Commit SHA | GitHub Actions Run ID & URL | Outcome | Receiver Status |
|---------------|-------------------|------------|-----------------------------|---------|-----------------|
| **Demo 1 — PASS** | Normal `app.py` with full validation | `43b1f855cd423479b7678b22f8a47a953507f7a0` | [43202359149](https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43202359149) & [43206713910](https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43206713910) | **SUCCESS (Green)** (All 3 tests passed) | `passed` (Total: 3, Passed: 3, Failed: 0) |
| **Demo 2 — FAIL** | Commented `reg_no` validation in `app.py` | `a049182d79a86ff2f59b605a3aef79754a9d43a2` | [43208600634](https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43208600634) | **FAILED (Red)** (`test_missing_registration_number` failed) | `failed` (Total: 3, Passed: 2, Failed: 1) |
| **Demo 3 — FIX** | Restored `reg_no` validation in `app.py` | `4988bffd5d7ae5e492f38893fce928b64586fb89` | [43208916556](https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/43208916556) | **SUCCESS (Green)** (All 3 tests passed, Pages redeployed) | `passed` (Total: 3, Passed: 3, Failed: 0) |

---

## 4. Local Receiver Audit Log (Verified Chronological Output)

```text
========================================
[DEMO 1] Test report received and saved!
Commit SHA:   43b1f855cd423479b7678b22f8a47a953507f7a0
Status:       passed
Test Counts:  Total: 3, Passed: 3, Failed: 0
Saved To:     C:\DevOps LabMid\DevOps-LabMid\testreport.json
========================================
127.0.0.1 - - [12/Nov/2026 16:09:53] "POST /report HTTP/1.1" 200 -

========================================
[DEMO 2] Test report received and saved!
Commit SHA:   a049182d79a86ff2f59b605a3aef79754a9d43a2
Status:       failed
Test Counts:  Total: 3, Passed: 2, Failed: 1
Saved To:     C:\DevOps LabMid\DevOps-LabMid\testreport.json
========================================
127.0.0.1 - - [12/Nov/2026 16:22:50] "POST /report HTTP/1.1" 200 -

========================================
[DEMO 3] Test report received and saved!
Commit SHA:   4988bffd5d7ae5e492f38893fce928b64586fb89
Status:       passed
Test Counts:  Total: 3, Passed: 3, Failed: 0
Saved To:     C:\DevOps LabMid\DevOps-LabMid\testreport.json
========================================
127.0.0.1 - - [12/Nov/2026 16:24:52] "POST /report HTTP/1.1" 200 -
```

---

## 5. Live JSON Reports

### 5.1 Final Passing JSON Report (`testreport.json` / `ci-test-report.json`)
```json
{
    "repository": "Zain-Qureshi-AI/Devops-LabMid",
    "branch": "main",
    "commit_sha": "4988bffd5d7ae5e492f38893fce928b64586fb89",
    "run_id": "43208916556",
    "timestamp": "2026-11-12T11:24:51.627753+00:00",
    "tests": [
        {
            "name": "tests/test_app.py::test_valid_submission",
            "result": "passed",
            "failure_message": null
        },
        {
            "name": "tests/test_app.py::test_missing_registration_number",
            "result": "passed",
            "failure_message": null
        },
        {
            "name": "tests/test_app.py::test_invalid_url",
            "result": "passed",
            "failure_message": null
        }
    ],
    "total": 3,
    "total_count": 3,
    "passed": 3,
    "passed_count": 3,
    "failed": 0,
    "failed_count": 0,
    "status": "passed",
    "overall_status": "passed"
}
```

### 5.2 Deliberate Defect JSON Report (`ci-test-report-failed.json`)
```json
{
    "repository": "Zain-Qureshi-AI/Devops-LabMid",
    "branch": "main",
    "commit_sha": "a049182d79a86ff2f59b605a3aef79754a9d43a2",
    "run_id": "43208600634",
    "timestamp": "2026-11-12T11:22:49.489841+00:00",
    "tests": [
        {
            "name": "tests/test_app.py::test_valid_submission",
            "result": "passed",
            "failure_message": null
        },
        {
            "name": "tests/test_app.py::test_missing_registration_number",
            "result": "failed",
            "failure_message": "client = <FlaskClient <Flask 'app'>>\n\n    def test_missing_registration_number(client):\n        response = client.post(\"/\", data={\n            \"name\": \"Ali Ahmed\",\n            \"reg_no\": \"\",\n            \"title\": \"DevOps Assignment\",\n            \"url\": \"https://github.com/example/project\"\n        })\n    \n>       assert b\"All fields are required\" in response.data\nE       assert b'All fields are required' in ...\ntests/test_app.py:49: AssertionError"
        },
        {
            "name": "tests/test_app.py::test_invalid_url",
            "result": "passed",
            "failure_message": null
        }
    ],
    "total": 3,
    "total_count": 3,
    "passed": 2,
    "passed_count": 2,
    "failed": 1,
    "failed_count": 1,
    "status": "failed",
    "overall_status": "failed"
}
```

---

## 6. Required Screenshots Checklist for University Report

### Section A: Flask Web Portal
- [ ] **Screenshot A.1**: Flask portal (`http://127.0.0.1:5000`) showing the assignment submission form with empty inputs.
- [ ] **Screenshot A.2**: Input validation error ("All fields are required!" or "Invalid submission URL!").
- [ ] **Screenshot A.3**: Successful submission flash message ("Assignment submitted successfully!") and student submission displayed in "Saved Submissions".

### Section B: GitHub Repository & Secrets
- [ ] **Screenshot B.1**: GitHub repository home page (`https://github.com/Zain-Qureshi-AI/DevOps-LabMid`) showing branches, latest commits, and file tree.
- [ ] **Screenshot B.2**: Repository Settings -> Secrets and variables -> Actions showing `RECEIVER_URL` and `REPORT_TOKEN`.
- [ ] **Screenshot B.3**: Repository Settings -> Pages showing GitHub Pages enabled with GitHub Actions source.

### Section C: CI/CD Pipeline & GitHub Actions Runs
- [ ] **Screenshot C.1 (Demo 1 — PASS)**: Run summary of Run #43202359149 showing green checkmarks for both `Run Automated Tests & Reporting` and `Deploy GitHub Pages Showcase`.
- [ ] **Screenshot C.2 (Demo 2 — FAIL)**: Run summary of Run #43208600634 showing red failure at `Check Test Result`, `Generate CI Report` executed, and `Deploy GitHub Pages Showcase` skipped.
- [ ] **Screenshot C.3 (Demo 3 — FIX)**: Run summary of Run #43208916556 showing all jobs green after validation restoration.
- [ ] **Screenshot C.4 (Pytest logs)**: Expanded pytest step log showing all 3 tests passed.
- [ ] **Screenshot C.5 (Artifacts)**: GitHub Actions Artifacts section showing downloadable `DevOps-Test-Reports` zip.

### Section D: Local Receiver & ngrok
- [ ] **Screenshot D.1**: Terminal running `ngrok http 5001` showing active tunnel `https://colony-clambake-snipping.ngrok-free.dev`.
- [ ] **Screenshot D.2**: Terminal running `python receiver.py` showing received report logs for Demo 1, Demo 2, and Demo 3.
- [ ] **Screenshot D.3**: Text editor showing `testreport.json` saved in the project folder with actual commit SHA `4988bff...`.

### Section E: Bonus Deliverables
- [ ] **Screenshot E.1**: Live GitHub Pages website (`https://zain-qureshi-ai.github.io/Devops-LabMid/`) open in browser showing Static Showcase and architecture notice.
- [ ] **Screenshot E.2**: *(Optional)* Email notification received in inbox if email secrets configured.
