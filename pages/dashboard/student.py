"""
Student dashboard - clean and consistent
"""
import streamlit as st
from data_manager import DataManager
from pages.dashboard.styles import apply_dashboard_styles


def render():
    """Render student dashboard"""
    apply_dashboard_styles()
    
    # Header
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px;">
            Hey {st.session_state.username}! 👋
        </h1>
        <p style="font-size: 15px; color: #B3B3B3;">Ready to master derivatives with ML-powered tutoring?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user progress
    progress = DataManager.get_user_progress(st.session_state.username)
    quiz_completed = progress.get('initial_quiz', {}).get('completed', False)
    
    # Top stats - olive green gradients
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        overall_prog = progress.get('overall_progress', 0)
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);">
            <div class="stat-number">{overall_prog}%</div>
            <div class="stat-label">Overall Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%);">
            <div class="stat-number">{lessons_completed}</div>
            <div class="stat-label">Lessons Done</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        badges_earned = len(progress.get('badges', []))
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #8B9F29 0%, #7BA428 100%);">
            <div class="stat-number">{badges_earned}</div>
            <div class="stat-label">Badges</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        quiz_score = progress.get('initial_quiz', {}).get('score', 0)
        quiz_total = progress.get('initial_quiz', {}).get('total', 8)
        score_pct = int((quiz_score/quiz_total*100)) if quiz_total > 0 else 0
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #9CAA3A 0%, #8B9F29 100%);">
            <div class="stat-number">{score_pct}%</div>
            <div class="stat-label">Quiz Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📝 Take Initial Quiz" if not quiz_completed else "📝 Retake Quiz", 
                     use_container_width=True, key="quiz_btn"):
            st.session_state.current_page = "initial_quiz"
            st.rerun()
    
    with action_col2:
        if st.button("📚 Browse Lessons", use_container_width=True, key="lessons_btn"):
            st.session_state.current_page = "lessons"
            st.rerun()
    
    with action_col3:
        if st.button("✏️ Practice Problems", use_container_width=True, key="practice_btn"):
            st.session_state.current_page = "practice"
            st.rerun()
    
    st.markdown("---")
    
    # Recent Activity
    st.subheader("📊 Your Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Current Focus")
        weak_topics = progress.get('initial_quiz', {}).get('weak_topics', [])
        if quiz_completed and weak_topics:
            st.info(f"📌 Work on: {', '.join(weak_topics[:3])}")
        elif quiz_completed:
            st.success("🎯 Great job! No weak areas identified!")
        else:
            st.warning("📝 Take the Initial Quiz to identify focus areas")
    
    with col2:
        st.markdown("### 🔥 Streak")
        st.metric("Days Active", "0", "Start your journey!")
