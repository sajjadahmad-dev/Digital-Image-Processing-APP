import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Digital Image Processing", page_icon="🎨", layout="wide")

def apply_custom_css():
    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    pdf_path = temp_file.name
    
    with tempfile.TemporaryDirectory() as temp_dir:
        img1_path = os.path.join(temp_dir, "image1.jpg")
        img2_path = os.path.join(temp_dir, "image2.jpg")
        Image.fromarray(img_array1).save(img1_path, format="JPEG")
        Image.fromarray(img_array2).save(img2_path, format="JPEG")
        
        processed_paths = {}
        for op_name, img_array in processed_images.items():
            img_path = os.path.join(temp_dir, f"{op_name.lower()}.jpg")
            Image.fromarray(img_array).save(img_path, format="JPEG")
            processed_paths[op_name] = img_path
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Digital Image Processing Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Name: {name}")
        c.drawString(50, height - 100, f"Registration Number: {reg_no}")
        c.drawString(50, height - 130, "Original Images:")
        c.drawImage(img1_path, 50, height - 330, width=(width-100)/2, height=180, preserveAspectRatio=True)
        c.drawString(50, height - 350, "Image One")
        c.drawImage(img2_path, width/2, height - 330, width=(width-100)/2, height=180, preserveAspectRatio=True)
        c.drawString(width/2, height - 350, "Image Two")
        
        for operation, img_path in processed_paths.items():
            c.showPage()
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Digital Image Processing Report")
            c.setFont("Helvetica", 14)
            c.drawString(50, height - 80, f"{operation} Operation:")
            img_width = (width-120)/3
            img_height = 180
            c.drawImage(img1_path, 50, height - 280, width=img_width, height=img_height, preserveAspectRatio=True)
            c.drawString(50, height - 300, "Image One")
            c.drawImage(img2_path, 60 + img_width, height - 280, width=img_width, height=img_height, preserveAspectRatio=True)
            c.drawString(60 + img_width, height - 300, "Image Two")
            c.drawImage(img_path, 70 + img_width*2, height - 280, width=img_width, height=img_height, preserveAspectRatio=True)
            c.drawString(70 + img_width*2, height - 300, "Result")
        c.save()
    
    return pdf_path

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

def main():
    apply_custom_css()
    st.title("🎨 Digital Image Processing System")
    
    name = st.text_input("Enter your name")
    reg_no = st.text_input("Enter your registration number (Format: 2000-AG-1000)")
    uploaded_file1 = st.file_uploader("Choose first image...", type=["jpg", "jpeg", "png"])
    uploaded_file2 = st.file_uploader("Choose second image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2 and name and reg_no:
        image1 = Image.open(uploaded_file1).convert('RGB')
        image2 = Image.open(uploaded_file2).convert('RGB').resize(image1.size)
        img_array1 = np.array(image1)
        img_array2 = np.array(image2)
        
        addition = st.checkbox("Addition")
        subtraction = st.checkbox("Subtraction")
        multiplication = st.checkbox("Multiplication")
        division = st.checkbox("Division")
        weight = st.slider("Weight factor", 0.0, 1.0, 0.5, step=0.1)
        
        if st.button("Process Images"):
            processed_images = {}
            if addition:
                processed_images["Addition"] = apply_operation(img_array1, img_array2, "Addition", weight)
            if subtraction:
                processed_images["Subtraction"] = apply_operation(img_array1, img_array2, "Subtraction", weight)
            if multiplication:
                processed_images["Multiplication"] = apply_operation(img_array1, img_array2, "Multiplication", weight)
            if division:
                processed_images["Division"] = apply_operation(img_array1, img_array2, "Division", weight)
            
            pdf_path = create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF Report", f, file_name="Image_Processing_Report.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
