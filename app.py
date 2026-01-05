from flask import Flask, render_template, request, send_from_directory
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import os

app = Flask(__name__)

# Folder for PDF reports
REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

skills_list = [
    "python", "java", "c++", "sql", "excel", "power bi", "tableau",
    "tensorflow", "pytorch", "scikit-learn", "nlp", "machine learning",
    "deep learning", "aws", "azure", "linux", "git", "docker"
]

def create_pdf(resume_name, score, found_skills, missing_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"ATS Resume Report - {resume_name}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Match Score: {score}%", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Skills Found: {', '.join(found_skills)}")
    pdf.ln(2)
    pdf.multi_cell(0, 10, f"Missing Skills: {', '.join(missing_skills)}")

    filename = f"{resume_name}_report.pdf".replace(" ", "_")
    filepath = os.path.join(REPORT_FOLDER, filename)
    pdf.output(filepath)
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        job_file = request.files["job"]
        job_file.save("temp_job.txt")
        with open("temp_job.txt", "r", encoding="utf-8") as f:
            job_text = f.read().lower()

        resume_files = request.files.getlist("resumes")

        for i, resume_file in enumerate(resume_files, start=1):
            filename = f"temp_resume_{i}.docx"
            resume_file.save(filename)
            resume_text = docx2txt.process(filename).lower()

            resume_skills = [skill for skill in skills_list if skill in resume_text]
            job_skills = [skill for skill in skills_list if skill in job_text]
            missing_skills = [skill for skill in job_skills if skill not in resume_skills]

            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([resume_text, job_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            score = round(similarity * 100, 2)

            pdf_file = create_pdf(resume_file.filename, score, resume_skills, missing_skills)

            results.append({
                "file": resume_file.filename,
                "score": score,
                "found_skills": resume_skills,
                "missing_skills": missing_skills,
                "pdf_report": pdf_file
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

    return render_template("index.html", results=results)

# Serve PDF files
@app.route("/reports/<filename>")
def download_pdf(filename):
    return send_from_directory(REPORT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
