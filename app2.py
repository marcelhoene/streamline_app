import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv
import os



import streamlit as st

if 'upload_field_count' not in st.session_state:
    st.session_state.upload_field_count = 1

if "files" not in st.session_state:
    st.session_state.files = [None] * st.session_state.upload_field_count

## Streamlit App ###



st.header("Upload all your files")

new_files = False

for i in range(st.session_state.upload_field_count):
    upload = st.file_uploader(label="Laden Sie hier Ihre Dokumente hoch", key=i)
    if upload is not None and st.session_state.files[i] is None:
        st.session_state.files[i] = upload
        new_files = True

if new_files:
    st.session_state.upload_field_count += 1
    st.session_state.files.append(None)
    st.rerun
