📄 AI Resume Matcher & Skill Gap Analyzer

An AI-powered web application that analyzes resumes, extracts key skills, compares them with job descriptions, and generates a relevance match score.
The app highlights missing technical/soft skills and provides actionable suggestions to improve resume quality.

🚀 Features

✔ Upload resume in PDF format
✔ Extract text using PDF parsing
✔ NLP-based cleaning and keyword extraction
✔ TF–IDF + Cosine Similarity for job match scoring
✔ Identifies missing professional skills
✔ Smart AI-style resume improvement suggestions
✔ User-friendly Streamlit UI
✔ Fast and lightweight — runs locally or deployable online

🧠 How It Works

User uploads a resume (PDF)

Resume text is extracted using pdfplumber

Job description text is provided by the user

Both texts are preprocessed using NLTK

TF-IDF vectors are created

Cosine similarity generates a match percentage

Missing technical & soft skills are identified

AI suggestions are generated for improving resume relevance

🛠️ Tech Stack

Frontend / UI: Streamlit
Backend Logic: Python
Libraries:

pdfplumber

scikit-learn

NLTK

Regular Expressions

TF-IDF Vectorizer

Cosine Similarity

📂 Project Structure
📁 ai-resume-matcher
 ├── app.py
 ├── requirements.txt
 ├── README.md

🔧 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/vaijanathwale/ai-resume-matcher.git
cd ai-resume-matcher

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
streamlit run app.py

🖼️ Screenshots
✔ Match Score
✔ Missing Keywords
✔ AI Suggestions

(Add your screenshot images here later)

🎯 Use Cases

Students applying for internships/placements

Job seekers improving resume-job relevance

Recruiters checking candidate-job match

Career guidance and resume optimization tools

📌 Future Enhancements (Optional)

OpenAI-powered advanced AI suggestions

Resume section-by-section breakdown

Visual skill graphs

Live job description scraping

Export report as PDF

Deployment on Streamlit Cloud / Render

🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

⭐ If you like this project, give it a star!

Your support motivates the development of more AI tools.

