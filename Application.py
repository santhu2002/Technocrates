import pandas as pd
import csv
import re
import os

# Read the Excel file
def read_excel_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# Read the text file with records
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    records = [line.strip().split(',') for line in lines]
    return records

# Validate Records
def validate_records(records, data_fields):
    validation_report = []
    for record in records:
        validation_errors = []
        for idx, row in data_fields.iterrows():
            field, dtype, required, min_val, max_val, regex = row['Field'], row['Type'], row['Required'], row.get('Min'), row.get('Max'), row.get('Regex')
            value = record[idx]
            
            # Check required
            if required and not value:
                validation_errors.append(f"{field} is required")
                continue
            
            try:
                # Validate data type
                if dtype == 'int':
                    value = int(value)
                elif dtype == 'float':
                    value = float(value)
                elif dtype == 'str':
                    value = str(value)
                else:
                    validation_errors.append(f"Unsupported data type: {dtype}")
                    continue
                
                # Validate min and max values for numeric types
                if dtype in ['int', 'float']:
                    if min_val and value < min_val:
                        validation_errors.append(f"{field} should be at least {min_val}")
                    if max_val and value > max_val:
                        validation_errors.append(f"{field} should be at most {max_val}")
                
                # Validate regex for string types
                if (dtype == 'str' or dtype=='float') and regex and not re.match(regex, str(value)):
                    validation_errors.append(f"{field} does not match the pattern {regex}")
                # if value:
                #     print(re.match(regex,value),value)
            
            except ValueError:
                validation_errors.append(f"Invalid value for {field}: expected {dtype}, got {record[idx]}")
        
        if validation_errors:
            validation_report.append({'record': record, 'errors': validation_errors})
        else:
            validation_report.append({'record': record, 'errors': 'No errors'})
    
    return validation_report

# Generate the report
def generate_report(validation_report, output_file_path):
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ['record', 'errors']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in validation_report:
            writer.writerow(entry)

# File paths
excel_file_path = 'validationchecks.xlsx'  # Update this to the correct path
text_file_path = 'data.txt'  # Update this to the correct path
output_file_path = 'validation_report.csv'  # Update this to the correct path

# Verify the Excel file exists
if not os.path.exists(excel_file_path):
    raise FileNotFoundError(f"Excel file not found: {excel_file_path}")

# Run the process
data_fields = read_excel_file(excel_file_path)
records = read_text_file(text_file_path)
validation_report = validate_records(records, data_fields)
generate_report(validation_report, output_file_path)
print(f"Validation report generated at {output_file_path}")
