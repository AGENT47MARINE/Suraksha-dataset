import csv
import os
import random
import string
import hashlib
from datetime import datetime, timedelta

# Output directory
workspace_dir = r"C:\Users\yagye\OneDrive\Desktop\Suraksha Dataset"
os.makedirs(workspace_dir, exist_ok=True)

# Seed for reproducibility
random.seed(42)

# Helper lists for name generation
first_names_default = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Mohammad", 
    "Krishna", "Rahul", "Ramesh", "Suresh", "Amit", "Anil", "Rajesh", "Sanjay", 
    "Vijay", "Sunil", "Kaushik", "Deepak", "Sandeep", "Vikram", "Karan",
    "Priya", "Ananya", "Diya", "Aaradhya", "Fatima", "Pooja", "Neha", "Ritu", 
    "Sunita", "Geeta", "Meena", "Kiran", "Shalini", "Divya", "Kavitha", "Swati"
]
last_names_default = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Mishra", "Prasad", "Yadav", 
    "Choudhury", "Bose", "Dutta", "Pillai", "Menon", "Nair", "Reddy", "Patel",
    "Patil", "Deshmukh", "Joshi", "Kulkarni"
]

state_name_pool = {
    "Maharashtra": {
        "first": ["Sanjay", "Anil", "Rajesh", "Sunil", "Vikram", "Priya", "Sunita", "Shalini", "Divya", "Ramesh"],
        "last": ["Patil", "Deshmukh", "Kulkarni", "Bhalerao", "Joshi", "Patel"]
    },
    "Karnataka": {
        "first": ["Aarav", "Vijay", "Suresh", "Sai", "Vikram", "Kavitha", "Swati", "Anil", "Rahul", "Priya"],
        "last": ["Gowda", "Kulkarni", "Patil", "Rao", "Joshi", "Naidu"]
    },
    "Tamil Nadu": {
        "first": ["Rajesh", "Sai", "Karan", "Vijay", "Sunil", "Kavitha", "Swati", "Divya", "Priya", "Aaradhya"],
        "last": ["Pillai", "Menon", "Nair", "Rao", "Naidu", "Kumar"]
    },
    "Andhra Pradesh": {
        "first": ["Sai", "Ramesh", "Vijay", "Sandeep", "Deepak", "Kavitha", "Swati", "Priya", "Ananya", "Rahul"],
        "last": ["Reddy", "Naidu", "Rao", "Prasad", "Yadav", "Singh"]
    },
    "Telangana": {
        "first": ["Sai", "Ramesh", "Vijay", "Sandeep", "Deepak", "Kavitha", "Swati", "Priya", "Ananya", "Rahul"],
        "last": ["Reddy", "Naidu", "Rao", "Prasad", "Yadav", "Singh"]
    },
    "Gujarat": {
        "first": ["Amit", "Ramesh", "Sanjay", "Karan", "Pooja", "Neha", "Ritu", "Meena", "Vijay", "Deepak"],
        "last": ["Patel", "Mehta", "Shah", "Gupta", "Joshi", "Kumar"]
    },
    "West Bengal": {
        "first": ["Aarav", "Rahul", "Amit", "Sanjay", "Priya", "Ananya", "Geeta", "Kiran", "Vijay", "Deepak"],
        "last": ["Banerjee", "Chatterjee", "Bose", "Dutta", "Singh", "Kumar"]
    },
    "Kerala": {
        "first": ["Sai", "Rahul", "Sunil", "Karan", "Neha", "Divya", "Priya", "Swati", "Kiran", "Vijay"],
        "last": ["Nair", "Pillai", "Menon", "Rao", "Kumar", "Reddy"]
    }
}

employers = [
    "Tata Consultancy Services", "Infosys Limited", "Wipro Technologies", 
    "Reliance Industries", "HDFC Bank Ltd", "ICICI Bank", "Larsen & Toubro", 
    "Tech Mahindra", "State Bank of India", "Aditya Birla Group", 
    "Godrej Industries", "Mahindra & Mahindra", "HCL Technologies",
    "Cognizant Technologies", "Accenture India", "Bharti Airtel"
]

state_metadata = {
    "Maharashtra": {"lang": "Marathi", "land_type": "7/12 Extract", "code": "27"},
    "Karnataka": {"lang": "Kannada", "land_type": "Khata", "code": "29"},
    "Tamil Nadu": {"lang": "Tamil", "land_type": "Patta", "code": "33"},
    "Andhra Pradesh": {"lang": "Telugu", "land_type": "Pattadar Passbook", "code": "37"},
    "Telangana": {"lang": "Telugu", "land_type": "Pattadar Passbook", "code": "36"},
    "Gujarat": {"lang": "Gujarati", "land_type": "7/12 Extract", "code": "24"},
    "West Bengal": {"lang": "Bengali", "land_type": "Khatian", "code": "19"},
    "Uttar Pradesh": {"lang": "Hindi", "land_type": "Record of Rights (Khatauni)", "code": "09"},
    "Rajasthan": {"lang": "Hindi", "land_type": "Jamabandi", "code": "08"},
    "Madhya Pradesh": {"lang": "Hindi", "land_type": "Khasra", "code": "23"},
    "Bihar": {"lang": "Hindi", "land_type": "Record of Rights", "code": "10"},
    "Punjab": {"lang": "Hindi", "land_type": "Fard", "code": "03"},
    "Haryana": {"lang": "Hindi", "land_type": "Fard", "code": "06"},
    "Kerala": {"lang": "Malayalam", "land_type": "Thandaper", "code": "32"},
    "Delhi NCT": {"lang": "Hindi", "land_type": None, "code": "07"},
    "Odisha": {"lang": "English", "land_type": "Record of Rights", "code": "21"},
    "Chhattisgarh": {"lang": "Hindi", "land_type": "Khasra", "code": "22"},
    "Jharkhand": {"lang": "Hindi", "land_type": "Khatiyan", "code": "20"},
    "Assam": {"lang": "English", "land_type": "Jamabandi", "code": "18"},
    "Uttarakhand": {"lang": "Hindi", "land_type": "Khatauni", "code": "05"},
    "Himachal Pradesh": {"lang": "Hindi", "land_type": "Jamabandi", "code": "02"},
    "Goa": {"lang": "English", "land_type": "Form I and XIV", "code": "30"},
    "Jammu & Kashmir": {"lang": "Hindi", "land_type": "Girdawari", "code": "01"}
}

states = list(state_metadata.keys())

sub_type_baselines = {
    "ITR_Income_Inflation": 950,
    "AI_Generated_Document": 900,
    "Bank_Statement_Manipulation": 850,
    "Encumbrance_Suppression": 830,
    "Survey_Number_Substitution": 800,
    "Salary_Slip_Manipulation": 750,
    "Property_Valuation_Inflation": 720,
    "GST_Turnover_Manipulation": 700,
    "Form16_Income_Inflation": 680,
    "Double_Pledging": 650,
    "Fabricated_Employment": 600,
    "Balance_Sheet_Fabrication": 560,
    "Ownership_Chain_Manipulation": 510,
    "Cultivator_Name_Substitution": 480,
    "NACH_Mandate_Manipulation": 420,
    "Cross_Pledging_Director": 360,
    "Mutation_Date_Manipulation": 300,
    "Guarantor_Overcommitment": 290,
    "Identity_Document_Fraud": 250,
}

# Helpers
def get_sub_type_counts(target_fraud):
    counts = {}
    total_baseline = sum(sub_type_baselines.values())
    for name, base in sub_type_baselines.items():
        counts[name] = int(base * target_fraud / total_baseline)
    
    # Adjust for rounding remainder
    current_sum = sum(counts.values())
    remainder = target_fraud - current_sum
    sorted_types = sorted(sub_type_baselines.keys(), key=lambda k: (sub_type_baselines[k] * target_fraud / total_baseline) % 1, reverse=True)
    for i in range(remainder):
        counts[sorted_types[i]] += 1
    return counts

def generate_tan():
    # 4 uppercase alpha + 5 digits + 1 uppercase alpha
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=5))
    chk = random.choice(string.ascii_uppercase)
    return f"{letters}{digits}{chk}"

def generate_gstin(state_code, pan):
    digit = random.choice(string.digits)
    alphanum = random.choice(string.ascii_uppercase + string.digits)
    return f"{state_code}{pan}{digit}Z{alphanum}"

def generate_ack():
    return ''.join(random.choices(string.digits, k=15))

def generate_survey_no(state):
    num = random.randint(10, 999)
    sub = random.randint(1, 12)
    part = random.choice(["", "A", "B", "C", "D"])
    if state == "Tamil Nadu":
        return f"{num}/{sub}{part}"
    elif state == "Maharashtra":
        return f"{num}/{sub}{part}"
    elif state == "Karnataka":
        return f"KA-KH-{random.randint(1000, 9999)}"
    else:
        return f"{num}/{sub}{part}"

def get_indian_name(state):
    pool = state_name_pool.get(state, state_name_pool.get("Default", {"first": first_names_default, "last": last_names_default}))
    if pool is None or "first" not in pool:
        return f"{random.choice(first_names_default)} {random.choice(last_names_default)}"
    return f"{random.choice(pool['first'])} {random.choice(pool['last'])}"

start_date = datetime(2022, 1, 1)
end_date = datetime(2026, 6, 17)
delta_days = (end_date - start_date).days

def random_date():
    days = random.randint(0, delta_days)
    d = start_date + timedelta(days=days)
    return d.strftime("%d-%m-%Y"), d

def get_itr_ay(sub_date_obj):
    year = sub_date_obj.year
    if year == 2022:
        return "FY2021-22"
    elif year == 2023:
        return random.choice(["FY2021-22", "FY2022-23"])
    elif year == 2024:
        return random.choice(["FY2022-23", "FY2023-24"])
    elif year == 2025:
        return random.choice(["FY2023-24", "FY2024-25"])
    else:  # 2026
        return "FY2024-25"

sub_type_loan_mapping = {
    "ITR_Income_Inflation": ["MSME"],
    "AI_Generated_Document": ["Agricultural", "MSME", "Housing_Finance", "Retail_Salaried"],
    "Bank_Statement_Manipulation": ["MSME"],
    "Encumbrance_Suppression": ["Agricultural", "Housing_Finance"],
    "Survey_Number_Substitution": ["Agricultural"],
    "Salary_Slip_Manipulation": ["Retail_Salaried"],
    "Property_Valuation_Inflation": ["Housing_Finance"],
    "GST_Turnover_Manipulation": ["MSME"],
    "Form16_Income_Inflation": ["Retail_Salaried"],
    "Double_Pledging": ["Agricultural", "Housing_Finance"],
    "Fabricated_Employment": ["Retail_Salaried"],
    "Balance_Sheet_Fabrication": ["MSME"],
    "Ownership_Chain_Manipulation": ["Housing_Finance"],
    "Cultivator_Name_Substitution": ["Agricultural"],
    "NACH_Mandate_Manipulation": ["Retail_Salaried"],
    "Cross_Pledging_Director": ["MSME"],
    "Mutation_Date_Manipulation": ["Agricultural"],
    "Guarantor_Overcommitment": ["Agricultural", "MSME", "Housing_Finance", "Retail_Salaried"],
    "Identity_Document_Fraud": ["Retail_Salaried"],
    "Clean": ["Agricultural", "MSME", "Housing_Finance", "Retail_Salaried"]
}

# Derived columns scoring logic
def compute_risk_score(row):
    score = 0
    if row['pixel_manipulation_detected']:        score += 15
    if row['metadata_timestamp_contradiction']:   score += 15
    if row['cloned_region_detected']:             score += 12
    if row['compression_anomaly_detected']:       score += 10
    if row['encumbrance_suppression_flag']:       score += 10
    if row['employment_tan_mismatch']:            score += 10
    if row['nach_mandate_alteration_detected']:   score += 10
    if row['unicode_substitution_detected']:      score += 8
    if row['font_inconsistency_score'] > 0.45:   score += 8
    if row['pdf_structural_anomaly_score'] > 0.50: score += 8
    if row['frequency_domain_anomaly_score'] > 0.50: score += 8
    if row['double_pledge_risk_score'] > 0.60:   score += 8
    if row['ai_generated_document_probability'] > 0.70: score += 8
    if row['income_cross_doc_variance_pct'] > 30: score += 6
    if row['itr_vs_bank_stmt_discrepancy_pct'] > 30: score += 6
    if row['property_valuation_discrepancy_pct'] is not None and row['property_valuation_discrepancy_pct'] > 30: score += 5
    if row['gst_cross_month_inconsistency']:      score += 5
    if row['guarantor_overcommitment_detected']:  score += 5
    if row['mutation_date_manipulated']:          score += 5
    if row['bank_statement_round_number_flag']:   score += 3
    score += min(row['bank_statement_unusual_credits_count'], 5)
    return min(int(score), 100)

def risk_category(score):
    if score <= 35:   return 'Clean'
    if score <= 55:   return 'Low_Risk'
    if score <= 75:   return 'Medium_Risk'
    return 'High_Risk'

def processing_time(fraud_risk_category):
    if fraud_risk_category == 'Clean':
        if random.random() < 0.05:
            return random.randint(1500, 6000)
        return random.randint(400, 1499)
    if fraud_risk_category == 'Low_Risk':
        return random.randint(3000, 7999)
    if fraud_risk_category == 'Medium_Risk':
        return random.randint(3000, 11999)
    return random.randint(5395, 11506)

def final_decision(row):
    if row['ground_truth_fraud_label'] == 0:
        return 'Approved'
    if row['fraud_risk_category'] == 'High_Risk':
        return 'Rejected'
    if row['fraud_risk_category'] in ('Medium_Risk', 'Low_Risk'):
        return 'Manual_Review'
    return 'Approved' # False negative

def format_adverse_reason(row):
    sub_type = row['fraud_sub_type']
    if not row['adverse_action_triggered']:
        return None
    
    itr_inc = f"{row['itr_declared_income']:,}" if row['itr_declared_income'] is not None else ""
    bank_cred = f"{row['bank_statement_annual_credits_inr']:,}" if row['bank_statement_annual_credits_inr'] is not None else ""
    sal_gross = f"{row['form_16_gross_salary']:,}" if row['form_16_gross_salary'] is not None else ""
    sal_monthly = f"{row['salary_slip_gross_monthly_inr']:,}" if row['salary_slip_gross_monthly_inr'] is not None else ""
    gst_turn = f"{row['gst_annual_turnover']:,}" if row['gst_annual_turnover'] is not None else ""
    sale_val = f"{row['sale_deed_consideration_value']:,}" if row['sale_deed_consideration_value'] is not None else ""
    ec_val = f"{row['ec_registered_value']:,}" if row['ec_registered_value'] is not None else ""
    
    doc_type_or_income = row['land_record_document_type'] if row['land_record_document_type'] is not None else "income verification"

    if sub_type == "ITR_Income_Inflation":
        return f"Income Tax Return for {row['itr_assessment_year']} declares annual income of ₹{itr_inc}; bank statement credits for the same period total ₹{bank_cred}, a {row['itr_vs_bank_stmt_discrepancy_pct']:.1f}% shortfall. Structural analysis of the ITR PDF indicates post-creation field modification ({row['pdf_structural_anomaly_score']:.2f} anomaly score). Application referred for income verification."
    
    elif sub_type == "AI_Generated_Document":
        return f"Document submitted for {doc_type_or_income} shows frequency-domain image characteristics (score {row['frequency_domain_anomaly_score']:.2f}) inconsistent with a physically scanned document, and exhibits no physical scan artefacts (coherence score {row['physical_scan_coherence_score']:.2f}). AI-generation probability: {row['ai_generated_document_probability']:.0%}. Document cannot be accepted as authentic."
    
    elif sub_type == "Bank_Statement_Manipulation":
        return f"Bank statement contains {row['bank_statement_unusual_credits_count']} unusual credit entries with round-number values inconsistent with employer salary patterns. Compression analysis indicates post-creation editing (anomaly score {row['pdf_structural_anomaly_score']:.2f}). Cross-document income variance of {row['income_cross_doc_variance_pct']:.1f}% exceeds the acceptable threshold of 22%."
    
    elif sub_type == "Encumbrance_Suppression":
        return f"Encumbrance certificate for property survey no. {row['land_record_survey_no']} shows zero registered liens. Cross-application analysis indicates the same property carries a double-pledge risk score of {row['double_pledge_risk_score']:.2f}, suggesting active collateral in another live application. Encumbrance data is suspected to have been suppressed."
    
    elif sub_type == "Survey_Number_Substitution":
        return f"Survey number {row['land_record_survey_no']} recorded in the submitted {row['land_record_document_type']} does not correspond to the property ownership asserted in the application. Font analysis detected inconsistency in the survey number field (score {row['font_inconsistency_score']:.2f}), indicating field-level editing."
    
    elif sub_type == "Double_Pledging":
        return f"Cross-application analysis has identified the property (survey no. {row['land_record_survey_no']}) as live collateral in at least one other active loan application (double-pledge risk score: {row['double_pledge_risk_score']:.2f}). Encumbrance certificate does not reflect existing registered charges. Application suspended pending collateral verification."
    
    elif sub_type == "Salary_Slip_Manipulation":
        return f"Declared monthly gross salary of ₹{sal_monthly} is {row['form16_vs_salary_slip_discrepancy_pct']:.1f}% higher than supported by Form 16 annual gross and bank statement credit history. Font inconsistency detected in the gross salary field (score {row['font_inconsistency_score']:.2f})."
    
    elif sub_type == "Form16_Income_Inflation":
        tan_msg = ""
        if row['employment_tan_mismatch']:
            tan_msg = f" Employer TAN on Form 16 ({row['form_16_employer_tan']}) does not match TAN on salary slip ({row['salary_slip_employer_tan']})."
        return f"Form 16 gross salary of ₹{sal_gross} is {row['form16_vs_salary_slip_discrepancy_pct']:.1f}% higher than supported by bank statement annual credits.{tan_msg} Metadata timestamp contradiction detected."
    
    elif sub_type == "Fabricated_Employment":
        return f"Employer TAN {row['form_16_employer_tan']} recorded on Form 16 cannot be verified against registered employer records. TAN on salary slip ({row['salary_slip_employer_tan']}) does not match. Employment documentation cannot be authenticated."
    
    elif sub_type == "GST_Turnover_Manipulation":
        return f"Declared GST annual turnover of ₹{gst_turn} is inconsistent with cross-month GST return submissions and exceeds bank credit evidence by {row['income_cross_doc_variance_pct']:.1f}%. GST registration {row['gst_registration_number']} flagged for cross-month inconsistency."
    
    elif sub_type == "Property_Valuation_Inflation":
        return f"Sale deed consideration value of ₹{sale_val} exceeds the encumbrance certificate registered value of ₹{ec_val} by {row['property_valuation_discrepancy_pct']:.1f}%. This discrepancy indicates possible sale deed value inflation to support a higher loan-to-value ratio."
    
    elif sub_type == "Guarantor_Overcommitment":
        return f"Guarantor {row['guarantor_name']} has been identified as a guarantor or co-borrower in multiple concurrent loan applications across institutions. Aggregate guarantee exposure materially exceeds the disclosure in this application. Application referred for guarantor liability assessment."
    
    elif sub_type == "NACH_Mandate_Manipulation":
        return f"NACH mandate shows font inconsistency (score {row['font_inconsistency_score']:.2f}) in the beneficiary name and authorised debit amount fields, indicating post-creation alteration of mandate terms. Original mandate fields suspected to have been modified after issuance."
    
    elif sub_type == "Ownership_Chain_Manipulation":
        return f"Mutation records for property survey no. {row['land_record_survey_no']} show signs of ownership chain alteration. Cloned stamp/signature detected (cloned signature flag: True). Application referred for title verification."
        
    elif sub_type == "Cultivator_Name_Substitution":
        return f"Cultivator name {row['land_record_owner_name']} on land record does not match borrower {row['borrower_name']}. Pixel-level compression anomalies detected in the name field, indicating cultivator name substitution."
        
    elif sub_type == "Cross_Pledging_Director":
        return f"Guarantor {row['guarantor_name']} is co-committed in multiple corporate applications as director. Aggregate exposure exceeds financial limit (double-pledge risk score: {row['double_pledge_risk_score']:.2f})."
        
    elif sub_type == "Mutation_Date_Manipulation":
        return f"Mutation registration date shows signs of timestamp contradiction. Modification delay is {row['pdf_metadata_modification_delay_days']} days, indicating post-notarisation editing."
        
    elif sub_type == "Identity_Document_Fraud":
        return f"Identity verification failed. Unicode lookalike character substitution detected in name/number fields on the submitted identity document (score {row['font_inconsistency_score']:.2f})."
        
    else:
        return f"Adverse Action Recommended: {sub_type.replace('_', ' ')} detected. Application referred for manual review."

# Generator
def generate_row(app_id, label, fraud_sub_type, clean_calibrator=0.0, fraud_calibrator=0.0, clean_coherence_calibrator=0.0, fraud_coherence_calibrator=0.0, accumulators=None):
    row = {}
    row['application_id'] = app_id
    
    # Context
    sub_date, sub_date_obj = random_date()
    row['submission_date'] = sub_date
    row['itr_assessment_year'] = get_itr_ay(sub_date_obj)
    
    # Select loan_type consistent with fraud sub-type
    valid_loans = sub_type_loan_mapping[fraud_sub_type]
    weights = {"Agricultural": 15, "MSME": 25, "Housing_Finance": 25, "Retail_Salaried": 35}
    if len(valid_loans) == 1:
        loan_type = valid_loans[0]
    else:
        valid_weights = [weights[l] for l in valid_loans]
        loan_type = random.choices(valid_loans, weights=valid_weights)[0]
    row['loan_type'] = loan_type

    # Select state (ensure non-null land record for land record fraud sub-types)
    land_fraud_types = (
        "Encumbrance_Suppression", "Survey_Number_Substitution", "Property_Valuation_Inflation",
        "Double_Pledging", "Ownership_Chain_Manipulation", "Cultivator_Name_Substitution",
        "Mutation_Date_Manipulation"
    )
    if fraud_sub_type in land_fraud_types or loan_type == "Agricultural" or (loan_type == "Housing_Finance" and random.random() < 0.80):
        state_list = [s for s in states if state_metadata[s]["land_type"] is not None]
        state = random.choice(state_list)
    else:
        state = random.choice(states)
        
    row['state'] = state
    row['document_primary_language'] = state_metadata[state]['lang']
    
    row['lender_type'] = random.choices(
        ["PSB", "Private_Bank", "NBFC", "HFC", "Small_Finance_Bank", "MFI"],
        weights=[30, 27, 23, 10, 7, 3]
    )[0]
    
    # Select employment_type consistent with loan_type
    if loan_type == "Agricultural":
        employment_type = random.choices(
            ["Agricultural_Cultivator", "Agricultural_Labourer", "Tenant_Farmer"],
            weights=[60, 20, 20]
        )[0]
    elif loan_type == "Retail_Salaried":
        employment_type = random.choices(
            ["Salaried_Private_Sector", "Salaried_Govt", "Salaried_MNC", "Salaried_PSU"],
            weights=[50, 15, 20, 15]
        )[0]
    elif loan_type == "MSME":
        employment_type = random.choices(
            ["Self_Employed_Professional", "Proprietor", "Partnership_Firm", "Private_Ltd_Director"],
            weights=[30, 40, 15, 15]
        )[0]
    else: # Housing_Finance
        is_salaried = random.choices([True, False], weights=[70, 30])[0]
        if is_salaried:
            employment_type = random.choices(
                ["Salaried_Private_Sector", "Salaried_Govt", "Salaried_MNC", "Salaried_PSU"],
                weights=[50, 15, 20, 15]
            )[0]
        else:
            employment_type = random.choices(
                ["Self_Employed_Professional", "Proprietor", "Partnership_Firm", "Private_Ltd_Director"],
                weights=[30, 40, 15, 15]
            )[0]
    row['employment_type'] = employment_type
    
    row['application_channel'] = random.choices(
        ["Branch", "Digital_Portal", "DSA", "Business_Correspondent", "Mobile_App"],
        weights=[34, 29, 21, 10, 6]
    )[0]
    
    # document_bundle_size
    if label == 0:
        row['document_bundle_size'] = int(random.triangular(4, 15, 9))
    else:
        row['document_bundle_size'] = int(random.triangular(4, 15, 10))
        
    # cibil_score
    if label == 0:
        cibil = int(random.normalvariate(698, 87))
    else:
        cibil = int(random.normalvariate(697, 87))
    row['cibil_score'] = max(300, min(900, cibil))
    
    # loan_amount_inr
    if loan_type == "Agricultural":
        row['loan_amount_inr'] = int(random.triangular(150000, 3000000, 750000))
    elif loan_type == "Retail_Salaried":
        row['loan_amount_inr'] = int(random.triangular(500000, 7500000, 2000000))
    elif loan_type == "MSME":
        row['loan_amount_inr'] = int(random.triangular(2000000, 50000000, 12000000))
    else: # Housing_Finance
        row['loan_amount_inr'] = int(random.triangular(2000000, 75000000, 15000000))
        
    row['borrower_name'] = get_indian_name(state)
    
    # Income baseline
    if loan_type == "Agricultural":
        declared_inc = int(row['loan_amount_inr'] / random.uniform(1.0, 3.0))
    elif loan_type == "Retail_Salaried":
        declared_inc = int(row['loan_amount_inr'] / random.uniform(1.5, 4.0))
    elif loan_type == "MSME":
        declared_inc = int(row['loan_amount_inr'] / random.uniform(2.0, 6.0))
    else: # Housing_Finance
        declared_inc = int(row['loan_amount_inr'] / random.uniform(2.0, 5.0))
    row['declared_income_annual_inr'] = max(170000, min(8800000, declared_inc))
    
    is_salaried_emp = employment_type in ("Salaried_Private_Sector", "Salaried_Govt", "Salaried_MNC", "Salaried_PSU")
    is_business_emp = employment_type in ("Self_Employed_Professional", "Proprietor", "Partnership_Firm", "Private_Ltd_Director")
    is_agri_emp = employment_type in ("Agricultural_Cultivator", "Agricultural_Labourer", "Tenant_Farmer")

    if is_agri_emp:
        row['itr_declared_income'] = None
        row['itr_acknowledgement_no'] = None
    else:
        row['itr_declared_income'] = max(170000, min(8800000, int(row['declared_income_annual_inr'] * random.uniform(0.95, 1.05))))
        row['itr_acknowledgement_no'] = generate_ack()
        
    if is_salaried_emp:
        row['form_16_gross_salary'] = int(row['declared_income_annual_inr'] * random.uniform(0.98, 1.02))
        row['form_16_employer_tan'] = generate_tan()
        row['salary_slip_gross_monthly_inr'] = int(row['form_16_gross_salary'] / 12 * random.uniform(0.92, 1.08))
        row['salary_slip_employer_name'] = random.choice(employers)
        row['salary_slip_employer_tan'] = row['form_16_employer_tan']
    else:
        row['form_16_gross_salary'] = None
        row['form_16_employer_tan'] = None
        row['salary_slip_gross_monthly_inr'] = None
        row['salary_slip_employer_name'] = None
        row['salary_slip_employer_tan'] = None
        
    row['bank_statement_annual_credits_inr'] = int(row['declared_income_annual_inr'] * random.uniform(0.88, 1.12))
    row['bank_statement_unusual_credits_count'] = random.randint(0, 2)
    
    # Delta-sigma accumulator for round number flag (clean: ~4%)
    if label == 0 and accumulators:
        accumulators['round_num_acc'] += 0.04
        if accumulators['round_num_acc'] >= 1.0:
            row['bank_statement_round_number_flag'] = True
            accumulators['round_num_acc'] -= 1.0
        else:
            row['bank_statement_round_number_flag'] = False
    else:
        row['bank_statement_round_number_flag'] = random.random() < 0.04
        
    if is_business_emp:
        gst_turn = int(row['declared_income_annual_inr'] * random.uniform(1.5, 3.0))
        row['gst_annual_turnover'] = max(435000, min(29400000, gst_turn))
        pan = ''.join(random.choices(string.ascii_uppercase, k=5)) + ''.join(random.choices(string.digits, k=4)) + random.choice(string.ascii_uppercase)
        row['gst_registration_number'] = generate_gstin(state_metadata[state]["code"], pan)
        row['gst_cross_month_inconsistency'] = False
    else:
        row['gst_annual_turnover'] = None
        row['gst_registration_number'] = None
        row['gst_cross_month_inconsistency'] = None
        
    if loan_type == "Agricultural" or (loan_type == "MSME" and random.random() < 0.40):
        row['nach_mandate_beneficiary_name'] = None
        row['nach_mandate_amount_inr'] = None
        row['nach_mandate_alteration_detected'] = None
    else:
        row['nach_mandate_beneficiary_name'] = f"{random.choice(['PolyOculus', 'HDFC', 'ICICI', 'SBI'])} Finance"
        nach_amt = int(row['loan_amount_inr'] / 60 * random.uniform(0.80, 1.20))
        row['nach_mandate_amount_inr'] = max(11000, min(125000, nach_amt))
        row['nach_mandate_alteration_detected'] = False
        
    # Guarantor requirement
    guarantor_req = False
    if fraud_sub_type in ("Guarantor_Overcommitment", "Cross_Pledging_Director"):
        guarantor_req = True
    elif random.random() < 0.50:
        guarantor_req = True
        
    if guarantor_req:
        g_name = get_indian_name(state)
        while g_name == row['borrower_name']:
            g_name = get_indian_name(state)
        row['guarantor_name'] = g_name
        row['guarantor_overcommitment_detected'] = False
    else:
        row['guarantor_name'] = None
        row['guarantor_overcommitment_detected'] = None

    # Land record
    has_land_record = False
    land_fraud_types = (
        "Encumbrance_Suppression", "Survey_Number_Substitution", "Property_Valuation_Inflation",
        "Double_Pledging", "Ownership_Chain_Manipulation", "Cultivator_Name_Substitution",
        "Mutation_Date_Manipulation"
    )
    if fraud_sub_type in land_fraud_types:
        has_land_record = True
    elif loan_type == "Agricultural":
        has_land_record = True
    elif loan_type == "Housing_Finance":
        if random.random() < 0.80:
            has_land_record = True
    elif loan_type == "MSME":
        if random.random() < 0.05:
            has_land_record = True

    if has_land_record and state_metadata[state]["land_type"] is not None:
        row['land_record_document_type'] = state_metadata[state]["land_type"]
        row['land_record_state'] = state
        row['land_record_survey_no'] = generate_survey_no(state)
        row['land_record_owner_name'] = row['borrower_name']
        row['sale_deed_consideration_value'] = max(2000000, min(37000000, int(row['loan_amount_inr'] / random.uniform(0.60, 0.90))))
        row['ec_registered_value'] = int(row['sale_deed_consideration_value'] * random.uniform(0.95, 1.05))
        row['ec_liens_count'] = random.choices([0, 1], weights=[75, 25])[0]
        row['mutation_date_manipulated'] = False
    else:
        row['land_record_document_type'] = None
        row['land_record_state'] = None
        row['land_record_survey_no'] = None
        row['land_record_owner_name'] = None
        row['sale_deed_consideration_value'] = None
        row['ec_registered_value'] = None
        row['ec_liens_count'] = None
        row['mutation_date_manipulated'] = None

    # Baseline forensic signals
    row['pdf_structural_anomaly_score'] = round(random.triangular(0.001, 0.75, 0.14 + clean_calibrator), 4)
    row['frequency_domain_anomaly_score'] = round(random.triangular(0.0, 0.82, 0.14 + clean_calibrator), 4)
    row['font_inconsistency_score'] = round(random.triangular(0.0, 0.82, 0.15 + clean_calibrator), 4)
    row['physical_scan_coherence_score'] = round(random.triangular(0.5, 0.999, 0.92 + clean_coherence_calibrator), 4)
    row['ai_generated_document_probability'] = round(random.triangular(0.010, 0.52, 0.05 + clean_calibrator), 4)
    row['pdf_metadata_modification_delay_days'] = int(random.triangular(0, 3, 2))
    row['compression_anomaly_detected'] = False
    row['documents_flagged_count'] = 0

    # Accumulators for clean binary signals
    if label == 0 and accumulators:
        # pixel_manipulation: 2.6%
        accumulators['pixel_acc'] += 0.026
        if accumulators['pixel_acc'] >= 1.0:
            row['pixel_manipulation_detected'] = True
            accumulators['pixel_acc'] -= 1.0
        else:
            row['pixel_manipulation_detected'] = False

        # cloned_region: 1.8%
        accumulators['clone_acc'] += 0.018
        if accumulators['clone_acc'] >= 1.0:
            row['cloned_region_detected'] = True
            accumulators['clone_acc'] -= 1.0
        else:
            row['cloned_region_detected'] = False

        # metadata_timestamp_contradiction: 2.6%
        accumulators['timestamp_acc'] += 0.026
        if accumulators['timestamp_acc'] >= 1.0:
            row['metadata_timestamp_contradiction'] = True
            accumulators['timestamp_acc'] -= 1.0
        else:
            row['metadata_timestamp_contradiction'] = False
    else:
        row['pixel_manipulation_detected'] = random.random() < 0.026
        row['cloned_region_detected'] = random.random() < 0.018
        row['metadata_timestamp_contradiction'] = random.random() < 0.026

    row['unicode_substitution_detected'] = False

    # Baseline coherence signals
    row['income_cross_doc_variance_pct'] = round(random.triangular(0.0, 18.0, 3.2), 4)
    row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.triangular(0.0, 22.0, 3.6), 4)
    if is_salaried_emp:
        row['form16_vs_salary_slip_discrepancy_pct'] = round(random.triangular(0.0, 14.0, 2.6), 4)
    else:
        row['form16_vs_salary_slip_discrepancy_pct'] = None
        
    if has_land_record and row['sale_deed_consideration_value'] is not None:
        row['property_valuation_discrepancy_pct'] = round(random.triangular(0.0, 18.0, 0.0), 4)
    else:
        row['property_valuation_discrepancy_pct'] = None
        
    row['encumbrance_suppression_flag'] = False
    row['double_pledge_risk_score'] = round(random.triangular(0.0, 0.67, 0.06), 4)
    row['employment_tan_mismatch'] = False

    # Apply fraud signal overrides
    if label == 1:
        row['pdf_structural_anomaly_score'] = round(random.triangular(0.35, 0.998, max(0.35, min(0.998, 0.59 + fraud_calibrator))), 4)
        row['frequency_domain_anomaly_score'] = round(random.triangular(0.35, 0.99, max(0.35, min(0.99, 0.55 + fraud_calibrator))), 4)
        row['font_inconsistency_score'] = round(random.triangular(0.35, 0.96, max(0.35, min(0.96, 0.58 + fraud_calibrator))), 4)
        row['physical_scan_coherence_score'] = round(random.triangular(0.01, 0.70, max(0.01, min(0.70, 0.20 + fraud_coherence_calibrator))), 4) # Target around 0.27
        row['ai_generated_document_probability'] = round(random.triangular(0.05, 0.99, max(0.05, min(0.99, 0.20 + fraud_calibrator))), 4)
        row['pdf_metadata_modification_delay_days'] = int(random.uniform(0, 82))
        
        row['pixel_manipulation_detected'] = random.random() < 0.58
        row['cloned_region_detected'] = random.random() < 0.461
        row['metadata_timestamp_contradiction'] = random.random() < 0.58
        row['compression_anomaly_detected'] = random.random() < 0.264
        row['documents_flagged_count'] = random.randint(1, 8)
        
        row['income_cross_doc_variance_pct'] = round(random.triangular(5.0, 20.0, 10.0), 4)
        row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.triangular(0.0, 20.0, 8.0), 4)
        if is_salaried_emp:
            row['form16_vs_salary_slip_discrepancy_pct'] = round(random.triangular(0.0, 15.0, 6.0), 4)
        if has_land_record:
            row['property_valuation_discrepancy_pct'] = round(random.triangular(0.0, 18.0, 4.0), 4)
            
        row['double_pledge_risk_score'] = round(random.triangular(0.15, 0.40, 0.25), 4)

        # Apply specific fraud sub-type rules
        if fraud_sub_type == "ITR_Income_Inflation":
            row['itr_declared_income'] = int(row['bank_statement_annual_credits_inr'] * random.uniform(1.30, 3.50))
            row['income_cross_doc_variance_pct'] = round(random.uniform(30.0, 250.0), 4)
            row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.uniform(30.0, 250.0), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.45, 0.90), 4)
            row['metadata_timestamp_contradiction'] = random.random() < 0.70
            row['pixel_manipulation_detected'] = random.random() < 0.55
            row['compression_anomaly_detected'] = random.random() < 0.50
            row['font_inconsistency_score'] = round(random.uniform(0.40, 0.75), 4)
            row['documents_flagged_count'] = random.randint(2, 5)

        elif fraud_sub_type == "AI_Generated_Document":
            row['ai_generated_document_probability'] = round(random.uniform(0.75, 0.988), 4)
            row['frequency_domain_anomaly_score'] = round(random.uniform(0.60, 0.988), 4)
            row['physical_scan_coherence_score'] = round(random.uniform(0.007, 0.350), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.50, 0.90), 4)
            row['metadata_timestamp_contradiction'] = random.random() < 0.80
            row['pixel_manipulation_detected'] = False
            row['cloned_region_detected'] = False
            row['compression_anomaly_detected'] = False
            row['documents_flagged_count'] = random.randint(1, 3)

        elif fraud_sub_type == "Bank_Statement_Manipulation":
            row['bank_statement_unusual_credits_count'] = random.randint(5, 15)
            row['bank_statement_round_number_flag'] = random.random() < 0.70
            row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.uniform(30.0, 250.0), 4)
            row['income_cross_doc_variance_pct'] = round(random.uniform(25.1, 200.0), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.45, 0.90), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.60
            row['compression_anomaly_detected'] = random.random() < 0.55
            row['frequency_domain_anomaly_score'] = round(random.uniform(0.45, 0.85), 4)
            row['documents_flagged_count'] = random.randint(2, 6)

        elif fraud_sub_type == "Encumbrance_Suppression":
            row['ec_liens_count'] = 0
            row['encumbrance_suppression_flag'] = True
            row['double_pledge_risk_score'] = round(random.uniform(0.50, 0.986), 4)
            row['cloned_region_detected'] = random.random() < 0.40
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.40, 0.80), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.50
            row['documents_flagged_count'] = random.randint(2, 5)

        elif fraud_sub_type == "Survey_Number_Substitution":
            row['land_record_survey_no'] = f"{random.randint(100, 999)}/ALT-{random.choice(['X', 'Y', 'Z'])}"
            row['pixel_manipulation_detected'] = random.random() < 0.70
            row['font_inconsistency_score'] = round(random.uniform(0.45, 0.85), 4)
            row['cloned_region_detected'] = random.random() < 0.35
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.40, 0.78), 4)
            row['compression_anomaly_detected'] = random.random() < 0.45
            row['documents_flagged_count'] = random.randint(1, 4)

        elif fraud_sub_type == "Salary_Slip_Manipulation":
            if row['form_16_gross_salary'] is not None:
                row['salary_slip_gross_monthly_inr'] = int(row['form_16_gross_salary'] / 12 * random.uniform(1.25, 2.20))
            else:
                row['salary_slip_gross_monthly_inr'] = int(row['declared_income_annual_inr'] / 12 * random.uniform(1.25, 2.20))
            row['form16_vs_salary_slip_discrepancy_pct'] = round(random.uniform(25.0, 250.0), 4)
            row['font_inconsistency_score'] = round(random.uniform(0.45, 0.85), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.65
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.42, 0.88), 4)
            row['compression_anomaly_detected'] = random.random() < 0.50
            row['documents_flagged_count'] = random.randint(1, 4)
            row['income_cross_doc_variance_pct'] = round(random.uniform(25.1, 200.0), 4)

        elif fraud_sub_type == "Property_Valuation_Inflation":
            if row['ec_registered_value'] is not None:
                row['sale_deed_consideration_value'] = int(row['ec_registered_value'] * random.uniform(1.30, 2.50))
            else:
                row['sale_deed_consideration_value'] = int(row['loan_amount_inr'] / random.uniform(0.3, 0.5))
            row['property_valuation_discrepancy_pct'] = round(random.uniform(30.0, 432.0), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.55
            row['font_inconsistency_score'] = round(random.uniform(0.40, 0.78), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.40, 0.82), 4)
            row['compression_anomaly_detected'] = random.random() < 0.45
            row['documents_flagged_count'] = random.randint(1, 4)

        elif fraud_sub_type == "GST_Turnover_Manipulation":
            row['gst_annual_turnover'] = int(row['bank_statement_annual_credits_inr'] * random.uniform(1.40, 3.00))
            row['gst_cross_month_inconsistency'] = random.random() < 0.80
            row['income_cross_doc_variance_pct'] = round(random.uniform(30.0, 200.0), 4)
            row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.uniform(20.0, 150.0), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.40, 0.80), 4)
            row['documents_flagged_count'] = random.randint(2, 5)

        elif fraud_sub_type == "Form16_Income_Inflation":
            row['form_16_gross_salary'] = int(row['bank_statement_annual_credits_inr'] * random.uniform(1.20, 2.50))
            row['form16_vs_salary_slip_discrepancy_pct'] = round(random.uniform(20.0, 250.0), 4)
            row['employment_tan_mismatch'] = random.random() < 0.40
            if row['employment_tan_mismatch']:
                row['salary_slip_employer_tan'] = generate_tan()
            row['metadata_timestamp_contradiction'] = random.random() < 0.60
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.42, 0.88), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.55
            row['documents_flagged_count'] = random.randint(1, 4)
            row['income_cross_doc_variance_pct'] = round(random.uniform(25.1, 200.0), 4)

        elif fraud_sub_type == "Double_Pledging":
            row['double_pledge_risk_score'] = round(random.uniform(0.65, 0.986), 4)
            row['encumbrance_suppression_flag'] = random.random() < 0.70
            row['ec_liens_count'] = 0
            row['documents_flagged_count'] = random.randint(1, 4)

        elif fraud_sub_type == "Fabricated_Employment":
            row['employment_tan_mismatch'] = True
            row['form_16_employer_tan'] = "MUMB99999Z"
            row['salary_slip_employer_tan'] = generate_tan()
            row['income_cross_doc_variance_pct'] = round(random.triangular(5.0, 18.0, 10.0), 4)
            row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.triangular(5.0, 20.0, 12.0), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.30, 0.60), 4)
            row['documents_flagged_count'] = random.randint(1, 3)

        elif fraud_sub_type == "Balance_Sheet_Fabrication":
            row['income_cross_doc_variance_pct'] = round(random.uniform(40.0, 250.0), 4)
            row['itr_vs_bank_stmt_discrepancy_pct'] = round(random.uniform(30.0, 200.0), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.50, 0.90), 4)
            row['metadata_timestamp_contradiction'] = random.random() < 0.75
            row['ai_generated_document_probability'] = round(random.uniform(0.20, 0.45), 4)
            row['documents_flagged_count'] = random.randint(2, 6)

        elif fraud_sub_type == "Ownership_Chain_Manipulation":
            row['mutation_date_manipulated'] = True
            row['cloned_region_detected'] = random.random() < 0.50
            row['font_inconsistency_score'] = round(random.uniform(0.40, 0.78), 4)
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.42, 0.82), 4)
            if row['ec_registered_value'] is not None:
                row['sale_deed_consideration_value'] = int(row['ec_registered_value'] * random.uniform(0.95, 1.05))
            row['documents_flagged_count'] = random.randint(2, 5)

        elif fraud_sub_type == "Cultivator_Name_Substitution":
            row['land_record_owner_name'] = get_indian_name(state)
            while row['land_record_owner_name'] == row['borrower_name']:
                row['land_record_owner_name'] = get_indian_name(state)
            row['pixel_manipulation_detected'] = random.random() < 0.70
            row['cloned_region_detected'] = random.random() < 0.40
            row['font_inconsistency_score'] = round(random.uniform(0.45, 0.85), 4)
            row['compression_anomaly_detected'] = random.random() < 0.50
            row['documents_flagged_count'] = random.randint(1, 4)

        elif fraud_sub_type == "NACH_Mandate_Manipulation":
            row['nach_mandate_alteration_detected'] = True
            row['font_inconsistency_score'] = round(random.uniform(0.35, 0.70), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.50
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.35, 0.72), 4)
            row['documents_flagged_count'] = random.randint(1, 3)

        elif fraud_sub_type == "Cross_Pledging_Director":
            row['double_pledge_risk_score'] = round(random.uniform(0.55, 0.90), 4)
            row['guarantor_overcommitment_detected'] = True
            if row['guarantor_name'] is None:
                row['guarantor_name'] = get_indian_name(state)
                row['guarantor_overcommitment_detected'] = True
            row['documents_flagged_count'] = random.randint(1, 3)

        elif fraud_sub_type == "Mutation_Date_Manipulation":
            row['mutation_date_manipulated'] = True
            row['metadata_timestamp_contradiction'] = random.random() < 0.80
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.45, 0.82), 4)
            row['cloned_region_detected'] = random.random() < 0.35
            row['documents_flagged_count'] = random.randint(1, 4)

        elif fraud_sub_type == "Guarantor_Overcommitment":
            if row['guarantor_name'] is None:
                row['guarantor_name'] = get_indian_name(state)
            row['guarantor_overcommitment_detected'] = True
            row['double_pledge_risk_score'] = round(random.uniform(0.30, 0.65), 4)
            # Reset forensics to clean distributions
            row['pdf_structural_anomaly_score'] = round(random.triangular(0.001, 0.75, 0.14), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.026
            row['cloned_region_detected'] = random.random() < 0.018
            row['frequency_domain_anomaly_score'] = round(random.triangular(0.0, 0.82, 0.14), 4)
            row['font_inconsistency_score'] = round(random.triangular(0.0, 0.82, 0.15), 4)
            row['physical_scan_coherence_score'] = round(random.triangular(0.5, 0.999, 0.92), 4)
            row['metadata_timestamp_contradiction'] = random.random() < 0.026
            row['ai_generated_document_probability'] = round(random.triangular(0.010, 0.52, 0.05), 4)
            row['compression_anomaly_detected'] = False
            row['documents_flagged_count'] = random.choice([0, 1])

        elif fraud_sub_type == "Identity_Document_Fraud":
            row['unicode_substitution_detected'] = random.random() < 0.60
            row['font_inconsistency_score'] = round(random.uniform(0.50, 0.85), 4)
            row['pixel_manipulation_detected'] = random.random() < 0.55
            row['pdf_structural_anomaly_score'] = round(random.uniform(0.42, 0.80), 4)
            row['income_cross_doc_variance_pct'] = round(random.uniform(5.0, 18.0), 4)
            row['documents_flagged_count'] = random.randint(1, 3)

    # Derived scoring and decision logic
    score = compute_risk_score(row)
    
    if label == 0:
        score = min(39, score)
    else:
        # Boost/calibrate score to ensure at least 90% of fraud rows are >= 20
        # and mean is in 45-55
        if score < 20:
            # Set flags progressively to guarantee score >= 20 in formula
            row['pixel_manipulation_detected'] = True
            score = compute_risk_score(row)
            if score < 20:
                row['metadata_timestamp_contradiction'] = True
                score = compute_risk_score(row)
        score = min(85, score)
        
    row['overall_fraud_risk_score'] = score
    row['fraud_risk_category'] = risk_category(score)
    row['manual_review_triggered'] = row['fraud_risk_category'] in ('Medium_Risk', 'High_Risk')
    
    # Decisions
    row['ground_truth_fraud_label'] = label
    row['fraud_sub_type'] = fraud_sub_type
    
    if label == 0:
        row['adverse_action_triggered'] = False
        row['final_decision'] = 'Approved'
    else:
        # Fraud: Approved 30.6% (false negatives), Manual_Review 58.6%, Rejected 10.8%
        fraud_roll = random.random()
        if fraud_roll < 0.108:
            row['final_decision'] = 'Rejected'
            row['adverse_action_triggered'] = True
        elif fraud_roll < 0.108 + 0.586:
            row['final_decision'] = 'Manual_Review'
            row['adverse_action_triggered'] = False
        else:
            row['final_decision'] = 'Approved' # False negative
            row['adverse_action_triggered'] = False
            
    row['processing_time_ms'] = processing_time(row['fraud_risk_category'])
    
    # Narrative and compliance
    row['adverse_action_reason'] = format_adverse_reason(row)
    row['rbi_fpc_compliant'] = (row['adverse_action_reason'] is not None) and (row['adverse_action_triggered'])
    row['audit_log_hash'] = hashlib.sha256(f"{app_id}{label}{score}".encode()).hexdigest()[:12]

    return row

def generate_dataset_file(filename, total_rows, target_fraud, year_counters=None):
    print(f"\nGenerating {filename} (Rows: {total_rows}, Fraud: {target_fraud})...")
    sub_type_counts = get_sub_type_counts(target_fraud)
    
    # Skeleton list of (label, sub_type)
    skeleton = []
    # Add fraud rows
    for st, count in sub_type_counts.items():
        for _ in range(count):
            skeleton.append((1, st))
            
    # Add clean rows
    clean_count = total_rows - target_fraud
    for _ in range(clean_count):
        skeleton.append((0, "Clean"))
        
    random.shuffle(skeleton)
    
    # Calibrator variables (feedback loop)
    clean_calibrator = 0.0
    fraud_calibrator = 0.0
    clean_coherence_calibrator = 0.0
    fraud_coherence_calibrator = 0.0
    
    accumulators = {
        'pixel_acc': 0.0,
        'clone_acc': 0.0,
        'timestamp_acc': 0.0,
        'round_num_acc': 0.0
    }
    
    records = []
    
    # Counters for running averages
    clean_score_sum = 0
    clean_score_count = 0
    fraud_score_sum = 0
    fraud_score_count = 0
    
    fraud_coherence_sum = 0.0
    fraud_coherence_count = 0
    clean_coherence_sum = 0.0
    clean_coherence_count = 0

    # Year counter for unique application_id sequence
    if year_counters is None:
        year_counters = {2022: 1, 2023: 1, 2024: 1, 2025: 1, 2026: 1}

    for idx, (label, sub_type) in enumerate(skeleton):
        year = random.choice([2022, 2023, 2024, 2025, 2026])
        seq_num = year_counters[year]
        year_counters[year] += 1
        app_id = f"SRS-{year}-{seq_num:06d}"
        
        # Adjust calibrations based on running scores
        if label == 0:
            if clean_score_count > 0:
                clean_avg = clean_score_sum / clean_score_count
                error = 10.0 - clean_avg # Target clean mean is 10.0
                clean_calibrator = max(-0.15, min(0.15, error * 0.05))
                
            if clean_coherence_count > 0:
                clean_coh_avg = clean_coherence_sum / clean_coherence_count
                coh_error = 0.825 - clean_coh_avg # Target clean coherence is 0.825
                clean_coherence_calibrator = max(-0.10, min(0.10, coh_error * 0.10))
        else:
            if fraud_score_count > 0:
                fraud_avg = fraud_score_sum / fraud_score_count
                error = 50.0 - fraud_avg # Target fraud mean is 50.0
                fraud_calibrator = max(-0.25, min(0.25, error * 0.08))
                
            if fraud_coherence_count > 0:
                fraud_coh_avg = fraud_coherence_sum / fraud_coherence_count
                coh_error = 0.30 - fraud_coh_avg # Target fraud coherence is 0.30
                fraud_coherence_calibrator = max(-0.15, min(0.15, coh_error * 0.40))

        row = generate_row(
            app_id=app_id,
            label=label,
            fraud_sub_type=sub_type,
            clean_calibrator=clean_calibrator,
            fraud_calibrator=fraud_calibrator,
            clean_coherence_calibrator=clean_coherence_calibrator,
            fraud_coherence_calibrator=fraud_coherence_calibrator,
            accumulators=accumulators
        )
        records.append(row)
        
        # Update running tallies
        if label == 0:
            clean_score_sum += row['overall_fraud_risk_score']
            clean_score_count += 1
            clean_coherence_sum += row['physical_scan_coherence_score']
            clean_coherence_count += 1
        else:
            fraud_score_sum += row['overall_fraud_risk_score']
            fraud_score_count += 1
            fraud_coherence_sum += row['physical_scan_coherence_score']
            fraud_coherence_count += 1

    # Run validation pipeline
    run_validations(records, filename)
    
    # Save CSV
    filepath = os.path.join(workspace_dir, filename)
    fieldnames = [
        "application_id", "submission_date", "itr_assessment_year", "state", "lender_type", "loan_type",
        "employment_type", "application_channel", "document_bundle_size", "cibil_score", "loan_amount_inr",
        "land_record_document_type", "land_record_state", "land_record_survey_no", "land_record_owner_name",
        "sale_deed_consideration_value", "ec_registered_value", "ec_liens_count", "mutation_date_manipulated",
        "borrower_name", "declared_income_annual_inr", "itr_declared_income", "itr_acknowledgement_no",
        "form_16_gross_salary", "form_16_employer_tan", "salary_slip_gross_monthly_inr", "salary_slip_employer_name",
        "salary_slip_employer_tan", "bank_statement_annual_credits_inr", "bank_statement_unusual_credits_count",
        "bank_statement_round_number_flag", "gst_annual_turnover", "gst_registration_number", "gst_cross_month_inconsistency",
        "nach_mandate_beneficiary_name", "nach_mandate_amount_inr", "nach_mandate_alteration_detected", "guarantor_name",
        "guarantor_overcommitment_detected", "pdf_structural_anomaly_score", "pixel_manipulation_detected",
        "cloned_region_detected", "frequency_domain_anomaly_score", "font_inconsistency_score",
        "physical_scan_coherence_score", "metadata_timestamp_contradiction", "unicode_substitution_detected",
        "ai_generated_document_probability", "compression_anomaly_detected", "documents_flagged_count",
        "pdf_metadata_modification_delay_days", "income_cross_doc_variance_pct", "itr_vs_bank_stmt_discrepancy_pct",
        "form16_vs_salary_slip_discrepancy_pct", "property_valuation_discrepancy_pct", "encumbrance_suppression_flag",
        "double_pledge_risk_score", "employment_tan_mismatch", "overall_fraud_risk_score", "fraud_risk_category",
        "manual_review_triggered", "adverse_action_triggered", "final_decision", "processing_time_ms",
        "ground_truth_fraud_label", "fraud_sub_type", "document_primary_language", "adverse_action_reason",
        "rbi_fpc_compliant", "audit_log_hash"
    ]
    
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {total_rows} records to {filepath}")
    return records

def generate_splits_and_combined(train_rows, val_rows, test_rows):
    master_counters = {2022: 1, 2023: 1, 2024: 1, 2025: 1, 2026: 1}
    train_records = generate_dataset_file("suraksha_sentinel_train.csv", train_rows, int(train_rows * 0.14), master_counters)
    val_records = generate_dataset_file("suraksha_sentinel_val.csv", val_rows, int(val_rows * 0.14), master_counters)
    test_records = generate_dataset_file("suraksha_sentinel_test.csv", test_rows, int(test_rows * 0.14), master_counters)
    
    # Combine them for the 70k master
    master_records = train_records + val_records + test_records
    
    # Save combined master file
    filepath = os.path.join(workspace_dir, "suraksha_sentinel_master_70k.csv")
    fieldnames = list(master_records[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(master_records)
    print(f"Combined split records: Saved {len(master_records)} total records to {filepath}")
    
    # Validate combined master file
    run_validations(master_records, "suraksha_sentinel_master_70k.csv")

def run_validations(records, split_name=""):
    print(f"\n--- Running validations for {split_name} (Total rows: {len(records)}) ---")
    
    # 1. No duplicate application_id values
    ids = [r['application_id'] for r in records]
    assert len(ids) == len(set(ids)), "Duplicate application_id found!"
    
    # 2. submission_date parses as DD-MM-YYYY between 01-01-2022 and 17-06-2026
    start_d = datetime(2022, 1, 1)
    end_d = datetime(2026, 6, 17)
    for r in records:
        dt = datetime.strptime(r['submission_date'], "%d-%m-%Y")
        assert start_d <= dt <= end_d, f"submission_date out of range: {r['submission_date']}"
        
        # 3. ITR Assessment Year constraint
        if r['itr_assessment_year'] is not None:
            ay_year = int(r['itr_assessment_year'][2:6]) # e.g. 2021 from FY2021-22
            assert dt.year - ay_year <= 3, f"itr_assessment_year {r['itr_assessment_year']} too old for submission_date {r['submission_date']}"

        # 4. land_record_state equals state
        if r['land_record_state'] is not None:
            assert r['land_record_state'] == r['state'], f"State mismatch: {r['land_record_state']} vs {r['state']}"
            
        # 5. land_record_document_type null check
        if r['loan_type'] == "Retail_Salaried":
            assert r['land_record_document_type'] is None, f"Land record present for Retail: {r['land_record_document_type']}"
            
        # 6. form_16_employer_tan and salary_slip_employer_tan are null for all non-salaried
        is_salaried = r['employment_type'] in ("Salaried_Private_Sector", "Salaried_Govt", "Salaried_MNC", "Salaried_PSU")
        if not is_salaried:
            assert r['form_16_employer_tan'] is None, f"form_16_employer_tan not null for non-salaried: {r['employment_type']}"
            assert r['salary_slip_employer_tan'] is None, f"salary_slip_employer_tan not null for non-salaried: {r['employment_type']}"
            
        # 7. gst_annual_turnover and gst_registration_number null check
        is_business = r['employment_type'] in ("Self_Employed_Professional", "Proprietor", "Partnership_Firm", "Private_Ltd_Director")
        if not is_business:
            assert r['gst_annual_turnover'] is None, f"gst_annual_turnover not null for non-business: {r['employment_type']}"
            assert r['gst_registration_number'] is None, f"gst_registration_number not null for non-business: {r['employment_type']}"
            
        # 8. nach_mandate_alteration_detected is null for all rows with null nach_mandate_beneficiary_name
        if r['nach_mandate_beneficiary_name'] is None:
            assert r['nach_mandate_alteration_detected'] is None, f"nach_mandate_alteration_detected not null for null beneficiary"
            
        # 9. mutation_date_manipulated is null for all rows with null land_record_document_type
        if r['land_record_document_type'] is None:
            assert r['mutation_date_manipulated'] is None, f"mutation_date_manipulated not null for null land record"

        # Label consistency checks
        if r['ground_truth_fraud_label'] == 0:
            assert r['overall_fraud_risk_score'] <= 39, f"Clean row with risk score > 39: {r['overall_fraud_risk_score']}"
            assert r['adverse_action_triggered'] is False, f"Clean row with adverse action triggered"
            assert r['final_decision'] == "Approved", f"Clean row final decision is not Approved: {r['final_decision']}"
            
        # fraud_risk_category check
        score = r['overall_fraud_risk_score']
        cat = r['fraud_risk_category']
        if score <= 35:
            assert cat == 'Clean', f"Category mismatch for score {score}: {cat}"
        elif score <= 55:
            assert cat == 'Low_Risk', f"Category mismatch for score {score}: {cat}"
        elif score <= 75:
            assert cat == 'Medium_Risk', f"Category mismatch for score {score}: {cat}"
        else:
            assert cat == 'High_Risk', f"Category mismatch for score {score}: {cat}"
            
        if cat == 'Clean':
            assert r['manual_review_triggered'] is False, f"Clean category row with manual_review_triggered True"
            
        if r['adverse_action_triggered']:
            assert r['adverse_action_reason'] is not None, f"adverse_action_triggered is True but reason is null"
            assert r['rbi_fpc_compliant'] is True, f"adverse_action_triggered but rbi_fpc_compliant not True"
        else:
            assert r['adverse_action_reason'] is None or r['adverse_action_reason'] == "", f"adverse_action_triggered is False but reason is present"

        # Fraud sub-type checks
        st = r['fraud_sub_type']
        if st == 'AI_Generated_Document':
            assert r['ai_generated_document_probability'] >= 0.75, f"AI generated doc probability too low: {r['ai_generated_document_probability']}"
            assert r['physical_scan_coherence_score'] <= 0.35, f"AI generated doc physical scan coherence too high: {r['physical_scan_coherence_score']}"
            assert r['pixel_manipulation_detected'] is False, f"AI generated doc pixel manipulation is True"
        elif st == 'Encumbrance_Suppression':
            assert r['encumbrance_suppression_flag'] is True, f"Encumbrance suppression flag is False"
            assert r['ec_liens_count'] == 0, f"Encumbrance suppression with ec_liens_count != 0: {r['ec_liens_count']}"
        elif st == 'Fabricated_Employment':
            assert r['employment_tan_mismatch'] is True, f"Fabricated employment TAN mismatch is False"
            assert r['form_16_employer_tan'] != r['salary_slip_employer_tan'], f"Fabricated employment TANs match"
        elif st == 'NACH_Mandate_Manipulation':
            assert r['nach_mandate_alteration_detected'] is True, f"NACH mandate alteration detected is False"
        elif st == 'Mutation_Date_Manipulation':
            assert r['mutation_date_manipulated'] is True, f"Mutation date manipulated is False"
        elif st == 'Guarantor_Overcommitment':
            assert r['guarantor_overcommitment_detected'] is True, f"Guarantor overcommitment detected is False"
        elif st == 'Double_Pledging':
            assert r['double_pledge_risk_score'] >= 0.65, f"Double pledge risk score too low: {r['double_pledge_risk_score']}"
        elif st in ('ITR_Income_Inflation', 'Bank_Statement_Manipulation', 'GST_Turnover_Manipulation', 'Balance_Sheet_Fabrication', 'Form16_Income_Inflation', 'Salary_Slip_Manipulation'):
            assert r['income_cross_doc_variance_pct'] > 25, f"Income manipulation sub-type {st} has cross doc variance <= 25: {r['income_cross_doc_variance_pct']}"
        elif st == 'Cultivator_Name_Substitution':
            assert r['land_record_owner_name'] != r['borrower_name'], f"Cultivator name substitution: owner matches borrower"
            
    # Aggregate checks
    fraud_rows = [r for r in records if r['ground_truth_fraud_label'] == 1]
    clean_rows = [r for r in records if r['ground_truth_fraud_label'] == 0]
    
    if len(fraud_rows) > 0:
        overall_fraud_score_ge_20 = len([r for r in fraud_rows if r['overall_fraud_risk_score'] >= 20]) / len(fraud_rows)
        assert overall_fraud_score_ge_20 >= 0.90, f"Less than 90% of fraud rows have risk score >= 20: {overall_fraud_score_ge_20:.2%}"
        
        fraud_mean_score = sum(r['overall_fraud_risk_score'] for r in fraud_rows) / len(fraud_rows)
        print(f"Fraud Mean Risk Score: {fraud_mean_score:.2f} (Target: 45-55)")
        assert 44.5 <= fraud_mean_score <= 55.5, f"Fraud Mean Risk Score {fraud_mean_score:.2f} out of range 45-55"
        
        fraud_pixel_detected_rate = len([r for r in fraud_rows if r['pixel_manipulation_detected']]) / len(fraud_rows)
        print(f"Fraud Pixel Manipulation Rate: {fraud_pixel_detected_rate:.2%} (Target: 50-65%)")
        assert 0.495 <= fraud_pixel_detected_rate <= 0.655, f"Fraud Pixel Manipulation Rate {fraud_pixel_detected_rate:.2%} out of range 50-65%"
        
        fraud_scan_coherence_mean = sum(r['physical_scan_coherence_score'] for r in fraud_rows) / len(fraud_rows)
        print(f"Fraud Physical Scan Coherence Mean: {fraud_scan_coherence_mean:.2f} (Target: 0.25-0.35)")
        assert 0.245 <= fraud_scan_coherence_mean <= 0.355, f"Fraud Physical Scan Coherence Mean {fraud_scan_coherence_mean:.2f} out of range 0.25-0.35"

    if len(clean_rows) > 0:
        clean_mean_score = sum(r['overall_fraud_risk_score'] for r in clean_rows) / len(clean_rows)
        print(f"Clean Mean Risk Score: {clean_mean_score:.2f} (Target: 8-12)")
        assert 7.5 <= clean_mean_score <= 12.5, f"Clean Mean Risk Score {clean_mean_score:.2f} out of range 8-12"
        
        clean_pixel_detected_rate = len([r for r in clean_rows if r['pixel_manipulation_detected']]) / len(clean_rows)
        print(f"Clean Pixel Manipulation Rate: {clean_pixel_detected_rate:.2%} (Target: 2-4%)")
        assert 0.019 <= clean_pixel_detected_rate <= 0.041, f"Clean Pixel Manipulation Rate {clean_pixel_detected_rate:.2%} out of range 2-4%"
        
        clean_scan_coherence_mean = sum(r['physical_scan_coherence_score'] for r in clean_rows) / len(clean_rows)
        print(f"Clean Physical Scan Coherence Mean: {clean_scan_coherence_mean:.2f} (Target: 0.80-0.85)")
        assert 0.795 <= clean_scan_coherence_mean <= 0.855, f"Clean Physical Scan Coherence Mean {clean_scan_coherence_mean:.2f} out of range 0.80-0.85"
        
        clean_max_income_var = max(r['income_cross_doc_variance_pct'] for r in clean_rows)
        assert clean_max_income_var <= 22, f"Clean row income cross doc variance > 22: {clean_max_income_var}"

    print("All checklist assertions passed successfully!")

def main():
    # 1. 5k version (4300 clean, 700 fraud)
    generate_dataset_file("suraksha_sentinel_5k.csv", 5000, 700)
    
    # 2. 15k version (12900 clean, 2100 fraud)
    generate_dataset_file("suraksha_sentinel_15k.csv", 15000, 2100)
    
    # 3. 30k version (25800 clean, 4200 fraud)
    generate_dataset_file("suraksha_sentinel_30k.csv", 30000, 4200)
    
    # 4. 70k Master version and splits (Train 50k, Val 10k, Test 10k)
    generate_splits_and_combined(50000, 10000, 10000)

if __name__ == "__main__":
    main()
