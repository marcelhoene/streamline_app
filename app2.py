import streamlit as st
import os

# Everything is accessible via the st.secrets dict:
st.write("DB username:", st.secrets.db_username)
st.write("DB password:", st.secrets.db_password)

