import streamlit as st
from ocr import extract_text
from categorizer import categorize
from advisor import get_advice
from save_expense import save_expense
from budget import get_budget
import pandas as pd
import plotly.express as px
import re


def set_attractive_bg() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bb-bg0: #0b1220;
            --bb-bg1: #101a33;
            --bb-bg2: #0c2a3a;
            --bb-text: rgba(255,255,255,0.95);
            --bb-muted: rgba(255,255,255,0.72);
            --bb-card: rgba(0,0,0,0.25);
            --bb-card2: rgba(0,0,0,0.35);
            --bb-border: rgba(255,255,255,0.10);
        }

        /* Base background */
        .stApp {
            background:
                radial-gradient(circle at 15% 20%, rgba(79, 172, 254, 0.32) 0%, rgba(79, 172, 254, 0) 45%),
                radial-gradient(circle at 85% 30%, rgba(253, 203, 110, 0.22) 0%, rgba(253, 203, 110, 0) 50%),
                radial-gradient(circle at 45% 90%, rgba(167, 139, 250, 0.20) 0%, rgba(167, 139, 250, 0) 55%),
                linear-gradient(135deg, var(--bb-bg0) 0%, var(--bb-bg1) 35%, var(--bb-bg2) 100%);
            background-attachment: fixed;
            color: var(--bb-text);
        }

        /* Prevent Streamlit panels from completely hiding the background */
        section[data-testid="stSidebar"],
        section[data-testid="stMain"] {
            background: rgba(0,0,0,0.0);
        }

        /* Vignette overlay */
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background: radial-gradient(circle at center, rgba(0,0,0,0) 28%, rgba(0,0,0,0.55) 100%);
        }

        /* Text contrast */
        h1, h2, h3, p, label, .stMarkdown, .stText, .stMetric {
            color: var(--bb-text) !important;
        }
        .stMarkdown a { color: rgba(170, 220, 255, 0.95) !important; }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(0,0,0,0.18) !important;
            border-right: 1px solid var(--bb-border);
            backdrop-filter: blur(10px);
        }

        /* Main content area cards */
        .block-container {
            padding-top: 18px;
            background: rgba(0,0,0,0.00);
        }

        /* Give Streamlit “card-like” containers a subtle glass effect */
        div[data-testid="stVerticalBlock"] > div,
        div[data-testid="stHorizontalBlock"] > div,
        .element-container {
            background: transparent;
        }

        /* Metrics */
        .stMetric {
            background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 12px;
            padding: 14px 16px;
            margin: 8px 0;
            backdrop-filter: blur(10px);
        }
        .stMetricLabel { color: var(--bb-muted) !important; }
        .stMetricValue { color: var(--bb-text) !important; }

        /* Tables/dataframes */
        table, th, td {
            border-color: rgba(255,255,255,0.12) !important;
        }
        th { color: var(--bb-muted) !important; }
        td { color: var(--bb-text) !important; }

        /* Buttons */
        div.stButton > button {
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            color: var(--bb-text) !important;
        }
        div.stButton > button:hover {
            background: rgba(255,255,255,0.12) !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def parse_transaction(text: str) -> dict:
    if not text:
        return {"amount": "Not found", "merchant": "Unknown"}

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    merchant = "Unknown"
    for line in lines:
        if len(line) > 2 and not re.search(r"\d", line):
            merchant = line
            break

    amount_candidates = re.findall(r"\$?\d{1,3}(?:[0-9,]*)(?:\.\d{2})?", text)
    parsed_amount = "Not found"
    numeric_values = []
    for candidate in amount_candidates:
        cleaned = candidate.replace("$", "").replace(",", "")
        try:
            numeric_values.append(float(cleaned))
        except ValueError:
            continue

    if numeric_values:
        amount_value = max(numeric_values)
        if amount_value.is_integer():
            parsed_amount = str(int(amount_value))
        else:
            parsed_amount = str(round(amount_value, 2))

    return {"amount": parsed_amount, "merchant": merchant}


set_attractive_bg()

st.title("Finance Advisor AI Agent")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

uploaded_file = st.file_uploader("Upload Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with open("temp.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text("temp.png")

    st.write("Extracted Text: ")
    st.write(text)

    parsed_data = parse_transaction(text)
    try:
        category = categorize(parsed_data["merchant"], text)
    except TypeError:
        category = categorize(text)

    save_expense(text, category)
    st.write("category: ", category)
    budget = get_budget(category)

    st.write("Budget Recommendation: ")
    st.write(budget)

    if parsed_data["amount"] != "Not found":
        st.session_state.expenses.append({
            "Amount": int(float(parsed_data["amount"])),
            "Category": category,
            "Merchant": parsed_data["merchant"],
        })

    if st.button("Get Finance Advice"):
        advice = get_advice(text)
        st.write(" AI Advice: ")
        st.write(advice)


# Convert to DataFrame
df = pd.DataFrame(st.session_state.expenses)

# Show graph if data exists
if not df.empty:

    st.subheader("📊 Expense Dashboard")

    # Total by category
    category_summary = df.groupby("Category")["Amount"].sum().reset_index()

    # Donut Chart
    donut = px.pie(
        category_summary,
        names="Category",
        values="Amount",
        hole=0.5,
        title="Expense Distribution"
    )
    st.plotly_chart(donut, use_container_width=True)

    # Bar Chart
    bar = px.bar(
        category_summary,
        x="Category",
        y="Amount",
        text="Amount",
        title="Category-wise Spending"
    )
    st.plotly_chart(bar, use_container_width=True)

    # Trend Line
    df["Transaction"] = range(1, len(df) + 1)

    line = px.line(
        df,
        x="Transaction",
        y="Amount",
        markers=True,
        title="Expense Trend"
    )
    st.plotly_chart(line, use_container_width=True)





