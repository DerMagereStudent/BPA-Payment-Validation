import json
import re

import pandas as pd
import pdfplumber

def extract_pdf_table(pdf_path):
    table_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Split text into lines
            lines = text.split("\n")

            # Process each line to detect table rows
            for line in lines:
                # Regex to match rows with date, description, and amounts
                match = re.match(r"(\d{2}\.\d{2}\.\d{4})\s+(.+?)\s+([+-]?\d{1,3}(?:\.\d{3})*,\d{2}\sEUR)\s+([+-]?\d{1,3}(?:\.\d{3})*,\d{2}\sEUR)", line)
                
                if match:
                    date, description, amount, balance = match.groups()
                    table_data.append({
                        "Date": date,
                        "Description": description,
                        "Amount": amount,
                        "Balance": balance
                    })

    # Convert to JSON
    return json.dumps(table_data, indent=4, ensure_ascii=False)