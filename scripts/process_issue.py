#!/usr/bin/env python3
import csv
import hashlib
import os
import re
import sys
from pathlib import Path


def parse_issue_body(body: str):
    email_match = re.search(r"^email:\s*(.+)$", body, re.IGNORECASE | re.MULTILINE)
    date_match = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})$", body, re.IGNORECASE | re.MULTILINE)
    drank_match = re.search(r"^drank:\s*(yes|no)$", body, re.IGNORECASE | re.MULTILINE)

    if not email_match:
        raise ValueError("Missing 'email:' in issue body")
    if not date_match:
        raise ValueError("Missing or invalid 'date:' in issue body")
    if not drank_match:
        raise ValueError("Missing or invalid 'drank:' in issue body")

    email = email_match.group(1).strip().lower()
    date = date_match.group(1).strip()
    drank = drank_match.group(1).strip().lower()

    email_hash = hashlib.sha256(email.encode("utf-8")).hexdigest()
    return date, email_hash, drank


def row_exists(rows, date, email_hash):
    for r in rows:
        if r["date"] == date and r["email_hash"] == email_hash:
            return True
    return False


def main():
    issue_body_path = os.environ.get("ISSUE_BODY_PATH")
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    csv_path = Path("data/drink-log.csv")

    if not issue_body_path:
        print("ISSUE_BODY_PATH is required", file=sys.stderr)
        sys.exit(1)

    body = Path(issue_body_path).read_text(encoding="utf-8")
    date, email_hash, drank = parse_issue_body(body)

    rows = []
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))

    if row_exists(rows, date, email_hash):
        print("Duplicate log detected; skip append.")
        return

    new_row = {
        "date": date,
        "email_hash": email_hash,
        "drank": drank,
        "source_issue": issue_number,
    }

    file_exists = csv_path.exists()
    with csv_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "email_hash", "drank", "source_issue"])
        if not file_exists or csv_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(new_row)

    print(f"Appended log for {date}.")


if __name__ == "__main__":
    main()
