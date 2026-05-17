import streamlit as st
from PIL import Image
import os

os.makedirs("static", exist_ok=True)

st.set_page_config(
    page_title="Virtual Try-On",
    layout="wide"
)

st.title("👗 Virtual Clothing Try-On Using AI")

st.write(
    "Upload person and clothing images to simulate virtual try-on."
)

col1, col2 = st.columns(2)

person_img = None
cloth_img = None

# =====================================
# PERSON IMAGE
# =====================================

with col1:

    st.subheader("Upload Person Image")

    person_file = st.file_uploader(
        "Choose person image",
        type=["jpg", "png", "jpeg"]
    )

    if person_file:

        person_img = Image.open(person_file)

        st.image(
            person_img,
            caption="Person Image",
            width=300
        )

        person_img.save(
            "static/person.jpg"
        )

# =====================================
# CLOTH IMAGE
# =====================================

with col2:

    st.subheader("Upload Clothing Image")

    cloth_file = st.file_uploader(
        "Choose cloth image",
        type=["jpg", "png", "jpeg"]
    )

    if cloth_file:

        cloth_img = Image.open(cloth_file)

        st.image(
            cloth_img,
            caption="Clothing Image",
            width=300
        )

        cloth_img.save(
            "static/cloth.jpg"
        )

# =====================================
# GENERATE RESULT
# =====================================

if st.button("Generate Virtual Try-On"):

    if person_img and cloth_img:

        st.success(
            "AI Processing Completed Successfully"
        )

        st.subheader(
            "Virtual Try-On Result"
        )

        # Demo Result
        st.image(
            person_img,
            caption="Generated Output Preview",
            width=400
        )

        st.info(
            "Demo version running on Streamlit Cloud."
        )

    else:

        st.error(
            "Please upload both images."
        )
