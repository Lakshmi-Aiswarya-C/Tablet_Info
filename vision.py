from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API with your API key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate a response from the Gemini model
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process uploaded image and prepare for input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set up Streamlit app with improved UI
st.set_page_config(
    page_title="Gemini Pharmaceutical Identifier",
    page_icon="💊",
    layout="wide"
)

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

# Main layout
input = st.text_input("Input Prompt:", placeholder="Optional custom input prompt...")
uploaded_file = st.file_uploader(
    "Choose an image of the tablet label:", type=["jpg", "jpeg", "png"]
)

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Button to trigger the model
submit = st.button("Analyze Image")

# Custom prompt
input_prompt = """
               You are an expert in understanding pharmaceutical information.
               You will receive input images of tablets with their labels.
               Based on the input image, you will:
               1. Identify the name of the tablet from the label.
               2. Search the web for its uses, side effects, and additional relevant information such as precautions, dosage instructions, and interactions.
               3. Provide a concise and accurate summary of the findings.
               Ensure that the information is up-to-date and sourced from reliable medical websites.
               """

# Display results
if submit:
    if uploaded_file is not None:
        try:
            # Prepare the image data for input to the Gemini model
            image_data = input_image_setup(uploaded_file)

            # Process the input and generate response
            response = get_gemini_response(input_prompt, image_data, input)

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
        except Exception as e:
            st.error(f"Error processing the image: {e}")
    else:
        st.warning("Please upload an image to proceed.")
