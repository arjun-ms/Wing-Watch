import streamlit as st
from fastai.vision.all import *
from PIL import Image

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

from details import find_details

# Set page title
st.set_page_config(page_title="Wing Watch")

# Image Prediction
def predict(path):
    model_inf = load_learner('525-species-v1.pkl')
    pred_class = model_inf.predict(path)
    # print(pred_class[0])
    return pred_class[0]


# Define page content
def page_content():
    # Display page header
    st.title("Wing Watch 🦜")

    # Display file uploader widgets for image and audio files
    uploaded_image_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    uploaded_audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

    # Check if at least one file is uploaded before displaying submit button
    if uploaded_image_file is not None or uploaded_audio_file is not None:
        # Display submit button
        if st.button("Submit"):
            # Check if at least one file is uploaded before displaying success message
            if uploaded_image_file is not None or uploaded_audio_file is not None:
                st.success("Files uploaded")
                # st.write(uploaded_image_file)
                # print(type(uploaded_image_file))
                if uploaded_image_file is not None:
                    img = Image.open(uploaded_image_file)
                    with open(f"test/{uploaded_image_file.name}","wb") as f:
                        f.write(uploaded_image_file.getbuffer())
                    # Perform prediction
                    prediction = predict(f"test/{uploaded_image_file.name}")
                    details = find_details(prediction)
                    # Display the predicted class
                    st.markdown(f"The predicted bird is: **{prediction}**", )
                    st.markdown(details)
            else:
                st.error("Please upload an image or audio file")
    else:
        st.error("Please upload an image or audio file")

# Run the app
if __name__ == "__main__":
    page_content()
