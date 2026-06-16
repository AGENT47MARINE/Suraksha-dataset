import csv
import os
import random
import string

# Output path
workspace_dir = r"C:\Users\yagye\OneDrive\Desktop\Suraksha Dataset"
output_path = os.path.join(workspace_dir, "suraksha_sentinel_dataset.csv")

# Ensure workspace exists
os.makedirs(workspace_dir, exist_ok=True)

# Seed for reproducibility
random.seed(42)

# Helper lists for synthetic data generation
first_names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Mohammad", 
    "Krishna", "Rahul", "Ramesh", "Suresh", "Amit", "Anil", "Rajesh", "Sanjay", 
    "Vijay", "Sunil", "Kaushik", "Deepak", "Sandeep", "Yagyesh", "Vikram", "Karan",
    "Priya", "Ananya", "Diya", "Aaradhya", "Fatima", "Pooja", "Neha", "Ritu", 
    "Sunita", "Geeta", "Meena", "Kiran", "Shalini", "Divya", "Kavitha", "Swati"
]

last_names = [
    "Sharma", "Verma", "Gupta", "Patel", "Mehta", "Singh", "Kumar", "Rao", 
    "Reddy", "Nair", "Joshi", "Kulkarni", "Patil", "Deshmukh", "Banerjee", 
    "Chatterjee", "Khan", "Mishra", "Prasad", "Yadav", "Gowda", "Naidu", 
    "Choudhury", "Bose", "Dutta", "Bhalerao", "Pillai", "Menon"
]

employers = [
    "Tata Consultancy Services", "Infosys Limited", "Wipro Technologies", 
    "Reliance Industries", "HDFC Bank Ltd", "ICICI Bank", "Larsen & Toubro", 
    "Tech Mahindra", "State Bank of India", "Aditya Birla Group", 
    "Godrej Industries", "Mahindra & Mahindra", "HCL Technologies"
]

languages = ["English", "Hindi", "Marathi", "Tamil", "Bengali", "Telugu", "Kannada", "Malayalam", "Gujarati"]

def generate_tan():
    # Format: 4 letters, 5 digits, 1 letter (e.g. MUMB12345A)
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=5))
    chk = random.choice(string.ascii_uppercase)
    return f"{letters}{digits}{chk}"

def generate_gstin():
    # Format: 2 digits, 10 char PAN, 1 digit, 1 letter, 1 digit (e.g. 27AAACR1234A1Z5)
    state = ''.join(random.choices(string.digits, k=2))
    pan_letters = ''.join(random.choices(string.ascii_uppercase, k=5))
    pan_digits = ''.join(random.choices(string.digits, k=4))
    pan_end = random.choice(string.ascii_uppercase)
    end = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{state}{pan_letters}{pan_digits}{pan_end}{end}"

def generate_ack():
    # 15 digit number
    return ''.join(random.choices(string.digits, k=15))

def generate_survey_no():
    # Survey number format (e.g. 142/3A or 89/B)
    num = random.randint(10, 999)
    sub = random.randint(1, 12)
    part = random.choice(["", "A", "B", "C", "D"])
    return f"{num}/{sub}{part}"

def generate_dataset(num_records=1200):
    fieldnames = [
        "application_id", "lending_segment", "borrower_name", "declared_income_annual",
        "itr_declared_income", "itr_acknowledgement_no", "form_16_gross_salary",
        "form_16_employer_tan", "salary_slip_gross_salary_monthly", "salary_slip_employer_name",
        "bank_statement_annual_credits", "bank_statement_unusual_credits",
        "gst_annual_turnover", "gst_registration_number", "gst_turnover_inconsistency_detected",
        "nach_mandate_beneficiary_name", "nach_mandate_authorized_amount", "nach_mandate_alteration_detected",
        "land_record_type", "land_record_survey_no", "land_record_owner_name", 
        "sale_deed_consideration_value", "ec_registered_value", "ec_liens_count", 
        "pdf_metadata_modification_delay_days", "compression_anomaly_detected", 
        "cloned_signature_detected", "font_substitution_detected", "physical_coherence_anomaly_detected",
        "ai_generation_score", "double_pledge_detected", "guarantor_name", "guarantor_overcommitment_detected",
        "document_primary_language", "is_fraud", "fraud_pattern", "adverse_action_reason"
    ]

    records = []

    for i in range(num_records):
        app_id = f"APP{20260000 + i}"
        segment = random.choice(["Agricultural", "MSME", "Housing", "Retail"])
        borrower_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Base templates (Clean defaults)
        declared_income = 0
        itr_income = 0
        itr_ack = "None"
        form_16_salary = 0
        employer_tan = "None"
        salary_slip_monthly = 0
        slip_employer = "None"
        bank_credits = 0
        bank_unusual = 0
        
        gst_turnover = 0
        gstin = "None"
        gst_inconsistency = 0
        
        nach_beneficiary = "None"
        nach_amount = 0
        nach_alteration = 0
        
        land_type = "None"
        survey_no = "None"
        land_owner = "None"
        sale_deed_val = 0
        ec_val = 0
        ec_liens = 0
        
        delay_days = random.randint(0, 3)
        compression_anomaly = 0
        cloned_signature = 0
        font_sub = 0
        physical_coherence_anomaly = 0
        ai_score = round(random.uniform(0.01, 0.15), 4)
        double_pledge = 0
        
        guarantor = "None"
        guarantor_overcommitment = 0
        doc_lang = "English"
        
        is_fraud = 0
        fraud_pattern = "clean"
        adverse_reason = "Application cleared all automated document checks."

        # Assign document sets based on segment
        if segment == "Retail":
            base_sal = random.randint(25000, 150000)
            salary_slip_monthly = base_sal
            form_16_salary = base_sal * 12
            itr_income = form_16_salary + random.randint(0, 30000)
            declared_income = itr_income
            itr_ack = generate_ack()
            employer_tan = generate_tan()
            slip_employer = random.choice(employers)
            bank_credits = form_16_salary + random.randint(-15000, 15000)
            
            nach_beneficiary = "PolyOculus Finance"
            nach_amount = int((salary_slip_monthly * 0.4) + 1000)
            doc_lang = random.choice(["English", "Hindi"])
            
        elif segment == "MSME":
            base_business_income = random.randint(300000, 5000000)
            itr_income = base_business_income
            declared_income = itr_income
            itr_ack = generate_ack()
            bank_credits = base_business_income + random.randint(-50000, 50000)
            
            gst_turnover = int(base_business_income * random.uniform(1.2, 1.8))
            gstin = generate_gstin()
            guarantor = f"{random.choice(first_names)} {random.choice(last_names)}"
            doc_lang = "English"
            
        elif segment == "Agricultural":
            land_type = random.choice(["Patta", "7/12 Extract"])
            survey_no = generate_survey_no()
            land_owner = borrower_name
            base_agri_income = random.randint(150000, 1200000)
            declared_income = base_agri_income
            bank_credits = base_agri_income + random.randint(-20000, 20000)
            
            doc_lang = "Marathi" if land_type == "7/12 Extract" else "Tamil"
            
        elif segment == "Housing":
            base_sal = random.randint(50000, 250000)
            salary_slip_monthly = base_sal
            form_16_salary = base_sal * 12
            itr_income = form_16_salary
            declared_income = itr_income
            itr_ack = generate_ack()
            employer_tan = generate_tan()
            slip_employer = random.choice(employers)
            bank_credits = form_16_salary + random.randint(-10000, 10000)
            
            property_base = random.randint(2000000, 15000000)
            sale_deed_val = property_base
            ec_val = property_base
            ec_liens = 0
            land_type = "7/12 Extract"
            survey_no = generate_survey_no()
            land_owner = borrower_name
            guarantor = f"{random.choice(first_names)} {random.choice(last_names)}"
            doc_lang = random.choice(["English", "Hindi", "Marathi"])
            
            nach_beneficiary = "PolyOculus Finance"
            nach_amount = int((salary_slip_monthly * 0.5))

        # Roll to decide if this row is fraud
        # 15% fraud rate overall
        fraud_roll = random.random()
        if fraud_roll < 0.15:
            is_fraud = 1
            
            # Select appropriate fraud pattern based on segment
            if segment == "Retail":
                pattern = random.choice(["income_inflation", "fabricated_employment", "ai_generated_document", "nach_manipulation"])
                if pattern == "income_inflation":
                    fraud_pattern = "income_inflation"
                    salary_slip_monthly = salary_slip_monthly * 2
                    declared_income = salary_slip_monthly * 12
                    font_sub = 1
                    compression_anomaly = 1
                    adverse_reason = "Adverse Action Recommended: Semantic mismatch detected. Declared annual salary slips project ₹{:,} gross income, but bank statement salary credits annualized show only ₹{:,}.".format(int(salary_slip_monthly*12), int(bank_credits))
                
                elif pattern == "fabricated_employment":
                    fraud_pattern = "fabricated_employment"
                    employer_tan = "MUMB99999Z"  # Mock invalid/blacklisted TAN
                    slip_employer = "Shell Company Pvt Ltd"
                    adverse_reason = "Adverse Action Recommended: Fabricated employment suspected. The employer stated on salary slips does not match the active registry data for the provided TAN."
                
                elif pattern == "ai_generated_document":
                    fraud_pattern = "ai_generated_document"
                    ai_score = round(random.uniform(0.88, 0.99), 4)
                    compression_anomaly = 1
                    delay_days = random.randint(45, 90)
                    adverse_reason = "Adverse Action Recommended: AI-Generated Document detected. Salary slips exhibit statistical image frequency noise consistent with text-to-image generator engines."
                
                elif pattern == "nach_manipulation":
                    fraud_pattern = "nach_manipulation"
                    nach_beneficiary = "Third Party Collector"  # Altered beneficiary
                    nach_alteration = 1
                    cloned_signature = 1
                    adverse_reason = "Adverse Action Recommended: NACH mandate alteration detected. The beneficiary name stated in the mandate has been altered post-signature."

            elif segment == "MSME":
                pattern = random.choice(["income_inflation", "unusual_credits", "gst_manipulation", "guarantor_overcommitment"])
                if pattern == "income_inflation":
                    fraud_pattern = "income_inflation"
                    itr_income = itr_income * 3
                    declared_income = itr_income
                    font_sub = 1
                    delay_days = random.randint(15, 60)
                    adverse_reason = "Adverse Action Recommended: Income inflation detected. Extracted ITR-V filing reports ₹{:,} net taxable income, while verified bank ledger credits total only ₹{:,}.".format(int(itr_income), int(bank_credits))
                
                elif pattern == "unusual_credits":
                    fraud_pattern = "unusual_credits"
                    bank_unusual = 1
                    bank_credits = bank_credits * 1.5
                    adverse_reason = "Adverse Action Recommended: Circular trading and artificial balance padding detected. Bank statement logs reveal repetitive, round-number credits from related entities."
                
                elif pattern == "gst_manipulation":
                    fraud_pattern = "gst_manipulation"
                    gst_turnover = gst_turnover * 4
                    gst_inconsistency = 1
                    font_sub = 1
                    adverse_reason = "Adverse Action Recommended: GST turnover inconsistency. Declared GST annual turnover of ₹{:,} contradicts verified ITR receipts of ₹{:,}.".format(int(gst_turnover), int(itr_income))
                
                elif pattern == "guarantor_overcommitment":
                    fraud_pattern = "guarantor_overcommitment"
                    guarantor_overcommitment = 1
                    adverse_reason = "Adverse Action Recommended: Guarantor risk alert. Stated guarantor '{}' is co-committed in 3 other active commercial credit applications exceeding their aggregate net worth.".format(guarantor)

            elif segment == "Agricultural":
                pattern = random.choice(["survey_number_substitution", "cultivator_name_substitution", "double_pledging"])
                if pattern == "survey_number_substitution":
                    fraud_pattern = "survey_number_substitution"
                    survey_no = "999/99X"
                    compression_anomaly = 1
                    font_sub = 1
                    physical_coherence_anomaly = 1
                    adverse_reason = "Adverse Action Recommended: Survey number substitution detected. Pixel-level compression differences and physical alignment errors on the land record document indicate the survey field was altered."
                
                elif pattern == "cultivator_name_substitution":
                    fraud_pattern = "cultivator_name_substitution"
                    land_owner = borrower_name
                    compression_anomaly = 1
                    cloned_signature = 1
                    physical_coherence_anomaly = 1
                    adverse_reason = "Adverse Action Recommended: Cultivator name mismatch. The cultivator name stated in the submitted land record contains edited pixel blocks; registry records list a different landowner."
                
                elif pattern == "double_pledging":
                    fraud_pattern = "double_pledging"
                    double_pledge = 1
                    adverse_reason = "Adverse Action Recommended: Double-pledging detected. The survey number {} is currently pledged as active collateral in another live loan application.".format(survey_no)

            elif segment == "Housing":
                pattern = random.choice(["encumbrance_suppression", "valuation_inflation", "double_pledging"])
                if pattern == "encumbrance_suppression":
                    fraud_pattern = "encumbrance_suppression"
                    ec_liens = 0
                    cloned_signature = 1
                    delay_days = random.randint(20, 40)
                    adverse_reason = "Adverse Action Recommended: Encumbrance certificate manipulation. Submitted EC lists 0 active charges, but registry verification shows active mortgages registered against the property."
                
                elif pattern == "valuation_inflation":
                    fraud_pattern = "valuation_inflation"
                    sale_deed_val = sale_deed_val * 2.5
                    font_sub = 1
                    adverse_reason = "Adverse Action Recommended: Property valuation inflation detected. The consideration amount of ₹{:,} stated in the Sale Deed is significantly higher than the registered EC valuation of ₹{:,}.".format(int(sale_deed_val), int(ec_val))
                
                elif pattern == "double_pledging":
                    fraud_pattern = "double_pledging"
                    double_pledge = 1
                    adverse_reason = "Adverse Action Recommended: Asset double-pledging. This property identifier is already registered as security under another active housing loan."

        records.append({
            "application_id": app_id,
            "lending_segment": segment,
            "borrower_name": borrower_name,
            "declared_income_annual": int(declared_income),
            "itr_declared_income": int(itr_income),
            "itr_acknowledgement_no": itr_ack,
            "form_16_gross_salary": int(form_16_salary),
            "form_16_employer_tan": employer_tan,
            "salary_slip_gross_salary_monthly": int(salary_slip_monthly),
            "salary_slip_employer_name": slip_employer,
            "bank_statement_annual_credits": int(bank_credits),
            "bank_statement_unusual_credits": bank_unusual,
            "gst_annual_turnover": int(gst_turnover),
            "gst_registration_number": gstin,
            "gst_turnover_inconsistency_detected": gst_inconsistency,
            "nach_mandate_beneficiary_name": nach_beneficiary,
            "nach_mandate_authorized_amount": int(nach_amount),
            "nach_mandate_alteration_detected": nach_alteration,
            "land_record_type": land_type,
            "land_record_survey_no": survey_no,
            "land_record_owner_name": land_owner,
            "sale_deed_consideration_value": int(sale_deed_val),
            "ec_registered_value": int(ec_val),
            "ec_liens_count": int(ec_liens),
            "pdf_metadata_modification_delay_days": delay_days,
            "compression_anomaly_detected": compression_anomaly,
            "cloned_signature_detected": cloned_signature,
            "font_substitution_detected": font_sub,
            "physical_coherence_anomaly_detected": physical_coherence_anomaly,
            "ai_generation_score": ai_score,
            "double_pledge_detected": double_pledge,
            "guarantor_name": guarantor,
            "guarantor_overcommitment_detected": guarantor_overcommitment,
            "document_primary_language": doc_lang,
            "is_fraud": is_fraud,
            "fraud_pattern": fraud_pattern,
            "adverse_action_reason": adverse_reason
        })

    # Save to CSV
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records in {output_path}")

if __name__ == "__main__":
    generate_dataset()
