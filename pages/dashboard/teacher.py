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
    
    # Get teacher data
    user_data = st.session_state.user_data
    teacher_code = user_data.get('teacher_code', 'TEACH-5000')
    
    # Get students
    students = DataManager.get_students_by_teacher_code(teacher_code)
    total_students = len(students)
    
    # Calculate average progress
    avg_progress = 0
    if students:
        progress_sum = 0
        for student in students:
            student_progress = DataManager.get_user_progress(student['username'])
            progress_sum += student_progress.get('overall_progress', 0)
        avg_progress = int(progress_sum / total_students) if total_students > 0 else 0
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);">
            <div class="stat-number">{total_students}</div>
            <div class="stat-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%);">
            <div class="stat-number">1</div>
            <div class="stat-label">Active Classes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #8B9F29 0%, #7BA428 100%);">
            <div class="stat-number">{avg_progress}%</div>
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
    
    # Recent Activity
    if students:
        st.subheader("📊 Recent Student Activity")
        recent_students = students[:5]  # Show first 5
        
        for student in recent_students:
            student_progress = DataManager.get_user_progress(student['username'])
            progress_pct = student_progress.get('overall_progress', 0)
            quiz_completed = student_progress.get('initial_quiz', {}).get('completed', False)
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{student['username']}**")
                with col2:
                    st.metric("Progress", f"{progress_pct}%")
                with col3:
                    status = "✅ Active" if quiz_completed else "⏳ Pending"
                    st.caption(status)
    
    st.markdown("---")
    
    # Teacher code
    st.subheader("👨‍🏫 Your Teacher Code")
    st.code(teacher_code, language=None)
    st.caption("Share this code with your students so they can connect to your class")
