import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="AI Document Analyzer",
    page_icon="📄"
)

st.title("AI Document Analyzer")
st.write("Upload a PDF document and analyze it with AI.")

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(f"File uploaded successfully: {uploaded_file.name}")

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if text.strip():
        st.subheader("Extracted Text")

        st.text_area(
            "PDF Content",
            text,
            height=300
        )

        if not API_KEY:
            st.error("GEMINI_API_KEY was not found.")

        else:
            if st.button("Analyze Document"):

                with st.spinner("Analyzing document..."):

                    client = genai.Client(api_key=API_KEY)

                    prompt = f"""
                    Analyze the following document.

                    Provide:
                    1. A short summary
                    2. The main key points
                    3. Important information or conclusions
                    4. The likely document type

                    Document:
                    {text}
                    """

                    interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=prompt,
                        generation_config={
                            "thinking_level": "low"
                        }
                    )

                    st.subheader("AI Analysis")
                    st.write(interaction.output_text)

    else:
        st.warning("No readable text was found in this PDF.")
        