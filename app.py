import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

# Setzen Sie Ihren OpenAI-API-Schlüssel hier
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


#################### Globale Variablen  ####################
def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = [
            {"role": "system", "content": """du bist ein Motivationschreiben Ersteller,
                schreibe aus dem Lebenslauf und dem Zeugnis was du bekommst ein ansprechendes
                Motivationsschreiben für den Bewerber zu erstellen. Versuche dabei explizit
                die Stärken des Bewerbers mit den Anforderungen der Jobbeschreibung in Einklang zu bringen.
                Die Jobbeschreibung bekommst du in der zweiten Nachricht als Text übergeben. Wichtig ist, dass du nichts erfindest
                und alles mit den gegebenen Informationen belegst. Du sollst nur den reinen Text ausgeben, Kopf und Fußzeilen sind nicht nötig.
            """}
        ]
    if 'gpt_analysis' not in st.session_state:
        st.session_state.gpt_analysis = None


    if 'upload_field_count' not in st.session_state:
        st.session_state.upload_field_count = 1

    if "input_data" not in st.session_state:
        st.session_state.input_data = [None] * st.session_state.upload_field_count

    if "applicant_info" not in st.session_state:
        st.session_state.applicant_info = ''

initialize_session_state()

#################### Funktionen ####################

def extract_text_from_pdf(pdf_file):
    """Extrahiert Text aus einer PDF-Datei."""
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    return page.extract_text()
ß

def analyze_resume_with_gpt():
    """Analysiert den Lebenslauf mit GPT-4."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.chat_log,
    )
    st.session_state.chat_log.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

def concat_pdf_text():
    """Kombiniert den Text aus Lebenslauf und Zeugnis."""
    combined_text = []
    for file in st.session_state.input_data:
        if file is not None:
            if file.name.endswith(".pdf"):
                combined_text.append(extract_text_from_pdf(file))
    return " ".join(combined_text)


def pre_generated_page(job_description):
    """Seite für das Hochladen und Verarbeiten von PDF-Dateien."""
    if st.button("Motivationsschreiben erstellen"):
        final_text = concat_pdf_text()

        if not job_description:
            job_description = 'erstelle ein allgemeines Motivationsschreiben'

        if final_text:
            st.session_state.chat_log.append({"role": "user", "content": final_text})
            st.session_state.chat_log.append({"role": "user", "content": "Jobbeschreibung: " + job_description})
            st.session_state.gpt_analysis = analyze_resume_with_gpt()
            st.session_state.page = 'post'
            st.rerun()
        else:
            st.error("Bitte laden Sie Ihren Lebenslauf oder ihr Zeugnis hoch.")

        print("hallo")


def post_generated_page():
    """Seite für die Anzeige und Verbesserung des Motivationsschreibens."""
    for message in st.session_state.chat_log:
        if message['role'] =="assistant":
            st.write(message["content"],)
            st.write("---")

    improvements = st.text_area(label="Was wollen Sie verbessern?", height=200)
    if st.button("Motivationsschreiben verbessern"):
        st.session_state.chat_log.append({"role": "user", "content": "überarbeite das Motivationsschreiben mit folgenden Verbesserungen: " + improvements})
        st.session_state.gpt_analysis = analyze_resume_with_gpt()
        st.rerun()


def upload_section():
    st.header("Lasse dir ein Motivationsschreiben erstellen")

    new_files = False

    for i in range(st.session_state.upload_field_count):
        upload = st.file_uploader(label="Laden Sie hier Ihre Dokumente hoch (Zeugnisse, Lebenslauf, Urkunden etc.)", key=i)
        if upload is not None and st.session_state.input_data[i] is None:
            st.session_state.input_data[i] = upload
            new_files = True

    if new_files:
        st.session_state.upload_field_count += 1
        st.session_state.input_data.append(None)
        st.rerun()


    applicant_info=st.text_area(label= "Was muss ich Außerdem über dich wissen ?",placeholder= "Ich bin jemand der sich schnell in neue Aufgabenstellungen einarbeiten kann")
    st.session_state.chat_log.append({"role": "user", "content": f"Berücksichtige diese Infos bitte auch noch in dem Motivationsschreiben{ applicant_info}"})



################### Streamlit App ###################

def main():
    upload_section()
    job_description = st.text_area(label="Jobbeschreibung", height=200)
    st.write("---")

    if st.session_state.page == 'home':
        pre_generated_page(job_description)
    else:
        post_generated_page()

if __name__ == "__main__":
    main()
