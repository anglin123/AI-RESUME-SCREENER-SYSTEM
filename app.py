from flask import Flask, render_template, request, send_from_directory
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import os
from pypdf import PdfReader
from werkzeug.utils import secure_filename

# ------------------ CONFIG ------------------
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

skills_list = [
    "python", "java", "c++", "sql", "excel", "power bi", "tableau",
    "tensorflow", "pytorch", "scikit-learn", "nlp", "machine learning",
    "deep learning", "aws", "azure", "linux", "git", "docker"
]

# ------------------ PDF READER ------------------
def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ------------------ PDF REPORT ------------------
def create_pdf(resume_name, score, found_skills, missing_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ATS Resume Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Candidate: {resume_name}", ln=True)
    pdf.cell(0, 10, f"Match Score: {score}%", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Skills Found: {', '.join(found_skills) if found_skills else 'None'}")
    pdf.ln(2)
    pdf.multi_cell(0, 10, f"Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}")

    safe = secure_filename(resume_name)
    safe = safe.replace(".pdf", "").replace(".docx", "")
    filename = f"{safe}_report.pdf"
    filepath = os.path.join(REPORT_FOLDER, filename)
    print("PDF saved at:", filepath)
    pdf.output(filepath)


    return filename

# ------------------ MAIN PAGE ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        # Read Job Description
        job_file = request.files["job"]
        job_path = os.path.join(UPLOAD_FOLDER, "job.txt")
        job_file.save(job_path)

        with open(job_path, "r", encoding="utf-8") as f:
            job_text = f.read().lower()

        resume_files = request.files.getlist("resumes")

        for i, resume_file in enumerate(resume_files, start=1):
            safe_name = secure_filename(resume_file.filename)
            resume_path = os.path.join(UPLOAD_FOLDER, f"{i}_{safe_name}")
            resume_file.save(resume_path)

            # Read resume text
            if safe_name.lower().endswith(".pdf"):
                resume_text = extract_pdf_text(resume_path)
            else:
                resume_text = docx2txt.process(resume_path).lower()

            # Skill matching
            resume_skills = [skill for skill in skills_list if skill in resume_text]
            job_skills = [skill for skill in skills_list if skill in job_text]
            missing_skills = [skill for skill in job_skills if skill not in resume_skills]

            # Similarity
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([resume_text, job_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            score = round(similarity * 100, 2)

            # Create PDF
            pdf_file = create_pdf(safe_name, score, resume_skills, missing_skills)

            results.append({
                "file": safe_name,
                "score": score,
                "found_skills": resume_skills,
                "missing_skills": missing_skills,
                "pdf_report": pdf_file
            })

        results.sort(key=lambda x: x["score"], reverse=True)

    return render_template("index.html", results=results)

# ------------------ DOWNLOAD ------------------
from flask import abort

@app.route("/reports/<path:filename>")
def download_pdf(filename):
    file_path = os.path.join(REPORT_FOLDER, filename)

    print("Trying to download:", file_path)

    if not os.path.exists(file_path):
        print("File NOT found!")
        abort(404)

    return send_from_directory(REPORT_FOLDER, filename, as_attachment=True)



# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
