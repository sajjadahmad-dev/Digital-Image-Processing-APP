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
        
        if st.button("Download PDF"):
            try:
                with st.spinner("Generating PDF..."):
                    pdf_path = create_two_image_pdf(name, reg_no, img_array1, img_array2)
                    
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    
                    os.remove(pdf_path)
                
                st.success("PDF Generated Successfully! Download Below:")
                
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name=f"{reg_no}_image_processing.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

def create_two_image_pdf(name, reg_no, img_array1, img_array2):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    pdf_path = temp_file.name
    
    with tempfile.TemporaryDirectory() as temp_dir:
        img1_path = os.path.join(temp_dir, "image1.jpg")
        img2_path = os.path.join(temp_dir, "image2.jpg")
        Image.fromarray(img_array1).save(img1_path, format="JPEG")
        Image.fromarray(img_array2).save(img2_path, format="JPEG")
        
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
        
        c.save()
    
    return pdf_path

if __name__ == "__main__":
    main()
