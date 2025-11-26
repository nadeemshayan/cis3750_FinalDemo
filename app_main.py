"""
BrainyYack - Intelligent Tutoring System
Group 11 - CIS3750
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from data_manager import DataManager

# --- Page Configuration ---
st.set_page_config(
    page_title="BrainyYack - ITS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DARK MODE PREMIUM DESIGN ---
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide the page navigation list */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* DARK MODE Color Palette */
    :root {
        --primary: #6B8E23;
        --primary-dark: #556B2F;
        --secondary: #1CB0F6;
        --accent: #FF9600;
        --background: #1a1a1a;
        --surface: #2a2a2a;
        --card: #2d2d2d;
        --text: #FFFFFF;
        --text-light: #B3B3B3;
        --border: #404040;
        --success: #58CC02;
        --warning: #FFC800;
        --error: #FF4B4B;
    }
    
    /* Dark background */
    [data-testid="stAppViewContainer"] {
        background: var(--background) !important;
        color: var(--text) !important;
    }
    
    /* All text white */
    body, p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: var(--text) !important;
    }
    
    /* Beautiful buttons - OLIVE GREEN */
    .stButton>button, .stFormSubmitButton>button {
        background: #6B8E23 !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 0 #556B2F !important;
        text-transform: none !important;
    }
    
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 0 #556B2F !important;
        background: #7BA428 !important;
    }
    
    .stButton>button:active, .stFormSubmitButton>button:active {
        transform: translateY(2px) !important;
        box-shadow: 0 2px 0 #556B2F !important;
    }
    
    /* Secondary buttons */
    .stButton>button[kind="secondary"] {
        background: var(--surface) !important;
        color: var(--text) !important;
        box-shadow: 0 4px 0 var(--border) !important;
    }
    
    /* Input fields - DARK MODE */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background: var(--surface) !important;
        border: 3px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        color: var(--text) !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--primary) !important;
        background: var(--card) !important;
        box-shadow: 0 0 0 3px rgba(88, 204, 2, 0.2) !important;
    }
    
    /* Placeholder text */
    .stTextInput>div>div>input::placeholder {
        color: var(--text-light) !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Cards - DARK */
    [data-testid="stVerticalBlock"] > [data-testid="stContainer"] {
        background: var(--card) !important;
        border-radius: 20px;
        padding: 24px;
        border: 3px solid var(--border);
        transition: all 0.2s ease;
    }
    
    /* Container borders dark */
    div[data-testid="column"] > div {
        background: var(--card) !important;
        color: var(--text) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: var(--text) !important;
    }
    
    /* Radio buttons - DARK */
    .stRadio > label {
        font-weight: 700 !important;
        color: var(--text) !important;
    }
    
    .stRadio > div {
        background: var(--surface) !important;
        padding: 8px;
        border-radius: 12px;
    }
    
    /* Select boxes dark */
    .stSelectbox > div > div {
        background: var(--surface) !important;
    }
    
    /* All form labels */
    label {
        color: var(--text) !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar styling - DARK (only when logged in) */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 3px solid var(--border) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }
    
    /* Hide sidebar button when not logged in */
    section[data-testid="stSidebar"] > div {
        background: var(--surface) !important;
    }
    
    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        text-align: left;
        justify-content: flex-start;
        padding: 14px 20px !important;
        margin-bottom: 8px;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 16px !important;
        padding: 16px 20px !important;
        font-weight: 600 !important;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: slideIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "logged_in": False,
        "username": None,
        "user_role": None,
        "user_data": None,
        "current_page": "dashboard",
        "auth_page": "login",
        
        # Quiz states
        "quiz_completed": False,
        "quiz_score": 0,
        "quiz_responses": [],
        "weak_topics": [],
        "strong_topics": [],
        
        # Lesson states
        "current_lesson": None,
        "lesson_progress": {},
        
        # Practice states
        "practice_attempts": {},
        
        # UI states
        "show_hint": False,
        "selected_age_level": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value




def route_to_page():
    """Route to the appropriate page based on current_page state"""
    if not st.session_state.logged_in:
        from pages.auth import render_auth
        render_auth()
        return
        
    page = st.session_state.current_page
    
    # Import pages dynamically
    if page == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
    
    elif page == "teacher_analytics":
        from pages.dashboard import teacher_analytics
        teacher_analytics.render()
    
    elif page == "initial_quiz":
        from pages import initial_quiz
        initial_quiz.main()
    
    elif page == "lessons":
        from pages import lessons_enhanced
        lessons_enhanced.main()
    
    elif page == "practice":
        from pages import practice_problems
        practice_problems.main()
    
    elif page == "progress":
        from pages import progress_tracker
        progress_tracker.main()
    
    elif page == "achievements":
        from pages import achievements
        achievements.main()
    
    elif page == "settings":
        from pages import settings
        settings.main()
    
    elif page == "lesson_quizzes":
        from pages import lesson_quizzes
        lesson_quizzes.main()
    
    else:
        st.error(f"Page '{page}' not found")


def main():
    init_session_state()
    
    from components.sidebar import render_sidebar
    render_sidebar()
    
    route_to_page()


if __name__ == "__main__":
    main()
