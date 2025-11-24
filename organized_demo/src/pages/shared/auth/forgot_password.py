"""
Forgot password page
"""
import streamlit as st
from data_manager import DataManager
from pages.auth.styles import apply_auth_styles


def render():
    """Render forgot password page"""
    apply_auth_styles()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Back button at very top
    if st.button("← Back", key="forgot_back_top", use_container_width=False):
        st.session_state.auth_page = "login"
        st.rerun()
    
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    
    # Logo
    col1, col2, col3 = st.columns([2.5, 1, 2.5])
    with col2:
        try:
            st.image("assets/logo.png", width='stretch')
        except:
            st.markdown("<div style='text-align: center; font-size: 40px;'>🧠</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-header" style="margin-top: 12px;">Reset password</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Enter your details to reset your password</div>', unsafe_allow_html=True)
    
    # Initialize code verification state
    if "code_verified" not in st.session_state:
        st.session_state.code_verified = False
    
    with st.form("forgot_password_form"):
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; font-size: 14px;">USERNAME/EMAIL</p>', unsafe_allow_html=True)
        username_or_email = st.text_input("Username", placeholder="Enter username or email", label_visibility="collapsed")
        
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">VERIFICATION CODE</p>', unsafe_allow_html=True)
        code = st.text_input("Code", placeholder="Enter verification code", label_visibility="collapsed")
        
        # Only show password fields if code is verified
        if st.session_state.code_verified or code == "111111":
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">NEW PASSWORD</p>', unsafe_allow_html=True)
            new_password = st.text_input("New Password", type="password", placeholder="Enter new password", label_visibility="collapsed")
            
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">CONFIRM PASSWORD</p>', unsafe_allow_html=True)
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm new password", label_visibility="collapsed")
        else:
            new_password = None
            confirm_password = None
        
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        
        submit = st.form_submit_button("Reset password", use_container_width=True, type="primary")
        
        if submit:
            if not username_or_email or not code:
                st.error("⚠️ Please fill in username/email and code")
            elif code != "111111":
                st.error("❌ Invalid verification code")
            elif not new_password or not confirm_password:
                st.error("⚠️ Please enter and confirm your new password")
            elif new_password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(new_password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                st.session_state.code_verified = True
                # Use username_or_email for both username and email
                success, message = DataManager.reset_password(username_or_email, username_or_email, new_password)
                if success:
                    st.success("✅ " + message)
                    st.session_state.code_verified = False
                    if st.button("Go to Login", use_container_width=True, type="primary"):
                        st.session_state.auth_page = "login"
                        st.rerun()
                else:
                    st.error("❌ " + message)
    
    st.markdown('</div>', unsafe_allow_html=True)
