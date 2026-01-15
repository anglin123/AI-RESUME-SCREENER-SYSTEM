🧠 AI Resume Screener (Flask Web App)

An AI-powered web application that automatically analyzes resumes against a job description and generates an ATS-style report with match score, found skills, and missing skills.

This tool helps recruiters, HR teams, and startups quickly shortlist the best candidates from multiple resumes.

🚀 Features

Upload multiple resumes (PDF or DOCX)

Upload job description

Extracts text from resumes

Uses NLP + Machine Learning to calculate match score

Finds skills present & missing

Generates downloadable PDF ATS reports

Ranks resumes automatically

Simple web interface using Flask

🛠 Tech Stack

Python

Flask

scikit-learn

PyPDF

docx2txt

FPDF

NLP (TF-IDF + Cosine Similarity)

📁 Project Structure
AI_Resume_Screener/
│
├── app.py
├── templates/
│   └── index.html
├── uploads/
├── reports/
└── README.md

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/anglin123/AI_Resume_Screener_Final.git
cd AI_Resume_Screener_Final

2️⃣ Install required libraries
pip install flask scikit-learn pypdf docx2txt fpdf

▶️ How to Run
python app.py


Open in browser:

http://127.0.0.1:5000

📌 How to Use

Upload the job description file

Upload multiple resume files (PDF or DOCX)

Click Submit

The system will:

Calculate match percentage

Show found & missing skills

Generate a downloadable PDF report for each resume

Download ATS reports from the results page

📊 Output Example
John_Doe.pdf → 82.4%
Jane_Smith.pdf → 71.2%
Mark_Taylor.pdf → 55.6%


Each resume also gets a professional ATS PDF report.

🎯 Use Cases

HR teams screening candidates

Startups hiring engineers

Recruiters

Fiverr resume analysis services

Students building AI portfolios

👨‍💻 Author

Angelin Abisha
AI & Data Science Student
GitHub: https://github.com/anglin123