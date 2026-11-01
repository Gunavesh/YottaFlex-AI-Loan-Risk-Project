\# YottaFlex AI Project — ChatGPT Prompt History



\*\*Tool used:\*\* ChatGPT  

\*\*Project:\*\* YottaFlex AI Candidate Project  

\*\*Purpose:\*\* Requirement analysis, database design, synthetic data generation, anomaly injection, validation and project documentation.



\---



\## Stage 1 — Requirement Analysis



\### Prompt 1 — Understand the project requirements



I have uploaded the original YottaFlex AI Candidate Project assignment PDF and project description.



Act as a data engineering project mentor. Carefully review the provided documents and use them as the primary sources of truth.



Explain the project in simple language, covering:



1\. Project objective and business problem.

2\. Overall workflow and implementation stages.

3\. Required database tables and their purposes.

4\. Relationships between the tables.

5\. Business rules and validation requirements.

6\. Required synthetic data and expected record counts.

7\. Required anomaly scenarios.

8\. Expected output files and final deliverables.

9\. Any assumptions or unclear requirements that need clarification.



Do not write code yet. Clearly distinguish official assignment requirements from proposed implementation assumptions. Explain everything in a beginner-friendly manner.



\---



\## Stage 2 — Database Design



\### Prompt 2 — Design the database structure



Based on the original YottaFlex assignment PDF, project description and completed requirement analysis, design the database structure for this project.



I need a clear database design that includes:



1\. All required tables and their purposes.

2\. Columns and appropriate data types for each table.

3\. Primary keys and foreign keys.

4\. Relationships between tables.

5\. Important constraints such as NOT NULL, UNIQUE and CHECK.

6\. How historical employment and income records will be handled.

7\. How credit facilities will be linked to loan applications.

8\. How affordability checks and credit assessments will be stored.

9\. How loan decisions, repayment schedules and disbursements will be maintained.

10\. How application events will be recorded.



Keep the design suitable for synthetic data generation and anomaly detection.



Do not write SQL or Python code yet. Explain the design simply and identify any assumptions.



\### Prompt 3 — Review the database design



Review my proposed database design carefully against the original YottaFlex assignment requirements.



Check:



1\. Whether all required entities and relationships are included.

2\. Whether primary and foreign keys are correctly defined.

3\. Whether historical employment and income records are supported.

4\. Whether income selection on the application date is properly handled.

5\. Whether credit facilities are correctly linked to applications.

6\. Whether multiple credit assessments and decisions can be tracked.

7\. Whether repayment schedules and disbursements are consistent.

8\. Whether database constraints are sufficient.

9\. Whether the design supports all five required anomaly scenarios.

10\. Whether a separate ground-truth file is needed.



Identify weaknesses and recommend corrections. Preserve the original requirements and avoid unnecessary tables.



Do not write implementation code yet. Provide a corrected final database design.



\---



\## Stage 3 — Synthetic Data Generation



\### Prompt 4 — Prepare the synthetic data generation plan



Using the original YottaFlex assignment, project description and approved database design, prepare a complete synthetic data generation plan.



Cover:



1\. Generation order of all 14 tables.

2\. Dependencies between parent and child tables.

3\. Expected record counts.

4\. Applicant and loan product generation.

5\. Employment and income history generation.

6\. Credit facility generation.

7\. Loan application generation.

8\. Credit assessment and application-credit-facility generation.

9\. Document generation.

10\. Affordability checks and decisions.

11\. Repayment schedules and disbursements.

12\. Application event generation.

13\. CSV export structure.

14\. Fixed random seed and reproducibility.



Generate clean baseline data first. Do not inject anomalies at this stage.



Do not write code yet. Explain the plan and identify assumptions that must be finalized before implementation.



\### Prompt 5 — Finalize implementation rules and begin coding



The synthetic data generation plan has been reviewed. Now finalize the implementation rules before writing code.



Use the approved database design and original assignment as the primary sources of truth.



Finalize:



1\. Four fictional loan products with principal limits, interest rates and repayment terms.

2\. Income selection and verification rules.

3\. EMI and debt-to-income ratio calculations.

4\. Loan approval, rejection and manual-review rules.

5\. Missing document and unverified income handling.

6\. Expected record counts and table dependencies.

7\. Fixed random seed, stable IDs and reference date.

8\. Clean baseline generation and reproducibility checks.

9\. Separate handling of the five anomalies and ground-truth labels.



Clearly identify project assumptions instead of presenting them as official YottaFlex policies.



After finalizing the rules, begin Python implementation in small sections. Start with project folder setup and generation of Applicant and LoanProduct tables.



Explain the code line by line, provide commands to run it and expected outputs. Wait for my confirmation before proceeding to the next section.



\### Prompt 6 — Continue Stage 3 implementation



Continue implementing Stage 3 using the finalized generation rules.



Generate the remaining tables in dependency order. For each part:



1\. Explain the table and its purpose.

2\. Identify its parent-table dependencies.

3\. Provide the Python code in manageable sections.

4\. Explain the code simply.

5\. Generate the records and export the CSV.

6\. Validate record counts, primary keys and foreign keys.

7\. Show the validation results thsesa are the promts



\---



\## Stage 4 — Anomaly Injection and Detection



\### Prompt 7 — Prepare the anomaly injection plan



I have completed Stage 3: Synthetic Data Generation. All 14 tables have been generated and their validation checks have passed.



Now guide me through Stage 4 of the YottaFlex project.



Implement these five required anomaly scenarios:



1\. Loan term outside the permitted product range.

2\. Repayment schedule totals do not reconcile.

3\. Decision made before required checks.

4\. Conflicting applicant income across sources.

5\. Duplicate application disbursed twice.



Requirements:



\- Preserve the original clean baseline CSV files.

\- Create separate working copies for anomaly injection.

\- Use fixed random seed 20261022.

\- Maintain valid primary and foreign keys unless a specific scenario requires otherwise.

\- Generate separate ground\_truth.csv and ground\_truth.json files.

\- Record anomaly ID, scenario, affected table, affected record, original value, injected value and detection rule.

\- Keep ground-truth labels separate from model input features.

\- Record the number of anomalies injected for each scenario.

\- Preserve traceability between original and modified records.

\- Validate every anomaly and check that unrelated records remain unchanged.



I am a beginner, so explain every step simply.



First prepare the implementation plan. Do not write code until I approve it.



\### Prompt 8 — Create the Stage 4 working copy



Let's begin Stage 4, Part 1.



Guide me step by step to create `output/stage4\_working/` and copy all 14 baseline CSV files into it.



Important:



\- Do not modify the original data folder.

\- Do not inject anomalies yet.

\- Do not correct the assessment timestamp mismatch yet.

\- First verify that all 14 files were copied successfully.

\- Inspect the actual formats and meanings of `assessed\_at` and `assessment\_date`.

\- Explain the mismatch before recommending a correction.



Give me one command at a time and wait for my confirmation.



\### Prompt 9 — Correct and validate assessment timestamps



Inspect the assessment timestamp mismatch between `CreditAssessment.assessed\_at` and `ApplicationCreditFacility.assessment\_date`.



Explain why the mismatch occurs and how the dates should relate.



Correct the mismatch only in the Stage 4 working copies. Preserve the original baseline files.



After correction:



1\. Validate all 4,318 bridge records.

2\. Confirm that no timestamp mismatches remain.

3\. Confirm that primary and foreign keys remain valid.

4\. Report the number of records checked and the validation result.



Do not inject anomalies until this correction is validated.



\### Prompt 10 — Inspect and prepare Anomaly 1



Let's proceed with Stage 4, Part 2 — Anomaly 1: Loan term outside the permitted product range.



First inspect `loan\_product.csv` and `loan\_application.csv` from `output/stage4\_working/`.



Do not modify anything yet.



Show me:



1\. Each product's minimum and maximum repayment term.

2\. The selected application's ID, product ID and original requested loan term.

3\. Why the selected application is suitable for this anomaly.

4\. The exact original and proposed modified values.



We will inject exactly one controlled anomaly initially.



Preserve all original data, maintain valid primary and foreign keys, and record the change for ground\_truth.csv and ground\_truth.json.



Explain everything simply. Wait for my approval before modifying the CSV file.



\### Prompt 11 — Approve and validate Anomaly 1



Approved. Change `requested\_term` from 30 to 48 for `LOAN-2026-000003` in the Stage 4 working copy only.



Please:



1\. Preserve the original baseline CSV.

2\. Record the original and injected values in ground\_truth.csv and ground\_truth.json.

3\. Validate that the application still has valid primary and foreign keys.

4\. Run the loan-term validation rule and confirm it detects exactly this intended anomaly.

5\. Show me the validation output before proceeding to Anomaly 2.



Do not modify any other records.



\### Prompt 12 — Continue the remaining anomaly scenarios



Continue Stage 4 with the remaining four agreed anomaly scenarios.



For each scenario:



1\. Explain the anomaly with a simple example.

2\. Identify the affected table and columns.

3\. Inspect and select suitable records.

4\. Show original and proposed modified values.

5\. Wait for my approval before making changes.

6\. Inject the anomaly only into the working copy.

7\. Update ground\_truth.csv and ground\_truth.json.

8\. Run the relevant validation rule.

9\. Confirm that the intended anomaly is detected and unrelated records remain unchanged.



Implement only one anomaly at a time. Do not proceed until the current anomaly is validated.



\---



\## Prompt History Recovery Note



This document contains the original prompts recovered from the available ChatGPT conversation history.



Separate original prompts for each of ANOM-002 through ANOM-005, the anomaly detection script and the final validation script are not present in the available conversation record.



These missing prompts have not been reconstructed or presented as original prompts.



