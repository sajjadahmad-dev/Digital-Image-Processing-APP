import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os

# Custom CSS for a modern and beautiful UI
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #f5f7fa; /* Light gray background */
        color: #2c3e50;
    }

    /* Title Styling */
    .stMarkdown h1 {
        color: #2c3e50;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Headers */
    .stMarkdown h2 {
        color: #2980b9;
        font-size: 24px;
        font-weight: bold;
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #ecf0f1; /* Light gray */
        color: #2c3e50;
        border-radius: 8px;
        border: 1px solid #bdc3c7;
        padding: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }

    /* Checkboxes */
    .stCheckbox>label {
        color: #2c3e50;
        font-weight: bold;
    }

    /* Sidebar */
    .stSidebar {
        background-color: #2c3e50;
        color: white;
        padding: 20px;
    }

    /* Image columns */
    .stImage {
        border-radius: 8px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.markdown("<h1>📸 Digital Image Processing System</h1>", unsafe_allow_html=True)
    
    st.markdown("## 🧑‍💻 User Information")
    name = st.text_input("Enter your name")
    reg_no = st.text_input("Enter your registration number (Format: 2000-AG-1000)")

    is_valid_reg = False
    if reg_no:
        import re
        pattern = r'^\d{4}-[aA][gG]-\d{4}$'
        is_valid_reg = bool(re.match(pattern, reg_no))
        if not is_valid_reg:
            st.error("❌ Please enter a valid registration number in the format 2000-AG-1000")

    st.markdown("## 📂 Upload Images")
    
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

        st.markdown("## 🎨 Original Images")
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="🖼️ Image One", use_column_width=True)
        with col2:
            st.image(image2, caption="🖼️ Image Two", use_column_width=True)

        st.markdown("## ⚙️ Image Operations")
        select_all = st.checkbox("Select All Operations")
        addition = st.checkbox("➕ Addition", value=select_all)
        subtraction = st.checkbox("➖ Subtraction", value=select_all)
        multiplication = st.checkbox("✖️ Multiplication", value=select_all)
        division = st.checkbox("➗ Division", value=select_all)

        weight = st.slider("🎛️ Weight factor for Image One (0 to 1)", 0.0, 1.0, 0.5, step=0.1)

        if st.button("🚀 Process Images"):
            if not (addition or subtraction or multiplication or division):
                st.error("⚠️ Please select at least one operation")
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
                    st.markdown(f"### {operation} Result")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(image1, caption="📌 Image One", use_column_width=True)
                    with col2:
                        st.image(image2, caption="📌 Image Two", use_column_width=True)
                    with col3:
                        st.image(result_img, caption="✅ Result", use_column_width=True)

                try:
                    with st.spinner("📄 Generating PDF..."):
                        pdf_path = create_two_image_pdf(name, reg_no, img_array1, img_array2, processed_images)
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        os.remove(pdf_path)

                    st.success("✅ Processing complete! Download your PDF below.")
                    st.download_button(
                        label="📥 Download as PDF",
                        data=pdf_bytes,
                        file_name=f"{reg_no}_image_processing.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"⚠️ Error generating PDF: {str(e)}")

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

if __name__ == "__main__":
    main()
