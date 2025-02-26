import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os
import zipfile

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
                
                download_results(name, reg_no, image1, image2, processed_images)

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

def download_results(name, reg_no, image1, image2, processed_images):
    with tempfile.TemporaryDirectory() as temp_dir:
        filename_prefix = f"{reg_no}_{name}" if name and reg_no else "processed_images"
        zip_filename = os.path.join(temp_dir, f"{filename_prefix}.zip")
        
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            image1_path = os.path.join(temp_dir, "image1.jpg")
            image2_path = os.path.join(temp_dir, "image2.jpg")
            image1.save(image1_path, format="JPEG")
            image2.save(image2_path, format="JPEG")
            zipf.write(image1_path, "image1.jpg")
            zipf.write(image2_path, "image2.jpg")
            
            for op_name, img_array in processed_images.items():
                img_path = os.path.join(temp_dir, f"{op_name.lower()}.jpg")
                Image.fromarray(img_array).save(img_path, format="JPEG")
                zipf.write(img_path, f"{op_name.lower()}.jpg")
        
        with open(zip_filename, "rb") as f:
            st.download_button(
                label="Download All Processed Images as ZIP",
                data=f.read(),
                file_name=f"{filename_prefix}.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
