import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Usman MCQ Academy", page_icon="🎓", layout="wide")

DATA_FILE = "questions.json"
ADMIN_PASSWORD = os.getenv("QUIZ_ADMIN_PASSWORD", "admin123")

DEFAULT_QUESTIONS = [
    {"id": 1, "subject": "English", "topic": "Grammar", "question": "Choose the correct sentence.", "options": ["He go to school.", "He goes to school.", "He going school.", "He gone school."], "answer": 1, "explanation": "With he/she/it in the present simple, use goes."},
    {"id": 2, "subject": "Mathematics", "topic": "Arithmetic", "question": "What is 12 × 5?", "options": ["50", "60", "70", "80"], "answer": 1, "explanation": "12 multiplied by 5 equals 60."},
    {"id": 3, "subject": "General Knowledge", "topic": "Pakistan", "question": "What is the capital of Pakistan?", "options": ["Karachi", "Lahore", "Islamabad", "Peshawar"], "answer": 2, "explanation": "Islamabad is the capital of Pakistan."},
    {"id": 4, "subject": "Computer Science", "topic": "Basics", "question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing User"], "answer": 0, "explanation": "CPU stands for Central Processing Unit."},
    {"id": 5, "subject": "Biology", "topic": "Human Body", "question": "Which organ pumps blood?", "options": ["Lungs", "Brain", "Heart", "Kidney"], "answer": 2, "explanation": "The heart pumps blood through the body."},
    {"id": 6, "subject": "Physics", "topic": "Basics", "question": "What is the SI unit of force?", "options": ["Joule", "Newton", "Watt", "Pascal"], "answer": 1, "explanation": "Force is measured in newtons."},
    {"id": 7, "subject": "Chemistry", "topic": "Atoms", "question": "What is the chemical symbol for oxygen?", "options": ["Ox", "O", "C", "H"], "answer": 1, "explanation": "The chemical symbol for oxygen is O."},
    {"id": 8, "subject": "Islamiyat", "topic": "Basics", "question": "How many pillars of Islam are there?", "options": ["3", "4", "5", "6"], "answer": 2, "explanation": "Islam has five pillars."}
]

def load_questions():
    if not os.path.exists(DATA_FILE):
        save_questions(DEFAULT_QUESTIONS)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_QUESTIONS.copy()

def save_questions(questions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

def reset_test():
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.test_questions = []

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "test_questions" not in st.session_state:
    st.session_state.test_questions = []

questions = load_questions()

st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; text-align: center; color: #2563eb;}
.subtitle {text-align: center; font-size: 18px; color: #64748b;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 Usman MCQ Academy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Entry Test Preparation • Practice Tests • Explanations</div>', unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation", ["Home", "Practice Test", "All MCQs", "Admin Panel", "About"])

if menu == "Home":
    subjects = sorted({q["subject"] for q in questions})
    c1, c2, c3 = st.columns(3)
    c1.metric("Total MCQs", len(questions))
    c2.metric("Subjects", len(subjects))
    c3.metric("Mode", "Online Practice")
    st.subheader("Available Subjects")
    for subject in subjects:
        count = sum(1 for q in questions if q["subject"] == subject)
        st.write(f"📘 **{subject}** — {count} MCQs")
    st.info("Use Practice Test to attempt questions. Use Admin Panel to add your own MCQs.")

elif menu == "Practice Test":
    st.header("📝 Practice Test")
    subjects = ["All Subjects"] + sorted({q["subject"] for q in questions})
    subject = st.selectbox("Select Subject", subjects)
    count = st.number_input("Number of MCQs", min_value=1, max_value=max(1, len(questions)), value=min(10, max(1, len(questions))), step=1)

    if st.button("Start / Restart Test", type="primary"):
        pool = questions if subject == "All Subjects" else [q for q in questions if q["subject"] == subject]
        st.session_state.test_questions = random.sample(pool, min(int(count), len(pool))) if pool else []
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()

    test_questions = st.session_state.test_questions
    if test_questions:
        with st.form("quiz_form"):
            for i, q in enumerate(test_questions):
                st.markdown(f"### {i+1}. {q['question']}")
                selected = st.radio("Select answer:", q["options"], index=None, key=f"q_{q['id']}", horizontal=False)
                st.session_state.answers[q["id"]] = selected
                st.divider()
            submitted = st.form_submit_button("Submit Test", type="primary")
        if submitted:
            score = 0
            for q in test_questions:
                chosen = st.session_state.answers.get(q["id"])
                if chosen == q["options"][q["answer"]]:
                    score += 1
            st.session_state.submitted = True
            st.success(f"Your score: {score}/{len(test_questions)} ({score/len(test_questions)*100:.1f}%)")
            for i, q in enumerate(test_questions):
                chosen = st.session_state.answers.get(q["id"])
                correct = q["options"][q["answer"]]
                if chosen == correct:
                    st.write(f"✅ Question {i+1}: Correct")
                else:
                    st.write(f"❌ Question {i+1}: Correct answer: **{correct}**")
                st.caption(q.get("explanation", "No explanation available."))
    else:
        st.warning("Click Start / Restart Test to begin.")

elif menu == "All MCQs":
    st.header("📚 Question Bank")
    subjects = ["All Subjects"] + sorted({q["subject"] for q in questions})
    subject = st.selectbox("Filter by subject", subjects)
    filtered = questions if subject == "All Subjects" else [q for q in questions if q["subject"] == subject]
    st.write(f"Showing {len(filtered)} MCQs")
    for i, q in enumerate(filtered, 1):
        st.markdown(f"**{i}. {q['question']}**")
        for n, option in enumerate(q["options"]):
            st.write(f"{chr(65+n)}. {option}")
        with st.expander("Show answer and explanation"):
            st.success(f"Answer: {q['options'][q['answer']]}")
            st.write(q.get("explanation", "No explanation available."))
        st.divider()

elif menu == "Admin Panel":
    st.header("🔐 Admin Panel")
    password = st.text_input("Admin password", type="password")
    if password == ADMIN_PASSWORD:
        st.success("Admin access granted")
        tab1, tab2 = st.tabs(["Add MCQ", "Delete MCQ"])
        with tab1:
            with st.form("add_question"):
                subject = st.text_input("Subject", placeholder="e.g. English, Biology, MDCAT")
                topic = st.text_input("Topic", placeholder="e.g. Grammar")
                question = st.text_area("Question")
                options = [st.text_input(f"Option {chr(65+i)}") for i in range(4)]
                answer = st.selectbox("Correct option", [0, 1, 2, 3], format_func=lambda x: f"Option {chr(65+x)}")
                explanation = st.text_area("Explanation")
                add = st.form_submit_button("Add MCQ")
            if add:
                if subject and question and all(options):
                    new_id = max([q["id"] for q in questions], default=0) + 1
                    questions.append({"id": new_id, "subject": subject, "topic": topic, "question": question, "options": options, "answer": answer, "explanation": explanation})
                    save_questions(questions)
                    st.success("MCQ added successfully. Commit the updated questions.json to GitHub to publish it.")
                    st.rerun()
                else:
                    st.error("Please fill the subject, question, and all four options.")
        with tab2:
            if questions:
                selected_id = st.selectbox("Select MCQ to delete", [q["id"] for q in questions])
                if st.button("Delete Selected MCQ"):
                    questions = [q for q in questions if q["id"] != selected_id]
                    save_questions(questions)
                    st.success("MCQ deleted.")
                    st.rerun()
    elif password:
        st.error("Incorrect password.")
    st.caption("Default demo password: admin123. Change QUIZ_ADMIN_PASSWORD in Streamlit secrets/environment before public use.")

elif menu == "About":
    st.header("About This Website")
    st.write("This is a Streamlit-based MCQ practice platform.")
    st.write("You can add subjects, questions, four options, answers, and explanations.")
    st.warning("The demo admin password must be changed before sharing the website publicly.")
