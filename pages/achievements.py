"""
Achievements - Badges and Certificates System
"""

import streamlit as st
from data_manager import DataManager
from datetime import datetime


# Available badges and how to earn them
AVAILABLE_BADGES = {
    "first_login": {
        "name": "Welcome Aboard! 👋",
        "description": "Created your account and logged in",
        "icon": "👋",
        "points": 10
    },
    "first_quiz": {
        "name": "Quiz Starter 📝",
        "description": "Completed your first initial quiz",
        "icon": "📝",
        "points": 20
    },
    "first_lesson": {
        "name": "First Lesson Complete! 🎓",
        "description": "Completed your first lesson",
        "icon": "🎓",
        "points": 25
    },
    "first_practice": {
        "name": "Practice Makes Perfect! ✏️",
        "description": "Correctly answered your first practice problem",
        "icon": "✏️",
        "points": 15
    },
    "quiz_master": {
        "name": "Quiz Master 🎯",
        "description": "Scored 80% or higher on the initial quiz",
        "icon": "🎯",
        "points": 50
    },
    "speed_learner": {
        "name": "Speed Learner ⚡",
        "description": "Completed 3 lessons in one day",
        "icon": "⚡",
        "points": 40
    },
    "persistent": {
        "name": "Never Give Up! 💪",
        "description": "Attempted a problem 3+ times before getting it right",
        "icon": "💪",
        "points": 30
    },
    "perfect_lesson": {
        "name": "Perfectionist ⭐",
        "description": "Got 100% on a lesson quiz",
        "icon": "⭐",
        "points": 45
    },
    "week_streak": {
        "name": "7-Day Streak 🔥",
        "description": "Practiced 7 days in a row",
        "icon": "🔥",
        "points": 60
    },
    "lesson_master": {
        "name": "Lesson Master 📚",
        "description": "Completed all lessons",
        "icon": "📚",
        "points": 100
    },
    "practice_warrior": {
        "name": "Practice Warrior ⚔️",
        "description": "Correctly answered 50 practice problems",
        "icon": "⚔️",
        "points": 75
    },
    "final_conqueror": {
        "name": "Final Test Conqueror 🏆",
        "description": "Passed the final test with 70% or higher",
        "icon": "🏆",
        "points": 150
    }
}

# Available certificates
CERTIFICATES = {
    "derivatives_basics": {
        "name": "Derivatives Fundamentals",
        "course": "Introduction to Derivatives",
        "requirement": "Complete first 3 lessons and score 70%+ on quizzes",
        "template": "basic"
    },
    "derivatives_advanced": {
        "name": "Advanced Derivatives",
        "course": "Advanced Derivative Techniques",
        "requirement": "Complete all lessons and score 80%+ on final test",
        "template": "advanced"
    },
    "calculus_master": {
        "name": "Calculus Mastery",
        "course": "Complete Calculus Course",
        "requirement": "Complete all content with 90%+ average",
        "template": "master"
    }
}


def check_and_award_badges(username: str):
    """Check if user qualifies for any new badges"""
    progress = DataManager.get_user_progress(username)
    earned_badges = [b['name'] for b in progress.get('badges', [])]
    new_badges = []
    
    # Check each badge condition
    # Quiz Master
    if "Quiz Master 🎯" not in earned_badges:
        quiz_score = progress.get('initial_quiz', {}).get('score', 0)
        quiz_total = progress.get('initial_quiz', {}).get('total', 8)
        if quiz_total > 0 and (quiz_score / quiz_total) >= 0.8:
            DataManager.award_badge(username, "Quiz Master 🎯", "Scored 80% or higher on the initial quiz")
            new_badges.append("Quiz Master 🎯")
    
    # Lesson Master
    if "Lesson Master 📚" not in earned_badges:
        lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
        if lessons_completed >= 5:  # Assuming 5 total lessons
            DataManager.award_badge(username, "Lesson Master 📚", "Completed all lessons")
            new_badges.append("Lesson Master 📚")
    
    # Practice Warrior
    if "Practice Warrior ⚔️" not in earned_badges:
        correct_problems = sum(p.get('correct', 0) for p in progress.get('practice_problems', {}).values())
        if correct_problems >= 50:
            DataManager.award_badge(username, "Practice Warrior ⚔️", "Correctly answered 50 practice problems")
            new_badges.append("Practice Warrior ⚔️")
    
    # Final Conqueror
    if "Final Test Conqueror 🏆" not in earned_badges:
        final_score = progress.get('final_test', {}).get('score', 0)
        final_total = progress.get('final_test', {}).get('total', 20)
        if final_total > 0 and (final_score / final_total) >= 0.7:
            DataManager.award_badge(username, "Final Test Conqueror 🏆", "Passed the final test with 70% or higher")
            new_badges.append("Final Test Conqueror 🏆")
    
    return new_badges


def check_and_award_certificates(username: str):
    """Check if user qualifies for any certificates"""
    progress = DataManager.get_user_progress(username)
    earned_certs = [c['name'] for c in progress.get('certificates', [])]
    new_certs = []
    
    # Derivatives Basics Certificate
    if "Derivatives Fundamentals" not in earned_certs:
        lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
        avg_quiz_score = 0
        quiz_scores = [q.get('score', 0) / q.get('total', 1) for q in progress.get('lesson_quizzes', {}).values()]
        if quiz_scores:
            avg_quiz_score = sum(quiz_scores) / len(quiz_scores)
        
        if lessons_completed >= 3 and avg_quiz_score >= 0.7:
            DataManager.award_certificate(username, "Derivatives Fundamentals", "Introduction to Derivatives")
            new_certs.append("Derivatives Fundamentals")
    
    # Advanced Certificate
    if "Advanced Derivatives" not in earned_certs:
        lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
        final_score = progress.get('final_test', {}).get('score', 0)
        final_total = progress.get('final_test', {}).get('total', 20)
        final_percentage = (final_score / final_total) if final_total > 0 else 0
        
        if lessons_completed >= 5 and final_percentage >= 0.8:
            DataManager.award_certificate(username, "Advanced Derivatives", "Advanced Derivative Techniques")
            new_certs.append("Advanced Derivatives")
    
    # Master Certificate
    if "Calculus Mastery" not in earned_certs:
        lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
        quiz_scores = [q.get('score', 0) / q.get('total', 1) for q in progress.get('lesson_quizzes', {}).values()]
        final_score = progress.get('final_test', {}).get('score', 0)
        final_total = progress.get('final_test', {}).get('total', 20)
        
        all_scores = quiz_scores + ([final_score / final_total] if final_total > 0 else [])
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
        
        if lessons_completed >= 5 and avg_score >= 0.9:
            DataManager.award_certificate(username, "Calculus Mastery", "Complete Calculus Course")
            new_certs.append("Calculus Mastery")
    
    return new_certs


def render_certificate(cert_name: str, cert_data: dict, award_date: str):
    """Render a certificate"""
    with st.container(border=True):
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
            <h1>🏆 Certificate of Achievement 🏆</h1>
            <h2>{cert_name}</h2>
            <p style="font-size: 1.2em; margin: 20px 0;">This certifies that</p>
            <h2 style="font-size: 2em; margin: 10px 0;">{st.session_state.username}</h2>
            <p style="font-size: 1.2em; margin: 20px 0;">has successfully completed</p>
            <h3>{cert_data['course']}</h3>
            <p style="margin-top: 30px;">Awarded on {award_date}</p>
            <p style="font-style: italic; margin-top: 20px;">BrainyYack Intelligent Tutoring System</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📥 Download {cert_name}", key=f"download_{cert_name}"):
            st.success("Certificate download would start here (PDF generation)")


def main():
    """Main achievements page"""
    # Header with home button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🏆 Badges & Certificates")
    with col2:
        if st.button("🏠 Home", key="achievements_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("Track your learning milestones and accomplishments")
    
    username = st.session_state.username
    
    # Check for new badges and certificates
    new_badges = check_and_award_badges(username)
    new_certs = check_and_award_certificates(username)
    
    # Show notifications for new achievements
    if new_badges:
        for badge in new_badges:
            st.success(f"🎉 New Badge Earned: {badge}!")
            st.balloons()
    
    if new_certs:
        for cert in new_certs:
            st.success(f"🎓 New Certificate Earned: {cert}!")
            st.balloons()
    
    # Get progress
    progress = DataManager.get_user_progress(username)
    earned_badges = progress.get('badges', [])
    earned_certificates = progress.get('certificates', [])
    
    # Calculate total points
    total_points = 0
    for badge in earned_badges:
        for badge_id, badge_data in AVAILABLE_BADGES.items():
            if badge_data['name'] == badge['name']:
                total_points += badge_data['points']
    
    # Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Badges Earned", f"{len(earned_badges)}/{len(AVAILABLE_BADGES)}")
    
    with col2:
        st.metric("Certificates", len(earned_certificates))
    
    with col3:
        st.metric("Total Points", total_points)
    
    st.progress(len(earned_badges) / len(AVAILABLE_BADGES))
    
    st.markdown("---")
    
    # Tabs for badges and certificates
    tab1, tab2 = st.tabs(["🏅 Badges", "🎓 Certificates"])
    
    with tab1:
        st.subheader("Your Badges")
        
        if earned_badges:
            # Display earned badges
            cols = st.columns(3)
            for idx, badge in enumerate(earned_badges):
                with cols[idx % 3]:
                    with st.container(border=True):
                        # Find badge details
                        badge_details = None
                        for badge_id, badge_data in AVAILABLE_BADGES.items():
                            if badge_data['name'] == badge['name']:
                                badge_details = badge_data
                                break
                        
                        if badge_details:
                            st.markdown(f"<h1 style='text-align: center; font-size: 4em;'>{badge_details['icon']}</h1>", unsafe_allow_html=True)
                            st.markdown(f"**{badge['name']}**")
                            st.caption(badge['description'])
                            st.caption(f"📅 {badge.get('date', 'N/A')[:10]}")
                            st.caption(f"⭐ {badge_details['points']} points")
        else:
            st.info("No badges earned yet. Keep learning to unlock achievements!")
        
        st.markdown("---")
        st.subheader("Available Badges")
        
        earned_badge_names = [b['name'] for b in earned_badges]
        
        for badge_id, badge_data in AVAILABLE_BADGES.items():
            is_earned = badge_data['name'] in earned_badge_names
            
            with st.container(border=True):
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if is_earned:
                        st.markdown(f"<h1 style='text-align: center; font-size: 3em;'>{badge_data['icon']}</h1>", unsafe_allow_html=True)
                    else:
                        st.markdown("<h1 style='text-align: center; font-size: 3em;'>🔒</h1>", unsafe_allow_html=True)
                
                with col2:
                    status = "✅ Earned" if is_earned else "🔒 Locked"
                    st.markdown(f"**{badge_data['name']}** - {status}")
                    st.caption(badge_data['description'])
                    st.caption(f"⭐ Worth {badge_data['points']} points")
    
    with tab2:
        st.subheader("Your Certificates")
        
        if earned_certificates:
            for cert in earned_certificates:
                # Find certificate details
                cert_details = None
                for cert_id, cert_data in CERTIFICATES.items():
                    if cert_data['name'] == cert['name']:
                        cert_details = cert_data
                        break
                
                if cert_details:
                    render_certificate(cert['name'], cert_details, cert.get('date', 'N/A')[:10])
                    st.markdown("---")
        else:
            st.info("No certificates earned yet. Complete courses to earn certificates!")
        
        st.markdown("---")
        st.subheader("Available Certificates")
        
        earned_cert_names = [c['name'] for c in earned_certificates]
        
        for cert_id, cert_data in CERTIFICATES.items():
            is_earned = cert_data['name'] in earned_cert_names
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    status = "✅ Earned" if is_earned else "🔒 Locked"
                    st.markdown(f"**{cert_data['name']}** - {status}")
                    st.caption(f"Course: {cert_data['course']}")
                    st.caption(f"Requirement: {cert_data['requirement']}")
                
                with col2:
                    if is_earned:
                        st.markdown("### 🎓")
                    else:
                        st.markdown("### 🔒")


if __name__ == "__main__":
    main()
