import streamlit as st
import pdfplumber
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

nltk.download("punkt")
nltk.download("stopwords")

# -----------------------------------------------------
# SKILL DICTIONARIES
# -----------------------------------------------------

TECH_SKILLS = [
    "python", "java", "c++", "sql", "mysql", "mongodb", "django", "flask",
    "fastapi", "react", "nextjs", "nodejs", "express", "aws", "docker",
    "kubernetes", "pandas", "numpy", "machine", "learning", "ml", "nlp",
    "rest", "api", "html", "css", "javascript", "git", "github"
]

SOFT_SKILLS = [
    "teamwork", "leadership", "communication", "problem-solving",
    "critical", "collaboration"
]

# -----------------------------------------------------
# PAGE STYLE
# -----------------------------------------------------

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

page_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

body {
    background: #f5f7fa;
    font-family: 'Segoe UI', sans-serif;
}

.header {
    background: linear-gradient(90deg, #4B79A1, #283E51);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.score-box {
    background: #e8f0fe;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #1a73e8;
    box-shadow: 0px 4px 10px rgba(66,133,244,0.2);
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# -----------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    return " ".join(tokens)


def extract_clean_keywords(text):
    text = text.lower()
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]+\b", text)

    stop_words = set(stopwords.words("english"))
    filtered = [w for w in words if w not in stop_words]

    return filtered


def get_professional_keywords(words):
    extracted = set()

    for w in words:
        if w in TECH_SKILLS or w in SOFT_SKILLS:
            extracted.add(w)

    return list(extracted)


def find_missing_keywords(resume_text, jd_text):
    resume_words = extract_clean_keywords(resume_text)
    jd_words = extract_clean_keywords(jd_text)

    professional_jd_keywords = get_professional_keywords(jd_words)
    professional_resume_keywords = get_professional_keywords(resume_words)

    missing = list(set(professional_jd_keywords) - set(professional_resume_keywords))
    return missing


def calculate_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)


def generate_ai_suggestions(missing_keywords):
    suggestions = []

    for kw in missing_keywords:
        if kw in TECH_SKILLS:
            suggestions.append(
                f"Add **{kw}** in your Technical Skills section and mention a project where you used {kw}."
            )
        elif kw in SOFT_SKILLS:
            suggestions.append(
                f"Highlight **{kw}** in your Summary or Experience bullet points."
            )
        else:
            suggestions.append(
                f"Include **{kw}** naturally inside your project descriptions or responsibilities."
            )

    return suggestions


# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.markdown(
    "<div class='header'><h1>📄 AI Resume Matcher</h1><p>Compare your resume with job descriptions using AI-powered matching.</p></div>",
    unsafe_allow_html=True,
)

# -----------------------------------------------------
# INPUT SECTION
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    resume_file = st.file_uploader("📁 Upload Resume (PDF)", type=["pdf"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    jd_text = st.text_area("📝 Paste Job Description Here")
    st.markdown("</div>", unsafe_allow_html=True)

# BUTTON
center = st.columns([1, 2, 1])
with center[1]:
    match_clicked = st.button("🔍 Generate Match Score", use_container_width=True)

# -----------------------------------------------------
# OUTPUT
# -----------------------------------------------------

if match_clicked:
    if resume_file is None or jd_text.strip() == "":
        st.error("⚠️ Please upload a resume and enter a job description.")
    else:

        resume_text = preprocess(extract_text_from_pdf(resume_file))
        jd_processed = preprocess(jd_text)

        score = calculate_similarity(resume_text, jd_processed)
        missing = find_missing_keywords(resume_text, jd_processed)

        # SCORE
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Match Score")
        st.markdown(f"<div class='score-box'>{score}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # MISSING KEYWORDS
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("❌ Missing Professional Keywords")
        st.write(", ".join(missing) if missing else "🎉 No missing keywords!")
        st.markdown("</div>", unsafe_allow_html=True)

        # AI Suggestions
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💡 AI Suggestions to Improve Your Resume")

        ai_suggestions = generate_ai_suggestions(missing)
        if ai_suggestions:
            for s in ai_suggestions:
                st.markdown(f"✔ {s}")
        else:
            st.success("🎉 Your resume looks highly relevant to the job description!")

        st.markdown("</div>", unsafe_allow_html=True)
