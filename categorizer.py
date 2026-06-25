def categorize(text):
    text = text.lower()

    if "uber" in text:
        return "Transport"
    elif "domino" in text or "dominos" in text:
        return "Food"
    elif "amazon" in text:
        return "Shopping"
    else:
        return "Others"
    