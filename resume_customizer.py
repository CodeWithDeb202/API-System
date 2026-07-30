import os
import google.generativeai as genai
from docx import Document
from docx2pdf import convert
from lock_util import com_lock

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def customize_resume_with_ai(candidate_docx, job_description, output_pdf_path):
    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))

    prompt = f"""
    You are an expert tech resume writer. Rewrite the professional summary and technical skills section 
    for an entry-level Full Stack Developer resume to closely align with this Job Description.
    Keep the text concise, sharp, and brief so that the final output easily fits onto a strict SINGLE PAGE layout.
    Avoid overly long paragraphs or excessive bullet points. Also make ATS scrore higher than 90%.

    Job Description:
    {job_description}
    """

    response = model.generate_content(prompt)
    custom_text = response.text

    doc = Document(candidate_docx)

    # Insert tailored highlights compactly
    doc.paragraphs[0].insert_paragraph_before(f"TAILORED HIGHLIGHTS:\n{custom_text[:300]}\n")
    
    temp_docx = output_pdf_path.replace(".pdf", ".docx")
    doc.save(temp_docx)

    with com_lock:
        convert(temp_docx, output_pdf_path)

    if os.path.exists(temp_docx):
        os.remove(temp_docx)

    return output_pdf_path