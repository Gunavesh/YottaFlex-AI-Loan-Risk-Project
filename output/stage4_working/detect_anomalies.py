import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
RESULT_FILE = BASE_DIR / "anomaly_detection_results.csv"
TOLERANCE = 0.02

results = []


def load_csv(name):
    path = BASE_DIR / f"{name}.csv"
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def parse_date(value):
    return datetime.fromisoformat(value.strip())


def add_result(anomaly_id, rule, application_id, record_id, details):
    results.append({
        "anomaly_id": anomaly_id,
        "rule": rule,
        "application_id": application_id,
        "record_id": record_id,
        "details": details,
        "status": "DETECTED"
    })


def add_pass_if_empty(anomaly_id, rule, findings):
    if not findings:
        results.append({
            "anomaly_id": anomaly_id,
            "rule": rule,
            "application_id": "",
            "record_id": "",
            "details": "No matching records found",
            "status": "NO FINDINGS"
        })


# Load input tables
applications = load_csv("loan_application")
products = load_csv("loan_product")
schedules = load_csv("repayment_schedule")
decisions = load_csv("decision")
affordability = load_csv("affordability_check")
assessments = load_csv("credit_assessment")
incomes = load_csv("income_record")
disbursements = load_csv("disbursement")

# Lookup dictionaries
product_map = {p["product_id"]: p for p in products}
affordability_map = {
    a["affordability_check_id"]: a for a in affordability
}
assessment_map = {
    a["assessment_id"]: a for a in assessments
}
application_map = {
    a["application_id"]: a for a in applications
}


# ANOM-001: Loan term outside product limits
findings = []

for loan in applications:
    product = product_map.get(loan["product_id"])

    if not product:
        continue

    term = float(loan["requested_term"])
    minimum = float(product["min_term"])
    maximum = float(product["max_term"])

    if term < minimum or term > maximum:
        findings.append(loan)
        add_result(
            "ANOM-001",
            "Loan term outside permitted product range",
            loan["application_id"],
            loan["application_id"],
            f"Requested term={term}; permitted range={minimum}-{maximum}"
        )

add_pass_if_empty("ANOM-001", "Loan term outside product range", findings)


# ANOM-002: Repayment schedule reconciliation
findings = []

for schedule in schedules:
    principal = float(schedule["principal_amount"])
    interest = float(schedule["interest_amount"])
    installment = float(schedule["installment_amount"])
    opening = float(schedule["opening_balance"])
    closing = float(schedule["closing_balance"])

    rule1_failed = abs((principal + interest) - installment) > TOLERANCE
    rule2_failed = abs((opening - principal) - closing) > TOLERANCE

    if rule1_failed or rule2_failed:
        findings.append(schedule)
        add_result(
            "ANOM-002",
            "Repayment schedule reconciliation mismatch",
            schedule["application_id"],
            schedule["schedule_id"],
            f"Principal+interest={principal + interest:.2f}; "
            f"installment={installment:.2f}; "
            f"opening-principal={opening - principal:.2f}; "
            f"closing={closing:.2f}"
        )

add_pass_if_empty("ANOM-002", "Repayment schedule reconciliation", findings)


# ANOM-003: Decision before required assessments
findings = []

for decision in decisions:
    affordability_record = affordability_map.get(
        decision["affordability_check_id"]
    )
    assessment_record = assessment_map.get(
        decision["credit_assessment_id"]
    )

    if not affordability_record or not assessment_record:
        continue

    decision_date = parse_date(decision["decision_date"])
    affordability_date = parse_date(affordability_record["checked_at"])
    assessment_date = parse_date(assessment_record["assessed_at"])

    if decision_date < affordability_date or decision_date < assessment_date:
        findings.append(decision)
        add_result(
            "ANOM-003",
            "Decision recorded before required assessments",
            decision["application_id"],
            decision["decision_id"],
            f"Decision={decision_date}; "
            f"Affordability={affordability_date}; "
            f"Credit assessment={assessment_date}"
        )

add_pass_if_empty("ANOM-003", "Decision timestamp validation", findings)


# ANOM-004: Conflicting verified income records
findings = []
income_by_applicant = defaultdict(list)

for income in incomes:
    income_by_applicant[income["applicant_id"]].append(income)

for loan in applications:
    applicant_id = loan["applicant_id"]
    application_date = parse_date(loan["application_date"])

    applicable = []

    for income in income_by_applicant[applicant_id]:
        if income["verification_status"].upper() != "VERIFIED":
            continue

        start = parse_date(income["effective_from"])
        end = parse_date(income["effective_to"])

        if start <= application_date <= end:
            applicable.append(income)

    for i in range(len(applicable)):
        for j in range(i + 1, len(applicable)):
            first = applicable[i]
            second = applicable[j]

            if first["income_source"] == second["income_source"]:
                continue

            value1 = float(first["monthly_income"])
            value2 = float(second["monthly_income"])
            smaller = min(value1, value2)

            if smaller <= 0:
                continue

            difference = abs(value1 - value2) / smaller * 100

            if difference > 10:
                findings.append(loan)
                add_result(
                    "ANOM-004",
                    "Conflicting verified income records",
                    loan["application_id"],
                    f'{first["income_id"]};{second["income_id"]}',
                    f'Sources={first["income_source"]}, '
                    f'{second["income_source"]}; '
                    f'Income={value1:.2f}, {value2:.2f}; '
                    f'Difference={difference:.2f}%'
                )

add_pass_if_empty("ANOM-004", "Verified income conflict", findings)


# ANOM-005: Multiple successful disbursements
approved_applications = {
    d["application_id"]
    for d in decisions
    if d["decision_status"].upper() == "APPROVED"
}

successful_by_application = defaultdict(list)

for disbursement in disbursements:
    if disbursement["disbursement_status"].upper() == "SUCCESS":
        successful_by_application[
            disbursement["application_id"]
        ].append(disbursement)

findings = []

for application_id, records in successful_by_application.items():
    if application_id in approved_applications and len(records) > 1:
        findings.append(application_id)
        record_ids = ";".join(
            record["disbursement_id"] for record in records
        )

        add_result(
            "ANOM-005",
            "Multiple successful disbursements for one approved application",
            application_id,
            record_ids,
            f"Successful disbursement count={len(records)}"
        )

add_pass_if_empty("ANOM-005", "Duplicate successful disbursements", findings)


# Save findings
fieldnames = [
    "anomaly_id",
    "rule",
    "application_id",
    "record_id",
    "details",
    "status"
]

with RESULT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)


# Print summary
print("\nYOTTAFLEX - ANOMALY DETECTION RESULTS\n")

for anomaly_id in [
    "ANOM-001", "ANOM-002", "ANOM-003", "ANOM-004", "ANOM-005"
]:
    rule_results = [
        row for row in results if row["anomaly_id"] == anomaly_id
    ]
    detected = sum(row["status"] == "DETECTED" for row in rule_results)
    status = "DETECTED" if detected else "NO FINDINGS"

    print(f"{anomaly_id}: {status} ({detected} finding(s))")

print(f"\nTotal rules checked: 5")
print(f"Rules with findings: {sum(any(r['status'] == 'DETECTED' for r in results if r['anomaly_id'] == a) for a in ['ANOM-001', 'ANOM-002', 'ANOM-003', 'ANOM-004', 'ANOM-005'])}")
print(f"Detailed results saved to: {RESULT_FILE}")