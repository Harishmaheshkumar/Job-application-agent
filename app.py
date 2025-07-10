import streamlit as st
from fpdf import FPDF
import os

# Import your agent setup from main.py
from main import executor, parser
from langchain_core.messages import HumanMessage, AIMessage

def create_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.cell(0, 10, txt=line, ln=True)
    pdf.output(filename)

st.title("Job Application Agent")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "doc", "docx", "txt"])
job_desc = st.text_area("Paste the job description here:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file and job_desc:
    if st.button("Submit Application"):
        st.info("Processing your application...")
        resume_path = f"uploaded_{uploaded_file.name}"
        with open(resume_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded file: {uploaded_file.name}")

        # --- AGENT CALL ---
        response = executor.invoke({
    "resume_path": resume_path,        # This should be a real file path!
    "job_description": job_desc,       # This should be the pasted job description!
    "query": "Please tailor my resume and write a cover letter for this job.",
    "chat_history": st.session_state.chat_history,
})

        try:
            parsed = parser.parse(response.get("output"))
            result = {
                "job_title": parsed.job_title,
                "tailored_resume": parsed.tailored_resume,
                "cover_letter": parsed.cover_letter
            }
            st.session_state.chat_history.append(HumanMessage(content=job_desc))
            st.session_state.chat_history.append(AIMessage(content=parsed.cover_letter))
        except Exception as e:
            st.error(f"[Error parsing output]: {e}")
            st.write("Raw:", response.get("output"))
            st.stop()

        st.markdown(f"**You:** I want to apply to the role described in the job description.")
        st.markdown(f"**Job Title:** {result['job_title']}")
        st.markdown("📄 **Cover Letter Preview:**")
        st.text(result["cover_letter"])

        st.subheader("Tailored Resume Preview:")
        st.text(result["tailored_resume"])

        pdf_filename = "tailored_resume.pdf"
        create_pdf(result["tailored_resume"], pdf_filename)
        with open(pdf_filename, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Tailored Resume as PDF",
            data=PDFbyte,
            file_name=pdf_filename,
            mime='application/pdf'
        )
