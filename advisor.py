def get_advice(text):
    text = text.lower()

    if "domino" in text or "dominos" in text:

        return """ spending Analysis:
        you spent mony on food.
        
        Saving Tip:
        Reduce food delivery expenses.
        
        Budget Recommendation:
        keep food spending below 20% of monthly income.
        """
    
    elif "uber" in text:
        return """
Spending Analysis:
you spent money on transport.

Saving Tip:
Use public transport when possible.

Budget Recommendation:
Allocate a fixed monthly transport budget.
"""
    else:
        return """
Spending Analysis:
Expense detected.

Saving Tip:
Track yout spending regularly.

Budget Recommendation:
Follow the 50-30-20 budgeting rule.
 """
