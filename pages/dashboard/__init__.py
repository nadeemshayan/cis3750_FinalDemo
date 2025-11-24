"""
Dashboard router - manages all dashboard pages
"""
import streamlit as st


def render_dashboard():
    """Main dashboard router"""
    # Route based on user role
    if st.session_state.user_role == "Student":
        from pages.dashboard import student
        student.render()
    elif st.session_state.user_role == "Teacher":
        from pages.dashboard import teacher
        teacher.render()
    elif st.session_state.user_role == "Parent":
        from pages.dashboard import parent
        parent.render()
    else:
        st.error("Unknown user role")
