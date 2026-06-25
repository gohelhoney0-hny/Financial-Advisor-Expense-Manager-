import streamlit as st
from ocr import extract_text
from categorizer import categorize
from advisor import get_advice
from save_expense import save_expense
from budget import get_budget


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


set_attractive_bg()

st.title("Finance Advisor AI Agent")

uploaded_file = st.file_uploader("Upload Screenshot")

if uploaded_file:
    with open("temp.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    text = extract_text("temp.png")

    st.write("Extracted Text: ")
    st.write(text)

    category = categorize(text)
    save_expense(text, category)
    st.write("category: ", category)
    budget = get_budget(category)

    st.write("Budget Recommendation: ")
    st.write(budget)

    if st.button("Get Finance Advice"):
        advice = get_advice(text)
        st.write(" AI Advice: ")
        st.write(advice)
import streamlit as st

uploaded_file = st.file_uploader("Upload receipt", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with open("temp.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text("temp.png")
    st.write(text)



