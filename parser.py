import re

def extract_data(text):
    amount = re.findall(r'\d+\.\d+', text)

    return {
        "amount": amount[0] if amount else "Not found"
    }