"""
Login page
"""
import streamlit as st
from data_manager import DataManager
from pages.auth.styles import apply_auth_styles


def render():
    """Render login page"""
    apply_auth_styles()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Logo
    col1, col2, col3 = st.columns([2.5, 1, 2.5])
    with col2:
        try:
            st.image("assets/logo.png", width='stretch')
        except:
            st.markdown("<div style='text-align: center; font-size: 40px;'>🧠</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="app-title">BrainyYack</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Master derivatives with ML-powered tutoring</div>', unsafe_allow_html=True)
    
    # Login form
    with st.container():
        st.markdown('<div class="form-header">Welcome back!</div>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; font-size: 14px;">USERNAME/EMAIL</p>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter username or email", label_visibility="collapsed")
            
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">PASSWORD</p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Please fill in all fields")
                else:
                    success, user_data, message = DataManager.login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_role = user_data["role"]
                        st.session_state.user_data = user_data
                        st.success("✅ " + message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ " + message)
        
        # Links
        st.markdown("<div style='margin-top: 24px; text-align: center;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Create account", use_container_width=True, key="create_acc"):
                st.session_state.auth_page = "register"
                st.rerun()
        with col2:
            if st.button("🔑 Forgot password?", use_container_width=True, key="forgot_pwd"):
                st.session_state.auth_page = "forgot_password"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
