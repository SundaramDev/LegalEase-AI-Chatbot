# step1 : Setup Upload PDF functionality

import streamlit as st

uploaded_file = st.file_uploader("Upload PDF",
                                 type="pdf",
                                 accept_multiple_files=True)


# step2: Chatbot Skeleton (Questions & answer)
user_query = st.text_area("Enter your prompt: ", height=150, placeholder="Aks Anything!")

