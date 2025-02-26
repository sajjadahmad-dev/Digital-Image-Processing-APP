import streamlit as st
import numpy as np
from PIL import Image
import tempfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Custom CSS for simple and minimal colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;  /* White background */
    }
    .stHeader {
        color: #2c3e50;  /* Dark blue for headers */
        font-size: 28px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #3498db;  /* Blue for buttons */
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #2980b9;  /* Darker blue on hover */
    }
    .stTextInput>div>div>input {
        background-color: #ecf0f1;  /* Light gray for input fields */
        color: #2c3e50;
    }
    .stCheckbox>label {
        color: #2c3e50;  /* Dark blue for checkbox labels */
    }
    .stSlider>div>div>div>div {
        background-color: #3498db;  /* Blue for slider */
    }
    </style

# Custom CSS for a clean and modern UI
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stHeader {
        color: #4A90E2;
        font-size: 28px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #000000;
    }
    .stCheckbox>label {
        color: #000000;
    }
    .stSlider>div>div>div>div {
        background-color: #4A90E2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("📷 Digital Image Processing System")
    
    # Sidebar for user input
    st.sidebar.header("User Information")
    name = st.sidebar.text_input("Enter your name")
    reg_no = st.sidebar.text_input("Enter your registration number (Format: 2000-AG-1000)")
    
    # Validate registration number
    is_valid_reg = False
    if reg_no:
        import re
        pattern = r'^[0-9]{4}-[aA][gG]-[0-9]{4}$'
        is_valid_reg = bool(re.match(pattern, reg_no))
        if not is_valid_reg:
            st.sidebar.error("Please enter a valid registration number in the format 2000-AG-1000")
    
    # Image upload
    st.sidebar.header("Upload Images")
    uploaded_file1 = st.sidebar.file_uploader("Choose first image", type=["jpg", "jpeg", "png"])
    uploaded_file2 = st.sidebar.file_uploader("Choose second image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file1 and uploaded_file2 and name and is_valid_reg:
        image1 = Image.open(uploaded_file1).convert('RGB')
        image2 = Image.open(uploaded_file2).convert('RGB')
        image2 = image2.resize(image1.size)
        img_array1 = np.array(image1)
        img_array2 = np.array(image2)
        
        # Display original images
        st.subheader("Original Images")
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="Image One", use_column_width=True)
        with col2:
            st.image(image2, caption="Image Two", use_column_width=True)
        
        # Image operations
        st.subheader("Image Operations")
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
                
                # Display processed images
                for operation, result_img in processed_images.items():
                    st.subheader(f"{operation} Result")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(image1, caption="Image One", use_column_width=True)
                    with col2:
                        st.image(image2, caption="Image Two", use_column_width=True)
                    with col3:
                        st.image(result_img, caption="Result", use_column_width=True)
                
                # Generate and download PDF
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
