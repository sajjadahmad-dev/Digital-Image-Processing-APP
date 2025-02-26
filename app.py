import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os

st.set_page_config(page_title="Digital Image Processing", page_icon="🎨", layout="wide")

def apply_custom_css():
    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
            }
            .stApp {
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                color: white;
            }
            .stTextInput>div>div>input {
                background-color: #fff;
                color: black;
                border-radius: 10px;
                padding: 10px;
            }
            .stFileUploader>div {
                background-color: #fff;
                padding: 10px;
                border-radius: 10px;
            }
            .css-1aumxhk {
                font-size: 24px !important;
                font-weight: bold;
            }
            .css-2trqyj {
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    apply_custom_css()
    
    st.title("🎨 Digital Image Processing System")
    
    st.sidebar.header("User Information")
    name = st.sidebar.text_input("Enter your name")
    reg_no = st.sidebar.text_input("Enter your registration number (Format: 2000-AG-1000)")
    
    is_valid_reg = False
    if reg_no:
        import re
        pattern = r'^\d{4}-[aA][gG]-\d{4}$'
        is_valid_reg = bool(re.match(pattern, reg_no))
        if not is_valid_reg:
            st.sidebar.error("⚠ Please enter a valid registration number in the format 2000-AG-1000")
    
    st.header("📤 Upload Images")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file1 = st.file_uploader("Choose first image...", type=["jpg", "jpeg", "png"])
    with col2:
        uploaded_file2 = st.file_uploader("Choose second image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2 and name and is_valid_reg:
        image1 = Image.open(uploaded_file1).convert('RGB')
        image2 = Image.open(uploaded_file2).convert('RGB').resize(image1.size)
        
        img_array1 = np.array(image1)
        img_array2 = np.array(image2)
        
        st.header("🖼 Original Images")
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="Image One", use_column_width=True)
        with col2:
            st.image(image2, caption="Image Two", use_column_width=True)
        
        st.header("⚙ Image Operations")
        select_all = st.checkbox("Select All Operations")
        addition = st.checkbox("Addition", value=select_all)
        subtraction = st.checkbox("Subtraction", value=select_all)
        multiplication = st.checkbox("Multiplication", value=select_all)
        division = st.checkbox("Division", value=select_all)
        
        weight = st.slider("🔀 Weight factor for Image One (0 to 1)", 0.0, 1.0, 0.5, step=0.1)
        
        if st.button("🚀 Process Images"):
            if not (addition or subtraction or multiplication or division):
                st.error("⚠ Please select at least one operation")
            else:
                processed_images = {}
                if addition:
                    processed_images["Addition"] = apply_operation(img_array1, img_array2, "Addition", weight)
                if subtraction:
                    processed_images["Subtraction"] = apply_operation(img_array1, img_array2, "Subtraction", weight)
                if multiplication:
                    processed_images["Multiplication"] = apply_operation(img_array1, img_array2, "Multiplication", weight)
                if division:
                    processed_images["Division"] = apply_operation(img_array1, img_array2, "Division", weight)
                
                for operation, result_img in processed_images.items():
                    st.subheader(f"📌 {operation} Result")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(image1, caption="Image One", use_column_width=True)
                    with col2:
                        st.image(image2, caption="Image Two", use_column_width=True)
                    with col3:
                        st.image(result_img, caption="Result", use_column_width=True)

def apply_operation(img_array1, img_array2, operation, weight=0.5):
    img1_float = img_array1.astype(np.float32)
    img2_float = img_array2.astype(np.float32)
    if operation == "Addition":
        result = np.clip(weight * img1_float + (1 - weight) * img2_float, 0, 255)
    elif operation == "Subtraction":
        result = np.clip(weight * img1_float - (1 - weight) * img2_float, 0, 255)
    elif operation == "Multiplication":
        result = np.clip((img1_float * img2_float) / 255.0, 0, 255)
    elif operation == "Division":
        epsilon = 1e-10
        result = np.clip(img1_float / (img2_float + epsilon) * 127.5, 0, 255)
    return result.astype(np.uint8)

if __name__ == "__main__":
    main()
