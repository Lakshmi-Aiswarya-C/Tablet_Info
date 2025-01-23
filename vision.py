from dotenv import load_dotenv
import streamlit as st
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

def input_image_setup(uploaded_file):
    else:
        raise FileNotFoundError("No file uploaded")

# Set up Streamlit app with improved UI
st.set_page_config(
    page_title="Gemini Pharmaceutical Identifier",
    page_icon="💊",
    layout="wide"
)
# Initialize the Streamlit app
st.set_page_config(page_title="Tablet Info Summarizer", layout="centered", page_icon="💊")

# Header section with a visually appealing title
st.markdown(
    """
    <div style="background-color:#2c3e50;padding:15px;border-radius:10px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;">Gemini Pharmaceutical Identifier 💊</h1>
        <p style="color:white;text-align:center;">Upload an image of a tablet label to get detailed information.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
# Add custom CSS for styling
st.markdown("""
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #ffffff;
        }
        .header {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #ffd700;
        }
        .subheader {
            text-align: center;
            font-size: 1.5em;
            color: #00ffcc;
        }
        .file-uploader {
            background-color: #343a40;
            padding: 10px;
            border-radius: 5px;
        }
        .button {
            background-color: #00adb5;
            color: #ffffff;
            font-size: 1.2em;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            margin-top: 10px;
        }
        .button:hover {
            background-color: #005f73;
        }
        .error {
            color: #ff6f61;
        }
        .warning {
            color: #ffd700;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.markdown(
        """
        <div style="background-color:#0a0a0a;padding:10px;border-radius:10px;">
            <h3>How to Use</h3>
            <p>1. Upload an image of a tablet or its label.</p>
            <p>2. Enter an optional prompt for clarification.</p>
            <p>3. Click on <strong>"Analyze Image"</strong>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
# Header
st.markdown("<div class='header'>Tablet Info Summarizer</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Upload a tablet image and get detailed information</div>", unsafe_allow_html=True)

# Main layout
input = st.text_input("Input Prompt:", placeholder="Optional custom input prompt...")
uploaded_file = st.file_uploader(
    "Choose an image of the tablet label:", type=["jpg", "jpeg", "png"]
)
# User inputs
input = st.text_input("Enter Additional Details (Optional):", key="input", help="Add any specific details or context about the tablet.")
uploaded_file = st.file_uploader("Upload Tablet Image (JPG, JPEG, PNG):", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Display the uploaded image
# Display uploaded image
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.image(image, caption="Uploaded Tablet Image", use_container_width=True)

# Button to trigger the model
submit = st.button("Analyze Image")
# Analyze tablet info button
submit = st.button("Analyze Tablet Info", use_container_width=True)

# Custom prompt
# Custom prompt for the tablet information summary
input_prompt = """
               You are an expert in understanding pharmaceutical information.
               You will receive input images of tablets with their labels.
               Based on the input image, you will:
               1. Identify the name of the tablet from the label.
               2. Search the web for its uses, side effects, and additional relevant information such as precautions, dosage instructions, and interactions.
               2. Search for its uses, side effects, precautions, dosage instructions, and interactions.
               3. Provide a concise and accurate summary of the findings.
               Ensure that the information is up-to-date and sourced from reliable medical websites.
               """

# Display results
# When the analyze button is clicked
if submit:
    if uploaded_file is not None:
        try:
            # Prepare the image data for input to the Gemini model
            image_data = input_image_setup(uploaded_file)

            # Process the input and generate response
            response = get_gemini_response(input_prompt, image_data, input)
            # Combine the extracted text with the user's input prompt
            complete_prompt = f"{input_prompt}\n\nTablet Details: {input}\n\nSummary:"
            # Process the tablet image with the Gemini model
            response = get_gemini_response(complete_prompt, image_data, input)

            # Display the response in a styled container
            st.markdown(
                """
                <div style="background-color:#dff9fb;padding:20px;border-radius:10px;margin-top:20px;">
                    <h3 style="color:#2c3e50;">Analysis Results</h3>
                    <p style="color:#34495e;">{}</p>
                </div>
                """.format(response),
                unsafe_allow_html=True,
            )
            # Show the summary to the user
            st.markdown("<h3 style='color:#ffd700;'>Tablet Information Summary</h3>", unsafe_allow_html=True)
            st.success(response)
        except Exception as e:
            st.error(f"Error processing the image: {e}")
            st.markdown(f"<div class='error'>Error processing the tablet info: {e}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload an image to proceed.")
        st.markdown("<div class='warning'>Please upload a tablet image to proceed.</div>", unsafe_allow_html=True)
