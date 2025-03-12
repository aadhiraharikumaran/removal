import streamlit as st
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from PIL import Image
import requests
import io
import uuid
import os

# login to cloudinary and get your key from here - https://console.cloudinary.com/pm/c-a8f7a41e4832cf677e6d5fe5a83cff/getting-started

# Configure Cloudinary
cloudinary.config(
    cloud_name="ddqt2h08a",
    api_key="812972373143139",
    api_secret="lOIlsazZF6_Cry5l1Ta5Y0INf9w",
    secure=True
)

# Streamlit app for removing items using Cloudinary's Gen Remove
st.title("Image Item Removal with Cloudinary's Gen Remove")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Generate a unique filename to avoid caching issues
    unique_filename = f"temp_image_{uuid.uuid4().hex}.jpg"

    # Save uploaded file temporarily
    with open(unique_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image
    st.image(unique_filename, caption="Uploaded Image", use_column_width=True)

    # Input field for item to remove
    item_to_remove = st.text_input("Item to Remove", "bottle")

    # Generate button for removal
    if st.button("Remove Item"):
        # Upload the image to Cloudinary with a unique public ID
        public_id = f"me/rm-{uuid.uuid4().hex}"
        upload_result = cloudinary.uploader.upload(unique_filename, public_id=public_id)

        # Generate the removal image URL
        removal_effect = f"gen_remove:prompt_{item_to_remove};multiple_true"
        removed_image_url, _ = cloudinary_url(
            public_id,
            effect=removal_effect
        )

        # Load images
        original_image = Image.open(unique_filename)

        # Fetch the transformed image from the generated URL
        response = requests.get(removed_image_url)
        transformed_image = Image.open(io.BytesIO(response.content))

        # Display images
        st.subheader("Compare Images")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(original_image, caption="Original Image", use_column_width=True)
        with col2:
            st.image(transformed_image, caption="Transformed Image", use_column_width=True)

    # Clean up the temporary file
    os.remove(unique_filename)
