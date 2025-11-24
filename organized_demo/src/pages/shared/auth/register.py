"""
Registration page
"""
import streamlit as st
import random
from data_manager import DataManager
from pages.auth.styles import apply_auth_styles


def generate_share_code():
    """Generate unique share code for parents"""
    return f"SHARE-{random.randint(1000, 9999)}"


def generate_teacher_code():
    """Generate unique teacher code"""
    return f"TEACH-{random.randint(1000, 9999)}"


def render():
    """Render registration page"""
    apply_auth_styles()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Back button at very top
    if st.button("← Back", key="register_back_top", use_container_width=False):
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
    
    st.markdown('<div class="form-header" style="margin-top: 12px;">Create account</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Start your derivatives learning journey</div>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; font-size: 14px;">USERNAME</p>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Choose a unique username", label_visibility="collapsed")
        
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">EMAIL</p>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed")
        
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">PASSWORD</p>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Choose a strong password", label_visibility="collapsed")
        
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">CONFIRM PASSWORD</p>', unsafe_allow_html=True)
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", label_visibility="collapsed")
        
        st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 20px; font-size: 14px;">WHO ARE YOU?</p>', unsafe_allow_html=True)
        role = st.selectbox("Role", ["Student", "Teacher", "Parent"], label_visibility="collapsed")
        
        age_level = None
        grade = None
        teacher_code_input = None
        
        if role == "Student":
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">AGE LEVEL</p>', unsafe_allow_html=True)
            age_level = st.selectbox("Age Level", ["Elementary", "Middle School", "High School", "College"], label_visibility="collapsed")
            
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">GRADE/YEAR</p>', unsafe_allow_html=True)
            grade = st.text_input("Grade", placeholder="e.g., 10th Grade", label_visibility="collapsed")
            
            st.markdown('<p style="color: #FFFFFF; font-weight: 700; margin-bottom: 8px; margin-top: 16px; font-size: 14px;">TEACHER CODE (OPTIONAL)</p>', unsafe_allow_html=True)
            teacher_code_input = st.text_input("Teacher Code", placeholder="TEACH-1234", label_visibility="collapsed")
        
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
        
        if submit:
            # Validation
            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif "@" not in email:
                st.error("Please enter a valid email")
            else:
                # Generate codes
                share_code = generate_share_code() if role == "Student" else None
                teacher_code = generate_teacher_code() if role == "Teacher" else None
                
                # Prepare kwargs
                kwargs = {
                    "age_level": age_level if role == "Student" else None,
                    "grade": grade if role == "Student" else None,
                    "share_code": share_code,
                    "teacher_code": teacher_code,
                    "teacher_codes": [teacher_code_input] if role == "Student" and teacher_code_input else [],
                    "parent_codes": []
                }
                
                success, message = DataManager.register_user(username, password, email, role, **kwargs)
                
                if success:
                    st.success("✅ Registration successful!")
                    st.balloons()
                    st.session_state.auth_page = "login"
                    st.rerun()
                else:
                    st.error("❌ " + message)
    
    st.markdown('</div>', unsafe_allow_html=True)
