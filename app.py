import streamlit as st
from pypdf import PdfReader
from groq import Groq

st.title("AI Document Q&A Assistant")

api_key = st.text_input("Enter your Groq API Key", type="password")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file and api_key:
    reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() or ""

    question = st.text_input("Ask a question about this PDF:")

    if question:
        client = Groq(api_key=api_key)
        prompt = f"Answer the question using only the text below.\n\nText:\n{pdf_text[:15000]}\n\nQuestion: {question}"
        
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write("### Answer:")
            st.write(response.choices[0].message.content)