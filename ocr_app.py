import streamlit as st
import pytesseract
import numpy as np
from PIL import Image
import cv2

# Set the path to the Tesseract executable (update this path as needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    # Convert the image to an array suitable for OpenCV
    img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Perform OCR on the image
    text = pytesseract.image_to_string(img_array, lang='hin+eng')  # Use 'hin+eng' for both Hindi and English
    return text

def search_keywords(text, keyword):
    if keyword:
        # Split the text into lines for better matching
        lines = text.split('\n')
        highlighted_lines = []

        # Check each line for the keyword
        for line in lines:
            if keyword.lower() in line.lower():  # Case-insensitive search
                # Highlight the keyword
                highlighted_line = line.replace(keyword, f"[{keyword}]")
                highlighted_lines.append(highlighted_line)
        
        # Join the highlighted lines if there are any, otherwise return "Keyword not found."
        return "\n".join(highlighted_lines) if highlighted_lines else "Keyword not found."
    return "Keyword not found."

# Streamlit app layout
st.title("OCR and Document Search Web Application")
st.write("Upload an image containing text in Hindi and English for OCR processing.")

# File uploader for image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract text from the image
    extracted_text = extract_text(image)
    st.subheader("Extracted Text:")
    st.write(extracted_text)
    
    # Keyword search
    keyword = st.text_input("Enter a keyword to search in the extracted text:")
    if keyword:
        search_result = search_keywords(extracted_text, keyword)
        st.subheader("Search Result:")
        st.write(search_result)

# Add footer
st.write("### Note:")
st.write("The text extraction might not be perfect. The accuracy of the OCR can depend on the quality of the image and the text.")
