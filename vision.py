from dotenv import load_dotenv
import os
import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# API Endpoints
RXNORM_API_URL = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name={}"
FDA_API_URL = "https://api.fda.gov/drug/label.json?search=openfda.brand_name:{}"
MEDLINEPLUS_API_URL = "https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term={}"
WHO_EML_URL = "https://www.who.int/medicines/publications/essentialmedicines/en/"  # Static source

# Function to generate a response from the Gemini model
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process uploaded image and prepare for input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to fetch RxNorm ID for the drug
def get_rxnorm_id(drug_name):
    response = requests.get(RXNORM_API_URL.format(drug_name))
    if response.status_code == 200:
        data = response.json()
        if "idGroup" in data and "rxnormId" in data["idGroup"]:
            return data["idGroup"]["rxnormId"][0]
    return None

# Function to fetch FDA drug information
def get_fda_drug_info(drug_name):
    response = requests.get(FDA_API_URL.format(drug_name))
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            return data["results"][0]["description"]
    return "No FDA-approved information available."

# Function to fetch MedlinePlus drug information
def get_medlineplus_info(drug_name):
    response = requests.get(MEDLINEPLUS_API_URL.format(drug_name))
    if response.status_code == 200:
        return "Drug details available on MedlinePlus."
    return "No MedlinePlus data found."

# Streamlit UI
st.set_page_config(page_title="Tablet Info Summarizer", layout="centered", page_icon="💊")

# UI Styling
st.markdown(
    """
    <style>
        .header {text-align: center; font-size: 2.5em; margin-bottom: 20px; color: #ffd700;}
        .subheader {text-align: center; font-size: 1.5em; color: #00ffcc;}
        .warning {color: #ffd700;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<div class='header'>Tablet Info Summarizer</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Upload a tablet image to get medical details</div>", unsafe_allow_html=True)

# User Inputs
input_text = st.text_input("Enter Additional Details (Optional):", key="input", help="Add specific details about the tablet.")
uploaded_file = st.file_uploader("Upload Tablet Image (JPG, JPEG, PNG):", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Tablet Image", use_column_width=True)

# Analyze Button
if st.button("Analyze Tablet Info", use_container_width=True):
    if uploaded_file:
        try:
            # Prepare image for Gemini model
            image_data = input_image_setup(uploaded_file)

            # Custom prompt for Gemini to extract tablet name
            input_prompt = """
            Identify the tablet name from the image label.
            Example: If the label says "Paracetamol", extract "Paracetamol".
            """

            # Get extracted tablet name
            tablet_name = get_gemini_response(input_prompt, image_data, input_text).strip()

            if tablet_name:
                # Fetch RxNorm ID
                rxnorm_id = get_rxnorm_id(tablet_name)

                # Get additional medical data
                fda_info = get_fda_drug_info(tablet_name)
                medline_info = get_medlineplus_info(tablet_name)

                # Display tablet info
                st.markdown("<h3 style='color:#ffd700;'>Tablet Information Summary</h3>", unsafe_allow_html=True)
                st.success(f"**Tablet Name:** {tablet_name}")
                st.info(f"**RxNorm ID:** {rxnorm_id if rxnorm_id else 'Not Available'}")
                st.info(f"**FDA Information:** {fda_info}")
                st.info(f"**MedlinePlus Information:** {medline_info}")
                st.info(f"**WHO Essential Medicines:** Check [WHO EML]({WHO_EML_URL}) for further details.")

            else:
                st.warning("Tablet name could not be extracted. Please try again.")

        except Exception as e:
            st.error(f"Error processing tablet info: {e}")
    else:
        st.warning("Please upload a tablet image to proceed.")
