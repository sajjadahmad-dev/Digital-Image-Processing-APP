import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def main():
    st.title("Digital Image Processing System")
    
    st.header("User Information")
    name = st.text_input("Enter your name")
    reg_no = st.text_input("Enter your registration number (Format: 2000-AG-1000)")
    
    is_valid_reg = False
    if reg_no:
        import re
        pattern = r'^\d{4}-[aA][gG]-\d{4}$'
        is_valid_reg = bool(re.match(pattern, reg_no))
        if not is_valid_reg:
            st.error("Please enter a valid registration number in the format 2000-AG-1000")
    
    st.header("Upload Images")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file1 = st.file_uploader("Choose first image...", type=["jpg", "jpeg", "png"])
    with col2:
        uploaded_file2 = st.file_uploader("Choose second image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2 and name and is_valid_reg:
        image1 = Image.open(uploaded_file1).convert('RGB')
        image2 = Image.open(uploaded_file2).convert('RGB')
        image2 = image2.resize(image1.size)
        img_array1 = np.array(image1)
        img_array2 = np.array(image2)
        
        st.header("Original Images")
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="Image One", use_column_width=True)
        with col2:
            st.image(image2, caption="Image Two", use_column_width=True)
        
        st.header("Image Operations")
        select_all = st.checkbox("Select All Operations")
        addition = st.checkbox("Addition", value=select_all)
        subtraction = st.checkbox("Subtraction", value=select_all)
        multiplication = st.checkbox("Multiplication", value=select_all)
        division = st.checkbox("Division", value=select_all)
        weight = st.slider("Weight factor for Image One (0 to 1)", 0.0, 1.0, 0.5, step=0.1)
        
        if st.button("Process Images"):
            if not (addition or subtraction or multiplication or division):
                st.error("Please select at least one operation")
            else:
                processed_images = {}
                if addition:
                    processed_images["Addition"] = apply_operation_two_images(img_array1, img_array2, "Addition", weight)
                if subtraction:
                    processed_images["Subtraction"] = apply_operation_two_images(img_array1, img_array2, "Subtraction", weight)
                if multiplication:
                    processed_images["Multiplication"] = apply_operation_two_images(img_array1, img_array2, "Multiplication", weight)
                if division:
                    processed_images["Division"] = apply_operation_two_images(img_array1, img_array2, "Division", weight)
                
                for operation, result_img in processed_images.items():
                    st.subheader(f"{operation} Result")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(image1, caption="Image One", use_column_width=True)
                    with col2:
                        st.image(image2, caption="Image Two", use_column_width=True)
                    with col3:
                        st.image(result_img, caption="Result", use_column_width=True)
                
                try:
                    with st.spinner("Generating PDF..."):
                        pdf_path = create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images)
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        os.remove(pdf_path)
                    st.success("Processing complete! Download your PDF below.")
                    st.download_button(label="Download as PDF", data=pdf_bytes, file_name=f"{reg_no}_image_processing.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

def apply_operation_two_images(img_array1, img_array2, operation, weight=0.5):
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

def create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    pdf_path = temp_file.name
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Digital Image Processing Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Name: {name}")
    c.drawString(50, 710, f"Registration Number: {reg_no}")
    c.showPage()
    c.save()
    return pdf_path

if __name__ == "__main__":
    main()


def main():
    st.title("Digital Image Processing System")
    
    st.header("User Information")
    name = st.text_input("Enter your name")
    reg_no = st.text_input("Enter your registration number (Format: 2000-AG-1000)")
    
    is_valid_reg = False
    if reg_no:
        import re
        pattern = r'^\d{4}-[aA][gG]-\d{4}$'
        is_valid_reg = bool(re.match(pattern, reg_no))
        if not is_valid_reg:
            st.error("Please enter a valid registration number in the format 2000-AG-1000")
    
    st.header("Upload Images")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file1 = st.file_uploader("Choose first image...", type=["jpg", "jpeg", "png"])
    with col2:
        uploaded_file2 = st.file_uploader("Choose second image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2 and name and is_valid_reg:
        image1 = Image.open(uploaded_file1).convert('RGB')
        image2 = Image.open(uploaded_file2).convert('RGB')
        image2 = image2.resize(image1.size)
        img_array1 = np.array(image1)
        img_array2 = np.array(image2)
        
        st.header("Original Images")
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="Image One", use_column_width=True)
        with col2:
            st.image(image2, caption="Image Two", use_column_width=True)
        
        st.header("Image Operations")
        select_all = st.checkbox("Select All Operations")
        addition = st.checkbox("Addition", value=select_all)
        subtraction = st.checkbox("Subtraction", value=select_all)
        multiplication = st.checkbox("Multiplication", value=select_all)
        division = st.checkbox("Division", value=select_all)
        weight = st.slider("Weight factor for Image One (0 to 1)", 0.0, 1.0, 0.5, step=0.1)
        
        if st.button("Process Images"):
            if not (addition or subtraction or multiplication or division):
                st.error("Please select at least one operation")
            else:
                processed_images = {}
                if addition:
                    processed_images["Addition"] = apply_operation_two_images(img_array1, img_array2, "Addition", weight)
                if subtraction:
                    processed_images["Subtraction"] = apply_operation_two_images(img_array1, img_array2, "Subtraction", weight)
                if multiplication:
                    processed_images["Multiplication"] = apply_operation_two_images(img_array1, img_array2, "Multiplication", weight)
                if division:
                    processed_images["Division"] = apply_operation_two_images(img_array1, img_array2, "Division", weight)
                
                for operation, result_img in processed_images.items():
                    st.subheader(f"{operation} Result")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(image1, caption="Image One", use_column_width=True)
                    with col2:
                        st.image(image2, caption="Image Two", use_column_width=True)
                    with col3:
                        st.image(result_img, caption="Result", use_column_width=True)
                
                try:
                    with st.spinner("Generating PDF..."):
                        pdf_path = create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images)
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        os.remove(pdf_path)
                    st.success("Processing complete! Download your PDF below.")
                    st.download_button(label="Download as PDF", data=pdf_bytes, file_name=f"{reg_no}_image_processing.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

def apply_operation_two_images(img_array1, img_array2, operation, weight=0.5):
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

def create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    pdf_path = temp_file.name
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Digital Image Processing Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Name: {name}")
    c.drawString(50, 710, f"Registration Number: {reg_no}")
    c.showPage()
    c.save()
    return pdf_path

if __name__ == "__main__":
    main()
