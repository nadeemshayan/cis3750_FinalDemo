"""
Authentication router - manages all auth pages
"""
import streamlit as st


def render_auth():
    """Main authentication router"""
    # Initialize auth page state
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"
    
    # Route to appropriate page
    if st.session_state.auth_page == "login":
        from pages.auth import login
        login.render()
    elif st.session_state.auth_page == "register":
        from pages.auth import register
        register.render()
    elif st.session_state.auth_page == "forgot_password":
        from pages.auth import forgot_password
        forgot_password.render()
