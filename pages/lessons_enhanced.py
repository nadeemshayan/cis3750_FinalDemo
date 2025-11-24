"""
Enhanced Lessons Module with ML-based recommendations and adaptive learning
"""

import streamlit as st
from datetime import datetime
import time
from data_manager import DataManager


# Lesson content with estimated times and prerequisites
LESSONS = {
    "lesson1": {
        "id": "lesson1",
        "title": "Introduction to Derivatives",
        "level": 1,
        "estimated_time": 15,
        "prerequisites": [],
        "topics": ["Definition of Derivatives", "Rate of Change", "Notation"],
        "content": """
        ## Introduction to Derivatives
        
        ### What is a Derivative?
        A derivative represents the **rate of change** of a function. Think of it as the slope of a curve at any given point.
        
        ### Key Concepts:
        1. **Instantaneous Rate of Change**: How fast something is changing at a specific moment
        2. **Slope of Tangent Line**: The derivative gives us the slope of the line that just touches the curve
        3. **Notation**: We write derivatives as f'(x), dy/dx, or df/dx
        
        ### Real-World Example:
        If s(t) represents your position at time t, then s'(t) is your **velocity** - how fast your position is changing!
        
        ### The Limit Definition:
        ```
        f'(x) = lim[h→0] (f(x+h) - f(x)) / h
        ```
        
        This formula captures the essence of derivatives!
        """,
        "video_url": "https://www.youtube.com/embed/example1",
        "quiz_questions": 3
    },
    "lesson2": {
        "id": "lesson2",
        "title": "Power Rule",
        "level": 1,
        "estimated_time": 20,
        "prerequisites": ["lesson1"],
        "topics": ["Power Rule", "Basic Derivatives", "Practice"],
        "content": """
        ## The Power Rule
        
        ### The Rule:
        If f(x) = x^n, then f'(x) = n·x^(n-1)
        
        ### Examples:
        1. f(x) = x³ → f'(x) = 3x²
        2. f(x) = x⁵ → f'(x) = 5x⁴
        3. f(x) = x → f'(x) = 1
        4. f(x) = 1 (constant) → f'(x) = 0
        
        ### Why Does It Work?
        The power rule comes directly from the limit definition but provides a quick shortcut!
        
        ### Practice Problems:
        Try finding derivatives of:
        - f(x) = x⁴
        - g(x) = x⁷
        - h(x) = 5
        """,
        "video_url": "https://www.youtube.com/embed/example2",
        "quiz_questions": 5
    },
    "lesson3": {
        "id": "lesson3",
        "title": "Product and Quotient Rules",
        "level": 2,
        "estimated_time": 25,
        "prerequisites": ["lesson1", "lesson2"],
        "topics": ["Product Rule", "Quotient Rule", "Combining Rules"],
        "content": """
        ## Product and Quotient Rules
        
        ### Product Rule:
        If f(x) = g(x)·h(x), then:
        ```
        f'(x) = g'(x)·h(x) + g(x)·h'(x)
        ```
        
        **Mnemonic**: "First times derivative of second, plus second times derivative of first"
        
        ### Quotient Rule:
        If f(x) = g(x)/h(x), then:
        ```
        f'(x) = [g'(x)·h(x) - g(x)·h'(x)] / [h(x)]²
        ```
        
        **Mnemonic**: "Low d-high minus high d-low, over the square of what's below"
        
        ### Examples:
        1. f(x) = x²·sin(x) (product rule needed)
        2. f(x) = x³/(x+1) (quotient rule needed)
        """,
        "video_url": "https://www.youtube.com/embed/example3",
        "quiz_questions": 5
    },
    "lesson4": {
        "id": "lesson4",
        "title": "Chain Rule",
        "level": 2,
        "estimated_time": 30,
        "prerequisites": ["lesson1", "lesson2"],
        "topics": ["Chain Rule", "Composition of Functions", "Advanced Derivatives"],
        "content": """
        ## The Chain Rule
        
        ### The Rule:
        If f(x) = g(h(x)), then:
        ```
        f'(x) = g'(h(x))·h'(x)
        ```
        
        **In words**: Derivative of outer function (evaluated at inner) times derivative of inner function
        
        ### Examples:
        1. f(x) = (x² + 1)³
           - Outer: g(u) = u³, Inner: h(x) = x² + 1
           - f'(x) = 3(x² + 1)²·2x = 6x(x² + 1)²
        
        2. f(x) = sin(x²)
           - f'(x) = cos(x²)·2x
        
        ### Tips:
        - Identify the "outer" and "inner" functions
        - Work from outside to inside
        - Don't forget to multiply by the inner derivative!
        """,
        "video_url": "https://www.youtube.com/embed/example4",
        "quiz_questions": 6
    },
    "lesson5": {
        "id": "lesson5",
        "title": "Applications of Derivatives",
        "level": 3,
        "estimated_time": 35,
        "prerequisites": ["lesson1", "lesson2", "lesson3", "lesson4"],
        "topics": ["Optimization", "Related Rates", "Real-World Problems"],
        "content": """
        ## Applications of Derivatives
        
        ### 1. Finding Maximum and Minimum Values
        - Set f'(x) = 0 to find critical points
        - Use second derivative test: f''(x) > 0 → minimum, f''(x) < 0 → maximum
        
        ### 2. Optimization Problems
        Example: Find the dimensions of a rectangle with perimeter 100 that maximizes area.
        
        ### 3. Related Rates
        When two quantities are related and both change over time.
        
        Example: A balloon is being inflated. If the radius increases at 2 cm/s, how fast is the volume changing?
        
        ### 4. Motion Problems
        - Position: s(t)
        - Velocity: v(t) = s'(t)
        - Acceleration: a(t) = v'(t) = s''(t)
        
        ### Real-World Applications:
        - Economics: Marginal cost and revenue
        - Physics: Velocity and acceleration
        - Biology: Population growth rates
        - Engineering: Optimization of designs
        """,
        "video_url": "https://www.youtube.com/embed/example5",
        "quiz_questions": 7
    }
}


def get_unlocked_lessons(username: str) -> list:
    """Determine which lessons are unlocked for the user based on their progress"""
    progress = DataManager.get_user_progress(username)
    completed_lessons = [lid for lid, data in progress.get('lessons', {}).items() if data.get('completed')]
    
    unlocked = []
    for lesson_id, lesson in LESSONS.items():
        # Check if prerequisites are met
        prerequisites_met = all(prereq in completed_lessons for prereq in lesson.get('prerequisites', []))
        
        # First lesson or prerequisites met
        if not lesson.get('prerequisites') or prerequisites_met:
            unlocked.append(lesson_id)
    
    return unlocked


def get_recommended_lesson(username: str) -> str:
    """ML-based recommendation for next lesson based on weak topics"""
    progress = DataManager.get_user_progress(username)
    weak_topics = progress.get('initial_quiz', {}).get('weak_topics', [])
    completed_lessons = [lid for lid, data in progress.get('lessons', {}).items() if data.get('completed')]
    unlocked = get_unlocked_lessons(username)
    
    # Find uncompleted lessons that match weak topics
    for lesson_id in unlocked:
        if lesson_id not in completed_lessons:
            lesson = LESSONS[lesson_id]
            # Check if lesson covers any weak topics
            if any(topic in str(lesson.get('topics', [])) for topic in weak_topics):
                return lesson_id
    
    # Default: return first uncompleted unlocked lesson
    for lesson_id in unlocked:
        if lesson_id not in completed_lessons:
            return lesson_id
    
    return list(LESSONS.keys())[0] if LESSONS else None


def render_lesson_card(lesson_id: str, is_unlocked: bool, is_completed: bool):
    """Render a lesson card"""
    lesson = LESSONS[lesson_id]
    
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            status = "✅" if is_completed else ("🔓" if is_unlocked else "🔒")
            st.markdown(f"### {status} {lesson['title']}")
            st.caption(f"Level {lesson['level']} • {', '.join(lesson['topics'])}")
        
        with col2:
            st.metric("Time", f"~{lesson['estimated_time']} min")
        
        with col3:
            st.metric("Questions", lesson['quiz_questions'])
        
        if is_unlocked:
            button_label = "Review Lesson" if is_completed else "Start Lesson"
            if st.button(button_label, key=f"start_{lesson_id}", use_container_width=True, 
                        type="primary" if not is_completed else "secondary"):
                st.session_state.viewing_lesson = lesson_id
                st.session_state.lesson_start_time = time.time()
                st.rerun()
        else:
            st.warning("🔒 Complete prerequisites to unlock")
            if lesson['prerequisites']:
                prereq_names = [LESSONS[pid]['title'] for pid in lesson['prerequisites']]
                st.caption(f"Prerequisites: {', '.join(prereq_names)}")


def render_lesson_view(lesson_id: str):
    """Render the full lesson view"""
    lesson = LESSONS[lesson_id]
    
    # Back button
    if st.button("← Back to Lessons"):
        st.session_state.viewing_lesson = None
        st.rerun()
    
    st.title(lesson['title'])
    st.caption(f"Level {lesson['level']} • Estimated time: {lesson['estimated_time']} minutes")
    
    # Progress indicator
    if lesson_id in st.session_state.get('lesson_progress', {}):
        progress_val = st.session_state.lesson_progress[lesson_id]
        st.progress(progress_val, text=f"Progress: {int(progress_val * 100)}%")
    
    st.markdown("---")
    
    # Tabs for content
    tab1, tab2, tab3 = st.tabs(["📖 Content", "🎥 Video", "✏️ Notes"])
    
    with tab1:
        st.markdown(lesson['content'])
        
        # Scroll progress simulation
        if st.button("Mark as Read", type="primary"):
            st.success("Content marked as read! ✓")
            if lesson_id not in st.session_state.get('lesson_progress', {}):
                st.session_state.lesson_progress = st.session_state.get('lesson_progress', {})
                st.session_state.lesson_progress[lesson_id] = 0.5
    
    with tab2:
        st.markdown("### 🎥 Video Lesson")
        st.info("Video player would be embedded here")
        # st.video(lesson['video_url'])  # Uncomment with real videos
        
        if st.button("Mark Video as Watched"):
            st.success("Video marked as watched! ✓")
            if lesson_id not in st.session_state.get('lesson_progress', {}):
                st.session_state.lesson_progress = st.session_state.get('lesson_progress', {})
            st.session_state.lesson_progress[lesson_id] = 0.8
    
    with tab3:
        st.markdown("### 📝 Your Notes")
        notes_key = f"notes_{lesson_id}"
        current_notes = st.session_state.get(notes_key, "")
        
        notes = st.text_area(
            "Write your notes here...",
            value=current_notes,
            height=200,
            placeholder="Take notes as you learn..."
        )
        
        if st.button("Save Notes"):
            st.session_state[notes_key] = notes
            st.success("Notes saved! 📝")
    
    st.markdown("---")
    
    # Complete lesson button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Complete Lesson & Take Quiz", use_container_width=True, type="primary"):
            # Calculate time spent
            if hasattr(st.session_state, 'lesson_start_time'):
                time_spent = int(time.time() - st.session_state.lesson_start_time)
            else:
                time_spent = lesson['estimated_time'] * 60
            
            # Save lesson progress
            DataManager.save_lesson_progress(
                st.session_state.username,
                lesson_id,
                completed=True,
                time_spent=time_spent
            )
            
            # Award badge for first lesson
            progress = DataManager.get_user_progress(st.session_state.username)
            if len(progress.get('lessons', {})) == 1:
                DataManager.award_badge(
                    st.session_state.username,
                    "First Lesson Complete! 🎓",
                    "Completed your first lesson"
                )
            
            st.success(f"Lesson completed! Time spent: {time_spent // 60} minutes")
            st.balloons()
            
            # Redirect to quiz
            st.session_state.current_page = "lesson_quizzes"
            st.session_state.quiz_lesson_id = lesson_id
            st.rerun()


def main():
    """Main lessons page"""
    if st.session_state.get('viewing_lesson'):
        render_lesson_view(st.session_state.viewing_lesson)
        return
    
    # Home button at top
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📚 Interactive Lessons")
    with col2:
        if st.button("🏠 Home", key="lessons_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("Master calculus concepts through structured, adaptive learning paths")
    
    username = st.session_state.username
    
    # Check if initial quiz is completed
    progress = DataManager.get_user_progress(username)
    quiz_completed = progress.get('initial_quiz', {}).get('completed', False)
    
    if not quiz_completed:
        st.warning("⚠️ Please complete the Initial Assessment Quiz first to unlock lessons!")
        st.markdown("---")
        if st.button("📝 Take Initial Quiz", use_container_width=True, type="primary"):
            st.session_state.current_page = "initial_quiz"
            st.rerun()
        return
    
    # Get user progress
    progress = DataManager.get_user_progress(username)
    completed_lessons = [lid for lid, data in progress.get('lessons', {}).items() if data.get('completed')]
    unlocked_lessons = get_unlocked_lessons(username)
    
    # Show overall progress
    total_lessons = len(LESSONS)
    completed_count = len(completed_lessons)
    progress_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lessons Completed", f"{completed_count}/{total_lessons}")
    with col2:
        st.metric("Overall Progress", f"{progress_percentage:.0f}%")
    with col3:
        total_time = progress.get('total_time_spent', 0)
        st.metric("Total Time", f"{total_time // 60}h {total_time % 60}m")
    
    st.progress(progress_percentage / 100)
    
    st.markdown("---")
    
    # Recommended lesson
    recommended = get_recommended_lesson(username)
    showed_recommended = False
    if recommended and recommended not in completed_lessons:
        st.subheader("🎯 Recommended for You")
        st.info(f"Based on your quiz results, we recommend: **{LESSONS[recommended]['title']}**")
        render_lesson_card(recommended, True, False)
        showed_recommended = True
        st.markdown("---")
    
    # All lessons
    st.subheader("📖 All Lessons")
    
    for lesson_id, lesson in LESSONS.items():
        # Skip if this was already shown as recommended
        if showed_recommended and lesson_id == recommended:
            continue
            
        is_unlocked = lesson_id in unlocked_lessons
        is_completed = lesson_id in completed_lessons
        render_lesson_card(lesson_id, is_unlocked, is_completed)


if __name__ == "__main__":
    main()
