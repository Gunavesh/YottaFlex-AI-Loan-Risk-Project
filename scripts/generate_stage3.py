
import random
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT SETTINGS
# --------------------------------------------------

SEED = 20261022
REFERENCE_DATE = date(2026, 10, 31)

# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

# Use a separate random generator for reproducibility
rng = random.Random(SEED)


# --------------------------------------------------
# 2. SAMPLE DATA
# --------------------------------------------------

first_names = [
    "Aarav", "Aditya", "Arjun", "Kiran", "Rahul",
    "Rohit", "Vijay", "Ananya", "Priya", "Sneha",
    "Divya", "Kavya", "Meera", "Pooja", "Riya"
]

last_names = [
    "Reddy", "Sharma", "Kumar", "Patel", "Verma",
    "Rao", "Singh", "Gupta", "Nair", "Iyer"
]

cities = [
    "Bengaluru", "Hyderabad", "Chennai",
    "Mumbai", "Pune", "Delhi",
    "Anantapur", "Vijayawada", "Kochi"
]


# --------------------------------------------------
# 3. GENERATE APPLICANT TABLE
# --------------------------------------------------

applicants = []

start_date = date(1961, 10, 31)
end_date = date(2005, 10, 31)

total_days = (end_date - start_date).days

for i in range(1, 10001):

    applicant_id = f"APP-2026-{i:06d}"

    full_name = (
        f"{rng.choice(first_names)} "
        f"{rng.choice(last_names)}"
    )

    date_of_birth = (
        start_date + timedelta(days=rng.randint(0, total_days))
    )

    city = rng.choice(cities)

    created_date = date(2026, 1, 1) + timedelta(
        days=rng.randint(0, 303)
    )

    created_time = datetime(
        created_date.year,
        created_date.month,
        created_date.day,
        rng.randint(0, 23),
        rng.randint(0, 59),
        rng.randint(0, 59)
    )

    applicants.append({
        "applicant_id": applicant_id,
        "full_name": full_name,
        "date_of_birth": date_of_birth.isoformat(),
        "city": city,
        "created_at": created_time.isoformat(sep=" ")
    })


applicant_df = pd.DataFrame(applicants)

applicant_df.to_csv(
    DATA_DIR / "applicant.csv",
    index=False
)

print("Applicant table generated:", len(applicant_df))


# --------------------------------------------------
# 4. GENERATE LOAN PRODUCT TABLE
# --------------------------------------------------

products = [
    {
        "product_id": "PROD-001",
        "product_name": "Personal Loan",
        "min_principal": 10000,
        "max_principal": 300000,
        "interest_rate": 14.0,
        "min_term": 6,
        "max_term": 36,
        "product_status": "ACTIVE"
    },
    {
        "product_id": "PROD-002",
        "product_name": "Education Loan",
        "min_principal": 25000,
        "max_principal": 1000000,
        "interest_rate": 9.0,
        "min_term": 12,
        "max_term": 84,
        "product_status": "ACTIVE"
    },
    {
        "product_id": "PROD-003",
        "product_name": "Vehicle Loan",
        "min_principal": 50000,
        "max_principal": 1500000,
        "interest_rate": 11.0,
        "min_term": 12,
        "max_term": 60,
        "product_status": "ACTIVE"
    },
    {
        "product_id": "PROD-004",
        "product_name": "Home Loan",
        "min_principal": 500000,
        "max_principal": 5000000,
        "interest_rate": 8.5,
        "min_term": 60,
        "max_term": 240,
        "product_status": "ACTIVE"
    }
]

product_df = pd.DataFrame(products)

product_df.to_csv(
    DATA_DIR / "loan_product.csv",
    index=False
)

print("Loan product table generated:", len(product_df))


# --------------------------------------------------
# 5. BASIC VALIDATION
# --------------------------------------------------

assert len(applicant_df) == 10000
assert applicant_df["applicant_id"].is_unique
assert applicant_df["applicant_id"].notna().all()
assert applicant_df["full_name"].notna().all()

assert len(product_df) == 4
assert product_df["product_id"].is_unique
assert product_df["product_name"].is_unique

assert (
    product_df["min_principal"]
    <= product_df["max_principal"]
).all()

assert (
    product_df["min_term"]
    <= product_df["max_term"]
).all()

print("\nAll basic validations passed.")

print("\nGenerated files:")
print(DATA_DIR / "applicant.csv")
print(DATA_DIR / "loan_product.csv")



# --------------------------------------------------
# 6. GENERATE EMPLOYMENT TABLE
# --------------------------------------------------

employers = [
    "ABC Technologies",
    "Global Solutions",
    "Future Systems",
    "Bright Enterprises",
    "Digital Services",
    "National Industries",
    "Apex Solutions"
]

employment_records = []
income_records = []

employment_counter = 1
income_counter = 1

for _, applicant in applicant_df.iterrows():

    applicant_id = applicant["applicant_id"]

    # 10% applicants have no employment record
    chance = rng.random()

    if chance < 0.10:
        employment_count = 0
    elif chance < 0.85:
        employment_count = 1
    else:
        employment_count = 2

    previous_start = None

    for job_number in range(employment_count):

        employment_id = f"EMP-2026-{employment_counter:06d}"
        employment_counter += 1

        # Generate employment dates
        if job_number == 0:
            start_date = date(
                rng.randint(2018, 2024),
                rng.randint(1, 12),
                1
            )
        else:
            start_date = previous_start + timedelta(
                days=rng.randint(500, 1200)
            )

        if job_number == employment_count - 1:
            # Latest job is current for most applicants
            is_current = rng.random() < 0.80
        else:
            is_current = False

        if is_current:
            end_date = None
            employment_status = "CURRENT"
            income_end = REFERENCE_DATE
        else:
            end_date = start_date + timedelta(
                days=rng.randint(365, 1800)
            )

            if end_date > REFERENCE_DATE:
                end_date = REFERENCE_DATE

            employment_status = "FORMER"
            income_end = end_date

        previous_start = start_date

        employment_type = rng.choice([
            "SALARIED",
            "SELF_EMPLOYED"
        ])

        employer_name = (
            rng.choice(employers)
            if employment_type == "SALARIED"
            else "SELF_EMPLOYED_BUSINESS"
        )

        employment_records.append({
            "employment_id": employment_id,
            "applicant_id": applicant_id,
            "employer_name": employer_name,
            "employment_type": employment_type,
            "start_date": start_date.isoformat(),
            "end_date": (
                end_date.isoformat() if end_date else None
            ),
            "employment_status": employment_status,
            "recorded_at": datetime.combine(
                REFERENCE_DATE,
                datetime.min.time()
            ).isoformat(sep=" ")
        })

        # --------------------------------------------------
        # 7. GENERATE INCOME RECORDS
        # --------------------------------------------------

        # Each employment has one or two income periods
        income_count = rng.choice([1, 2])

        total_days = (income_end - start_date).days

        if total_days < 1:
            income_count = 1

        split_date = None

        if income_count == 2:
            split_date = start_date + timedelta(
                days=total_days // 2
            )

        for period in range(income_count):

            income_id = f"INC-2026-{income_counter:06d}"
            income_counter += 1

            if period == 0:
                effective_from = start_date

                if split_date:
                    effective_to = split_date - timedelta(days=1)
                else:
                    effective_to = income_end

            else:
                effective_from = split_date
                effective_to = income_end

            if employment_type == "SALARIED":
                monthly_income = rng.randint(18000, 120000)
                income_type = "SALARY"
                income_source = "EMPLOYER"

            else:
                monthly_income = rng.randint(20000, 150000)
                income_type = "BUSINESS"
                income_source = "BUSINESS_RECORD"

            verification_status = rng.choices(
                ["VERIFIED", "PENDING", "REJECTED"],
                weights=[85, 10, 5],
                k=1
            )[0]

            income_records.append({
                "income_id": income_id,
                "applicant_id": applicant_id,
                "employment_id": employment_id,
                "income_source": income_source,
                "income_type": income_type,
                "monthly_income": monthly_income,
                "effective_from": effective_from.isoformat(),
                "effective_to": effective_to.isoformat(),
                "verification_status": verification_status,
                "recorded_at": datetime.combine(
                    REFERENCE_DATE,
                    datetime.min.time()
                ).isoformat(sep=" ")
            })


# Convert records into DataFrames
employment_df = pd.DataFrame(employment_records)
income_df = pd.DataFrame(income_records)


# Save CSV files
employment_df.to_csv(
    DATA_DIR / "employment.csv",
    index=False
)

income_df.to_csv(
    DATA_DIR / "income_record.csv",
    index=False
)

print("Employment table generated:", len(employment_df))
print("IncomeRecord table generated:", len(income_df))


# --------------------------------------------------
# 8. VALIDATE EMPLOYMENT AND INCOME
# --------------------------------------------------

assert employment_df["employment_id"].is_unique
assert income_df["income_id"].is_unique

# Every employment applicant must exist
assert employment_df["applicant_id"].isin(
    applicant_df["applicant_id"]
).all()

# Every income applicant must exist
assert income_df["applicant_id"].isin(
    applicant_df["applicant_id"]
).all()

# Every income employment must exist
assert income_df["employment_id"].isin(
    employment_df["employment_id"]
).all()

assert employment_df["employment_id"].notna().all()
assert income_df["monthly_income"].ge(0).all()

assert employment_df["employment_id"].nunique() == len(employment_df)

print("\nEmployment and Income validations passed.")



# --------------------------------------------------
# 9. GENERATE CREDIT FACILITY TABLE
# --------------------------------------------------

facility_types = [
    "CREDIT_CARD",
    "PERSONAL_LOAN",
    "VEHICLE_LOAN",
    "HOME_LOAN"
]

facility_records = []

facility_counter = 1

for _, applicant in applicant_df.iterrows():

    applicant_id = applicant["applicant_id"]

    # Decide how many facilities this applicant has
    facility_count = rng.choices(
        [0, 1, 2],
        weights=[25, 60, 15],
        k=1
    )[0]

    for _ in range(facility_count):

        facility_id = f"FAC-2026-{facility_counter:06d}"
        facility_counter += 1

        facility_type = rng.choice(facility_types)

        # Generate outstanding balance and monthly payment
        if facility_type == "CREDIT_CARD":
            outstanding_balance = rng.randint(1000, 150000)
            monthly_payment = round(
                outstanding_balance * rng.uniform(0.03, 0.08), 2
            )
            interest_rate = round(rng.uniform(18, 36), 3)

        elif facility_type == "PERSONAL_LOAN":
            outstanding_balance = rng.randint(10000, 300000)
            monthly_payment = rng.randint(1000, 15000)
            interest_rate = round(rng.uniform(10, 20), 3)

        elif facility_type == "VEHICLE_LOAN":
            outstanding_balance = rng.randint(50000, 800000)
            monthly_payment = rng.randint(3000, 25000)
            interest_rate = round(rng.uniform(8, 15), 3)

        else:
            outstanding_balance = rng.randint(100000, 3000000)
            monthly_payment = rng.randint(5000, 40000)
            interest_rate = round(rng.uniform(7, 12), 3)

        # Generate facility start date
        effective_from = date(
            rng.randint(2020, 2025),
            rng.randint(1, 12),
            1
        )

        # Decide whether the facility is active or closed
        if rng.random() < 0.80:
            facility_status = "ACTIVE"
            effective_to = None
        else:
            facility_status = "CLOSED"

            days_available = (
                REFERENCE_DATE - effective_from
            ).days

            effective_to = effective_from + timedelta(
                days=rng.randint(1, days_available)
            )

            # Closed facilities have no outstanding debt
            outstanding_balance = 0
            monthly_payment = 0

        facility_records.append({
            "facility_id": facility_id,
            "applicant_id": applicant_id,
            "facility_type": facility_type,
            "outstanding_balance": outstanding_balance,
            "monthly_payment": monthly_payment,
            "interest_rate": interest_rate,
            "facility_status": facility_status,
            "effective_from": effective_from.isoformat(),
            "effective_to": (
                effective_to.isoformat()
                if effective_to else None
            )
        })


# Convert records into DataFrame
facility_df = pd.DataFrame(facility_records)


# Save CSV file
facility_df.to_csv(
    DATA_DIR / "credit_facility.csv",
    index=False
)

print("CreditFacility table generated:", len(facility_df))


# --------------------------------------------------
# 10. VALIDATE CREDIT FACILITY TABLE
# --------------------------------------------------

assert facility_df["facility_id"].is_unique

# Check applicant relationships
assert facility_df["applicant_id"].isin(
    applicant_df["applicant_id"]
).all()

# Check balances and payments
assert facility_df["outstanding_balance"].ge(0).all()
assert facility_df["monthly_payment"].ge(0).all()
assert facility_df["interest_rate"].ge(0).all()

# Check facility types
assert facility_df["facility_type"].isin(
    facility_types
).all()

# Check statuses
assert facility_df["facility_status"].isin(
    ["ACTIVE", "CLOSED"]
).all()

# Closed facilities must have zero balance and payment
closed_facilities = facility_df[
    facility_df["facility_status"] == "CLOSED"
]

assert closed_facilities["outstanding_balance"].eq(0).all()
assert closed_facilities["monthly_payment"].eq(0).all()

print("\nCreditFacility validations passed.")



# --------------------------------------------------
# 11. GENERATE LOAN APPLICATION TABLE
# --------------------------------------------------

application_records = []

for i in range(1, 6001):

    application_id = f"LOAN-2026-{i:06d}"

    # Select an existing applicant
    applicant_id = rng.choice(
        applicant_df["applicant_id"].tolist()
    )

    # Select one of the four loan products
    product = product_df.iloc[
        rng.randrange(len(product_df))
    ]

    product_id = product["product_id"]

    # Generate principal within product limits
    requested_principal = rng.randint(
        int(product["min_principal"]),
        int(product["max_principal"])
    )

    # Generate repayment term within product limits
    requested_term = rng.randint(
        int(product["min_term"]),
        int(product["max_term"])
    )

    # Generate application date in 2026
    application_day = date(2026, 1, 1) + timedelta(
        days=rng.randint(0, 303)
    )

    application_time = datetime(
        application_day.year,
        application_day.month,
        application_day.day,
        rng.randint(0, 23),
        rng.randint(0, 59),
        rng.randint(0, 59)
    )

    application_records.append({
        "application_id": application_id,
        "applicant_id": applicant_id,
        "product_id": product_id,
        "requested_principal": requested_principal,
        "requested_term": requested_term,
        "application_date": application_time.isoformat(sep=" "),
        "application_status": "SUBMITTED"
    })


# Convert records into DataFrame
application_df = pd.DataFrame(application_records)


# Save CSV file
application_df.to_csv(
    DATA_DIR / "loan_application.csv",
    index=False
)

print("LoanApplication table generated:", len(application_df))


# --------------------------------------------------
# 12. VALIDATE LOAN APPLICATION TABLE
# --------------------------------------------------

# Check exact record count
assert len(application_df) == 6000

# Check unique application IDs
assert application_df["application_id"].is_unique

# Check applicant relationships
assert application_df["applicant_id"].isin(
    applicant_df["applicant_id"]
).all()

# Check product relationships
assert application_df["product_id"].isin(
    product_df["product_id"]
).all()

# Join applications with products to check limits
application_check = application_df.merge(
    product_df,
    on="product_id",
    how="left"
)

# Principal must be within product limits
assert (
    application_check["requested_principal"]
    >= application_check["min_principal"]
).all()

assert (
    application_check["requested_principal"]
    <= application_check["max_principal"]
).all()

# Term must be within product limits
assert (
    application_check["requested_term"]
    >= application_check["min_term"]
).all()

assert (
    application_check["requested_term"]
    <= application_check["max_term"]
).all()

# Check application status
assert application_df["application_status"].eq(
    "SUBMITTED"
).all()

print("\nLoanApplication validations passed.")



# --------------------------------------------------
# 13. GENERATE CREDIT ASSESSMENT TABLE
# --------------------------------------------------

assessment_records = []

for _, application in application_df.iterrows():

    application_id = application["application_id"]

    application_date = datetime.fromisoformat(
        application["application_date"]
    )

    # Assessment happens after application submission
    assessed_at = application_date + timedelta(
        days=rng.randint(1, 5)
    )

    assessment_id = f"ASSESS-{application_id}"

    credit_score = rng.randint(300, 900)

    assessment_records.append({
        "assessment_id": assessment_id,
        "application_id": application_id,
        "assessment_version": 1,
        "credit_score": credit_score,
        "credit_bureau": rng.choice([
            "BUREAU_A",
            "BUREAU_B",
            "BUREAU_C"
        ]),
        "assessment_status": "COMPLETED",
        "assessed_at": assessed_at.isoformat(sep=" "),
        "supersedes_assessment_id": None
    })


assessment_df = pd.DataFrame(assessment_records)

assessment_df.to_csv(
    DATA_DIR / "credit_assessment.csv",
    index=False
)

print("CreditAssessment table generated:", len(assessment_df))


# --------------------------------------------------
# 14. GENERATE APPLICATION-CREDIT FACILITY BRIDGE
# --------------------------------------------------

application_facility_records = []

for _, application in application_df.iterrows():

    application_id = application["application_id"]
    applicant_id = application["applicant_id"]

    application_date = datetime.fromisoformat(
        application["application_date"]
    )

    # Assessment date is the same as the related assessment
    assessed_at = application_date + timedelta(
        days=1
    )

    # Find facilities belonging to this applicant
    applicant_facilities = facility_df[
        facility_df["applicant_id"] == applicant_id
    ]

    for _, facility in applicant_facilities.iterrows():

        effective_from = date.fromisoformat(
            facility["effective_from"]
        )

        if pd.notna(facility["effective_to"]):
            effective_to = date.fromisoformat(
                facility["effective_to"]
            )
        else:
            effective_to = None

        # Include only facilities active on assessment date
        assessment_date = assessed_at.date()

        is_active_on_assessment_date = (
            effective_from <= assessment_date
            and (
                effective_to is None
                or effective_to >= assessment_date
            )
            and facility["facility_status"] == "ACTIVE"
        )

        if is_active_on_assessment_date:

            application_facility_records.append({
                "application_id": application_id,
                "facility_id": facility["facility_id"],
                "included_in_assessment": True,
                "assessment_date": assessed_at.isoformat(sep=" ")
            })


application_facility_df = pd.DataFrame(
    application_facility_records,
    columns=[
        "application_id",
        "facility_id",
        "included_in_assessment",
        "assessment_date"
    ]
)

application_facility_df.to_csv(
    DATA_DIR / "application_credit_facility.csv",
    index=False
)

print(
    "ApplicationCreditFacility table generated:",
    len(application_facility_df)
)


# --------------------------------------------------
# 15. VALIDATE BOTH TABLES
# --------------------------------------------------

# Credit assessment checks
assert len(assessment_df) == 6000
assert assessment_df["assessment_id"].is_unique

assert assessment_df["application_id"].is_unique

assert assessment_df["application_id"].isin(
    application_df["application_id"]
).all()

assert assessment_df["credit_score"].between(
    300, 900
).all()

assert assessment_df["assessment_status"].eq(
    "COMPLETED"
).all()


# Bridge table checks
assert not application_facility_df.duplicated(
    subset=["application_id", "facility_id"]
).any()

assert application_facility_df["application_id"].isin(
    application_df["application_id"]
).all()

assert application_facility_df["facility_id"].isin(
    facility_df["facility_id"]
).all()


# Confirm that linked facilities belong to the same applicant
bridge_check = (
    application_facility_df
    .merge(
        application_df[["application_id", "applicant_id"]],
        on="application_id"
    )
    .merge(
        facility_df[["facility_id", "applicant_id"]],
        on="facility_id",
        suffixes=("_application", "_facility")
    )
)

assert (
    bridge_check["applicant_id_application"]
    == bridge_check["applicant_id_facility"]
).all()

assert application_facility_df[
    "included_in_assessment"
].eq(True).all()

print("\nCreditAssessment validations passed.")
print("ApplicationCreditFacility validations passed.")



# ==============================
# PART 6: DOCUMENT
# ==============================

document_rows = []

document_types = [
    "IDENTITY_PROOF",
    "ADDRESS_PROOF",
    "INCOME_PROOF"
]

document_statuses = ["VERIFIED", "PENDING", "REJECTED", "MISSING"]
document_weights = [82, 8, 4, 6]

reference_end = (
    pd.Timestamp(REFERENCE_DATE)
    + pd.Timedelta(days=1)
    - pd.Timedelta(seconds=1)
)

for _, app in application_df.iterrows():

    application_id = app["application_id"]
    application_date = pd.to_datetime(app["application_date"])

    for number, document_type in enumerate(document_types, start=1):

        status = rng.choices(
            document_statuses,
            weights=document_weights,
            k=1
        )[0]

        submission_date = None
        verified_at = None
        document_reference = None

        if status != "MISSING":

            max_days = max(
                0,
                (reference_end.normalize() - application_date.normalize()).days
            )

            days_after_application = rng.randint(0, max_days)

            submission_date = (
                application_date.normalize()
                + pd.Timedelta(days=days_after_application)
                + pd.Timedelta(hours=10)
            )

            submission_date = max(submission_date, application_date)
            submission_date = min(submission_date, reference_end)

            document_reference = (
                f"DOCREF-{application_id}-{number:03d}"
            )

            if status == "VERIFIED":
                verified_at = min(
                    submission_date + pd.Timedelta(hours=1),
                    reference_end
                )

        document_rows.append({
            "document_id": f"DOC-{application_id}-{number:03d}",
            "application_id": application_id,
            "document_type": document_type,
            "submission_date": submission_date,
            "verification_status": status,
            "verified_at": verified_at,
            "document_reference": document_reference
        })


document_df = pd.DataFrame(document_rows)

document_df.to_csv(
    "data/document.csv",
    index=False
)

# ==============================
# PART 6 VALIDATIONS
# ==============================

assert len(document_df) == 18000
assert document_df["document_id"].is_unique
assert document_df["application_id"].isin(
    application_df["application_id"]
).all()

assert set(document_df["verification_status"]).issubset(
    {"VERIFIED", "PENDING", "REJECTED", "MISSING"}
)

assert document_df.groupby("application_id")["document_type"].nunique().eq(3).all()

missing_docs = document_df[
    document_df["verification_status"] == "MISSING"
]

assert missing_docs["submission_date"].isna().all()
assert missing_docs["verified_at"].isna().all()

verified_docs = document_df[
    document_df["verification_status"] == "VERIFIED"
]

assert verified_docs["submission_date"].notna().all()
assert verified_docs["verified_at"].notna().all()
assert (
    verified_docs["verified_at"] >= verified_docs["submission_date"]
).all()

print("Document table generated:", len(document_df))
print("Document validations passed!")
print(document_df["verification_status"].value_counts())


# ==============================
# PART 7: AFFORDABILITY CHECK
# ==============================

app_df = pd.read_csv(DATA_DIR / "loan_application.csv")
income_df = pd.read_csv(DATA_DIR / "income_record.csv")
facility_df = pd.read_csv(DATA_DIR / "credit_facility.csv")
bridge_df = pd.read_csv(DATA_DIR / "application_credit_facility.csv")
assessment_df = pd.read_csv(DATA_DIR / "credit_assessment.csv")
product_df = pd.read_csv(DATA_DIR / "loan_product.csv")

# Convert date columns
app_df["application_date"] = pd.to_datetime(app_df["application_date"])
income_df["effective_from"] = pd.to_datetime(income_df["effective_from"])
income_df["effective_to"] = pd.to_datetime(
    income_df["effective_to"], errors="coerce"
)
facility_df["effective_from"] = pd.to_datetime(facility_df["effective_from"])
facility_df["effective_to"] = pd.to_datetime(
    facility_df["effective_to"], errors="coerce"
)
assessment_df["assessed_at"] = pd.to_datetime(assessment_df["assessed_at"])

# Create lookup dictionaries
product_lookup = product_df.set_index("product_id").to_dict("index")
assessment_lookup = assessment_df.set_index("application_id").to_dict("index")
facility_lookup = facility_df.set_index("facility_id").to_dict("index")

bridge_lookup = {
    app_id: group["facility_id"].tolist()
    for app_id, group in bridge_df.groupby("application_id")
}

affordability_rows = []

for _, app in app_df.iterrows():

    app_id = app["application_id"]
    applicant_id = app["applicant_id"]
    app_date = app["application_date"]

    # Get product and credit assessment
    product = product_lookup[app["product_id"]]
    assessment = assessment_lookup[app_id]

    # 1. Find verified income effective on application date
    eligible_income = income_df[
        (income_df["applicant_id"] == applicant_id)
        & (income_df["verification_status"] == "VERIFIED")
        & (income_df["effective_from"] <= app_date)
        & (
            income_df["effective_to"].isna()
            | (income_df["effective_to"] >= app_date)
        )
    ].copy()

    selected_income = None
    selected_income_id = None
    income_conflict = False

    if not eligible_income.empty:

        # Check whether different sources conflict by more than 10%
        source_values = eligible_income.groupby(
            "income_source"
        )["monthly_income"].first()

        if len(source_values) > 1:
            highest = source_values.max()
            lowest = source_values.min()

            if highest > 0 and (highest - lowest) / highest > 0.10:
                income_conflict = True

        # Select the most recent eligible income record
        eligible_income = eligible_income.sort_values(
            "effective_from",
            ascending=False
        )

        selected = eligible_income.iloc[0]
        selected_income = float(selected["monthly_income"])
        selected_income_id = selected["income_id"]

    # 2. Calculate existing monthly debt
    existing_debt = 0.0

    linked_facilities = bridge_lookup.get(app_id, [])

    assessment_date = assessment["assessed_at"]

    for facility_id in linked_facilities:

        facility = facility_lookup[facility_id]

        active = (
            facility["facility_status"] == "ACTIVE"
            and facility["effective_from"] <= assessment_date
            and (
                pd.isna(facility["effective_to"])
                or facility["effective_to"] >= assessment_date
            )
        )

        if active:
            existing_debt += float(facility["monthly_payment"])

    # 3. Calculate proposed EMI
    principal = float(app["requested_principal"])
    annual_rate = float(product["interest_rate"])
    months = int(app["requested_term"])

    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)

    emi = round(emi, 2)

    # 4. Calculate total debt, DTI and disposable income
    total_debt = round(existing_debt + emi, 2)

    if selected_income is not None and selected_income > 0:
        dti = round((total_debt / selected_income) * 100, 3)
        disposable_income = round(selected_income - total_debt, 2)
    else:
        dti = None
        disposable_income = None

    # 5. Determine affordability check status
    if selected_income is None or income_conflict:
        check_status = "MANUAL_REVIEW"
    else:
        check_status = "COMPLETED"

    affordability_rows.append({
        "affordability_check_id": f"AFF-{app_id}",
        "application_id": app_id,
        "check_version": 1,
        "credit_assessment_id": assessment["assessment_id"],
        "selected_income_record_id": selected_income_id,
        "selected_income": selected_income,
        "existing_monthly_debt": round(existing_debt, 2),
        "proposed_emi": emi,
        "total_monthly_debt": total_debt,
        "dti_ratio": dti,
        "disposable_income": disposable_income,
        "check_status": check_status,
        "checked_at": assessment_date
    })


affordability_df = pd.DataFrame(affordability_rows)

affordability_df.to_csv(
    DATA_DIR / "affordability_check.csv",
    index=False
)

# ==============================
# PART 7 VALIDATIONS
# ==============================

assert len(affordability_df) == 6000
assert affordability_df["affordability_check_id"].is_unique
assert affordability_df["application_id"].is_unique
assert affordability_df["application_id"].isin(app_df["application_id"]).all()

assert (affordability_df["proposed_emi"] >= 0).all()
assert (affordability_df["existing_monthly_debt"] >= 0).all()
assert (
    affordability_df["total_monthly_debt"]
    - (
        affordability_df["existing_monthly_debt"]
        + affordability_df["proposed_emi"]
    )
).abs().lt(0.01).all()
assert affordability_df["check_status"].isin(
    ["COMPLETED", "MANUAL_REVIEW"]
).all()

missing_income = affordability_df["selected_income"].isna()

assert affordability_df.loc[
    missing_income, "dti_ratio"
].isna().all()

print("AffordabilityCheck table generated:", len(affordability_df))
print("Affordability validations passed!")
print(affordability_df["check_status"].value_counts())


# ==============================
# PART 8: LOAN DECISION
# ==============================

app_df = pd.read_csv(DATA_DIR / "loan_application.csv")
employment_df = pd.read_csv(DATA_DIR / "employment.csv")
document_df = pd.read_csv(DATA_DIR / "document.csv")
assessment_df = pd.read_csv(DATA_DIR / "credit_assessment.csv")
affordability_df = pd.read_csv(DATA_DIR / "affordability_check.csv")

# Convert date columns
app_df["application_date"] = pd.to_datetime(app_df["application_date"])
employment_df["start_date"] = pd.to_datetime(employment_df["start_date"])
assessment_df["assessed_at"] = pd.to_datetime(assessment_df["assessed_at"])
affordability_df["checked_at"] = pd.to_datetime(affordability_df["checked_at"])

decision_rows = []

for _, app in app_df.iterrows():

    app_id = app["application_id"]
    applicant_id = app["applicant_id"]
    app_date = app["application_date"]

    assessment = assessment_df[
        assessment_df["application_id"] == app_id
    ].iloc[0]

    affordability = affordability_df[
        affordability_df["application_id"] == app_id
    ].iloc[0]

    # 1. Check credit score
    credit_score = int(assessment["credit_score"])

    # 2. Check DTI
    dti = affordability["dti_ratio"]

    # 3. Check whether all required documents are verified
    applicant_docs = document_df[
        document_df["application_id"] == app_id
    ]

    required_docs_verified = (
        len(applicant_docs) == 3
        and (applicant_docs["verification_status"] == "VERIFIED").all()
    )

    # 4. Check employment stability
    applicant_jobs = employment_df[
        (employment_df["applicant_id"] == applicant_id)
        & (employment_df["employment_status"] == "CURRENT")
        & (employment_df["start_date"] <= app_date)
    ]

    stable_employment = False

    if not applicant_jobs.empty:
        employment_days = (
            app_date - applicant_jobs["start_date"]
        ).dt.days

        stable_employment = (employment_days >= 180).any()

    # 5. Apply decision rules
    if credit_score < 600 or (
        pd.notna(dti) and dti > 50
    ):
        decision_status = "REJECTED"
        reason = "Credit score below 600 or DTI above 50%"

    elif (
        credit_score >= 650
        and pd.notna(dti)
        and dti <= 40
        and affordability["check_status"] == "COMPLETED"
        and required_docs_verified
        and stable_employment
    ):
        decision_status = "APPROVED"
        reason = "All project approval conditions satisfied"

    else:
        decision_status = "MANUAL_REVIEW"
        reason = "One or more approval conditions require review"

    # Decision must happen after required checks
    decision_date = max(
        assessment["assessed_at"],
        affordability["checked_at"]
    ) + pd.Timedelta(minutes=1)

    decision_rows.append({
        "decision_id": f"DEC-{app_id}-01",
        "application_id": app_id,
        "affordability_check_id": affordability["affordability_check_id"],
        "credit_assessment_id": assessment["assessment_id"],
        "decision_version": 1,
        "decision_status": decision_status,
        "decision_reason": reason,
        "rule_reference": "PROJECT_RULES_V1",
        "decision_date": decision_date,
        "supersedes_decision_id": None
    })


decision_df = pd.DataFrame(decision_rows)

decision_df.to_csv(
    DATA_DIR / "decision.csv",
    index=False
)

# ==============================
# PART 8 VALIDATIONS
# ==============================

assert len(decision_df) == 6000
assert decision_df["decision_id"].is_unique
assert decision_df["application_id"].is_unique

assert decision_df["application_id"].isin(
    app_df["application_id"]
).all()

assert decision_df["decision_status"].isin(
    ["APPROVED", "REJECTED", "MANUAL_REVIEW"]
).all()

assert (
    decision_df["decision_date"]
    > decision_df["application_id"].map(
        affordability_df.set_index("application_id")["checked_at"]
    )
).all()

assert decision_df["decision_date"].notna().all()

print("Decision table generated:", len(decision_df))
print("Decision validations passed!")
print(decision_df["decision_status"].value_counts())


# ==============================
# PART 9: REPAYMENT SCHEDULE + DISBURSEMENT
# ==============================

from decimal import Decimal, ROUND_HALF_UP
import calendar

app_df = pd.read_csv(DATA_DIR / "loan_application.csv")
product_df = pd.read_csv(DATA_DIR / "loan_product.csv")
decision_df = pd.read_csv(DATA_DIR / "decision.csv")

app_df["application_date"] = pd.to_datetime(app_df["application_date"])

product_lookup = product_df.set_index("product_id").to_dict("index")

approved_ids = set(
    decision_df.loc[
        decision_df["decision_status"] == "APPROVED",
        "application_id"
    ]
)

schedule_rows = []
disbursement_rows = []

def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

def add_months(original_date, months):
    month_index = original_date.month - 1 + months
    year = original_date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(original_date.day, calendar.monthrange(year, month)[1])
    return original_date.replace(year=year, month=month, day=day)


for _, app in app_df.iterrows():

    app_id = app["application_id"]
    application_date = app["application_date"]

    # --------------------------------
    # A. Generate repayment schedule
    # --------------------------------

    if app_id in approved_ids:

        product = product_lookup[app["product_id"]]

        principal = money(app["requested_principal"])
        annual_rate = Decimal(str(product["interest_rate"]))
        months = int(app["requested_term"])

        monthly_rate = annual_rate / Decimal("1200")

        if monthly_rate == 0:
            emi = money(principal / months)
        else:
            factor = (1 + monthly_rate) ** months
            emi = money(
                principal * monthly_rate * factor / (factor - 1)
            )

        opening_balance = principal

        for installment_no in range(1, months + 1):

            interest = money(opening_balance * monthly_rate)

            if installment_no == months:
                # Adjust final installment to clear remaining balance
                principal_payment = opening_balance
            else:
                principal_payment = min(
                    opening_balance,
                    money(emi - interest)
                )

            installment_amount = money(
                principal_payment + interest
            )

            closing_balance = money(
                opening_balance - principal_payment
            )

            due_date = add_months(
                application_date.date(),
                installment_no
            )

            schedule_rows.append({
                "schedule_id": f"SCH-{app_id}-{installment_no:03d}",
                "application_id": app_id,
                "installment_number": installment_no,
                "due_date": due_date,
                "opening_balance": float(opening_balance),
                "principal_amount": float(principal_payment),
                "interest_amount": float(interest),
                "installment_amount": float(installment_amount),
                "closing_balance": float(closing_balance),
                "schedule_status": "SCHEDULED"
            })

            opening_balance = closing_balance

        assert opening_balance == Decimal("0.00")

    # --------------------------------
    # B. Generate disbursement record
    # --------------------------------

    if app_id in approved_ids:
        eligibility_status = "ELIGIBLE"
        eligibility_reason = "Application approved"
    else:
        eligibility_status = "NOT_ELIGIBLE"
        eligibility_reason = "Application not approved"

    # No actual money transfer is simulated in this baseline
    disbursement_rows.append({
        "disbursement_id": f"DISB-{app_id}",
        "application_id": app_id,
        "eligibility_status": eligibility_status,
        "eligibility_reason": eligibility_reason,
        "disbursement_status": "NOT_DISBURSED",
        "disbursement_amount": 0.00,
        "transaction_reference": None,
        "disbursement_date": None
    })


schedule_df = pd.DataFrame(schedule_rows)
disbursement_df = pd.DataFrame(disbursement_rows)

schedule_df.to_csv(
    DATA_DIR / "repayment_schedule.csv",
    index=False
)

disbursement_df.to_csv(
    DATA_DIR / "disbursement.csv",
    index=False
)

# ==============================
# PART 9 VALIDATIONS
# ==============================

assert len(disbursement_df) == 6000
assert disbursement_df["disbursement_id"].is_unique
assert disbursement_df["application_id"].is_unique

assert disbursement_df["application_id"].isin(
    app_df["application_id"]
).all()

assert set(schedule_df["application_id"]).issubset(approved_ids)

assert (
    disbursement_df["eligibility_status"]
    == disbursement_df["application_id"].map(
        lambda x: "ELIGIBLE" if x in approved_ids else "NOT_ELIGIBLE"
    )
).all()

# Check each approved application's repayment schedule
for app_id in approved_ids:

    app_schedule = schedule_df[
        schedule_df["application_id"] == app_id
    ]

    app_record = app_df[
        app_df["application_id"] == app_id
    ].iloc[0]

    expected_principal = money(app_record["requested_principal"])

    actual_principal = sum(
        (money(x) for x in app_schedule["principal_amount"]),
        Decimal("0.00")
    )

    assert actual_principal == expected_principal
    assert app_schedule["installment_number"].is_unique
    assert app_schedule.iloc[-1]["closing_balance"] == 0.0

print("RepaymentSchedule records generated:", len(schedule_df))
print("Disbursement records generated:", len(disbursement_df))
print("Approved applications with schedules:", len(approved_ids))
print("Repayment and Disbursement validations passed!")



# ==============================
# PART 10: APPLICATION EVENTS
# ==============================

app_df = pd.read_csv(DATA_DIR / "loan_application.csv")
assessment_df = pd.read_csv(DATA_DIR / "credit_assessment.csv")
decision_df = pd.read_csv(DATA_DIR / "decision.csv")

app_df["application_date"] = pd.to_datetime(app_df["application_date"])
assessment_df["assessed_at"] = pd.to_datetime(assessment_df["assessed_at"])
decision_df["decision_date"] = pd.to_datetime(decision_df["decision_date"])

assessment_lookup = assessment_df.set_index("application_id").to_dict("index")
decision_lookup = decision_df.set_index("application_id").to_dict("index")

event_rows = []

for _, app in app_df.iterrows():

    app_id = app["application_id"]
    application_date = app["application_date"]

    assessment = assessment_lookup[app_id]
    decision = decision_lookup[app_id]

    final_status = decision["decision_status"]

    # Event 1: Application submitted
    event_rows.append({
        "event_id": f"EVT-{app_id}-001",
        "application_id": app_id,
        "previous_status": None,
        "new_status": "SUBMITTED",
        "event_timestamp": application_date,
        "event_reason": "Loan application submitted",
        "actor_type": "APPLICANT"
    })

    # Event 2: Application enters review
    event_rows.append({
        "event_id": f"EVT-{app_id}-002",
        "application_id": app_id,
        "previous_status": "SUBMITTED",
        "new_status": "UNDER_REVIEW",
        "event_timestamp": assessment["assessed_at"],
        "event_reason": "Credit assessment completed",
        "actor_type": "SYSTEM"
    })

    # Event 3: Final decision
    event_rows.append({
        "event_id": f"EVT-{app_id}-003",
        "application_id": app_id,
        "previous_status": "UNDER_REVIEW",
        "new_status": final_status,
        "event_timestamp": decision["decision_date"],
        "event_reason": decision["decision_reason"],
        "actor_type": "SYSTEM"
    })


event_df = pd.DataFrame(event_rows)

event_df.to_csv(
    DATA_DIR / "application_event.csv",
    index=False
)

# Update current application status to match its decision
decision_status_lookup = decision_df.set_index(
    "application_id"
)["decision_status"]

app_df["application_status"] = app_df["application_id"].map(
    decision_status_lookup
)

app_df.to_csv(
    DATA_DIR / "loan_application.csv",
    index=False
)

# ==============================
# PART 10 VALIDATIONS
# ==============================

assert len(event_df) == 18000
assert event_df["event_id"].is_unique

assert event_df["application_id"].isin(
    app_df["application_id"]
).all()

# Every application must have exactly 3 events
assert event_df.groupby("application_id").size().eq(3).all()

# Check event order
event_df["event_timestamp"] = pd.to_datetime(
    event_df["event_timestamp"]
)

for app_id, group in event_df.groupby("application_id"):

    group = group.sort_values("event_timestamp")

    assert group.iloc[0]["new_status"] == "SUBMITTED"
    assert group.iloc[1]["new_status"] == "UNDER_REVIEW"

    assert (
        group.iloc[2]["new_status"]
        == decision_lookup[app_id]["decision_status"]
    )

    assert group["event_timestamp"].is_monotonic_increasing

# Current application status must match decision
assert (
    app_df["application_status"]
    == app_df["application_id"].map(decision_status_lookup)
).all()

print("ApplicationEvent records generated:", len(event_df))
print("ApplicationEvent validations passed!")


# ==============================
# FINAL STAGE 3 VALIDATION
# ==============================

tables = {
    "applicant": ("applicant.csv", "applicant_id"),
    "employment": ("employment.csv", "employment_id"),
    "income_record": ("income_record.csv", "income_id"),
    "credit_facility": ("credit_facility.csv", "facility_id"),
    "loan_product": ("loan_product.csv", "product_id"),
    "loan_application": ("loan_application.csv", "application_id"),
    "credit_assessment": ("credit_assessment.csv", "assessment_id"),
    "application_credit_facility": (
        "application_credit_facility.csv", None
    ),
    "document": ("document.csv", "document_id"),
    "affordability_check": (
        "affordability_check.csv", "affordability_check_id"
    ),
    "decision": ("decision.csv", "decision_id"),
    "repayment_schedule": ("repayment_schedule.csv", "schedule_id"),
    "disbursement": ("disbursement.csv", "disbursement_id"),
    "application_event": ("application_event.csv", "event_id")
}

data = {}

for table_name, (filename, primary_key) in tables.items():

    df = pd.read_csv(DATA_DIR / filename)
    data[table_name] = df

    if primary_key is not None:
        assert df[primary_key].notna().all()
        assert df[primary_key].is_unique

# Foreign key validations
relationships = [
    ("employment", "applicant_id", "applicant", "applicant_id"),
    ("income_record", "applicant_id", "applicant", "applicant_id"),
    ("income_record", "employment_id", "employment", "employment_id"),
    ("credit_facility", "applicant_id", "applicant", "applicant_id"),
    ("loan_application", "applicant_id", "applicant", "applicant_id"),
    ("loan_application", "product_id", "loan_product", "product_id"),
    ("credit_assessment", "application_id", "loan_application", "application_id"),
    ("application_credit_facility", "application_id", "loan_application", "application_id"),
    ("application_credit_facility", "facility_id", "credit_facility", "facility_id"),
    ("document", "application_id", "loan_application", "application_id"),
    ("affordability_check", "application_id", "loan_application", "application_id"),
    ("affordability_check", "credit_assessment_id", "credit_assessment", "assessment_id"),
    ("decision", "application_id", "loan_application", "application_id"),
    ("decision", "affordability_check_id", "affordability_check", "affordability_check_id"),
    ("decision", "credit_assessment_id", "credit_assessment", "assessment_id"),
    ("repayment_schedule", "application_id", "loan_application", "application_id"),
    ("disbursement", "application_id", "loan_application", "application_id"),
    ("application_event", "application_id", "loan_application", "application_id")
]

for child, child_col, parent, parent_col in relationships:

    child_values = data[child][child_col].dropna()
    parent_values = set(data[parent][parent_col].dropna())

    assert child_values.isin(parent_values).all(), (
        f"Foreign key validation failed: {child}.{child_col}"
    )

# Optional income record references
income_refs = data["affordability_check"]["selected_income_record_id"].dropna()
assert income_refs.isin(data["income_record"]["income_id"]).all()

# Bridge composite key validation
bridge = data["application_credit_facility"]
assert not bridge.duplicated(
    ["application_id", "facility_id"]
).any()

# Exact mandatory counts
assert len(data["applicant"]) == 10000
assert len(data["loan_product"]) == 4
assert len(data["loan_application"]) == 6000
assert len(data["credit_assessment"]) == 6000
assert len(data["document"]) == 18000
assert len(data["affordability_check"]) == 6000
assert len(data["decision"]) == 6000
assert len(data["disbursement"]) == 6000
assert len(data["application_event"]) == 18000

print("\nALL 14 TABLES LOADED SUCCESSFULLY")
print("Primary key validations passed!")
print("Foreign key validations passed!")
print("Mandatory record count validations passed!")
print("\nSTAGE 3 DATA GENERATION COMPLETED!")


