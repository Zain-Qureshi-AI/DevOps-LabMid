
# DevOps Lab Mid - Assignment Submission Portal

## Technologies
- Python
- Flask
- SQLite
- Pytest
- GitHub Actions

## Install dependencies
pip install -r requirements.txt

## Run the application
python app.py

Open http://127.0.0.1:5000

## Run tests
python -m pytest tests/ -v

## Start local report receiver
Set the REPORT_TOKEN environment variable.

Windows PowerShell:
$env:REPORT_TOKEN = "your-secret"
python receiver.py

Receiver address:
http://127.0.0.1:5001/report

## CI/CD
GitHub Actions runs automated tests on each push.

A self-hosted Windows runner sends the report
to the local receiver after passing and failing tests.

## Test cases
1. Valid submission
2. Missing registration number
3. Invalid submission URL
