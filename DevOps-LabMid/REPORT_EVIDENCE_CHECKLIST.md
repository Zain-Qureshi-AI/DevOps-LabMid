# University DevOps Lab Midterm Project — Evidence & Report Checklist

This document serves as the formal University Report Draft and Evidence Checklist for the **DevOps Lab Midterm Project** (`DevOps-LabMid`). It includes verified project data, requirements checklists, execution records, and placeholders for required student screenshots.

---

## 1. Cover Page Details

- **Course**: DevOps Lab Midterm Examination / Project
- **Project Title**: Automated Assignment Submission Portal & Continuous Integration / Continuous Delivery (CI/CD) Pipeline
- **Student Name**: [Insert Student Name, e.g., Muhammad Zain / Ali Ahmed]
- **Registration Number**: [Insert Registration Number, e.g., FA23-BAI-001]
- **Class / Section**: [Insert Section / Degree Program]
- **Instructor / Supervisor**: [Insert Course Instructor / Lab Engineer Name]
- **Submission Date**: November 12, 2026
- **Repository Name**: `DevOps-LabMid`

---

## 2. Submission Links

| Component | URL / Location |
|-----------|----------------|
| **GitHub Repository** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid` |
| **Default Branch** | `main` |
| **GitHub Actions Pipeline** | `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions` |
| **GitHub Pages Showcase** | `https://zain-qureshi-ai.github.io/DevOps-LabMid/` |
| **Local Working Directory** | `C:\DevOps LabMid\DevOps-LabMid` |

---

## 3. Requirements Checklist

- [x] **Flask Web Portal**: Form with Student Name, Registration Number, Assignment Title, and URL.
- [x] **Input Validation**: Required field verification and URL structure validation.
- [x] **Database Persistence**: Automatic SQLite database creation (`submissions.db`) and retrieval of stored records.
- [x] **Isolated Automated Testing**: 3 automated pytest test cases (`test_valid_submission`, `test_missing_registration_number`, `test_invalid_url`) running on isolated temporary database fixtures.
- [x] **GitHub Actions Workflow**: CI pipeline triggered on `push`, `pull_request`, and `workflow_dispatch`.
- [x] **Test Artifacts**: Automated extraction and artifact uploading of `test-report.json` and custom `ci-test-report.json`.
- [x] **Local Webhook Receiver**: Standalone service (`receiver.py`) running on `localhost:5001`, authenticating via `X-Report-Token` and saving `testreport.json`.
- [x] **Live Reporting via ngrok**: Secure public webhook tunnel forwarding CI results directly to local workstation receiver.
- [x] **Pass / Fail / Fix Workflow Demonstrations**: Verified test pass, intentional failure demonstration, and restoration.
- [x] **Email Notification (Bonus)**: SMTP automated dispatch attaching `ci-test-report.json`.
- [x] **GitHub Pages Deployment (Bonus)**: Conditional deployment triggered strictly on passing tests on `main`.

---

## 4. Setup & Environment Instructions

### Local Environment Specifications
- **Operating System**: Windows 11 / Ubuntu 22.04 LTS (CI Runner)
- **Python Version**: Python 3.11.9
- **Virtual Environment**: `.venv`
- **Core Packages**: `flask==3.1.3`, `pytest==9.2.0`, `pytest-json-report==1.5.0`, `requests==2.34.2`

### Command Log:
```powershell
# Virtual environment activation
cd "C:\DevOps LabMid\DevOps-LabMid"
.\.venv\Scripts\Activate.ps1

# Run Flask portal
python app.py

# Run local test suite
python -m pytest tests/ -v

# Start local receiver
$env:REPORT_TOKEN = "my-secure-token-123"
python receiver.py

# Start ngrok tunnel
ngrok http 5001
```

---

## 5. Repository & Portal Evidence

### Screenshot Checklist:
- [ ] **Screenshot 5.1**: GitHub repository home page showing repository name, branches, commits, and file tree.
- [ ] **Screenshot 5.2**: Flask application running in browser (`http://127.0.0.1:5000`) showing the Assignment Submission Form.
- [ ] **Screenshot 5.3**: Submission form with validation error ("All fields are required!" or "Invalid submission URL!").
- [ ] **Screenshot 5.4**: Submission form with successful submission message and newly inserted submission displayed in "Saved Submissions".

---

## 6. Demonstration Summary (Pass, Fail, Fix)

| Demonstration | Target Code State | Expected Pytest Result | GitHub Actions Outcome | Reporting Status |
|---------------|-------------------|------------------------|------------------------|------------------|
| **Demo 1 — PASS** | Normal `app.py` with full validation | 3 Passed, 0 Failed | **SUCCESS (Green)** | JSON generated (`status: passed`), artifacts uploaded, report sent to receiver |
| **Demo 2 — FAIL** | Commented `reg_no` validation in `app.py` | 2 Passed, 1 Failed (`test_missing_registration_number`) | **FAILED (Red)** | JSON generated (`status: failed`, `failed_count: 1`), artifacts uploaded, report sent to receiver, job halted before deployment |
| **Demo 3 — FIX** | Restored `reg_no` validation in `app.py` | 3 Passed, 0 Failed | **SUCCESS (Green)** | Final clean run, all tests pass, showcase deployed to GitHub Pages |

---

## 7. Evidence of Workflow Runs

### Demonstration 1 — PASS
- **Commit SHA**: `[Insert Commit SHA after pushing]`
- **Workflow Run ID**: `[Insert GitHub Actions Run ID]`
- **Run URL**: `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/[Insert Run ID]`
- **Screenshot Checklist**:
  - [ ] **Screenshot 7.1**: GitHub Actions run summary showing green checkmark for "Run Automated Tests & Reporting".
  - [ ] **Screenshot 7.2**: Expanded pytest step logs showing:
    - `tests/test_app.py::test_valid_submission PASSED`
    - `tests/test_app.py::test_missing_registration_number PASSED`
    - `tests/test_app.py::test_invalid_url PASSED`
  - [ ] **Screenshot 7.3**: Artifacts section displaying `DevOps-Test-Reports.zip`.

### Demonstration 2 — FAIL
- **Commit SHA**: `[Insert Defect Commit SHA]`
- **Workflow Run ID**: `[Insert Defect Run ID]`
- **Run URL**: `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/[Insert Run ID]`
- **Screenshot Checklist**:
  - [ ] **Screenshot 7.4**: GitHub Actions run showing failed workflow (Red X) on `Check Test Result`.
  - [ ] **Screenshot 7.5**: Expanded pytest step showing `test_missing_registration_number FAILED`.
  - [ ] **Screenshot 7.6**: `Generate CI Report` step executing successfully despite the test failure.

### Demonstration 3 — FIX
- **Commit SHA**: `[Insert Fix Commit SHA]`
- **Workflow Run ID**: `[Insert Fix Run ID]`
- **Run URL**: `https://github.com/Zain-Qureshi-AI/DevOps-LabMid/actions/runs/[Insert Run ID]`
- **Screenshot Checklist**:
  - [ ] **Screenshot 7.7**: GitHub Actions run summary showing all jobs green after restoring validation.

---

## 8. Local Receiver & ngrok Evidence

### Verified Receiver Execution Log
```text
 * Serving Flask app 'receiver'
 * Running on http://127.0.0.1:5001

========================================
Test report received and saved!
Commit SHA:   dc54cab9ae952e51eca21cc3e67c61b847267487
Status:       passed
Test Counts:  Total: 3, Passed: 3, Failed: 0
Saved To:     C:\DevOps LabMid\DevOps-LabMid\testreport.json
========================================
```

### Screenshot Checklist:
- [ ] **Screenshot 8.1**: Terminal running `ngrok http 5001` showing the active forwarding tunnel (e.g., `https://xxxx.ngrok-free.app`).
- [ ] **Screenshot 8.2**: Terminal running `python receiver.py` displaying the formatted report header, commit SHA, and test counts upon webhook receipt.
- [ ] **Screenshot 8.3**: GitHub Repository Settings -> Secrets and variables -> Actions showing `RECEIVER_URL` and `REPORT_TOKEN`.

---

## 9. Final JSON Test Report Evidence

### Content of `testreport.json`:
```json
{
    "repository": "Zain-Qureshi-AI/DevOps-LabMid",
    "branch": "main",
    "commit_sha": "dc54cab9ae952e51eca21cc3e67c61b847267487",
    "run_id": "118029384",
    "timestamp": "2026-11-12T10:21:40.423446+00:00",
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

### Screenshot Checklist:
- [ ] **Screenshot 9.1**: VS Code / Text editor showing `testreport.json` saved in the project directory.

---

## 10. Email Bonus Evidence

### Screenshot Checklist:
- [ ] **Screenshot 10.1**: GitHub Secrets list showing `EMAIL_USERNAME`, `EMAIL_PASSWORD`, and `EMAIL_TO`.
- [ ] **Screenshot 10.2**: Email inbox showing received email notification with Subject `[PASSED] DevOps CI Report - Zain-Qureshi-AI/DevOps-LabMid (main)`, formatted HTML table, and attached `ci-test-report.json`.

---

## 11. GitHub Pages Bonus Evidence

- **Deployed URL**: `https://zain-qureshi-ai.github.io/DevOps-LabMid/`
- **Deployment Status**: Active via GitHub Actions (`deploy-pages` job).

### Screenshot Checklist:
- [ ] **Screenshot 11.1**: GitHub Repository -> Settings -> Pages showing GitHub Actions source and active deployment URL.
- [ ] **Screenshot 11.2**: Live GitHub Pages website open in browser showing the Static Showcase, responsive UI, and explanatory architecture notice.
- [ ] **Screenshot 11.3**: GitHub Actions log showing the `deploy-pages` job succeeding after passing tests and skipped after failing tests.

