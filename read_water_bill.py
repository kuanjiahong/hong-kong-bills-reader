import os
import PyPDF2
import re
import csv

def read_water_bill(filename):
    print(f"Reading {filename} file")
    pdf_file = open(filename, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    
    amount_pattern =  r'Total Amount Due \$(\d+\.\d+)'
    date_pattern = r'BillDate of Issue : (\d{2}/\d{2}/\d{4})'

    d = {"bill_amount": 0,"bill_date": ""}
    
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        content = page.extract_text()

        date_match = re.search(date_pattern, content)
        amount_match = re.search(amount_pattern, content)
        if date_match:
            print("Found date")
            bill_date = date_match.group(1).strip()
            d["bill_date"] = bill_date

        if amount_match:
            print("Found amount")
            bill_amount = amount_match.group(1).strip()
            bill_amount = bill_amount.replace(",", "")
            d["bill_amount"] = float(bill_amount)
            break

    with open("water_bill_amount.csv", "a", newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow([d["bill_date"], d["bill_amount"]])
    

    pdf_file.close()
