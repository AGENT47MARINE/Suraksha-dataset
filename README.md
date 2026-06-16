# SuRaksha Sentinel — Document Integrity & Fraud Detection Benchmark Dataset

This directory contains a high-fidelity synthetic benchmark dataset designed to evaluate and train risk engines on document integrity and cross-document coherence checks within the Indian lending space. 

The dataset models realistic anomalies, image-level manipulations, metadata edits, and semantic contradictions across financial, tax, and land records.

---

## Dataset File

- **Path**: `suraksha_sentinel_dataset.csv`
- **Total Records**: 1,200 applications
- **Lending Segments**: Agricultural, MSME, Housing, Retail (Salaried)
- **Target Fraud Rate**: ~15% overall

---

## Data Schema Definition

The CSV dataset contains the following 37 columns:

| Column Name | Data Type | Description |
|---|---|---|
| `application_id` | String | Unique application ID (e.g. `APP20260001`) |
| `lending_segment` | String | Loan category: `Agricultural`, `MSME`, `Housing`, or `Retail` |
| `borrower_name` | String | Name of the borrower |
| `declared_income_annual` | Integer | Annual income declared on the application form (INR) |
| `itr_declared_income` | Integer | Net income extracted from the ITR acknowledgement (INR) |
| `itr_acknowledgement_no` | String | Extracted ITR acknowledgement number (15-digits or `None`) |
| `form_16_gross_salary` | Integer | Gross salary extracted from Form 16 (INR) |
| `form_16_employer_tan` | String | Employer TAN extracted from Form 16 (`None` if not applicable) |
| `salary_slip_gross_salary_monthly` | Integer | Gross salary from the last salary slip (INR) |
| `salary_slip_employer_name` | String | Employer name from the salary slip (`None` if not applicable) |
| `bank_statement_annual_credits` | Integer | Sum of salary/business credits in the bank statement (INR) |
| `bank_statement_unusual_credits` | Binary (1/0) | Flag for circular trading or artificial balance padding |
| **`gst_annual_turnover`** | Integer | Annual turnover extracted from the GST returns (INR) |
| **`gst_registration_number`** | String | Extracted GSTIN (`None` if not applicable) |
| **`gst_turnover_inconsistency_detected`** | Binary (1/0) | Flag for mismatch between GST returns and ITR/bank credits |
| **`nach_mandate_beneficiary_name`** | String | Stated beneficiary on the NACH repayment mandate |
| **`nach_mandate_authorized_amount`** | Integer | Maximum authorized debit amount on the NACH mandate (INR) |
| **`nach_mandate_alteration_detected`** | Binary (1/0) | Flag indicating NACH mandate name or amount alterations |
| `land_record_type` | String | Type of land document: `Patta`, `7/12 Extract`, or `None` |
| `land_record_survey_no` | String | Survey / Khasra number (`None` if not applicable) |
| `land_record_owner_name` | String | Owner name stated on the land record (`None` if not applicable) |
| `sale_deed_consideration_value` | Integer | Registered property value in the sale deed (INR) |
| `ec_registered_value` | Integer | Property value registered in the Encumbrance Certificate (INR) |
| `ec_liens_count` | Integer | Number of active mortgages/liens registered against the property |
| `pdf_metadata_modification_delay_days` | Integer | Days between document stated date and PDF modification date |
| `compression_anomaly_detected` | Binary (1/0) | Flag for pixel compression history edits (image tampering indicator) |
| `cloned_signature_detected` | Binary (1/0) | Flag indicating cloned stamps, seals, or signatures |
| `font_substitution_detected` | Binary (1/0) | Flag for font inconsistencies or Unicode substitutions |
| **`physical_coherence_anomaly_detected`** | Binary (1/0) | Flag for scan anomalies (inconsistent shadows, bleed-through) |
| `ai_generation_score` | Float | Probability (0.0 to 1.0) of the document being AI-generated |
| `double_pledge_detected` | Binary (1/0) | Flag for asset registered in another active application |
| **`guarantor_name`** | String | Name of the stated loan guarantor (`None` if not applicable) |
| **`guarantor_overcommitment_detected`** | Binary (1/0) | Flag indicating the guarantor is over-committed in other active applications |
| **`document_primary_language`** | String | Detected script language of the document (e.g. `English`, `Marathi`, `Tamil`) |
| **`is_fraud`** | Binary (1/0) | **Target Variable**: 1 = Fraudulent, 0 = Clean |
| `fraud_pattern` | String | Category of fraud detected (or `clean`) |
| `adverse_action_reason` | String | Natural-language explanation aligned with RBI & DPDPA explainability |

---

## Simulated Fraud Patterns

1. **`income_inflation`**:
   - *Scenario*: The applicant inflates gross salary or business earnings.
   - *Signal*: Discrepancy between declared/salary slips and annualized bank statement credits.
2. **`fabricated_employment`**:
   - *Scenario*: The borrower submits salary slips from a shell/non-existent employer.
   - *Signal*: Stated Employer TAN mismatches official registries or matches blacklisted/invalid patterns.
3. **`ai_generated_document`**:
   - *Scenario*: Entirely fabricated tax returns or salary slips.
   - *Signal*: High `ai_generation_score` (>0.90) accompanied by high delay in modification dates.
4. **`survey_number_substitution`**:
   - *Scenario*: Lower-value land is substituted with higher-value land on a patta or 7/12 extract.
   - *Signal*: Altered survey coordinates leading to high `font_substitution_detected`, `physical_coherence_anomaly_detected`, and `compression_anomaly_detected`.
5. **`cultivator_name_substitution`**:
   - *Scenario*: Borrower substitutes their name on a family or third-party land record.
   - *Signal*: High `compression_anomaly`, `physical_coherence_anomaly_detected`, and `cloned_signature_detected` flags.
6. **`double_pledging`**:
   - *Scenario*: The same survey land or housing property is pledged concurrently for multiple loans.
   - *Signal*: `double_pledge_detected` sets to 1.
7. **`encumbrance_suppression`**:
   - *Scenario*: Extracted mortgage registrations are deleted from the Encumbrance Certificate.
   - *Signal*: Mismatches between submitted document and registry database lookup, triggering `cloned_signature_detected`.
8. **`valuation_inflation`**:
   - *Scenario*: Property valuation inflated on sale deeds to justify a higher loan-to-value (LTV) ratio.
   - *Signal*: Sale deed values are significantly higher than value registered in the official EC records.
9. **`nach_manipulation`**:
   - *Scenario*: Direct debit authorization form altered to change beneficiary name.
   - *Signal*: `nach_mandate_alteration_detected` sets to 1.
10. **`gst_manipulation`**:
    - *Scenario*: MSME borrower inflates sales invoices/GST filings.
    - *Signal*: `gst_turnover_inconsistency_detected` sets to 1.
11. **`guarantor_overcommitment`**:
    - *Scenario*: Guarantor guarantees multiple loans concurrently beyond financial capacity.
    - *Signal*: `guarantor_overcommitment_detected` sets to 1.

---

## Example Usage (Python / Pandas)

Below is a quick Python sample to load and analyze the dataset:

```python
import pandas as pd

# Load dataset
df = pd.read_csv("suraksha_sentinel_dataset.csv")

# 1. Check fraud distribution
print("Fraud distribution:")
print(df["is_fraud"].value_counts(normalize=True))

# 2. Query income inflation instances in MSME segment
inflated_msme = df[(df["fraud_pattern"] == "income_inflation") & (df["lending_segment"] == "MSME")]
print(f"\nFound {len(inflated_msme)} MSME income inflation cases.")
print(inflated_msme[["borrower_name", "declared_income_annual", "bank_statement_annual_credits", "adverse_action_reason"]].head())

# 3. List common forensic markers active in fraud cases
print("\nActive forensic markers in fraud:")
print(df[df["is_fraud"] == 1][["compression_anomaly_detected", "cloned_signature_detected", "font_substitution_detected", "double_pledge_detected"]].mean())
```
