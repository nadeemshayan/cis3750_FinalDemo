"""
Clean sidebar component - always consistent
"""
import streamlit as st
from data_manager import DataManager


def render_sidebar():
    """Render the beautiful sidebar - ALWAYS consistent"""
    
    # FORCE hide the ugly Streamlit default navigation
    st.markdown("""
    <style>
        /* FORCE HIDE DEFAULT STREAMLIT NAVIGATION */
        [data-testid="stSidebarNav"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            overflow: hidden !important;
        }
        
        /* Custom sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #2a2a2a !important;
        }
        
        /* Sidebar buttons - olive green */
        [data-testid="stSidebar"] .stButton>button {
            background: #6B8E23 !important;
            color: white !important;
            border-radius: 16px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 4px 0 #556B2F !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }
        
        [data-testid="stSidebar"] .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 0 #556B2F !important;
            background: #7BA428 !important;
        }
        
        [data-testid="stSidebar"] .stButton>button:active {
            transform: translateY(2px) !important;
            box-shadow: 0 2px 0 #556B2F !important;
        }
        
        /* Progress bar - olive green */
        [data-testid="stSidebar"] .stProgress > div > div {
            background-color: #6B8E23 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Don't show sidebar if not logged in
    if not st.session_state.get('logged_in', False):
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            button[kind="header"] {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)
        return
    
    # Show beautiful sidebar
    with st.sidebar:
        # Logo
        try:
            st.image("assets/logo.png", width=120)
        except:
            st.title("🧠 BrainyYack")
        
        st.markdown("### ML-Powered Tutoring")
        st.markdown("---")
        
        # User info
        st.markdown(f"**Welcome, {st.session_state.username}!**")
        st.caption(f"Role: {st.session_state.user_role}")
        
        # Progress bar - only for students
        if st.session_state.user_role == "Student":
            progress = DataManager.get_user_progress(st.session_state.username)
            overall_progress = progress.get("overall_progress", 0)
            print(f"🔍 Sidebar loading progress for {st.session_state.username}: {overall_progress}%")
            st.progress(overall_progress / 100, text=f"Overall Progress: {overall_progress}%")
        elif st.session_state.user_role == "Teacher":
            # Show teacher stats instead
            user_data = st.session_state.user_data
            teacher_code = user_data.get('teacher_code', 'N/A')
            st.markdown(f"📋 Code: `{teacher_code}`")
        
        st.markdown("---")
        st.markdown("### Navigation")
        
        # Role-specific navigation
        if st.session_state.user_role == "Student":
            render_student_nav()
        elif st.session_state.user_role == "Teacher":
            render_teacher_nav()
        elif st.session_state.user_role == "Parent":
            render_parent_nav()
        
        st.markdown("---")
        
        # Settings button
        if st.button("⚙️ Settings", key="sidebar_settings", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        
        # Logout
        if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_student_nav():
    """Student navigation buttons"""
    pages = [
        ("🏠 Dashboard", "dashboard"),
        ("📝 Initial Quiz", "initial_quiz"),
        ("📚 Lessons", "lessons"),
        ("✏️ Practice", "practice"),
        ("📊 Progress", "progress"),
        ("🏆 Achievements", "achievements"),
    ]
    
    current_page = st.session_state.get('current_page', 'dashboard')
    
    for label, page_key in pages:
        button_type = "primary" if current_page == page_key else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=button_type):
            st.session_state.current_page = page_key
            st.rerun()


def render_teacher_nav():
    """Teacher navigation buttons"""
    pages = [
        ("🏠 Dashboard", "dashboard"),
        ("📊 Analytics", "teacher_analytics"),
        ("👥 Students", "students"),
    ]
    
    current_page = st.session_state.get('current_page', 'dashboard')
    
    for label, page_key in pages:
        button_type = "primary" if current_page == page_key else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=button_type):
            st.session_state.current_page = page_key
            st.rerun()


def render_parent_nav():
    """Parent navigation buttons"""
    # Parents only have dashboard - children's progress shown there
    pages = [
        ("🏠 Dashboard", "dashboard"),
    ]
    
    current_page = st.session_state.get('current_page', 'dashboard')
    
    for label, page_key in pages:
        button_type = "primary" if current_page == page_key else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=button_type):
            st.session_state.current_page = page_key
            st.rerun()
