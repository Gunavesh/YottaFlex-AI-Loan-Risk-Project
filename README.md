# YottaFlex – AI Loan Risk Assessment System



## 1. Project Overview



YottaFlex is a loan risk assessment and data quality monitoring project designed to identify unusual, inconsistent, and potentially risky records in a loan processing system.



The project uses structured loan-related datasets and Python-based rule checks to detect anomalies across loan applications, repayment schedules, credit decisions, income records, and disbursements.



## 2. Objectives



- Identify data quality issues in loan records.

- Detect inconsistencies across related database tables.

- Validate loan terms against product rules.

- Identify repayment and decision-timestamp inconsistencies.

- Detect conflicting income information.

- Identify duplicate successful disbursements.

- Maintain a ground-truth dataset for identified anomalies.



## 3. Dataset



The project contains 14 CSV tables:



- Applicant

- LoanApplication

- LoanProduct

- Employment

- IncomeRecord

- CreditFacility

- ApplicationCreditFacility

- ApplicationEvent

- CreditAssessment

- AffordabilityCheck

- Decision

- Disbursement

- RepaymentSchedule

- Document



The baseline dataset contains 123,526 records across these 14 tables. Stage 4 includes controlled anomaly changes in working copies.



## 4. Anomaly Scenarios



| ID | Anomaly | Affected table |

|---|---|---|

| ANOM-001 | Loan term outside permitted product range | LoanApplication |

| ANOM-002 | Repayment schedule financial reconciliation failure | RepaymentSchedule |

| ANOM-003 | Decision date before required assessment timestamps | Decision |

| ANOM-004 | Conflicting verified income sources | IncomeRecord |

| ANOM-005 | Duplicate successful disbursements | Disbursement |



ANOM-001, ANOM-002, ANOM-003, and ANOM-005 were deliberately introduced in the working dataset. ANOM-004 represents a pre-existing baseline data conflict.



## 5. Detection Approach



The project uses Python-based rule-driven anomaly detection.



The detection script checks:



1\. Loan term against the minimum and maximum permitted product term.

2\. Repayment schedule financial reconciliation.

3\. Decision date against affordability and credit assessment timestamps.

4\. Conflicting verified income records from different sources.

5\. Multiple successful disbursements for an approved loan.



The script uses Python standard libraries, including:



- csv

- pathlib

- datetime

- collections



## 6. Detection Results



| Anomaly | Findings detected |

|---|---:|

| ANOM-001 | 1 |

| ANOM-002 | 1 |

| ANOM-003 | 1 |

| ANOM-004 | 39 |

| ANOM-005 | 1 |

| \*\*Total\*\* | \*\*43\*\* |



All 43 findings were assigned the status `DETECTED`.



Note: ANOM-004 findings are risk signals, not proof of fraud. One selected example was independently verified; all 39 findings were not manually reviewed.



## 7. Project Structure



```text

YottaFlex\_Project/

├── data/

│   └── Original baseline CSV datasets

├── output/

│   └── stage4\_working/

│       ├── 14 working CSV datasets

│       ├── ground\_truth.csv

│       ├── ground\_truth.json

│       ├── detect\_anomalies.py

│       └── anomaly\_detection\_results.csv

├── scripts/

│   └── generate\_stage3.py

└── README.md

```



Backup files are retained separately in the working folder and are not canonical input tables.



## 8. How to Run



### Requirements



- Python 3

- Windows, Linux, or macOS



No external Python packages are required for the anomaly detection script.



### Execution



Navigate to the project directory and run:



```bash

python output/stage4\_working/detect\_anomalies.py

```



The detection results are saved to:



```text

output/stage4\_working/anomaly\_detection\_results.csv

```



## 9. Validation



The project includes:



- Primary-key and composite-key uniqueness checks across all 14 tables.

- Validation of selected foreign-key relationships.

- Ground-truth verification for five anomaly scenarios.

- Detection-result verification.



Two foreign-key relationships were explicitly validated: LoanApplication to Applicant and LoanApplication to LoanProduct. The remaining foreign-key relationships have not been exhaustively checked.



## 10. Limitations and Future Improvements



- Expand foreign-key validation across all relationships.

- Review and reconcile the ANOM-004 finding-count discrepancy.

- Add machine-learning-based anomaly detection.

- Develop a dashboard to visualize anomaly findings.

- Improve risk scoring and reporting.



## 11. Project Status



The Stage 4 anomaly injection and initial rule-based detection workflow are complete. Final documentation, remaining validation, and repository preparation are in progress.

