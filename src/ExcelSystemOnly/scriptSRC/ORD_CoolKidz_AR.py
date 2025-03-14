import pandas as pd 
import datetime 
import numpy as np
import os  # Import the os module
import zipfile  # Import the zipfile module
import warnings

warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings('ignore', category=FutureWarning)  

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def apply_logic_FOR_AR_CoolKidz(pathing1, pathing2):
    data = pd.read_excel(pathing1)
    date = datetime.date.today() 
    data_Dictionary = pd.read_excel(pathing2, sheet_name='page')
    # data_npi = pd.read_excel(pathing2, sheet_name='Sheet1')
    data['Service Date'] = pd.to_datetime(data['Service Date'])
    data['Patient DOB'] = pd.to_datetime(data['Patient DOB'])
    today = pd.Timestamp(datetime.date.today())
    data['Number of Days'] = (today - data['Service Date']).dt.days
    
    npi_dict = {
    "Fine, Ann": 1821013327,
    "ROLLAND, LILIVETTE": 1831205103,
    "Pillai, Ananthan K": 1154330165,
    "Vindhya, Naveena": 1306063466,
    "Kumar, Sujata": 1679559512,
    "Sanchez, Mario": 1235260746,
    "Babu, Keshava": 1215040621,
    "Patel, Anilkumar": 1295848554,
    "Cardona, Sabrina": 1063471043,
    "Harris, Staci": 1144779927,
    "Churilla, Michaela": 1295260891,
    "Smith, Vicki": 1629060298,
    "Morales, Frances": 1235131582,
    "Fox, Teresita": 1003974056
}
    

    # Changing the column name of data_Dictionary to match with the dataframe. 
    data_Dictionary.rename(columns={'Claim No' : 'Claim ID #'}, inplace=True)
    # data_npi.rename(columns={'Appointment / Servicing Provider' : 'Rendering Provider Name', 'NPI' : 'Provider NPI'}, inplace=True)

    feature_mapping = {
    'Claim No' : 'Claim ID #', 
    'Patient Acct No' : 'Patient Acc#',
    'Patient Date Of Birth' : 'Patient DOB',
    'Payer Subscriber No' : 'Subscriber ID', 
    'Payer Name' : 'Insurance Name', 
    'Service Date' : 'Date Of Service', # Error. 
    'Charges' : 'Charges Amount', 
    'Patient DOB' : 'Patient Date Of Birth', # doubt & Error
    'Balance' : 'Total Outstanding Balance'
    }

    data['Payer Subscriber No']  = data['Payer Subscriber No'].astype(str) 
    data['Payer Subscriber No'].fillna("NaN", inplace=True)

    # Ensure the 'Charges' column is treated as a float for consistent formatting
    data['Charges'] = data['Charges'].astype(float)
    data['Charges Amount'] = data['Charges'].apply(lambda x: f"${x:,.2f}")
    
    data['Balance'] = data['Balance'].astype(float)
    data['Total Outstanding Balance'] = data['Balance'].apply(lambda x: f"${x:,.2f}")
    
    filtered_data = data[['Claim No','Patient DOB', 'Patient Acct No', 'Payer Subscriber No', 'Payer Name', 'Charges Amount', 'Number of Days', 'Service Date', 'Total Outstanding Balance']]
    filtered_data.rename(columns=feature_mapping, inplace=True)
    filtered_data['Patient First Name'] = data['Patient Name'].apply(lambda x: x.split(",")[0])
    filtered_data['Patient Last Name'] = data['Patient Name'].apply(lambda x: x.split(",")[1])

    filtered_data['Subscriber First Name'] = data['Patient Name'].apply(lambda x: x.split(",")[0])
    filtered_data['Subscriber Last Name'] = data['Patient Name'].apply(lambda x: x.split(",")[1])

    filtered_data['Patient Date Of Birth'] = filtered_data['Patient Date Of Birth'].apply(convert_date)
    filtered_data['Date Of Service'] = filtered_data['Date Of Service'].apply(convert_date)
    # print(filtered_data.columns)
    # Creating a new field "Subscriber DOB"
    filtered_data['Subscriber DOB'] = filtered_data['Patient Date Of Birth'] 
    # print(filtered_data['Total Outstanding Balance'].head())



    # Importing and applying the logic of vlookup here. 
    data_dictionary_unique = data_Dictionary.drop_duplicates(subset=['Claim ID #'], keep='first')
    resultant_data = pd.merge(filtered_data, data_dictionary_unique[['Claim ID #', 'Rendering Provider Name', 'CPT Code']], on='Claim ID #', how='left')

    generated_files = []
    # Splitting "Render Provider Name" into there "'First name" & "Last Name"
    resultant_data['Provider First Name'] = resultant_data['Rendering Provider Name'].astype(str).apply(lambda x: x.split(",")[1].strip() if "," in x else "")
    # resultant_data['Provider Last Name'] = resultant_data['Rendering Provider Name'].astype(str).apply(lambda x: x.split(",")[0] if "," in x else x)
    resultant_data['Provider Last Name'] = resultant_data['Rendering Provider Name'].astype(str).apply(lambda x: x.split(",")[0] if "," in x else "")

    # if resultant_data['CPT Code'].last_valid_index() == resultant_data['Provider First Name'].last_valid_index() == resultant_data['Provider Last Name'].last_valid_index():
    #     print([resultant_data['CPT Code'].last_valid_index()])
    #     print([resultant_data['Provider First Name'].last_valid_index()])
    #     print([resultant_data['Provider Last Name'].last_valid_index()])
    #     # formated_data = resultant_data[:resultant_data['CPT Code'].last_valid_index() + 1]
    #     # formated_data.to_excel("Results/AR/AR_Coolkidz/_Sample___AR___Coolkidz_.xlsx", index=False)
    # else:
    #     print([resultant_data['CPT Code'].last_valid_index()])
    #     print([resultant_data['Provider First Name'].last_valid_index()])
    #     print([resultant_data['Provider Last Name'].last_valid_index()])
    resultant_data = resultant_data[ : resultant_data['CPT Code'].last_valid_index() + 1]
    resultant_data['Assigned Emp ID#'] = " "
    # resultant_data = pd.merge(resultant_data, data_npi[['Rendering Provider Name', 'Provider NPI']], on='Rendering Provider Name', how='left')
    resultant_data['Rendering Provider Name'] = resultant_data['Rendering Provider Name'].str.replace('XXX', '').str.strip()
    resultant_data['Provider NPI'] = resultant_data['Rendering Provider Name'].map(npi_dict)

    resultant_data["Provider Group NPI"] = 1710468848
    resultant_data["Provider Group Name"] = "Cool Kidz Pediatrics LLC"

    # Ensure the directory exists before saving the Excel file
    ensure_directory_exists("Results/AR/AR_Coolkidz/Reference Files")
    resultant_data.to_excel("Results/AR/AR_Coolkidz/Reference Files/Reference_AR_Coolkidz_File.xlsx", index=False)
    generated_files.append("Results/AR/AR_Coolkidz/Reference Files/Reference_AR_Coolkidz_File.xlsx")  # Append file path to generated_files

    # Removing "Rendering Provider Name" From the Resultant data 
    resultant_data = resultant_data.drop(columns=['Rendering Provider Name'])

    # Splitting the entire dataset according to the number of dayes allocated 
    resultant_data_above_120 = resultant_data[resultant_data['Number of Days'] > 120]
    resultant_data_between_91_and_120 = resultant_data[(resultant_data['Number of Days'] >= 91) & (resultant_data['Number of Days'] <= 120)]
    resultant_data_between_61_and_90 = resultant_data[(resultant_data['Number of Days'] >= 61) & (resultant_data['Number of Days'] <= 90)]
    resultant_data_between_31_and_60 = resultant_data[(resultant_data['Number of Days'] >= 31) & (resultant_data['Number of Days'] <= 60)]
    resultant_data_less_30 = resultant_data[resultant_data['Number of Days'] < 30]


    # Desized Column Ordering with respect to RAIO Coolkidz AR
    columns_arrangment = ['Claim ID #', 'Patient Acc#', 'Patient First Name', 'Patient Last Name',
       'Patient Date Of Birth', 'Subscriber ID', 'Subscriber First Name',
       'Subscriber Last Name', 'Subscriber DOB', 'Insurance Name',
       'Date Of Service', 'CPT Code', 'Provider First Name',
       'Provider Last Name', 'Provider NPI', 'Provider Group Name',
       'Provider Group NPI', 'Charges Amount', 'Total Outstanding Balance',
       'Assigned Emp ID#']


    # Dropping the 'Number of Days' column from resultant_data_above_120 || Also Rearranging the column format. 
    resultant_data_above_120 = resultant_data_above_120.drop(columns=['Number of Days'])
    resultant_data_above_120 = resultant_data_above_120[columns_arrangment]
    ensure_directory_exists('Results/AR/AR_Coolkidz/Insurances_Above_120')  # Ensure the directory exists
    insurance_groups_above_120 = resultant_data_above_120.groupby('Insurance Name')
    counter = 0
    for insurance_name, group in insurance_groups_above_120:
        # Splitting the group into 'Same' and 'Different' based on the comparison
        group_same = group[group['Charges Amount'] == group['Total Outstanding Balance']]
        group_different = group[group['Charges Amount'] != group['Total Outstanding Balance']]

        # Processing the 'Same' group
        if not group_same.empty:
            filename_same = "Coolkidz_120+_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Primary" + ".xlsx"
            group_same.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Above_120/{filename_same}', index=False)
            counter += 1
            print(f"Saved {filename_same} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Above_120/{filename_same}')  # Append file path to generated_files

        # Processing the 'Different' group
        if not group_different.empty:
            filename_different = "Coolkidz_120+_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Partial" + ".xlsx"
            group_different.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Above_120/{filename_different}', index=False)
            counter += 1
            print(f"Saved {filename_different} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Above_120/{filename_different}')  # Append file path to generated_files




    # Dropping the 'Number of Days' column from resultant_data_between_91_and_120 || Also Rearranging the column format. 
    resultant_data_between_91_and_120 = resultant_data_between_91_and_120.drop(columns=['Number of Days'])
    resultant_data_between_91_and_120 = resultant_data_between_91_and_120[columns_arrangment]
    ensure_directory_exists('Results/AR/AR_Coolkidz/Insurances_Between_91_To_120')  # Ensure the directory exists
    insurance_groups_between_91_to_120 = resultant_data_between_91_and_120.groupby('Insurance Name')
    counter = 0
    for insurance_name, group in insurance_groups_between_91_to_120:
        group_same = group[group['Charges Amount'] == group['Total Outstanding Balance']]
        group_different = group[group['Charges Amount'] != group['Total Outstanding Balance']]

        if not group_same.empty:
            filename_same = "Coolkidz_91_To_120_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Primary" + ".xlsx"
            group_same.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Between_91_To_120/{filename_same}', index=False)
            counter += 1
            print(f"Saved {filename_same} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Between_91_To_120/{filename_same}')  # Append file path to generated_files

        if not group_different.empty:
            filename_different = "Coolkidz_91_To_120_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Partial" + ".xlsx"
            group_different.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Between_91_To_120/{filename_different}', index=False)
            counter += 1
            print(f"Saved {filename_different} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Between_91_To_120/{filename_different}')  # Append file path to generated_files



    # Dropping the 'Number of Days' column from resultant_data_between_61_and_90 || Also Rearranging the column format. 
    resultant_data_between_61_and_90 = resultant_data_between_61_and_90.drop(columns=['Number of Days'])
    resultant_data_between_61_and_90 = resultant_data_between_61_and_90[columns_arrangment]
    ensure_directory_exists('Results/AR/AR_Coolkidz/Insurances_Between_61_To_90')  # Ensure the directory exists
    insurance_groups_between_61_to_90 = resultant_data_between_61_and_90.groupby('Insurance Name')
    counter = 0
    for insurance_name, group in insurance_groups_between_61_to_90:
        group_same = group[group['Charges Amount'] == group['Total Outstanding Balance']]
        group_different = group[group['Charges Amount'] != group['Total Outstanding Balance']]

        if not group_same.empty:
            filename_same = "Coolkidz_61_To_90_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Primary" + ".xlsx"
            group_same.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Between_61_To_90/{filename_same}', index=False)
            counter += 1
            print(f"Saved {filename_same} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Between_61_To_90/{filename_same}')  # Append file path to generated_files

        if not group_different.empty:
            filename_different = "Coolkidz_61_To_90_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Partial" + ".xlsx"
            group_different.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Between_61_To_90/{filename_different}', index=False)
            counter += 1
            print(f"Saved {filename_different} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Between_61_To_90/{filename_different}')  # Append file path to generated_files





    # Dropping the 'Number of Days' column from resultant_data_between_31_and_60 || Also Rearranging the column format. 
    resultant_data_between_31_and_60 = resultant_data_between_31_and_60.drop(columns=['Number of Days'])
    resultant_data_between_31_and_60 = resultant_data_between_31_and_60[columns_arrangment]
    ensure_directory_exists('Results/AR/AR_Coolkidz/Insurances_Between_31_To_60')  # Ensure the directory exists
    insurance_groups_between_31_to_60 = resultant_data_between_31_and_60.groupby('Insurance Name')
    counter = 0
    for insurance_name, group in insurance_groups_between_31_to_60:
        group_same = group[group['Charges Amount'] == group['Total Outstanding Balance']]
        group_different = group[group['Charges Amount'] != group['Total Outstanding Balance']]

        if not group_same.empty:
            filename_same = "Coolkidz_31_To_60_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Primary" + ".xlsx"
            group_same.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Between_31_To_60/{filename_same}', index=False)
            counter += 1
            print(f"Saved {filename_same} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Between_31_To_60/{filename_same}')  # Append file path to generated_files

        if not group_different.empty:
            filename_different = "Coolkidz_31_To_60_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Partial" + ".xlsx"
            group_different.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Between_31_To_60/{filename_different}', index=False)
            counter += 1
            print(f"Saved {filename_different} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Between_31_To_60/{filename_different}')  # Append file path to generated_files





    # Dropping the 'Number of Days' column from resultant_data_less_30 || Also Rearranging the column format. 
    resultant_data_less_30 = resultant_data_less_30.drop(columns=['Number of Days'])
    resultant_data_less_30 = resultant_data_less_30[columns_arrangment]
    ensure_directory_exists('Results/AR/AR_Coolkidz/Insurances_Below_30')  # Ensure the directory exists
    insurance_groups_less_30 = resultant_data_less_30.groupby('Insurance Name')
    counter = 0
    for insurance_name, group in insurance_groups_less_30:
        group_same = group[group['Charges Amount'] == group['Total Outstanding Balance']]
        group_different = group[group['Charges Amount'] != group['Total Outstanding Balance']]

        if not group_same.empty:
            filename_same = "Coolkidz_30-_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Primary" + ".xlsx"
            group_same.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Below_30/{filename_same}', index=False)
            counter += 1
            print(f"Saved {filename_same} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Below_30/{filename_same}')  # Append file path to generated_files

        if not group_different.empty:
            filename_different = "Coolkidz_30-_" + insurance_name.replace('/', '_').replace('\\', '_') + f"_As of {date}_Partial" + ".xlsx"
            group_different.to_excel(f'Results/AR/AR_Coolkidz/Insurances_Below_30/{filename_different}', index=False)
            counter += 1
            print(f"Saved {filename_different} - Group {counter}")
            generated_files.append(f'Results/AR/AR_Coolkidz/Insurances_Below_30/{filename_different}')  # Append file path to generated_files



    resultant_data_above_120.to_excel('Results/AR/AR_Coolkidz/Reference Files/Data_Above_120.xlsx', index = False)
    generated_files.append('Results/AR/AR_Coolkidz/Reference Files/Data_Above_120.xlsx')  # Append file path to generated_files
    resultant_data_between_91_and_120.to_excel('Results/AR/AR_Coolkidz/Reference Files/Data_Between_91_To_120.xlsx', index = False)
    generated_files.append('Results/AR/AR_Coolkidz/Reference Files/Data_Between_91_To_120.xlsx')  # Append file path to generated_files
    resultant_data_between_61_and_90.to_excel('Results/AR/AR_Coolkidz/Reference Files/Data_Between_61_To_90.xlsx', index = False)
    generated_files.append('Results/AR/AR_Coolkidz/Reference Files/Data_Between_61_To_90.xlsx')  # Append file path to generated_files
    resultant_data_between_31_and_60.to_excel('Results/AR/AR_Coolkidz/Reference Files/Data_Between_31_To_60.xlsx', index = False)
    generated_files.append('Results/AR/AR_Coolkidz/Reference Files/Data_Between_31_To_60.xlsx')  # Append file path to generated_files
    resultant_data_less_30.to_excel('Results/AR/AR_Coolkidz/Reference Files/Data_Less_30.xlsx', index = False)
    generated_files.append('Results/AR/AR_Coolkidz/Reference Files/Data_Less_30.xlsx')  # Append file path to generated_files

    # Create a ZIP file to store all result files
    zip_file_path = 'temp/AR_Coolkidz_output_files.zip'
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in generated_files:
            archive_path = os.path.relpath(file_path, 'Results/AR/AR_Coolkidz')
            zipf.write(file_path, archive_path)
    print(f"ZIP file created at: {zip_file_path}")
    return zip_file_path

def convert_date(date_obj, input_format="%Y-%m-%d %H:%M:%S", output_format='%B %d, %Y'):
    if isinstance(date_obj, datetime.date):
        # Format the date object into the desired output format
        formatted_date = date_obj.strftime(output_format)       
        return formatted_date
    else:
        return date_obj
    
