import os
import PyPDF2
import re
import csv

def read_internet_bill(filename):
    pdf_file = open(filename, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    with open('internet_bill.txt', 'w', encoding="utf-8") as f:
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            f.write(page.extract_text())
    pdf_file.close()

    d = {"bill_amount": 0,"bill_date": "",}

    with open("internet_bill.txt", "r") as file:
        line = file.readline()
        pattern = r'Amount Due'
        while line:
            match = re.search(pattern, line)
            if match and d["bill_amount"] == 0:
                file.readline()
                file.readline()
                file.readline()
                line = file.readline()

                line = line.strip()
                line = line.replace(",", "")
                d["bill_amount"] = line
                pattern = r'Issue Date'
                continue
            
            if match and d["bill_date"] == "":
                line = file.readline()
                line = line.strip()
                d["bill_date"] = line
                break
            
            line = file.readline()
        
    with open("internet_bill_amount.csv", "a", newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow([d["bill_date"], d["bill_amount"]])
