import os
import PyPDF2
import re
import csv

def read_electricity_bill(filename):
    print(f"Reading {filename} file")
    pdf_file = open(filename, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    
    with open("electricity_bill.txt", 'w', encoding="utf-8") as f:
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            f.write(page.extract_text())
    
    pdf_file.close()
    

    d = {"bill_amount": 0,"bill_date": ""}


    with open("electricity_bill.txt", "r") as file:
        line = file.readline()
        pattern =  r'Date of Bill.*'
        while line:
            match = re.search(pattern, line)
            if match:
                print("Found date of bill")
                line = file.readline()
                print("Date: ", line)
                line = line.strip()
                d["bill_date"] = line

                file.readline()
                file.readline()
                line = file.readline()
                line = line[1:]
                line = line.replace(",", "")
                line = line.strip()
                d["bill_amount"] = float(line)
                break
            line = file.readline()

    with open("electricity_bill_amount.csv", "a", newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow([d["bill_date"], d["bill_amount"]])
    
