# Final Demo - Main Application
# Consolidates all features into a single, role-based Streamlit app.

import streamlit as st
from pages import initial_quiz, lessons, lesson_quizzes, final_test, quiz_feedback, dashboards

# --- Page Configuration ---
st.set_page_config(
    page_title="BrainyYack Final Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
def init_session_state():
    if "role" not in st.session_state:
        st.session_state.role = "Student"
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_responses" not in st.session_state:
        st.session_state.quiz_responses = []
    if "weak_topics" not in st.session_state:
        st.session_state.weak_topics = []

init_session_state()

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.title("BrainyYack ITS")
    st.markdown("---_Final Demo_---")

    # Role Switcher
    role = st.radio(
        "Select Your Role",
        ["Student", "Teacher", "Parent"],
        key="role",
        on_change=lambda: st.session_state.update(page="dashboard") # Reset to dashboard on role change
    )

    st.markdown("### Navigation")

    # Dynamic Navigation based on Role
    if role == "Student":
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("Initial Quiz", use_container_width=True):
            st.session_state.page = "initial_quiz"
            st.rerun()
        if st.button("Lessons", use_container_width=True):
            st.session_state.page = "lessons"
            st.rerun()
        if st.button("Lesson Quizzes", use_container_width=True):
            st.session_state.page = "lesson_quizzes"
            st.rerun()
        if st.button("Quiz Feedback", use_container_width=True):
            st.session_state.page = "quiz_feedback"
            st.rerun()
        if st.button("Final Mastery Test", use_container_width=True, type="primary"):
            st.session_state.page = "final_test"
            st.rerun()
    else: # Teacher and Parent
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("---")
    st.caption("Group 11 Final Demo")

# --- Main Content Routing ---
def navigate():
    page = st.session_state.page
    role = st.session_state.role

    if page == "dashboard":
        if role == "Student":
            dashboards.render_student_dashboard()
        elif role == "Teacher":
            dashboards.render_teacher_dashboard()
        else: # Parent
            dashboards.render_parent_dashboard()
    elif page == "initial_quiz":
        initial_quiz.main() # Assuming a main() function in the copied file
    elif page == "lessons":
        lessons.main() # Assuming a main() function
    elif page == "lesson_quizzes":
        lesson_quizzes.main() # Assuming a main() function
    elif page == "quiz_feedback":
        quiz_feedback.main() # Assuming a main() function
    elif page == "final_test":
        final_test.show() # This one had a show() function
    else:
        st.error("Page not found!")

navigate()
