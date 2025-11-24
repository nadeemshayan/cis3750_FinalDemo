"""Parent dashboard - Monitor children's progress
"""
import streamlit as st
from data_manager import DataManager
from pages.dashboard.styles import apply_dashboard_styles
from datetime import datetime, timedelta


def render():
    """Render parent dashboard"""
    apply_dashboard_styles()
    
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px;">
            Parent Dashboard 👨‍👩‍👧‍👦
        </h1>
        <p style="font-size: 15px; color: #B3B3B3;">Monitor your children's learning progress</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get parent user data
    username = st.session_state.username
    parent_data = DataManager.get_user(username)
    linked_children = parent_data.get('children', [])
    
    # Calculate stats
    if linked_children:
        total_children = len(linked_children)
        children_progress = []
        active_this_week = 0
        
        for child_username in linked_children:
            child_progress = DataManager.get_user_progress(child_username)
            children_progress.append(child_progress)
            
            # Check if active this week
            last_active = child_progress.get('last_active', '')
            if last_active:
                try:
                    last_active_date = datetime.fromisoformat(last_active.split('.')[0])
                    if (datetime.now() - last_active_date).days <= 7:
                        active_this_week += 1
                except:
                    pass
        
        avg_progress = sum(p.get('overall_progress', 0) for p in children_progress) // total_children if total_children > 0 else 0
    else:
        total_children = 0
        avg_progress = 0
        active_this_week = 0
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);">
            <div class="stat-number">{total_children}</div>
            <div class="stat-label">Connected Children</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%);">
            <div class="stat-number">{avg_progress}%</div>
            <div class="stat-label">Avg Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #8B9F29 0%, #7BA428 100%);">
            <div class="stat-number">{active_this_week}</div>
            <div class="stat-label">Active This Week</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Add child section
    with st.expander("➕ Connect New Child", expanded=not linked_children):
        st.markdown("**Enter your child's share code to link their account**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            child_code = st.text_input("Child's Share Code", placeholder="SHARE-XXXX", label_visibility="collapsed")
        with col2:
            if st.button("Connect", use_container_width=True):
                if child_code:
                    with st.spinner("Connecting..."):
                        success, message = DataManager.link_parent_to_child(
                            username,
                            child_code
                        )
                        if success:
                            st.success(f"✅ {message}")
                            st.balloons()
                            st.info("Refresh the page to see your child's progress!")
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.error("Please enter a share code")
    
    st.markdown("---")
    
    # Children's progress reports
    if linked_children:
        st.subheader("📊 Children's Progress Reports")
        
        for child_username in linked_children:
            render_child_report(child_username)
    else:
        st.info("👨‍👩‍👧‍👦 No children connected yet. Use your child's share code to link their account and monitor their progress!")


def render_child_report(child_username: str):
    """Render detailed progress report for a child"""
    child_data = DataManager.get_user(child_username)
    child_progress = DataManager.get_user_progress(child_username)
    
    with st.expander(f"👤 {child_username} - Progress Report", expanded=True):
        
        # Overview stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall = child_progress.get('overall_progress', 0)
            st.metric("Overall Progress", f"{overall}%")
        
        with col2:
            quiz_data = child_progress.get('initial_quiz', {})
            if quiz_data.get('completed'):
                score = quiz_data.get('score', 0)
                total = quiz_data.get('total', 8)
                pct = int((score/total)*100) if total > 0 else 0
                st.metric("Quiz Score", f"{pct}%")
            else:
                st.metric("Quiz Score", "Not taken")
        
        with col3:
            lessons_done = len([l for l in child_progress.get('lessons', {}).values() if l.get('completed')])
            st.metric("Lessons Done", f"{lessons_done}/5")
        
        with col4:
            badges = len(child_progress.get('badges', []))
            st.metric("Badges Earned", badges)
        
        st.markdown("---")
        
        # Detailed sections
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Quiz Results", "📚 Lessons", "⚡ Activity", "🏆 Achievements"])
        
        with tab1:
            render_quiz_details(child_progress)
        
        with tab2:
            render_lesson_details(child_progress)
        
        with tab3:
            render_activity_log(child_username, child_progress)
        
        with tab4:
            render_achievements(child_progress)


def render_quiz_details(progress: dict):
    """Show quiz performance details"""
    quiz_data = progress.get('initial_quiz', {})
    
    if not quiz_data.get('completed'):
        st.info("📝 Initial quiz not yet completed")
        return
    
    score = quiz_data.get('score', 0)
    total = quiz_data.get('total', 8)
    pct = round((score/total)*100) if total > 0 else 0
    
    # Score display
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #2d2d2d; border-radius: 12px;">
            <div style="font-size: 48px; font-weight: 900; color: {'#6B8E23' if pct >= 70 else '#FFA500'};">{pct}%</div>
            <div style="color: #B3B3B3; margin-top: 8px;">{score}/{total} Correct</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Weak & strong topics
        weak = quiz_data.get('weak_topics', [])
        strong = quiz_data.get('strong_topics', [])
        
        if weak:
            st.markdown("**⚠️ Needs practice:**")
            for topic in weak:
                st.markdown(f"- {topic}")
        
        if strong:
            st.markdown("**✅ Strong areas:**")
            for topic in strong:
                st.markdown(f"- {topic}")
    
    # Date taken
    date = quiz_data.get('date', '')
    if date:
        st.caption(f"Completed: {date[:10]}")


def render_lesson_details(progress: dict):
    """Show lesson completion details"""
    lessons = progress.get('lessons', {})
    
    if not lessons:
        st.info("📚 No lessons started yet")
        return
    
    lesson_names = {
        'lesson1': 'Introduction to Derivatives',
        'lesson2': 'Power Rule',
        'lesson3': 'Product & Quotient Rules',
        'lesson4': 'Chain Rule',
        'lesson5': 'Applications'
    }
    
    for lesson_id, lesson_name in lesson_names.items():
        lesson_data = lessons.get(lesson_id, {})
        completed = lesson_data.get('completed', False)
        
        if completed:
            st.success(f"✅ {lesson_name} - Completed")
        else:
            st.info(f"⏳ {lesson_name} - Not started")


def render_activity_log(username: str, progress: dict):
    """Show recent activity and engagement metrics"""
    last_active = progress.get('last_active', '')
    
    if last_active:
        try:
            last_date = datetime.fromisoformat(last_active.split('.')[0])
            days_ago = (datetime.now() - last_date).days
            
            if days_ago == 0:
                status = "🟢 Active today"
                color = "#6B8E23"
            elif days_ago <= 3:
                status = f"🟡 Last active {days_ago} days ago"
                color = "#FFA500"
            elif days_ago <= 7:
                status = f"🟠 Last active {days_ago} days ago"
                color = "#FF8C00"
            else:
                status = f"🔴 Inactive for {days_ago} days"
                color = "#DC3545"
            
            st.markdown(f"""
            <div style="padding: 15px; background: #2d2d2d; border-left: 4px solid {color}; border-radius: 8px; margin-bottom: 15px;">
                <div style="font-size: 18px; font-weight: 600;">{status}</div>
                <div style="color: #B3B3B3; font-size: 14px; margin-top: 5px;">Last seen: {last_date.strftime('%B %d, %Y at %I:%M %p')}</div>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.info("Activity data not available")
    
    # Engagement metrics
    st.markdown("### 📈 Engagement Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        streak = progress.get('streak', 0)
        st.metric("Current Streak", f"{streak} days")
    
    with col2:
        time_spent = progress.get('total_time_spent', 0)
        hours = time_spent // 60
        mins = time_spent % 60
        st.metric("Total Time", f"{hours}h {mins}m")
    
    # Practice activity
    practice = progress.get('practice_problems', {})
    if practice:
        total_attempts = sum(p.get('total', 0) for p in practice.values())
        correct_answers = sum(p.get('correct', 0) for p in practice.values())
        accuracy = round((correct_answers / total_attempts * 100)) if total_attempts > 0 else 0
        
        st.markdown("### ✏️ Practice Activity")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Problems Attempted", total_attempts)
        with col2:
            st.metric("Correct Answers", correct_answers)
        with col3:
            st.metric("Accuracy", f"{accuracy}%")


def render_achievements(progress: dict):
    """Show badges and achievements"""
    badges = progress.get('badges', [])
    
    if not badges:
        st.info("🏆 No badges earned yet")
        return
    
    st.markdown(f"**{len(badges)} Badges Earned:**")
    
    # Display badges in grid
    cols = st.columns(3)
    for idx, badge in enumerate(badges):
        with cols[idx % 3]:
            name = badge.get('name', 'Badge')
            desc = badge.get('description', '')
            date = badge.get('date', '')[:10] if badge.get('date') else ''
            
            st.markdown(f"""
            <div style="background: #2d2d2d; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px;">
                <div style="font-size: 32px; margin-bottom: 8px;">{name.split()[0]}</div>
                <div style="font-size: 14px; font-weight: 600; color: #FFFFFF; margin-bottom: 5px;">{' '.join(name.split()[1:])}</div>
                <div style="font-size: 12px; color: #B3B3B3; margin-bottom: 8px;">{desc}</div>
                <div style="font-size: 11px; color: #777;">{date}</div>
            </div>
            """, unsafe_allow_html=True)
