import pandas as pd
import csv
import re
import os


def read_excel_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    records = [line.strip().split('|') for line in lines]
    return records


def validate_records(records, data_fields):
    validation_report = []
    i=1
    for record in records:
        validation_errors = []
        Wrong_Format = []
        for idx, row in data_fields.iterrows():
            field,pattern = row['Field'], row['Pattern']
            value = record[idx]
            if value:
                # print(field,value)
                if not re.match(pattern, value):
                    # print(f"{field} does not match the pattern {value}")
                    # validation_errors.append(f"{field} does not match the pattern {pattern}")
                    validation_errors.append(f"{field}")
                    Wrong_Format.append(f"{value}")
        if validation_errors:
            validation_report.append({'index': i,'record': record, 'errors': validation_errors,'wrong Format':Wrong_Format})
        i+=1
    return validation_report

def generate_report(validation_report, output_file_path):
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ['index','record', 'errors','wrong Format']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in validation_report:
            writer.writerow(entry)

text_file_path = 'new_data.txt' 
excel_file_path = 'Validation_Checks_New.xlsx'
output_file_path = 'validation_report.csv'

# print(read_text_file(text_file_path))
# print(read_excel_file(excel_file_path))
data_fields = read_excel_file(excel_file_path)
records = read_text_file(text_file_path)
# print(data_fields)
# print(len(records))
validation_report = validate_records(records, data_fields)
generate_report(validation_report, output_file_path)
print(f"Validation report generated at {output_file_path}")