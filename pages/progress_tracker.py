"""
Progress Tracker - Detailed view of user progress across all areas
"""

import streamlit as st
from data_manager import DataManager
import pandas as pd


def main():
    """Main progress tracker page"""
    # Header with home button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📊 My Progress")
    with col2:
        if st.button("🏠 Home", key="progress_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("Detailed overview of your learning journey")
    
    username = st.session_state.username
    progress = DataManager.get_user_progress(username)
    
    # Overall Progress
    st.subheader("🎯 Overall Progress")
    overall_progress = progress.get('overall_progress', 0)
    st.progress(overall_progress / 100, text=f"{overall_progress}%")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        quiz_completed = progress.get('initial_quiz', {}).get('completed', False)
        st.metric("Initial Quiz", "✅" if quiz_completed else "⏳")
    
    with col2:
        lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
        st.metric("Lessons", f"{lessons_completed}/5")
    
    with col3:
        practice_correct = sum(1 for p in progress.get('practice_problems', {}).values() if p.get('correct', 0) > 0)
        st.metric("Practice Problems", practice_correct)
    
    with col4:
        final_completed = progress.get('final_test', {}).get('completed', False)
        st.metric("Final Test", "✅" if final_completed else "⏳")
    
    st.markdown("---")
    
    # Initial Quiz Results
    st.subheader("📝 Initial Quiz Results")
    
    if progress.get('initial_quiz', {}).get('completed'):
        quiz_data = progress['initial_quiz']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Score", f"{quiz_data['score']}/{quiz_data['total']}")
            percentage = (quiz_data['score'] / quiz_data['total'] * 100) if quiz_data['total'] > 0 else 0
            st.progress(percentage / 100, text=f"{percentage:.1f}%")
        
        with col2:
            st.markdown("**Date Taken:**")
            st.caption(quiz_data.get('date', 'N/A')[:10] if quiz_data.get('date') else 'N/A')
        
        strength_col, weak_col = st.columns(2)
        
        with strength_col:
            with st.container(border=True):
                st.markdown("**💪 Strengths:**")
                for topic in quiz_data.get('strong_topics', []):
                    st.markdown(f"✅ {topic}")
        
        with weak_col:
            with st.container(border=True):
                st.markdown("**🎯 Focus Areas:**")
                for topic in quiz_data.get('weak_topics', []):
                    st.markdown(f"⚠️ {topic}")
    else:
        st.info("Take the initial quiz to see your results here!")
    
    st.markdown("---")
    
    # Lesson Progress
    st.subheader("📚 Lesson Progress")
    
    lessons_data = progress.get('lessons', {})
    
    if lessons_data:
        lesson_names = {
            "lesson1": "Introduction to Derivatives",
            "lesson2": "Power Rule",
            "lesson3": "Product and Quotient Rules",
            "lesson4": "Chain Rule",
            "lesson5": "Applications"
        }
        
        for lesson_id, lesson_progress in lessons_data.items():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    lesson_name = lesson_names.get(lesson_id, lesson_id)
                    status = "✅" if lesson_progress.get('completed') else "⏳"
                    st.markdown(f"**{status} {lesson_name}**")
                
                with col2:
                    time_spent = lesson_progress.get('time_spent', 0)
                    st.caption(f"⏱️ {time_spent // 60} min")
                
                with col3:
                    date = lesson_progress.get('date', 'N/A')[:10] if lesson_progress.get('date') else 'N/A'
                    st.caption(f"📅 {date}")
    else:
        st.info("Start lessons to track your progress!")
    
    st.markdown("---")
    
    # Practice Problems Stats
    st.subheader("✏️ Practice Problems Statistics")
    
    practice_data = progress.get('practice_problems', {})
    
    if practice_data:
        total_attempts = sum(p.get('attempts', 0) for p in practice_data.values())
        total_correct = sum(p.get('correct', 0) for p in practice_data.values())
        total_incorrect = sum(p.get('incorrect', 0) for p in practice_data.values())
        accuracy = (total_correct / (total_correct + total_incorrect) * 100) if (total_correct + total_incorrect) > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Attempts", total_attempts)
        with col2:
            st.metric("Correct", total_correct, delta="✅")
        with col3:
            st.metric("Incorrect", total_incorrect, delta="❌")
        with col4:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        
        # Show problems that need review
        needs_review = [pid for pid, data in practice_data.items() if data.get('needs_review')]
        if needs_review:
            st.warning(f"⚠️ {len(needs_review)} problem(s) need review")
    else:
        st.info("Practice problems to see your statistics!")
    
    st.markdown("---")
    
    # Time Tracking
    st.subheader("⏰ Time Spent Learning")
    
    total_time = progress.get('total_time_spent', 0)
    hours = total_time // 3600
    minutes = (total_time % 3600) // 60
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Time", f"{hours}h {minutes}m")
    with col2:
        st.metric("Sessions", len(lessons_data))
    with col3:
        avg_time = (total_time // len(lessons_data)) if lessons_data else 0
        st.metric("Avg Session", f"{avg_time // 60}m")
    
    st.markdown("---")
    
    # Badges and Achievements
    st.subheader("🏆 Achievements")
    
    badges = progress.get('badges', [])
    certificates = progress.get('certificates', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Badges Earned", len(badges))
        if badges:
            for badge in badges[-5:]:  # Show last 5
                st.caption(f"🏅 {badge['name']}")
    
    with col2:
        st.metric("Certificates", len(certificates))
        if certificates:
            for cert in certificates:
                st.caption(f"🎓 {cert['name']}")
    
    if st.button("🏆 View All Achievements", use_container_width=True, type="primary"):
        st.session_state.current_page = "achievements"
        st.rerun()


if __name__ == "__main__":
    main()
