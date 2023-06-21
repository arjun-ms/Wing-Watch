import streamlit as st
import streamlit_authenticator as stauth

import pickle

from fastai.vision.all import *
from PIL import Image

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

from details import find_details
from voice import audio_predict

# Set page title
st.set_page_config(page_title="Wing Watch")

import yaml
from yaml.loader import SafeLoader


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


def login_page():
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.write(f'Welcome *{name}*')
        prediction_page()
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.error('Please register a user first')


def register_page():
    st.title("Register")
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            # login_page()
    except Exception as e:
        st.error(e)
        

# Image Prediction
def predict(path):
    model_inf = load_learner('525-species-v1.pkl')
    pred_class = model_inf.predict(path)
    return pred_class[0]


# Define page content
def prediction_page():
    st.title("Wing Watch 🐦🔍")

    # Display file uploader widgets for image and audio files
    uploaded_image_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    uploaded_audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

    authenticator.logout('Logout', 'main', key='unique_key')
    # Check if at least one file is uploaded before displaying submit button
    if uploaded_image_file is not None or uploaded_audio_file is not None:
        # Display submit button
        if st.button("Submit"):
            # Check if at least one file is uploaded before displaying success message
            if uploaded_image_file is not None or uploaded_audio_file is not None:
                st.success("Files uploaded")

                if uploaded_image_file is not None:
                    img = Image.open(uploaded_image_file)
                    with open(f"test/{uploaded_image_file.name}", "wb") as f:
                        f.write(uploaded_image_file.getbuffer())
                    # Perform prediction
                    prediction = predict(f"test/{uploaded_image_file.name}")
                    details = find_details(prediction)
                    # Display the predicted class
                    st.image(img, caption=prediction)
                    st.markdown(f"The predicted bird is: **{prediction}**")
                    st.markdown(details)
                elif uploaded_audio_file is not None:

                    # Provide a play button for the audio file
                    st.write("Play the audio:")
                    st.audio(uploaded_audio_file, format='audio/ogg')

                    prediction = audio_predict(uploaded_audio_file)
                    details = find_details(prediction)
                    st.markdown(f"The predicted bird is: **{prediction}**")
                    st.markdown(details)
                    
            else:
                st.error("Please upload an image or audio file")
    else:
        st.error("Please upload an image or audio file")


# Run the app
if __name__ == "__main__":
    page_options = ["Login", "Register"]
    selected_page = st.sidebar.radio("Select Page", page_options)

    if selected_page == "Login":
        login_page()
    elif selected_page == "Register":
        register_page()
