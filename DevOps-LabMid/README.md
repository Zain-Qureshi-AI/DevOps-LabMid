# DevOps Lab Mid - Assignment Submission Portal & CI/CD Pipeline

A complete, enterprise-grade DevOps implementation featuring a Python Flask assignment submission portal, SQLite database persistence, automated pytest test suite, GitHub Actions CI/CD pipeline, custom JSON test reporting, live webhook report delivery via ngrok, automated email notifications, and static showcase deployment to GitHub Pages.

---

## 1. Project Overview

The **Assignment Submission Portal** is designed for academic workflows, enabling students to submit assignments with robust validation (required fields, student details, and valid URLs) and database persistence.

The DevOps pipeline provides automated continuous integration and continuous delivery (CI/CD):
- **Automated Testing**: Validates core portal behavior across 3 distinct test scenarios using `pytest`.
- **Automated Test Report Generation**: Converts raw pytest outputs into structured, machine-readable JSON (`ci-test-report.json`).
- **Live Local Receiver**: A dedicated Flask service (`receiver.py`) running on `localhost:5001` that authenticates incoming test reports via custom HTTP headers (`X-Report-Token`) and saves them locally (`testreport.json`).
- **Secure Tunneling (ngrok)**: Exposes the local receiver securely to GitHub Actions runners.
- **Email Notifications (Bonus)**: Automatically sends formatted test results and attaches JSON reports via SMTP.
- **GitHub Pages Showcase (Bonus)**: Conditionally deploys a static interactive preview of the portal upon successful CI runs on the `main` branch.

---

## 2. Technologies Used

- **Web Framework**: Python 3.11, Flask 3.1.3, Jinja2
- **Database**: SQLite3
- **Testing**: Pytest 9.2.0, `pytest-json-report` 1.5.0
- **HTTP & Networking**: `requests`, `urllib.parse`, `smtplib`, ngrok v3
- **CI/CD Platform**: GitHub Actions (Ubuntu latest runner)
- **Deployment**: GitHub Pages (`actions/deploy-pages@v4`)

---

## 3. Repository Structure

```text
DevOps-LabMid/
├── .github/
│   └── workflows/
│       └── main.yml                 # Master GitHub Actions CI/CD workflow
├── .gitignore                       # Repository-wide git ignore rules
├── README.md                        # Master documentation
├── REPORT_EVIDENCE_CHECKLIST.md     # University submission report & screenshot evidence guide
└── DevOps-LabMid/                   # Application source directory
    ├── app.py                       # Main Flask web portal with SQLite integration
    ├── generate_report.py           # Custom CI JSON report generator
    ├── receiver.py                  # Local report receiver webhook service (port 5001)
    ├── send_report.py               # Report sender client to local receiver / ngrok
    ├── send_email.py                # Automated SMTP email notification script
    ├── requirements.txt             # Python dependencies
    ├── submissions.db               # SQLite database file (auto-initialized)
    ├── static_site/
    │   └── index.html               # GitHub Pages static showcase portal
    ├── templates/
    │   └── index.html               # Dynamic Flask Jinja2 portal template
    └── tests/
        └── test_app.py              # Pytest automated test suite (3 test cases)
```

---

## 4. Installation Commands

Clone the repository and set up a Python virtual environment:

### Windows (PowerShell)
```powershell
# Navigate into the project folder
cd "C:\DevOps LabMid\DevOps-LabMid"

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-json-report requests
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-json-report requests
```

---

## 5. Running the Flask Application

To start the submission portal locally:

```powershell
python app.py
```

The portal runs at **`http://127.0.0.1:5000`**.

### Portal Features:
1. **Student Name**: Required text input.
2. **Registration Number**: Required text input (e.g., `FA23-BAI-001`).
3. **Assignment Title**: Required text input.
4. **Assignment Submission URL**: Validated URL (must be valid HTTP/HTTPS link).
5. **Automatic Database Creation**: If `submissions.db` or the `submissions` table does not exist, it is initialized automatically on startup.
6. **Submission Feed**: Displays all stored submissions in reverse chronological order.

---

## 6. Running Automated Tests

The automated test suite evaluates three critical scenarios:
1. `test_valid_submission`: Submits valid student data and verifies successful insertion and database count.
2. `test_missing_registration_number`: Submits an empty registration number and asserts error validation without database insertion.
3. `test_invalid_url`: Submits a malformed URL and asserts validation rejection without database insertion.

> **Note**: Tests run against an isolated temporary database created via pytest's `tmp_path` fixture and never touch or corrupt the live `submissions.db`.

Execute tests locally:

```powershell
python -m pytest tests/ -v
```

Execute tests and generate the raw pytest JSON report:

```powershell
python -m pytest tests/ -v --json-report --json-report-file=test-report.json
```

---

## 7. GitHub Actions CI/CD Configuration

The master workflow file is located at **`.github/workflows/main.yml`**.

### Key Workflow Triggers:
- `push` to branch `main`
- `pull_request` to branch `main`
- `workflow_dispatch` (manual trigger from GitHub Actions tab)

### Pipeline Stages:
1. **Checkout Repository**: Uses `actions/checkout@v4`.
2. **Setup Python**: Configures Python 3.11 via `actions/setup-python@v5`.
3. **Install Dependencies**: Upgrades pip and installs `requirements.txt`, `pytest`, `pytest-json-report`, and `requests`.
4. **Run Pytest**: Runs tests with `--json-report` and `--json-report-file=test-report.json`. Marked with `continue-on-error: true` so reporting steps execute even on test failures.
5. **Generate CI Report**: Executes `generate_report.py` to produce structured `ci-test-report.json`.
6. **Artifact Upload**: Uses `actions/upload-artifact@v4` to save both `test-report.json` and `ci-test-report.json` for 90 days.
7. **Webhook Delivery**: Calls `send_report.py` to transmit the test report to the local receiver via ngrok tunnel if secrets are configured.
8. **Email Notification (Bonus)**: Executes `send_email.py` to dispatch detailed status and attach the report if email secrets are configured.
9. **Outcome Check**: Evaluates `steps.pytest.outcome`. If any test failed, the step explicitly exits with code `1`, failing the CI run.
10. **Deploy GitHub Pages (Bonus)**: Deploys the static showcase to GitHub Pages only from `main` when all tests pass.

---

## 8. JSON Report Generation (`generate_report.py`)

The script `generate_report.py` processes raw pytest output and creates `ci-test-report.json` with the following schema:

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

To run manually:
```powershell
python generate_report.py
```

---

## 9. Running `receiver.py`

`receiver.py` is an authenticated webhook endpoint that listens on port `5001`.

### Start the Receiver:
```powershell
# Set your authentication token
$env:REPORT_TOKEN = "my-secure-token-123"

# Start receiver
python receiver.py
```

### Receiver Specifications:
- Endpoint: `POST http://127.0.0.1:5001/report`
- Header: `X-Report-Token: <token>`
- Authenticates token matching `$env:REPORT_TOKEN`.
- Validates payload structure and fields.
- Saves received payload to `testreport.json`.
- Prints summary directly to console: Commit SHA, overall status, and test counts.

---

## 10. ngrok Setup & Tunneling

To allow GitHub Actions (running on cloud runners) to deliver reports to your local receiver:

1. **Start the local receiver** on port 5001:
   ```powershell
   $env:REPORT_TOKEN = "my-secure-token-123"
   python receiver.py
   ```

2. **Open a new terminal and launch ngrok**:
   ```bash
   ngrok http 5001
   ```

3. **Copy the Forwarding URL** from the ngrok output:
   Example: `https://abcd-1234-5678.ngrok-free.app`

4. Test locally using `send_report.py`:
   ```powershell
   $env:RECEIVER_URL = "https://abcd-1234-5678.ngrok-free.app/report"
   $env:REPORT_TOKEN = "my-secure-token-123"
   python send_report.py
   ```

---

## 11. GitHub Secrets Configuration

Navigate to your repository on GitHub:
**Settings** -> **Secrets and variables** -> **Actions** -> **Repository secrets**

Add the following secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `RECEIVER_URL` | Public ngrok tunnel URL | `https://xxxx-xxxx.ngrok-free.app/report` |
| `REPORT_TOKEN` | Shared secret token | `my-secure-token-123` |
| `EMAIL_USERNAME` | SMTP account email (Bonus) | `student@gmail.com` |
| `EMAIL_PASSWORD` | SMTP app password (Bonus) | `xxxx xxxx xxxx xxxx` |
| `EMAIL_TO` | Notification recipient email (Bonus) | `supervisor@university.edu` |
| `SMTP_SERVER` | SMTP host (optional, defaults to Gmail) | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (optional, defaults to 587) | `587` |

---

## 12. Pass, Fail, Fix Demonstration Guide

University requirements specify three distinct workflow demonstrations:

### Demonstration 1 — PASS
1. Ensure `app.py` has complete validation.
2. Verify all 3 tests pass:
   ```powershell
   python -m pytest tests/ -v
   ```
3. Push to `main` or trigger `workflow_dispatch`.
4. Result: CI run succeeds (Green checkmark), all 3 tests pass, reports uploaded and delivered.

### Demonstration 2 — FAIL (Deliberate Defect)
1. Introduce a deliberate defect in `app.py` by commenting out the registration number validation:
   ```python
   # Line in app.py:
   # if not all([name, reg_no, title, url]):
   if not all([name, title, url]):  # Defect: reg_no not required!
   ```
2. Run pytest locally to confirm test failure:
   ```powershell
   python -m pytest tests/ -v
   ```
   `test_missing_registration_number` fails with `AssertionError`.
3. Commit and push the defect branch or main:
   ```bash
   git commit -am "test: deliberate defect in registration validation"
   git push origin main
   ```
4. GitHub Actions execution:
   - Pytest step reports failure (1 failed, 2 passed).
   - `Generate CI Report` step executes anyway and writes:
     - `total_count: 3`
     - `passed_count: 2`
     - `failed_count: 1`
     - `overall_status: "failed"`
   - Reports are uploaded as artifacts and delivered to the receiver.
   - Job properly fails at `Check Test Result`.
   - `deploy-pages` is skipped (preserving existing deployment).

### Demonstration 3 — FIX (Restoration)
1. Restore proper validation in `app.py`:
   ```python
   if not all([name, reg_no, title, url]):
   ```
2. Verify all 3 tests pass:
   ```powershell
   python -m pytest tests/ -v
   ```
3. Commit and push the fix:
   ```bash
   git commit -am "fix: restore registration validation"
   git push origin main
   ```
4. GitHub Actions succeeds completely. All 3 tests pass.

---

## 13. Email Notifications (Bonus)

Automated email reporting is implemented via `send_email.py`.
- Formats an HTML notification displaying repository, branch, commit SHA, run ID, and color-coded status.
- Attaches the complete `ci-test-report.json`.
- If secrets are not present, the script skips gracefully without breaking CI execution.

---

## 14. GitHub Pages Deployment (Bonus)

- Static showcase files live in `DevOps-LabMid/static_site/`.
- Deployed via `actions/deploy-pages@v4` on Ubuntu runners.
- Configured with `needs: test` and condition `github.ref == 'refs/heads/main' && github.event_name == 'push'`.
- Deploys **only when tests pass**. Never deploys on failed runs.
- **Pages URL**: `https://<github-username>.github.io/<repo-name>/`
  *(e.g., `https://zain-qureshi-ai.github.io/DevOps-LabMid/`)*

> **To enable GitHub Pages in your repo:**
> 1. Go to repository **Settings** -> **Pages**.
> 2. Under **Build and deployment** -> **Source**, select **GitHub Actions**.

---

## 15. Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| `Receiver error (HTTP 503)` | `REPORT_TOKEN` not set in receiver environment | Set `$env:REPORT_TOKEN` before launching `python receiver.py`. |
| `Receiver error (HTTP 401)` | Mismatched secret token | Ensure GitHub secret `REPORT_TOKEN` matches the receiver's `$env:REPORT_TOKEN`. |
| `Connection refused on :5001` | Receiver not running or ngrok URL expired | Restart `python receiver.py` and ensure `ngrok http 5001` is active with an updated `RECEIVER_URL`. |
| `GitHub Actions doesn't run workflow` | Workflow located in subfolder | Workflow must be at repository root `.github/workflows/main.yml`. |
| `Pages deployment failed 403` | Missing GitHub Pages permission | In Settings -> Actions -> General -> Workflow permissions, select "Read and write permissions". |
test 
test 
