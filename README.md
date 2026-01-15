🧠 AI Resume Screener (Flask Web App)

An AI-powered resume screening tool that analyzes multiple resumes against a job description and generates ATS-style PDF reports with match scores, found skills, and missing skills.

Perfect for recruiters, HR teams, startups, or freelancers providing resume analysis services.

🚀 Features

Upload multiple resumes (PDF or DOCX)

Upload job description file

Extracts text from resumes

Matches skills automatically from a predefined skills list

Calculates match score using TF-IDF + cosine similarity

Generates professional PDF ATS reports

Ranks resumes by match score

Download PDF reports directly from the web interface

Works on local machine or can be deployed online

🛠 Tech Stack

Python

Flask

scikit-learn

PyPDF

docx2txt

FPDF

📁 Project Structure
AI_Resume_Screener/
│
├── app.py                   # Main Flask application
├── templates/
│   └── index.html           # Web interface template
├── uploads/                 # Temporary uploaded resumes and job files
├── reports/                 # Generated PDF reports
└── README.md

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/anglin123/AI-RESUME-SCREENER-SYSTEM.git
cd AI-RESUME-SCREENER-SYSTEM

2️⃣ Install dependencies
pip install flask scikit-learn pypdf docx2txt fpdf

▶️ How to Run
python app.py


Open in browser:

http://127.0.0.1:5000

📌 How to Use

Upload the job description file (.txt)

Upload one or more resumes (.pdf or .docx)

Click Submit

View the match score, found skills, and missing skills

Download the professional PDF report for each resume

📊 Output Example
Resume Name	Match Score	Found Skills	Missing Skills
John_Doe.pdf	82.4%	python, machine learning	aws, docker
Jane_Smith.pdf	71.2%	python, sql	tensorflow, aws
Mark_Taylor.pdf	55.6%	python	sql, tensorflow

Each resume gets a PDF report like:

John_Doe_report.pdf

🎯 Use Cases

HR teams screening candidates

Startups hiring engineers

Freelancers offering resume analysis services on Fiverr

Students building AI portfolios

👨‍💻 Author

Angelin Abisha
AI & Data Science Student
GitHub: https://github.com/anglin123
