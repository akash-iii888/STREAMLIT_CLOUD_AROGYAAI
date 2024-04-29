import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import pandas as pd  # Import pandas for data formatting

genai.configure(api_key=os.getenv("KEY"))

## Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_prompt, image_data, input_text):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_data[0], input_text])
    return pd.DataFrame(response.text.split("\n\n")[1:])  # Convert response to DataFrame

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize Streamlit app 
st.set_page_config(page_title="AROGYA", page_icon="", layout="wide")  # Optional layout setting

st.title("AROGYA")


with st.sidebar:
    st.header("Input Options")
    input_text = st.text_input("Input Prompt:", key="input", placeholder="Describe your health goal...")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image 
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)



submit = st.button("Show facts", key="calorie_button")

st.markdown("""
    <style>
        .custom-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Define input prompt with informative structure
input_prompt = """
Analyze the food items in the image and provide the following information:

 You are an expert in field of nutrition where you need to see the food items from the image
               and calculate the total calories, protein, fats, carbohydrates, etc also provide the details of every food items with calories intake
               is below format

               1. Item 1 - All the information
               2. Item 2 - All the information
               ----
               ----
               ----


also other nutritional things about image and also provide information in paragrapgh if asked in input prommpt,

You are the expert in this field so you have to give output according to the input prompt.
answer should be accurate and readable.

"""

# Process response upon button click
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)

    # Display results in a visually appealing format using pandas DataFrame
    if response.empty:
        st.subheader("The Response is:")
        st.write("No food items were detected in the image.")
    else:
        st.subheader("Nutrition Information:")

        # Display the DataFrame with adjusted display settings for better visibility
        st.dataframe(response)
