"""
Teacher dashboard - clean and consistent
"""
import streamlit as st
from data_manager import DataManager
from pages.dashboard.styles import apply_dashboard_styles


def render():
    """Render teacher dashboard"""
    apply_dashboard_styles()
    
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px;">
            Teacher Dashboard 👨‍🏫
        </h1>
        <p style="font-size: 15px; color: #B3B3B3;">Manage your classes and track student progress</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);">
            <div class="stat-number">0</div>
            <div class="stat-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%);">
            <div class="stat-number">0</div>
            <div class="stat-label">Active Classes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #8B9F29 0%, #7BA428 100%);">
            <div class="stat-number">0</div>
            <div class="stat-label">Avg Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    st.subheader("🎯 Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 View Student Analytics", use_container_width=True):
            st.session_state.current_page = "teacher_analytics"
            st.rerun()
    
    with col2:
        if st.button("📝 Manage Classes", use_container_width=True):
            st.info("Class management coming soon!")
    
    st.markdown("---")
    
    # Teacher code
    user_data = st.session_state.user_data
    teacher_code = user_data.get('teacher_code', 'TEACH-5000')
    
    st.subheader("👨‍🏫 Your Teacher Code")
    st.code(teacher_code, language=None)
    st.caption("Share this code with your students so they can connect to your class")
