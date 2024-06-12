from pypdf import PdfReader
import streamlit as st

reader = PdfReader("/Users/marcelhoene/Python/Bewerbungsbot/Lebenslauf komplett .pdf")
page = reader.pages[0]


st.write(page.extract_text())
