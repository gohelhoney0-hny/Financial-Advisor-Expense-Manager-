import streamlit as st
import pytesseract
from PIL import Image, ImageOps
import re

# ------------------------------------
# TESSERACT PATH (FOR LOCAL WINDOWS)
# ------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ------------------------------------
# IMAGE PREPROCESSING (MOBILE FIX)
# ------------------------------------
def preprocess_image(image):
    image = ImageOps.exif_transpose(image)   # Fix rotated images
    image = image.convert("L")               # Convert to grayscale
    return image


# ------------------------------------
# OCR FUNCTION
# ------------------------------------
def extract_text(image):
    try:
        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )
        return text
    except Exception as e:
        return f"OCR Error: {str(e)}"


# ------------------------------------
# PARSER FUNCTION
# ------------------------------------
def parse_transaction(text):
    data = {}

    # Extract amount (₹)
    amount = re.findall(r'₹\s?(\d+)', text)
    data["amount"] = amount[0] if amount else "Not found"

    # Extract UPI ID
    upi = re.findall(r'[\w\.-]+@[\w]+', text)
    data["upi_id"] = upi[0] if upi else "Not found"

    # Extract merchant keywords
    merchant_list = [
        "swiggy",
        "zomato",
        "uber",
        "ola",
        "amazon",
        "flipkart"
    ]

    merchant_found = "Unknown"

    for merchant in merchant_list:
        if merchant in text.lower():
            merchant_found = merchant.title()
            break

    data["merchant"] = merchant_found

    return data


# ------------------------------------
# CATEGORIZER FUNCTION
# ------------------------------------
def categorize(merchant, text):

    merchant = merchant.lower()
    text = text.lower()

    if merchant in ["swiggy", "zomato"]:
        return "Food"

    elif merchant in ["uber", "ola"]:
        return "Transport"

    elif merchant in ["amazon", "flipkart"]:
        return "Shopping"

    elif "recharge" in text or "bill" in text:
        return "Bills"

    elif "transfer" in text:
        return "Transfer"

    else:
        return "Other"


# ------------------------------------
# FINANCIAL ADVICE ENGINE
# ------------------------------------
def financial_advice(category):

    advice = {
        "Food": "Try reducing food delivery expenses to save more.",
        "Transport": "Track fuel and travel expenses regularly.",
        "Shopping": "Avoid unnecessary shopping and impulse buying.",
        "Bills": "Pay bills on time to avoid extra charges.",
        "Transfer": "Keep track of money sent to friends/family.",
        "Other": "Monitor your spending and build savings habits."
    }

    return advice.get(category, "No advice available.")


# ------------------------------------
# STREAMLIT UI
# ------------------------------------
st.set_page_config(page_title="AI Expense Manager", layout="centered")

st.title("💰 AI Expense Manager")
st.write("Upload payment screenshots (works better on mobile too)")

uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file)

        st.subheader("📷 Uploaded Image")
        st.image(image, use_container_width=True)

        # Preprocess image
        processed_image = preprocess_image(image)

        # OCR
        text = extract_text(processed_image)

        st.subheader("🔍 OCR Output")
        st.text(text)

        # Parse
        parsed_data = parse_transaction(text)

        st.subheader("🧾 Parsed Transaction")
        st.json(parsed_data)

        # Categorize
        category = categorize(
            parsed_data["merchant"],
            text
        )

        st.subheader("📂 Category")
        st.success(category)

        # Final Summary
        st.subheader("📊 Transaction Summary")

        st.write("**Amount:**", parsed_data["amount"])
        st.write("**UPI ID:**", parsed_data["upi_id"])
        st.write("**Merchant:**", parsed_data["merchant"])
        st.write("**Category:**", category)

        # Financial Advice
        advice = financial_advice(category)

        st.subheader("🧠 Financial Advice")
        st.info(advice)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")