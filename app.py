import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def main():
    st.title("Digital Image Processing System")
    
    st.header("User Information")
    name = st.text_input("Enter your name")
    reg_no = st.text_input("Enter your registration number (Format: 2000-AG-1000)")
    
    is_valid_reg = validate_registration(reg_no) if reg_no else False
    if reg_no and not is_valid_reg:
        st.error("Please enter a valid registration number in the format 2000-AG-1000")
    
    st.header("Upload Images")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file1 = st.file_uploader("Choose first image...", type=["jpg", "jpeg", "png"])
    with col2:
        uploaded_file2 = st.file_uploader("Choose second image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2:
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
        operations = {"Addition": select_all, "Subtraction": select_all, "Multiplication": select_all, "Division": select_all}
        for op in operations.keys():
            operations[op] = st.checkbox(op, value=select_all)
        
        weight = st.slider("Weight factor for Image One (0 to 1)", 0.0, 1.0, 0.5, step=0.1)
        
        if st.button("Process Images"):
            if not any(operations.values()):
                st.error("Please select at least one operation")
            else:
                processed_images = {}
                for op, selected in operations.items():
                    if selected:
                        processed_images[op] = apply_operation_two_images(img_array1, img_array2, op, weight)
                
                pdf_path = create_pdf_report(name, reg_no, image1, image2, processed_images)
                with open(pdf_path, "rb") as f:
                    st.download_button("Download Report as PDF", f, file_name=f"{reg_no}_report.pdf", mime="application/pdf")

def validate_registration(reg_no):
    import re
    pattern = r'^\d{4}-[aA][gG]-\d{4}$'
    return bool(re.match(pattern, reg_no))

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

def create_pdf_report(name, reg_no, image1, image2, processed_images):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf_path = temp_file.name
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Digital Image Processing Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Name: {name}")
    c.drawString(50, height - 100, f"Registration Number: {reg_no}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        img1_path = os.path.join(temp_dir, "image1.jpg")
        img2_path = os.path.join(temp_dir, "image2.jpg")
        image1.save(img1_path, format="JPEG")
        image2.save(img2_path, format="JPEG")
        
        c.drawString(50, height - 130, "Original Images:")
        c.drawImage(img1_path, 50, height - 330, width=200, height=200, preserveAspectRatio=True)
        c.drawString(50, height - 350, "Image One")
        c.drawImage(img2_path, 300, height - 330, width=200, height=200, preserveAspectRatio=True)
        c.drawString(300, height - 350, "Image Two")
        
        for op_name, img_array in processed_images.items():
            c.showPage()
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Digital Image Processing Report")
            c.setFont("Helvetica", 14)
            c.drawString(50, height - 80, f"{op_name} Operation:")
            
            img_path = os.path.join(temp_dir, f"{op_name.lower()}.jpg")
            Image.fromarray(img_array).save(img_path, format="JPEG")
            
            c.drawImage(img1_path, 50, height - 280, width=150, height=150, preserveAspectRatio=True)
            c.drawString(50, height - 300, "Image One")
            c.drawImage(img2_path, 230, height - 280, width=150, height=150, preserveAspectRatio=True)
            c.drawString(230, height - 300, "Image Two")
            c.drawImage(img_path, 410, height - 280, width=150, height=150, preserveAspectRatio=True)
            c.drawString(410, height - 300, "Result")
            
        c.save()
    
    return pdf_path

if __name__ == "__main__":
    main()
