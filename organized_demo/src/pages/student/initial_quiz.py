"""
Initial Assessment Quiz - Adaptive ML-Powered
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from data_manager import DataManager

# Apply dark mode quiz styling
from pages.quiz.styles import apply_quiz_styles
apply_quiz_styles()

# Don't set page config here - it's set in main app

# -------------------------
# QUESTION BANK WITH EXPLANATIONS
# -------------------------
QUESTIONS = [
    {
        "id": "q1", 
        "topic": "Limit Definition", 
        "stem": "Using the limit definition, what is f'(x) if f(x)=x²?", 
        "choices": ["2x", "x", "x²", "1"], 
        "answer": 0,
        "explanation": "Using the limit definition: f'(x) = lim(h→0) [(x+h)² - x²]/h = lim(h→0) [2xh + h²]/h = 2x"
    },
    {
        "id": "q2", 
        "topic": "Basic Rules", 
        "stem": "Differentiate: f(x)=5x³ − 4x + 7.", 
        "choices": ["15x² − 4", "15x² − 4x", "5x² − 4", "15x³ − 4"], 
        "answer": 0,
        "explanation": "Using the power rule: d/dx(5x³) = 15x², d/dx(4x) = 4, d/dx(7) = 0. Result: 15x² - 4"
    },
    {
        "id": "q3", 
        "topic": "Product Rule", 
        "stem": "Differentiate: f(x) = x²·sin x.", 
        "choices": ["2x sin x + x² cos x", "x² cos x", "2x sin x", "cos x"], 
        "answer": 0,
        "explanation": "Product Rule: (uv)' = u'v + uv'. Here u=x², v=sin x, so (x²)'(sin x) + (x²)(sin x)' = 2x sin x + x² cos x"
    },
    {
        "id": "q4", 
        "topic": "Chain Rule", 
        "stem": "Differentiate: f(x) = (3x² + 1)⁴.", 
        "choices": ["4(3x²+1)³·6x", "(3x²+1)³", "12x(3x²+1)⁴", "6x(3x²+1)"], 
        "answer": 0,
        "explanation": "Chain Rule: outer derivative × inner derivative = 4(3x²+1)³ · 6x = 24x(3x²+1)³"
    },
    {
        "id": "q5", 
        "topic": "Implicit Diff.", 
        "stem": "For x² + y² = 25, what is dy/dx?", 
        "choices": ["−x/y", "x/y", "−y/x", "y/x"], 
        "answer": 0,
        "explanation": "Differentiate both sides: 2x + 2y(dy/dx) = 0. Solving for dy/dx: dy/dx = -2x/2y = -x/y"
    },
    {
        "id": "q6", 
        "topic": "Applications", 
        "stem": "At x=2, the slope of the tangent to f(x)=x² is:", 
        "choices": ["4", "2", "1", "0"], 
        "answer": 0,
        "explanation": "f'(x) = 2x. At x=2, f'(2) = 2(2) = 4. The derivative gives the slope of the tangent line."
    },
    {
        "id": "q7", 
        "topic": "Product Rule", 
        "stem": "Differentiate: f(x)= (x³)(eˣ).", 
        "choices": ["3x² eˣ + x³ eˣ", "3x² eˣ", "x³ eˣ", "eˣ"], 
        "answer": 0,
        "explanation": "Product Rule: (x³)'(eˣ) + (x³)(eˣ)' = 3x² eˣ + x³ eˣ = eˣ(3x² + x³)"
    },
    {
        "id": "q8", 
        "topic": "Chain Rule", 
        "stem": "Differentiate: f(x)=sin(5x²).", 
        "choices": ["cos(5x²)·10x", "cos(5x²)", "5cos(5x²)", "10x"], 
        "answer": 0,
        "explanation": "Chain Rule: outer derivative × inner derivative = cos(5x²) · 10x"
    },
]


def main():
    """Main quiz render function"""
    # -------------------------
    # SESSION STATE INITIALIZATION (MUST BE FIRST!)
    # -------------------------
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_responses" not in st.session_state:
        st.session_state.quiz_responses = [None] * len(QUESTIONS)
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {}

    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.error("⛔ Please login to access the quiz")
        st.stop()

    # -------------------------
    # HEADER WITH HOME BUTTON
    # -------------------------
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📝 Initial Assessment Quiz")
    with col2:
        if st.button("🏠 Home", key="quiz_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

    st.markdown("---")

    # -------------------------
    # START SCREEN
    # -------------------------
    if not st.session_state.quiz_started:
        st.markdown("""
        <h1 style="font-size: 36px; font-weight: 900; color: #FFFFFF; margin-bottom: 12px;">
            📝 Ready to test your knowledge?
        </h1>
        <p style="font-size: 18px; color: #B3B3B3; margin-bottom: 32px;">
            Take the <b style="color: #6B8E23;">Introduction to Derivatives</b> quiz
        </p>
        """, unsafe_allow_html=True)
    
        # Info cards with dark mode
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="quiz-card" style="background: #2d2d2d; border-radius: 16px; padding: 24px; text-align: center; border: 2px solid #404040;">
                <div style="font-size: 48px; margin-bottom: 15px;">📝</div>
                <div style="font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">8</div>
                <div style="font-size: 16px; color: #B3B3B3;">Questions</div>
            </div>
            """, unsafe_allow_html=True)
    
        with col2:
            st.markdown("""
            <div class="quiz-card" style="background: #2d2d2d; border-radius: 16px; padding: 24px; text-align: center; border: 2px solid #404040;">
                <div style="font-size: 48px; margin-bottom: 15px;">⏱️</div>
                <div style="font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">~15</div>
                <div style="font-size: 16px; color: #B3B3B3;">Minutes</div>
            </div>
            """, unsafe_allow_html=True)
    
        with col3:
            st.markdown("""
            <div class="quiz-card" style="background: #2d2d2d; border-radius: 16px; padding: 24px; text-align: center; border: 2px solid #404040;">
                <div style="font-size: 48px; margin-bottom: 15px;">🎯</div>
                <div style="font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">6</div>
                <div style="font-size: 16px; color: #B3B3B3;">Topics</div>
            </div>
            """, unsafe_allow_html=True)
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        # Topics covered
        st.markdown("""
        <h3 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 16px;">
            📚 Topics Covered
        </h3>
        """, unsafe_allow_html=True)
        topics_col1, topics_col2 = st.columns(2)
        with topics_col1:
            st.markdown("✓ **Limit Definition**")
            st.markdown("✓ **Basic Rules**")
            st.markdown("✓ **Product Rule**")
        with topics_col2:
            st.markdown("✓ **Chain Rule**")
            st.markdown("✓ **Implicit Differentiation**")
            st.markdown("✓ **Applications**")
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_responses = [None] * len(QUESTIONS)
                st.session_state.quiz_finished = False
                st.rerun()

    # -------------------------
    # QUIZ SCREEN
    # -------------------------
    elif not st.session_state.quiz_finished:
        q = QUESTIONS[st.session_state.quiz_idx]
        progress = (st.session_state.quiz_idx + 1) / len(QUESTIONS) * 100
    
        # Progress bar
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown(f'<div class="question-number">Question {st.session_state.quiz_idx + 1} of {len(QUESTIONS)}</div>', unsafe_allow_html=True)
    
        # Question card
        st.markdown(f"""
        <div class="question-card">
            <div class="question-topic">{q['topic']}</div>
            <div class="question-stem">{q['stem']}</div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        # Answer choices with proper label
        st.markdown("**Select your answer:**")
        key = f"choice_{q['id']}"
        current = st.session_state.quiz_responses[st.session_state.quiz_idx]
    
        # Create radio button with proper index handling
        if current is not None:
            choice = st.radio("choices", q["choices"], index=current, key=key, label_visibility="collapsed")
        else:
            choice = st.radio("choices", q["choices"], key=key, label_visibility="collapsed")
    
        # Save selection
        if choice is not None:
            st.session_state.quiz_responses[st.session_state.quiz_idx] = q["choices"].index(choice)
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.quiz_idx > 0:
                if st.button("◀ Previous", use_container_width=True):
                    st.session_state.quiz_idx -= 1
                    st.rerun()
    
        with col2:
            if st.button("🔄 Restart Quiz", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.quiz_idx = 0
                st.session_state.quiz_responses = [None] * len(QUESTIONS)
                st.rerun()
    
        with col3:
            if st.session_state.quiz_idx < len(QUESTIONS) - 1:
                if st.button("Next ▶", type="primary", use_container_width=True):
                    st.session_state.quiz_idx += 1
                    st.rerun()
            else:
                submit_enabled = all(r is not None for r in st.session_state.quiz_responses)
                if st.button("✅ Submit Quiz", disabled=not submit_enabled, type="primary", use_container_width=True):
                    # Calculate results
                    correct_count = sum(1 for r, q in zip(st.session_state.quiz_responses, QUESTIONS) if r == q["answer"])
                    st.session_state.quiz_score = correct_count
                
                    # Store detailed quiz data for feedback page
                    st.session_state.quiz_data = {
                        "questions": QUESTIONS,
                        "responses": st.session_state.quiz_responses,
                        "score": correct_count,
                        "total": len(QUESTIONS)
                    }
                
                    st.session_state.quiz_finished = True
                    st.session_state.quiz_completed = True  # Mark quiz as completed for feedback access
                    st.rerun()

    # -------------------------
    # RESULTS SCREEN - ENHANCED WITH EXPLANATIONS
    # -------------------------
    else:
        score = st.session_state.quiz_score
        total = len(QUESTIONS)
        pct = round(100 * score / total)
        
        # Performance message
        if pct >= 90:
            perf_msg = "🌟 Outstanding!"
            perf_color = "#28A745"
        elif pct >= 75:
            perf_msg = "🎉 Great Job!"
            perf_color = "#6B8E23"
        elif pct >= 60:
            perf_msg = "👍 Good Effort!"
            perf_color = "#FFA500"
        else:
            perf_msg = "📚 Keep Practicing!"
            perf_color = "#DC3545"
    
        # ML Analysis: Identify weak and strong topics
        if not st.session_state.get('quiz_analyzed', False):
            topic_performance = {}
            for i, (r, q) in enumerate(zip(st.session_state.quiz_responses, QUESTIONS)):
                topic = q["topic"]
                is_correct = (r == q["answer"]) if r is not None else False
                if topic not in topic_performance:
                    topic_performance[topic] = {"correct": 0, "total": 0}
                topic_performance[topic]["total"] += 1
                if is_correct:
                    topic_performance[topic]["correct"] += 1
        
            # Identify weak (< 50%) and strong (100%) topics
            weak_topics = [topic for topic, perf in topic_performance.items() 
                          if perf["correct"] / perf["total"] < 0.5]
            strong_topics = [topic for topic, perf in topic_performance.items() 
                            if perf["correct"] / perf["total"] == 1.0]
        
            # Save to database with ML analysis
            DataManager.save_quiz_results(
                st.session_state.username,
                "initial",
                score,
                total,
                weak_topics,
                strong_topics
            )
        
            # Award badge
            if pct >= 80:
                DataManager.award_badge(
                    st.session_state.username,
                    "Quiz Master 🎯",
                    "Scored 80% or higher on initial quiz"
                )
            else:
                DataManager.award_badge(
                    st.session_state.username,
                    "Quiz Starter 📝",
                    "Completed initial quiz"
                )
        
            st.session_state.quiz_analyzed = True
    
        # Enhanced Result card
        st.markdown(f"""
        <div class="result-card" style="background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%); border: 2px solid {perf_color}; border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 30px;">
            <div style="font-size: 48px; margin-bottom: 15px;">{perf_msg}</div>
            <div style="font-size: 72px; font-weight: 900; color: {perf_color}; margin: 20px 0;">{pct}%</div>
            <div style="font-size: 24px; color: #B3B3B3; font-weight: 600;">{score} out of {total} correct</div>
            <div style="font-size: 16px; color: #777; margin-top: 10px;">Quiz completed successfully!</div>
        </div>
        """, unsafe_allow_html=True)
    
        # Topic Performance Summary
        topic_stats = {}
        for r, q in zip(st.session_state.quiz_responses, QUESTIONS):
            topic = q['topic']
            if topic not in topic_stats:
                topic_stats[topic] = {'correct': 0, 'total': 0}
            topic_stats[topic]['total'] += 1
            if r == q['answer']:
                topic_stats[topic]['correct'] += 1
        
        st.markdown("### 📊 Performance by Topic")
        cols = st.columns(min(3, len(topic_stats)))
        for idx, (topic, stats) in enumerate(topic_stats.items()):
            topic_pct = round(100 * stats['correct'] / stats['total'])
            with cols[idx % len(cols)]:
                color = "#28A745" if topic_pct >= 75 else "#FFA500" if topic_pct >= 50 else "#DC3545"
                st.markdown(f"""
                <div style="background: #2d2d2d; border-radius: 12px; padding: 20px; text-align: center; border-left: 4px solid {color};">
                    <div style="font-size: 14px; color: #B3B3B3; margin-bottom: 8px;">{topic}</div>
                    <div style="font-size: 32px; font-weight: 700; color: {color};">{topic_pct}%</div>
                    <div style="font-size: 12px; color: #777;">{stats['correct']}/{stats['total']} correct</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Review with Explanations")
    
        for i, (r, q) in enumerate(zip(st.session_state.quiz_responses, QUESTIONS), start=1):
            is_correct = (r == q["answer"]) if r is not None else False
            status_icon = "✅" if is_correct else "❌"
            status_color = "#28A745" if is_correct else "#DC3545"
            border_color = "#28A745" if is_correct else "#DC3545"
        
            with st.expander(f"{status_icon} Question {i}: {q['topic']}" + (" ✓ Correct" if is_correct else " ✗ Incorrect"), expanded=not is_correct):
                st.markdown(f"""
                <div style="background: #2d2d2d; border-radius: 12px; padding: 20px; border-left: 4px solid {border_color};">
                    <div style="font-size: 18px; color: #FFFFFF; margin-bottom: 15px; font-weight: 600;">{q['stem']}</div>
                    <div style="font-size: 14px; margin-bottom: 10px;">
                        <div style="color: #B3B3B3; margin-bottom: 5px;"><b>Your answer:</b></div>
                        <div style="color: {status_color}; font-size: 16px; padding: 10px; background: #1a1a1a; border-radius: 8px; margin-bottom: 10px;">
                            {q['choices'][r] if r is not None else '— (No answer selected)'}
                        </div>
                    </div>
                    {"" if is_correct else f'''
                    <div style="font-size: 14px; margin-bottom: 10px;">
                        <div style="color: #B3B3B3; margin-bottom: 5px;"><b>Correct answer:</b></div>
                        <div style="color: #28A745; font-size: 16px; padding: 10px; background: #1a1a1a; border-radius: 8px; margin-bottom: 10px;">
                            {q['choices'][q['answer']]}
                        </div>
                    </div>
                    '''}
                    <div style="background: #1a1a1a; border-radius: 8px; padding: 15px; margin-top: 15px;">
                        <div style="color: #6B8E23; font-weight: 600; margin-bottom: 8px;">💡 Explanation:</div>
                        <div style="color: #CCCCCC; line-height: 1.6;">{q.get('explanation', 'No explanation available.')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
        st.markdown("<br>", unsafe_allow_html=True)
    
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 View Progress", type="primary", use_container_width=True):
                if "current_page" in st.session_state:
                    st.session_state.current_page = "progress"
                    st.rerun()
    
        with col2:
            if st.button("📚 Study Lessons", use_container_width=True):
                if "current_page" in st.session_state:
                    st.session_state.current_page = "lessons"
                    st.rerun()
    
        with col3:
            if st.button("🔁 Retake Quiz", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_responses = [None] * len(QUESTIONS)
                st.session_state.quiz_finished = False
                st.session_state.quiz_analyzed = False
                st.rerun()
