import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(
    page_title="M. Soomro Entry Test Preparation Academy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "questions.json"
ADMIN_PASSWORD = os.getenv("QUIZ_ADMIN_PASSWORD", "admin123")

# Main academic subjects
ACADEMIC_SUBJECTS = [
    "English",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "General Knowledge",
    "Islamiyat",
    "Pakistan Studies",
    "Current Affairs",
    "IQ / Analytical Reasoning",
]

# Entry-test categories
ENTRY_TESTS = [
    "STHP",
    "NTHP",
    "IBA Karachi",
    "NTS NAT",
    "MDCAT",
    "SALU",
    "COMSATS",
    "DOW University",
]

DEFAULT_QUESTIONS = [
    {"id": 1, "subject": "English", "topic": "Grammar", "question": "Choose the correct sentence.", "options": ["He go to school.", "He goes to school.", "He going school.", "He gone school."], "answer": 1, "explanation": "With he/she/it in the present simple, use goes."},
    {"id": 2, "subject": "Mathematics", "topic": "Arithmetic", "question": "What is 12 × 5?", "options": ["50", "60", "70", "80"], "answer": 1, "explanation": "12 multiplied by 5 equals 60."},
    {"id": 3, "subject": "General Knowledge", "topic": "Pakistan", "question": "What is the capital of Pakistan?", "options": ["Karachi", "Lahore", "Islamabad", "Peshawar"], "answer": 2, "explanation": "Islamabad is the capital of Pakistan."},
    {"id": 4, "subject": "Computer Science", "topic": "Basics", "question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing User"], "answer": 0, "explanation": "CPU stands for Central Processing Unit."},
    {"id": 5, "subject": "Biology", "topic": "Human Body", "question": "Which organ pumps blood?", "options": ["Lungs", "Brain", "Heart", "Kidney"], "answer": 2, "explanation": "The heart pumps blood through the body."},
    {"id": 6, "subject": "Physics", "topic": "Basics", "question": "What is the SI unit of force?", "options": ["Joule", "Newton", "Watt", "Pascal"], "answer": 1, "explanation": "Force is measured in newtons."},
    {"id": 7, "subject": "Chemistry", "topic": "Atoms", "question": "What is the chemical symbol for oxygen?", "options": ["Ox", "O", "C", "H"], "answer": 1, "explanation": "The chemical symbol for oxygen is O."},
    {"id": 8, "subject": "Islamiyat", "topic": "Basics", "question": "How many pillars of Islam are there?", "options": ["3", "4", "5", "6"], "answer": 2, "explanation": "Islam has five pillars."},
    {"id": 9, "subject": "Pakistan Studies", "topic": "Pakistan", "question": "On which date is Pakistan Independence Day observed?", "options": ["23 March", "14 August", "6 September", "25 December"], "answer": 1, "explanation": "Pakistan observes Independence Day on 14 August."},
    {"id": 10, "subject": "IQ / Analytical Reasoning", "topic": "Series", "question": "What comes next: 2, 4, 6, 8, ?", "options": ["9", "10", "11", "12"], "answer": 1, "explanation": "The sequence increases by 2 each time."},
]

def load_questions():
    if not os.path.exists(DATA_FILE):
        save_questions(DEFAULT_QUESTIONS)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else DEFAULT_QUESTIONS.copy()
    except Exception:
        return DEFAULT_QUESTIONS.copy()

def save_questions(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def reset_test():
    st.session_state.test_questions = []
    st.session_state.answers = {}
    st.session_state.submitted = False

if "test_questions" not in st.session_state:
    st.session_state.test_questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

questions = load_questions()
question_subjects = sorted({q.get("subject", "") for q in questions if q.get("subject")})
all_subjects = ACADEMIC_SUBJECTS + [s for s in question_subjects if s not in ACADEMIC_SUBJECTS]

st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; text-align: center; color: #2563eb; margin-bottom: 4px;}
.subtitle {text-align: center; font-size: 18px; color: #64748b; margin-bottom: 22px;}
.card {padding: 16px; border: 1px solid #dbeafe; border-radius: 14px; margin-bottom: 10px;}
.small {color: #64748b; font-size: 14px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 M. Soomro Entry Test Preparation Academy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">MCQs • Practice Tests • Entry Test Preparation • Answers & Explanations</div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "📌 Navigation",
    ["Home", "Subjects", "Entry Tests", "Practice Test", "All MCQs", "Admin Panel", "About"]
)

if menu == "Home":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total MCQs", len(questions))
    c2.metric("Subjects", len(all_subjects))
    c3.metric("Entry Tests", len(ENTRY_TESTS))
    c4.metric("Mode", "Online Practice")

    st.subheader("📚 Subjects")
    cols = st.columns(3)
    for i, subject in enumerate(all_subjects):
        count = sum(1 for q in questions if q.get("subject") == subject)
        with cols[i % 3]:
            st.markdown(f'<div class="card"><b>📘 {subject}</b><br><span class="small">{count} MCQs available</span></div>', unsafe_allow_html=True)

    st.subheader("🎯 Entry Test Categories")
    st.write(" | ".join([f"**{x}**" for x in ENTRY_TESTS]))
    st.info("Use Practice Test to attempt MCQs. Use Admin Panel to add your own questions.")

elif menu == "Subjects":
    st.header("📚 All Subjects")
    for subject in all_subjects:
        count = sum(1 for q in questions if q.get("subject") == subject)
        with st.expander(f"📘 {subject} — {count} MCQs"):
            if count:
                st.write(f"{count} questions are currently available in this subject.")
            else:
                st.warning("No MCQs have been added for this subject yet. Admin can add them from Admin Panel.")

elif menu == "Entry Tests":
    st.header("🎯 Entry Test Preparation")
    st.write("Choose an entry-test category to see its preparation area.")
    for test in ENTRY_TESTS:
        count = sum(1 for q in questions if q.get("topic", "").upper() == test.upper() or q.get("subject", "").upper() == test.upper())
        st.markdown(f"### 🎓 {test}")
        st.write(f"MCQs tagged for this test: **{count}**")
        st.divider()

elif menu == "Practice Test":
    st.header("📝 Practice Test")
    test_choices = ["All Subjects"] + all_subjects
    subject = st.selectbox("Select Subject", test_choices)

    pool = questions if subject == "All Subjects" else [q for q in questions if q.get("subject") == subject]
    available = len(pool)
    if available == 0:
        st.warning(f"No MCQs are currently available for **{subject}**. Add questions from Admin Panel.")
    else:
        count = st.number_input("Number of MCQs", min_value=1, max_value=available, value=min(10, available), step=1)
        if st.button("🚀 Start / Restart Test", type="primary"):
            st.session_state.test_questions = random.sample(pool, min(int(count), available))
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.rerun()

        test_questions = st.session_state.test_questions
        if test_questions:
            with st.form("quiz_form"):
                for i, q in enumerate(test_questions):
                    st.markdown(f"### {i + 1}. {q['question']}")
                    selected = st.radio(
                        "Select one answer:",
                        q["options"],
                        index=None,
                        key=f"q_{q['id']}",
                    )
                    st.session_state.answers[q["id"]] = selected
                    st.divider()
                submitted = st.form_submit_button("✅ Submit Test", type="primary")

            if submitted:
                unanswered = sum(1 for q in test_questions if not st.session_state.answers.get(q["id"]))
                if unanswered:
                    st.error(f"Please answer all questions before submitting. Unanswered: {unanswered}")
                else:
                    score = sum(
                        1 for q in test_questions
                        if st.session_state.answers.get(q["id"]) == q["options"][q["answer"]]
                    )
                    percentage = score / len(test_questions) * 100
                    st.success(f"🎉 Score: {score}/{len(test_questions)} ({percentage:.1f}%)")
                    for i, q in enumerate(test_questions):
                        chosen = st.session_state.answers.get(q["id"])
                        correct = q["options"][q["answer"]]
                        if chosen == correct:
                            st.write(f"✅ Question {i + 1}: Correct")
                        else:
                            st.write(f"❌ Question {i + 1}: Correct answer: **{correct}**")
                        st.caption(q.get("explanation", "No explanation available."))

elif menu == "All MCQs":
    st.header("📖 Question Bank")
    subject = st.selectbox("Filter by subject", ["All Subjects"] + all_subjects)
    filtered = questions if subject == "All Subjects" else [q for q in questions if q.get("subject") == subject]
    st.write(f"Showing **{len(filtered)}** MCQs")
    for i, q in enumerate(filtered, 1):
        st.markdown(f"**{i}. {q['question']}**")
        for n, option in enumerate(q["options"]):
            st.write(f"{chr(65 + n)}. {option}")
        with st.expander("Show answer and explanation"):
            st.success(f"Answer: {q['options'][q['answer']]}")
            st.write(q.get("explanation", "No explanation available."))
        st.divider()

elif menu == "Admin Panel":
    st.header("🔐 Admin Panel")
    password = st.text_input("Admin password", type="password")
    if password == ADMIN_PASSWORD:
        st.success("Admin access granted")
        tab1, tab2 = st.tabs(["➕ Add MCQ", "🗑️ Delete MCQ"])

        with tab1:
            with st.form("add_question"):
                subject = st.selectbox("Subject", all_subjects + ["Other / Custom"])
                custom_subject = st.text_input("Custom subject (only if Other / Custom)")
                topic = st.text_input("Topic / Test", placeholder="e.g. Grammar, STHP, NTS NAT")
                question = st.text_area("Question")
                options = [st.text_input(f"Option {chr(65 + i)}") for i in range(4)]
                answer = st.selectbox("Correct option", [0, 1, 2, 3], format_func=lambda x: f"Option {chr(65 + x)}")
                explanation = st.text_area("Explanation")
                add = st.form_submit_button("Add MCQ")

            if add:
                final_subject = custom_subject.strip() if subject == "Other / Custom" else subject
                if final_subject and question.strip() and all(x.strip() for x in options):
                    new_id = max([q.get("id", 0) for q in questions], default=0) + 1
                    questions.append({
                        "id": new_id,
                        "subject": final_subject,
                        "topic": topic.strip(),
                        "question": question.strip(),
                        "options": options,
                        "answer": answer,
                        "explanation": explanation.strip(),
                    })
                    save_questions(questions)
                    st.success("MCQ added successfully.")
                    st.rerun()
                else:
                    st.error("Please fill the subject, question, and all four options.")

        with tab2:
            if questions:
                selected_id = st.selectbox(
                    "Select MCQ to delete",
                    [q.get("id") for q in questions],
                    format_func=lambda x: next((f"{x} — {q['question'][:60]}" for q in questions if q.get("id") == x), str(x)),
                )
                if st.button("Delete Selected MCQ"):
                    questions = [q for q in questions if q.get("id") != selected_id]
                    save_questions(questions)
                    st.success("MCQ deleted.")
                    st.rerun()
            else:
                st.info("No MCQs available.")

        st.caption("For public deployment, set QUIZ_ADMIN_PASSWORD in Streamlit Secrets. The default password is only for initial setup.")
    elif password:
        st.error("Incorrect password.")

elif menu == "About":
    st.header("ℹ️ About")
    st.write("M. Soomro Entry Test Preparation Academy is a Streamlit MCQ practice platform.")
    st.write("It provides subject-wise practice, entry-test categories, answer explanations, and an admin question bank.")
    st.warning("Before sharing the website publicly, change the admin password in Streamlit Secrets.")
