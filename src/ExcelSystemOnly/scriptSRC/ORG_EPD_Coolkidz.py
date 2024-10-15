import pandas as pd 
import os
import warnings

warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings('ignore', category=FutureWarning)  

def convert_date_format(date_str):
    # Convert the input date string to datetime format
    date_obj = pd.to_datetime(date_str, format='%m/%d/%Y')
    # Return the formatted date: Month_Name dd, yyyy
    return date_obj.strftime('%B %d, %Y')

def function_for_EPD_coolkidz(pathing):
    # Read the Excel file
    data = pd.read_excel(pathing)

    # Process the patient names
    data['Patient First Name'] = data['PATIENT'].apply(lambda x: x.split(",")[1].strip() if isinstance(x, str) else "")
    data['Patient Last Name'] = data['PATIENT'].apply(lambda x: x.split(",")[0].strip() if isinstance(x, str) else "")

    data['Subscriber First Name'] = data['Patient First Name']  
    data['Subscriber Last Name'] = data['Patient Last Name']  

    # Change the Provider Name 
    data['Provider First Name'] = data['Provider Name'].apply(lambda x: x.split(",")[1].strip() if isinstance(x, str) else "")
    data['Provider Last Name'] = data['Provider Name'].apply(lambda x: x.split(",")[0].strip() if isinstance(x, str) else "")

    # Convert date formats
    data["Date Of Service"] = data['SERVICE DATE'].apply(convert_date_format)
    data["CPT Code"] = "NA"
    data["Provider NPI"] = "NA"
    data['Provider Group NPI'] = 1710468848
    data["Provider Group Name"] = "Cool Kidz Pediatrics LLC"
    data["Patient Date Of Birth"] = "NA"
    data["Subscriber DOB"] = "NA"
    data["Assigned Emp ID#"] = "NA"
    data["Subscriber ID"] = "NA"

    # Rename columns
    data.rename(columns={
        'CLAIMS#': 'Claim ID #',
        'Account Number': 'Patient Acc#', 
        'PAYER': 'Insurance Name', 
        'CHARGES': 'Charges Amount', 
        'Balance': 'Total Outstanding Balance'
    }, inplace=True)

    
    # Convert Charges Amount and Total Outstanding Balance
    data['Charges Amount'] = pd.to_numeric(data['Charges Amount'], errors='coerce')
    data['Total Outstanding Balance'] = pd.to_numeric(data['Total Outstanding Balance'], errors='coerce')
    data['Charges Amount'] = data['Charges Amount'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")
    data['Total Outstanding Balance'] = data['Total Outstanding Balance'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")

    # Dropping unnecessary columns
    data.drop(columns=['SERVICE DATE', 'PATIENT', 'Provider Name', 'Guarantor Name', 'WithHeld', 'Adjustment', 'PMTS/ADJS', 'PVDR', 'COLL', 'CLAIMTYPE', 'STATUS', 'Visit Type'], inplace=True)


    # Column arrangement
    columns_arrangement = ['Claim ID #', 'Patient Acc#', 'Patient First Name', 'Patient Last Name',
                           'Patient Date Of Birth', 'Subscriber ID', 'Subscriber First Name',
                           'Subscriber Last Name', 'Subscriber DOB', 'Insurance Name',
                           'Date Of Service', 'CPT Code', 'Provider First Name',
                           'Provider Last Name', 'Provider NPI', 'Provider Group Name',
                           'Provider Group NPI', 'Charges Amount', 'Total Outstanding Balance',
                           'Assigned Emp ID#']
    
    data = data[columns_arrangement]

    # Create output directory
    output_dir = 'Results/AR/EPD/Coolkidz'
    os.makedirs(output_dir, exist_ok=True)

    # Prepare output file name
    filename = os.path.basename(pathing)
    filename_no_ext = os.path.splitext(filename)[0]
    parts = filename_no_ext.split('_')
    kunjdate = parts[-1] 

    # Save the processed data to Excel
    output_path = os.path.join(output_dir, f'EPD_{kunjdate}.xlsx')
    data.to_excel(output_path, index=False)

    return output_path
