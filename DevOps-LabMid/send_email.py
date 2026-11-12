import os
import sys
import json
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email_report():
    username = os.environ.get("EMAIL_USERNAME", "").strip()
    password = os.environ.get("EMAIL_PASSWORD", "").strip()
    recipient = os.environ.get("EMAIL_TO", "").strip()
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com").strip()
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))

    if not username or not password or not recipient:
        print("Notice: Email notification skipped (EMAIL_USERNAME, EMAIL_PASSWORD, or EMAIL_TO not configured).")
        return

    report_path = Path("ci-test-report.json")
    if not report_path.exists():
        print("Warning: ci-test-report.json not found, skipping email.")
        return

    try:
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading ci-test-report.json: {e}")
        return

    repository = report_data.get("repository", "Unknown Repo")
    branch = report_data.get("branch", "Unknown Branch")
    commit_sha = report_data.get("commit_sha", "Unknown SHA")
    run_id = report_data.get("run_id", "Unknown Run ID")
    status = (report_data.get("overall_status") or report_data.get("status", "unknown")).upper()
    total = report_data.get("total_count", report_data.get("total", 0))
    passed = report_data.get("passed_count", report_data.get("passed", 0))
    failed = report_data.get("failed_count", report_data.get("failed", 0))

    subject = f"[{status}] DevOps CI Report - {repository} ({branch})"

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: {'#16a34a' if status == 'PASSED' else '#dc2626'};">
          DevOps CI Test Execution Report: {status}
        </h2>
        <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Repository</td><td style="padding: 8px; border: 1px solid #ddd;">{repository}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Branch</td><td style="padding: 8px; border: 1px solid #ddd;">{branch}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Commit SHA</td><td style="padding: 8px; border: 1px solid #ddd;"><code>{commit_sha}</code></td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Run ID</td><td style="padding: 8px; border: 1px solid #ddd;">{run_id}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Overall Status</td><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold; color: {'#16a34a' if status == 'PASSED' else '#dc2626'};">{status}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Total Tests</td><td style="padding: 8px; border: 1px solid #ddd;">{total}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Passed</td><td style="padding: 8px; border: 1px solid #ddd; color: #16a34a;">{passed}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Failed</td><td style="padding: 8px; border: 1px solid #ddd; color: #dc2626;">{failed}</td></tr>
        </table>
        <p style="margin-top: 16px;">The full machine-readable JSON test report is attached to this email.</p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    with open(report_path, "rb") as f:
        part = MIMEApplication(f.read(), Name="ci-test-report.json")
        part["Content-Disposition"] = 'attachment; filename="ci-test-report.json"'
        msg.attach(part)

    try:
        print(f"Connecting to SMTP server {smtp_server}:{smtp_port}...")
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            server.starttls()
        server.login(username, password)
        server.sendmail(username, [recipient], msg.as_string())
        server.quit()
        print(f"Email report successfully sent to {recipient}!")
    except Exception as e:
        print(f"Failed to deliver email: {e}")
        # Note: Do not hard exit with 1 if email fails so CI reporting does not block workflow


if __name__ == "__main__":
    send_email_report()

