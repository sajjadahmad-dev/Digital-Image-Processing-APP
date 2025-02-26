import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os
import re

def main():
    st.set_page_config(page_title="Digital Image Processing", layout="wide")
    st.markdown("""
        <style>
            .main {
                background-color: #f0f2f6;
            }
            h1, h2, h3 {
                color: #333366;
                text-align: center;
            }
            .stTextInput, .stFileUploader, .stCheckbox, .stButton, .stSlider {
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📸 Digital Image Processing System")
    st.subheader("🔹 Upload two images and apply various operations")
    
    with st.expander("👤 User Information", expanded=True):
        name = st.text_input("Enter your name")
        reg_no = st.text_input("Enter your registration number (Format: 2000-AG-1000)")
    
    is_valid_reg = bool(re.match(r'^\d{4}-[aA][gG]-\d{4}$', reg_no)) if reg_no else False
    if reg_no and not is_valid_reg:
        st.error("⚠️ Please enter a valid registration number in the format 2000-AG-1000")
    
    st.markdown("---")
    
    st.subheader("📂 Upload Images")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file1 = st.file_uploader("📥 Choose first image", type=["jpg", "jpeg", "png"])
    with col2:
        uploaded_file2 = st.file_uploader("📥 Choose second image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2 and name and is_valid_reg:
        image1 = Image.open(uploaded_file1).convert('RGB')
        image2 = Image.open(uploaded_file2).convert('RGB').resize(image1.size)
        img_array1, img_array2 = np.array(image1), np.array(image2)
        
        st.markdown("---")
        st.subheader("🖼️ Original Images")
        col1, col2 = st.columns(2)
        col1.image(image1, caption="Image One", use_column_width=True)
        col2.image(image2, caption="Image Two", use_column_width=True)
        
        st.markdown("---")
        st.subheader("⚙️ Image Operations")
        col1, col2 = st.columns(2)
        select_all = col1.checkbox("Select All Operations")
        weight = col2.slider("🔄 Weight factor for Image One", 0.0, 1.0, 0.5, step=0.1)
        
        operations = {
            "Addition": st.checkbox("➕ Addition", value=select_all),
            "Subtraction": st.checkbox("➖ Subtraction", value=select_all),
            "Multiplication": st.checkbox("✖️ Multiplication", value=select_all),
            "Division": st.checkbox("➗ Division", value=select_all)
        }
        
        if st.button("🚀 Process Images"):
            if not any(operations.values()):
                st.error("⚠️ Please select at least one operation")
            else:
                processed_images = {op: apply_operation_two_images(img_array1, img_array2, op, weight) for op, selected in operations.items() if selected}
                
                for op, result_img in processed_images.items():
                    st.subheader(f"🖼️ {op} Result")
                    col1, col2, col3 = st.columns(3)
                    col1.image(image1, caption="Image One", use_column_width=True)
                    col2.image(image2, caption="Image Two", use_column_width=True)
                    col3.image(result_img, caption="Result", use_column_width=True)
                
                with st.spinner("📄 Generating PDF..."):
                    pdf_path = create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images)
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    os.remove(pdf_path)
                    st.success("✅ Processing complete! Download your PDF below.")
                    st.download_button("📥 Download as PDF", data=pdf_bytes, file_name=f"{reg_no}_image_processing.pdf", mime="application/pdf")

def apply_operation_two_images(img_array1, img_array2, operation, weight=0.5):
    img1_float, img2_float = img_array1.astype(np.float32), img_array2.astype(np.float32)
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
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    pdf_path = temp_file.name
    
    with tempfile.TemporaryDirectory() as temp_dir:
        img1_path, img2_path = os.path.join(temp_dir, "image1.jpg"), os.path.join(temp_dir, "image2.jpg")
        Image.fromarray(img_array1).save(img1_path, format="JPEG")
        Image.fromarray(img_array2).save(img2_path, format="JPEG")
        
        processed_paths = {op: os.path.join(temp_dir, f"{op.lower()}.jpg") for op in processed_images}
        for op, img_array in processed_images.items():
            Image.fromarray(img_array).save(processed_paths[op], format="JPEG")
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Digital Image Processing Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Name: {name}")
        c.drawString(50, 710, f"Registration Number: {reg_no}")
        c.save()
    
    return pdf_path

if __name__ == "__main__":
    main()
