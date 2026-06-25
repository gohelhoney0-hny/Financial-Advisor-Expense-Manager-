def get_budget(category):

    if category == "Food":
        return "Recommended Budget: keep food expenses below $5000 per month."
    
    elif category == "Transport":
        return "Recommendation Budget: keep transport expenses below $3000 per month."
    
    elif category == "Shopping":
        return "Recommendation Budget: Avoid Spending more than 20% of your income on shopping."
    
    else:
        return "Recommendation Budget: Follow the 50-30-20 budgeting rule"