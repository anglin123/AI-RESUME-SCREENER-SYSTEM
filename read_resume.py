import os
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Job description ----------
with open("job.txt", "r") as f:
    job_text = f.read().lower()

# ---------- Skills list ----------
skills_list = [
    "python", "java", "c++", "sql", "excel", "power bi", "tableau",
    "tensorflow", "pytorch", "scikit-learn", "nlp", "machine learning",
    "deep learning", "aws", "azure", "linux", "git", "docker"
]

# ---------- Process resumes ----------
resumes_folder = "resume"
results = []

for file in os.listdir(resumes_folder):
    if file.endswith(".docx"):
        path = os.path.join(resumes_folder, file)
        resume_text = docx2txt.process(path).lower()
        
        # Skills found
        resume_skills = [skill for skill in skills_list if skill in resume_text]
        job_skills = [skill for skill in skills_list if skill in job_text]
        missing_skills = [skill for skill in job_skills if skill not in resume_skills]
        
        # Match score
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_text, job_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        results.append({
            "file": file,
            "score": similarity,
            "found_skills": resume_skills,
            "missing_skills": missing_skills
        })

# ---------- Rank resumes ----------
results = sorted(results, key=lambda x: x["score"], reverse=True)

# ---------- Print results ----------
for i, r in enumerate(results, start=1):
    print(f"🏆 Rank {i}: {r['file']}")
    print(f"   ✅ Match Score: {r['score']*100:.2f}%")
    print(f"   💡 Skills Found: {r['found_skills']}")
    print(f"   ⚠️ Missing Skills: {r['missing_skills']}\n")
