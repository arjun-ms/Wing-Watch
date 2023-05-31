import streamlit as st

# Set page title
st.set_page_config(page_title="Wing Watch")

# Define page content
def page_content():
    # Display page header
    st.header("Wing Watch")

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
            else:
                st.error("Please upload an image or audio file")
    else:
        st.error("Please upload an image or audio file")

# Run the app
if __name__ == "__main__":
    page_content()
