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
        type=["jpg", "png", "jpeg"],
        key="person"
    )

    if person_file:

        person_img = Image.open(person_file).convert("RGBA")

        st.image(
            person_img,
            caption="Person Image",
            width=300
        )

# =====================================
# CLOTH IMAGE
# =====================================

with col2:

    st.subheader("Upload Clothing Image")

    cloth_file = st.file_uploader(
        "Choose cloth image",
        type=["jpg", "png", "jpeg"],
        key="cloth"
    )

    if cloth_file:

        cloth_img = Image.open(cloth_file).convert("RGBA")

        st.image(
            cloth_img,
            caption="Clothing Image",
            width=300
        )

# =====================================
# GENERATE RESULT
# =====================================

if st.button("Generate Virtual Try-On"):

    if person_img and cloth_img:

        # Resize person image
        person_img = person_img.resize(
            (400, 600)
        )

        # Resize cloth image
        cloth_img = cloth_img.resize(
            (180, 220)
        )

        # Overlay cloth onto person
        result = person_img.copy()

        result.paste(
            cloth_img,
            (110, 170),
            cloth_img
        )

        # Save result
        result.save(
            "static/final_output.png"
        )

        st.success(
            "Virtual Try-On Generated Successfully"
        )

        st.subheader(
            "Generated Result"
        )

        st.image(
            result,
            width=400
        )

        st.info(
            "Demo AI virtual try-on simulation running on Streamlit Cloud."
        )

    else:

        st.error(
            "Please upload both images."
        )
