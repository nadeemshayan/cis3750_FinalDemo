"""
Teacher Analytics - ML-Powered Student Insights
"""
import streamlit as st
from data_manager import DataManager
from pages.dashboard.styles import apply_dashboard_styles
import json
from pathlib import Path


def get_students_by_teacher(teacher_code):
    """Get all students connected to this teacher"""
    users_file = Path(__file__).parent.parent.parent / "data" / "users.json"
    with open(users_file, 'r') as f:
        users = json.load(f)
    
    students = []
    for username, user_data in users.items():
        if user_data.get('role') == 'Student':
            if teacher_code in user_data.get('teacher_codes', []):
                students.append({
                    'username': username,
                    'email': user_data.get('email'),
                    'grade': user_data.get('grade'),
                    'age_level': user_data.get('age_level')
                })
    return students


def analyze_student_performance(username):
    """ML-powered analysis of student performance"""
    progress = DataManager.get_user_progress(username)
    
    # Extract metrics
    quiz_data = progress.get('initial_quiz', {})
    lessons_data = progress.get('lessons', {})
    practice_data = progress.get('practice_problems', {})
    
    # Calculate scores
    quiz_score = quiz_data.get('score', 0) / max(quiz_data.get('total', 1), 1) * 100
    overall_progress = progress.get('overall_progress', 0)
    
    # Identify weak/strong topics
    weak_topics = quiz_data.get('weak_topics', [])
    strong_topics = quiz_data.get('strong_topics', [])
    
    # Calculate engagement
    total_time = progress.get('total_time_spent', 0)
    lessons_completed = sum(1 for l in lessons_data.values() if l.get('completed'))
    
    # Practice accuracy
    practice_correct = sum(1 for p in practice_data.values() if p.get('correct', 0) > 0)
    practice_total = len(practice_data)
    practice_accuracy = (practice_correct / max(practice_total, 1)) * 100 if practice_total > 0 else 0
    
    # ML Prediction: Risk level
    risk_level = "Low"
    if quiz_score < 50 or overall_progress < 20:
        risk_level = "High"
    elif quiz_score < 70 or overall_progress < 40:
        risk_level = "Medium"
    
    # Recommendations
    recommendations = []
    if weak_topics:
        recommendations.append(f"Focus on: {', '.join(weak_topics)}")
    if practice_accuracy < 60:
        recommendations.append("Needs more practice problems")
    if total_time < 60:
        recommendations.append("Low engagement - encourage regular study")
    if lessons_completed == 0:
        recommendations.append("Has not completed any lessons yet")
    
    return {
        'quiz_score': quiz_score,
        'overall_progress': overall_progress,
        'weak_topics': weak_topics,
        'strong_topics': strong_topics,
        'total_time': total_time,
        'lessons_completed': lessons_completed,
        'practice_accuracy': practice_accuracy,
        'risk_level': risk_level,
        'recommendations': recommendations
    }


def render():
    """Render teacher analytics page"""
    apply_dashboard_styles()
    
    st.markdown("""
    <h1 style="font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px;">
        📊 Student Analytics
    </h1>
    <p style="font-size: 15px; color: #B3B3B3; margin-bottom: 20px;">
        ML-powered insights into student performance
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get teacher code
    user_data = st.session_state.user_data
    teacher_code = user_data.get('teacher_code', 'TEACH-5000')
    
    st.markdown(f"""
    <div style="background: #2d2d2d; padding: 16px; border-radius: 12px; margin-bottom: 20px;">
        <p style="color: #B3B3B3; font-size: 14px; margin: 0;">Your Teacher Code</p>
        <p style="color: #6B8E23; font-size: 24px; font-weight: 900; margin: 8px 0 0 0;">{teacher_code}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get students
    students = get_students_by_teacher(teacher_code)
    
    if not students:
        st.info("📋 No students enrolled yet. Share your teacher code with students!")
        st.code(teacher_code, language=None)
        return
    
    # Class overview
    st.subheader(f"👥 Class Overview ({len(students)} students)")
    
    # Analyze all students
    all_analytics = {}
    for student in students:
        all_analytics[student['username']] = analyze_student_performance(student['username'])
    
    # Class statistics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_quiz = sum(a['quiz_score'] for a in all_analytics.values()) / len(all_analytics)
    avg_progress = sum(a['overall_progress'] for a in all_analytics.values()) / len(all_analytics)
    total_time = sum(a['total_time'] for a in all_analytics.values())
    at_risk = sum(1 for a in all_analytics.values() if a['risk_level'] == 'High')
    
    with col1:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);">
            <div class="stat-number">{:.0f}%</div>
            <div class="stat-label">Avg Quiz Score</div>
        </div>
        """.format(avg_quiz), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%);">
            <div class="stat-number">{:.0f}%</div>
            <div class="stat-label">Avg Progress</div>
        </div>
        """.format(avg_progress), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #8B9F29 0%, #7BA428 100%);">
            <div class="stat-number">{:.0f}h</div>
            <div class="stat-label">Total Study Time</div>
        </div>
        """.format(total_time / 60), unsafe_allow_html=True)
    
    with col4:
        color = "#DC3545" if at_risk > 0 else "#6B8E23"
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, {} 0%, {} 100%);">
            <div class="stat-number">{}</div>
            <div class="stat-label">At Risk</div>
        </div>
        """.format(color, color, at_risk), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Individual student analysis
    st.subheader("🎓 Individual Student Performance")
    
    for student in students:
        username = student['username']
        analytics = all_analytics[username]
        
        # Risk color
        risk_colors = {
            'Low': '#28A745',
            'Medium': '#FFA500', 
            'High': '#DC3545'
        }
        risk_color = risk_colors[analytics['risk_level']]
        
        with st.expander(f"📚 {username.upper()} - {student['grade']} ({analytics['risk_level']} Risk)", expanded=(analytics['risk_level'] == 'High')):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Performance metrics
                st.markdown("**📊 Performance Metrics**")
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("Quiz Score", f"{analytics['quiz_score']:.0f}%")
                with metric_col2:
                    st.metric("Progress", f"{analytics['overall_progress']:.0f}%")
                with metric_col3:
                    st.metric("Practice Accuracy", f"{analytics['practice_accuracy']:.0f}%")
                
                st.markdown("---")
                
                # Topics analysis
                if analytics['strong_topics']:
                    st.markdown("**✅ Strong Topics:**")
                    for topic in analytics['strong_topics']:
                        st.markdown(f"- {topic}")
                
                if analytics['weak_topics']:
                    st.markdown("**⚠️ Struggling With:**")
                    for topic in analytics['weak_topics']:
                        st.markdown(f"- {topic}")
            
            with col2:
                # Engagement
                st.markdown("**⏱️ Engagement**")
                st.metric("Study Time", f"{analytics['total_time']}min")
                st.metric("Lessons Done", f"{analytics['lessons_completed']}")
                
                st.markdown(f"""
                <div style="background: {risk_color}20; border-left: 4px solid {risk_color}; padding: 12px; border-radius: 8px; margin-top: 16px;">
                    <p style="color: {risk_color}; font-weight: 700; margin: 0;">
                        {analytics['risk_level']} Risk
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # ML Recommendations
            if analytics['recommendations']:
                st.markdown("**🤖 ML Recommendations:**")
                for rec in analytics['recommendations']:
                    st.info(f"💡 {rec}")
    
    st.markdown("---")
    
    # Class-wide insights
    st.subheader("🔍 Class-Wide Insights")
    
    # Most common weak topics
    all_weak = []
    for a in all_analytics.values():
        all_weak.extend(a['weak_topics'])
    
    if all_weak:
        from collections import Counter
        weak_counts = Counter(all_weak)
        st.markdown("**⚠️ Topics Most Students Struggle With:**")
        for topic, count in weak_counts.most_common(3):
            percentage = (count / len(students)) * 100
            st.markdown(f"- **{topic}**: {count} students ({percentage:.0f}%)")
    
    # Most common strong topics
    all_strong = []
    for a in all_analytics.values():
        all_strong.extend(a['strong_topics'])
    
    if all_strong:
        from collections import Counter
        strong_counts = Counter(all_strong)
        st.markdown("**✅ Topics Most Students Excel At:**")
        for topic, count in strong_counts.most_common(3):
            percentage = (count / len(students)) * 100
            st.markdown(f"- **{topic}**: {count} students ({percentage:.0f}%)")
