import streamlit as st
import sys
from pathlib import Path
import random

sys.path.insert(0, str(Path(__file__).parent.parent))
from data_manager import DataManager
from pages.quiz.styles import apply_quiz_styles

apply_quiz_styles()

# quiz questions - 18 total (3 per topic across 6 topics)
QUESTIONS = [
    # Limit Definition (3 questions)
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
        "topic": "Limit Definition",
        "stem": "Using the limit definition, f'(x) for f(x) = 3x is:",
        "choices": ["3", "3x", "x", "0"],
        "answer": 0,
        "explanation": "f'(x) = lim(h→0) [3(x+h) - 3x]/h = lim(h→0) 3h/h = 3"
    },
    {
        "id": "q3",
        "topic": "Limit Definition",
        "stem": "The derivative as a limit represents:",
        "choices": ["Instantaneous rate of change", "Average rate of change", "Total change", "Indefinite integral"],
        "answer": 0,
        "explanation": "The limit definition captures the instantaneous rate of change at a point"
    },
    # Basic Rules (3 questions)
    {
        "id": "q4", 
        "topic": "Basic Rules", 
        "stem": "Differentiate: f(x)=5x³ − 4x + 7", 
        "choices": ["15x² − 4", "15x² − 4x", "5x² − 4", "15x³ − 4"], 
        "answer": 0,
        "explanation": "Using the power rule: d/dx(5x³) = 15x², d/dx(4x) = 4, d/dx(7) = 0. Result: 15x² - 4"
    },
    {
        "id": "q5",
        "topic": "Basic Rules",
        "stem": "What is the derivative of f(x) = 7?",
        "choices": ["0", "7", "7x", "1"],
        "answer": 0,
        "explanation": "The derivative of any constant is 0"
    },
    {
        "id": "q6",
        "topic": "Basic Rules",
        "stem": "Differentiate: f(x) = √x",
        "choices": ["1/(2√x)", "√x", "2√x", "x/2"],
        "answer": 0,
        "explanation": "Rewrite as x^(1/2), then power rule: (1/2)x^(-1/2) = 1/(2√x)"
    },
    # Product Rule (3 questions)
    {
        "id": "q7", 
        "topic": "Product Rule", 
        "stem": "Differentiate: f(x) = x²·sin x", 
        "choices": ["2x sin x + x² cos x", "x² cos x", "2x sin x", "cos x"], 
        "answer": 0,
        "explanation": "Product Rule: (uv)' = u'v + uv'. Here u=x², v=sin x, so (x²)'(sin x) + (x²)(sin x)' = 2x sin x + x² cos x"
    },
    {
        "id": "q8", 
        "topic": "Product Rule", 
        "stem": "Differentiate: f(x)= (x³)(eˣ)", 
        "choices": ["3x² eˣ + x³ eˣ", "3x² eˣ", "x³ eˣ", "eˣ"], 
        "answer": 0,
        "explanation": "Product Rule: (x³)'(eˣ) + (x³)(eˣ)' = 3x² eˣ + x³ eˣ = eˣ(3x² + x³)"
    },
    {
        "id": "q9",
        "topic": "Product Rule",
        "stem": "Differentiate: f(x) = x·cos(x)",
        "choices": ["cos(x) - x·sin(x)", "-x·sin(x)", "cos(x)", "x·cos(x)"],
        "answer": 0,
        "explanation": "Product Rule: (x)'·cos(x) + x·(cos x)' = 1·cos(x) + x·(-sin x) = cos(x) - x·sin(x)"
    },
    # Chain Rule (3 questions)
    {
        "id": "q10", 
        "topic": "Chain Rule", 
        "stem": "Differentiate: f(x) = (3x² + 1)⁴", 
        "choices": ["4(3x²+1)³·6x", "(3x²+1)³", "12x(3x²+1)⁴", "6x(3x²+1)"], 
        "answer": 0,
        "explanation": "Chain Rule: outer derivative × inner derivative = 4(3x²+1)³ · 6x = 24x(3x²+1)³"
    },
    {
        "id": "q11", 
        "topic": "Chain Rule", 
        "stem": "Differentiate: f(x)=sin(5x²)", 
        "choices": ["cos(5x²)·10x", "cos(5x²)", "5cos(5x²)", "10x"], 
        "answer": 0,
        "explanation": "Chain Rule: outer derivative × inner derivative = cos(5x²) · 10x"
    },
    {
        "id": "q12",
        "topic": "Chain Rule",
        "stem": "Find f'(x) if f(x) = e^(3x)",
        "choices": ["3e^(3x)", "e^(3x)", "3x·e^(3x)", "e^(3x)/3"],
        "answer": 0,
        "explanation": "Chain Rule: e^(3x) · 3 = 3e^(3x)"
    },
    # Implicit Differentiation (3 questions)
    {
        "id": "q13", 
        "topic": "Implicit Diff.", 
        "stem": "For x² + y² = 25, what is dy/dx?", 
        "choices": ["−x/y", "x/y", "−y/x", "y/x"], 
        "answer": 0,
        "explanation": "Differentiate both sides: 2x + 2y(dy/dx) = 0. Solving for dy/dx: dy/dx = -2x/2y = -x/y"
    },
    {
        "id": "q14",
        "topic": "Implicit Diff.",
        "stem": "For xy = 10, find dy/dx",
        "choices": ["-y/x", "y/x", "-x/y", "10"],
        "answer": 0,
        "explanation": "Differentiate: y + x(dy/dx) = 0, so dy/dx = -y/x"
    },
    {
        "id": "q15",
        "topic": "Implicit Diff.",
        "stem": "For x³ + y³ = 6xy, find dy/dx",
        "choices": ["(2y - x²)/(y² - 2x)", "(x² - 2y)/(2x - y²)", "-x²/y²", "3x²/3y²"],
        "answer": 0,
        "explanation": "Differentiate: 3x² + 3y²(dy/dx) = 6y + 6x(dy/dx). Solve: dy/dx = (2y - x²)/(y² - 2x)"
    },
    # Applications (3 questions)
    {
        "id": "q16", 
        "topic": "Applications", 
        "stem": "At x=2, the slope of the tangent to f(x)=x² is:", 
        "choices": ["4", "2", "1", "0"], 
        "answer": 0,
        "explanation": "f'(x) = 2x. At x=2, f'(2) = 2(2) = 4. The derivative gives the slope of the tangent line."
    },
    {
        "id": "q17",
        "topic": "Applications",
        "stem": "The position of an object is s(t) = t³ - 6t². Its velocity at t=1 is:",
        "choices": ["-9", "3", "-5", "-12"],
        "answer": 0,
        "explanation": "Velocity v(t) = s'(t) = 3t² - 12t. At t=1: v(1) = 3(1)² - 12(1) = -9"
    },
    {
        "id": "q18",
        "topic": "Applications",
        "stem": "The area of a circle is A = πr². The rate of change of area with respect to radius is:",
        "choices": ["2πr", "πr²", "πr", "2π"],
        "answer": 0,
        "explanation": "dA/dr = d/dr(πr²) = 2πr (circumference!)"
    },
]


def main():
    # init session state
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_responses" not in st.session_state:
        st.session_state.quiz_responses = []
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {}
    if "shuffled_questions" not in st.session_state:
        st.session_state.shuffled_questions = None
    if "hints_used" not in st.session_state:
        st.session_state.hints_used = []
    if "skipped_questions" not in st.session_state:
        st.session_state.skipped_questions = []

    # check login
    if not st.session_state.get('logged_in', False):
        st.error("⛔ Please login to access the quiz")
        st.stop()

    # header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📝 Initial Assessment Quiz")
    with col2:
        if st.button("🏠 Home", key="quiz_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

    st.markdown("---")

    # start screen
    if not st.session_state.quiz_started:
        st.markdown("""
        <h1 style="font-size: 36px; font-weight: 900; color: #FFFFFF; margin-bottom: 12px;">
            📝 Ready to test your knowledge?
        </h1>
        <p style="font-size: 16px; color: #B3B3B3; margin-bottom: 32px;">
            This assessment has 18 questions covering 6 key topics (3 questions each). It will help us understand your strengths and recommend personalized lessons.
        </p>
        """, unsafe_allow_html=True)
    
        # Info cards with dark mode
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="quiz-card" style="background: #2d2d2d; border-radius: 16px; padding: 24px; text-align: center; border: 2px solid #404040;">
                <div style="font-size: 48px; margin-bottom: 15px;">📝</div>
                <div style="font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">18</div>
                <div style="font-size: 16px; color: #B3B3B3;">Questions</div>
            </div>
            """, unsafe_allow_html=True)
    
        with col2:
            st.markdown("""
            <div class="quiz-card" style="background: #2d2d2d; border-radius: 16px; padding: 24px; text-align: center; border: 2px solid #404040;">
                <div style="font-size: 48px; margin-bottom: 15px;">⏱️</div>
                <div style="font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">~30</div>
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
                # Use all 18 questions (already organized by topic with 3 per topic)
                selected_questions = QUESTIONS.copy()
                random.shuffle(selected_questions)  # Shuffle order for variety
                
                # Shuffle answer choices for each question
                shuffled_questions = []
                for q in selected_questions:
                    shuffled_q = q.copy()
                    choices_with_indices = list(enumerate(q['choices']))
                    random.shuffle(choices_with_indices)
                    shuffled_q['choices'] = [c for _, c in choices_with_indices]
                    shuffled_q['answer_map'] = [i for i, _ in choices_with_indices]
                    shuffled_q['original_answer'] = q['answer']
                    shuffled_q['shuffled_answer'] = shuffled_q['answer_map'].index(q['answer'])
                    shuffled_questions.append(shuffled_q)
                
                st.session_state.shuffled_questions = shuffled_questions
                st.session_state.quiz_started = True
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_responses = [None] * 18
                st.session_state.hints_used = [False] * 18
                st.session_state.skipped_questions = []
                st.rerun()

    # quiz screen
    elif not st.session_state.quiz_finished:
        # Bounds check to prevent IndexError
        if st.session_state.quiz_idx >= len(st.session_state.shuffled_questions):
            st.session_state.quiz_idx = len(st.session_state.shuffled_questions) - 1
        
        q = st.session_state.shuffled_questions[st.session_state.quiz_idx]
        progress = (st.session_state.quiz_idx + 1) / len(st.session_state.shuffled_questions) * 100
    
        # Progress bar
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown(f'<div class="question-number">Question {st.session_state.quiz_idx + 1} of {len(st.session_state.shuffled_questions)}</div>', unsafe_allow_html=True)
    
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
    
        # Create radio button with shuffled choices
        if current is not None:
            choice = st.radio("choices", q["choices"], index=current, key=key, label_visibility="collapsed")
        else:
            choice = st.radio("choices", q["choices"], key=key, label_visibility="collapsed")
    
        # Save selection
        if choice is not None:
            st.session_state.quiz_responses[st.session_state.quiz_idx] = q["choices"].index(choice)
        
        # Hint and Skip functionality
        hint_col, skip_col = st.columns(2)
        with hint_col:
            if not st.session_state.hints_used[st.session_state.quiz_idx]:
                if st.button("💡 Show Hint", use_container_width=True):
                    st.session_state.hints_used[st.session_state.quiz_idx] = True
                    st.rerun()
            else:
                st.info(f"💡 **Hint:** {q.get('explanation', 'Think about the rule carefully.')[:100]}...")
        
        with skip_col:
            if st.button("⏭️ Skip Question", use_container_width=True):
                if st.session_state.quiz_idx not in st.session_state.skipped_questions:
                    st.session_state.skipped_questions.append(st.session_state.quiz_idx)
                if st.session_state.quiz_idx < len(st.session_state.shuffled_questions) - 1:
                    st.session_state.quiz_idx += 1
                    st.rerun()
    
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
                st.session_state.quiz_responses = [None] * 18
                st.rerun()
    
        with col3:
            if st.session_state.quiz_idx < len(st.session_state.shuffled_questions) - 1:
                if st.button("Next ▶", type="primary", use_container_width=True):
                    st.session_state.quiz_idx += 1
                    st.rerun()
            else:
                # Allow submission if all questions answered or if some were skipped
                answered_count = sum(1 for r in st.session_state.quiz_responses if r is not None)
                submit_enabled = answered_count >= len(st.session_state.shuffled_questions) - len(st.session_state.skipped_questions)
                
                if st.button("✅ Submit Quiz", disabled=not submit_enabled, type="primary", use_container_width=True):
                    # Calculate results with shuffled answers
                    correct_count = 0
                    answered_count = 0
                    for r, q in zip(st.session_state.quiz_responses, st.session_state.shuffled_questions):
                        if r is not None:
                            answered_count += 1
                            if r == q["shuffled_answer"]:
                                correct_count += 1
                    st.session_state.quiz_score = correct_count
                    print(f"📊 Quiz Submission: Answered={answered_count}/18, Correct={correct_count}/18, Skipped={18-answered_count}")
                
                    # Store detailed quiz data for feedback page
                    st.session_state.quiz_data = {
                        "questions": st.session_state.shuffled_questions,
                        "responses": st.session_state.quiz_responses,
                        "score": correct_count,
                        "total": len(st.session_state.shuffled_questions)
                    }
                
                    st.session_state.quiz_finished = True
                    st.session_state.quiz_completed = True  # Mark quiz as completed for feedback access
                    st.rerun()

    # results screen
    else:
        score = st.session_state.quiz_score
        total = len(st.session_state.shuffled_questions)
        pct = round(100 * score / total)
        
        if pct >= 90:
            perf_msg = "🌟 Outstanding!"
            perf_color = "#6B8E23"
        elif pct >= 75:
            perf_msg = "🎉 Great Job!"
            perf_color = "#6B8E23"
        elif pct >= 60:
            perf_msg = "👍 Good Effort!"
            perf_color = "#FFA500"
        else:
            perf_msg = "📚 Keep Practicing!"
            perf_color = "#FFA500"
    
        # analyze performance
        if not st.session_state.get('quiz_analyzed', False):
            topic_performance = {}
            for i, (r, q) in enumerate(zip(st.session_state.quiz_responses, st.session_state.shuffled_questions)):
                topic = q["topic"]
                is_correct = (r == q["shuffled_answer"]) if r is not None else False
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
            print(f"🎓 Saving initial quiz: {st.session_state.username}, Score: {score}/{total}, Weak: {weak_topics}, Strong: {strong_topics}")
            DataManager.save_quiz_results(
                st.session_state.username,
                "initial",
                score,
                total,
                weak_topics,
                strong_topics
            )
            print(f"✅ Initial quiz saved successfully")
        
            # Award badge with explanation
            badge_earned = ""
            badge_reason = ""
            if pct >= 80:
                DataManager.award_badge(
                    st.session_state.username,
                    "Quiz Master 🎯",
                    "Scored 80% or higher on initial quiz"
                )
                badge_earned = "Quiz Master 🎯"
                badge_reason = "You scored 80%+ showing strong foundational understanding!"
            else:
                DataManager.award_badge(
                    st.session_state.username,
                    "Quiz Starter 📝",
                    "Completed initial quiz"
                )
                badge_earned = "Quiz Starter 📝"
                badge_reason = "You've taken the first step in your learning journey!"
            
            # Store badge info for display
            st.session_state.badge_earned = badge_earned
            st.session_state.badge_reason = badge_reason
        
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
        
        # Badge award notification
        if hasattr(st.session_state, 'badge_earned'):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                        padding: 20px; border-radius: 12px; border-left: 4px solid #6B8E23; margin-bottom: 20px;">
                <div style="font-size: 18px; font-weight: 600; color: #FFFFFF; margin-bottom: 8px;">
                    🏆 Badge Earned: {st.session_state.badge_earned}
                </div>
                <div style="font-size: 13px; color: #E0E0E0;">
                    <strong>🤖 Why you earned this:</strong> {st.session_state.badge_reason}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # Topic Performance Summary
        topic_stats = {}
        for r, q in zip(st.session_state.quiz_responses, st.session_state.shuffled_questions):
            topic = q['topic']
            if topic not in topic_stats:
                topic_stats[topic] = {'correct': 0, 'total': 0}
            topic_stats[topic]['total'] += 1
            # Only count as correct if answered AND correct (not if skipped/None)
            if r is not None and r == q['shuffled_answer']:
                topic_stats[topic]['correct'] += 1
        
        st.markdown("### 📊 Performance by Topic")
        cols = st.columns(min(3, len(topic_stats)))
        weak_found = []
        strong_found = []
        for idx, (topic, stats) in enumerate(topic_stats.items()):
            topic_pct = round(100 * stats['correct'] / stats['total'])
            with cols[idx % len(cols)]:
                color = "#6B8E23" if topic_pct >= 75 else "#FFA500" if topic_pct >= 50 else "#DC3545"
                if topic_pct >= 75:
                    strong_found.append(topic)
                elif topic_pct < 50:
                    weak_found.append(topic)
                st.markdown(f"""
                <div style="background: #2d2d2d; border-radius: 12px; padding: 20px; text-align: center; border-left: 4px solid {color};">
                    <div style="font-size: 14px; color: #B3B3B3; margin-bottom: 8px;">{topic}</div>
                    <div style="font-size: 32px; font-weight: 700; color: {color};">{topic_pct}%</div>
                    <div style="font-size: 12px; color: #777;">{stats['correct']}/{stats['total']} correct</div>
                </div>
                """, unsafe_allow_html=True)
        
        # ML explanation for topic performance
        st.markdown("### 🤖 ML Analysis of Your Performance")
        
        if strong_found:
            st.markdown(f"""
            <div style="background: rgba(107, 142, 35, 0.2); 
                        padding: 12px; border-radius: 8px; border-left: 4px solid #6B8E23; 
                        margin: 10px 0;">
                <div style="color: #6B8E23; font-weight: 600;">
                    ✅ <strong>Strengths:</strong> {", ".join(strong_found)}
                </div>
                <div style="color: #E0E0E0; font-size: 14px; margin-top: 4px;">
                    You aced these! We'll challenge you with harder questions here.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if weak_found:
            topic_order = [
                "Basic Rules",
                "Limit Definition",
                "Implicit Diff.",
                "Applications",
                "Chain Rule",
                "Product Rule"
            ]
            ordered_weak = [topic for topic in topic_order if topic in weak_found]

            st.markdown(f"""
            <div style="background: rgba(220, 53, 69, 0.2); 
                        padding: 12px; border-radius: 8px; border-left: 4px solid #DC3545;
                        margin: 10px 0;">
                <div style="color: #DC3545; font-weight: 600;">
                    🔍 <strong>Focus Areas:</strong> {", ".join(ordered_weak)}
                </div>
                <div style="color: #E0E0E0; font-size: 14px; margin-top: 4px;">
                    These topics need more work. We'll recommend targeted lessons and practice questions.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if not (weak_found or strong_found):
            st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.2); 
                        padding: 12px; border-radius: 8px; border-left: 4px solid #FFC107;
                        margin: 10px 0;">
                <div style="color: #FFC107; font-weight: 600;">
                    📊 <strong>Consistent Performance</strong>
                </div>
                <div style="color: #E0E0E0; font-size: 14px; margin-top: 4px;">
                    Your performance is balanced across all topics. Keep practicing to improve further!
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Review with Explanations")
    
        for i, (r, q) in enumerate(zip(st.session_state.quiz_responses, st.session_state.shuffled_questions), start=1):
            is_correct = (r == q["shuffled_answer"]) if r is not None else False
            status_icon = "✅" if is_correct else "❌"
            status_color = "#6B8E23" if is_correct else "#DC3545"
            border_color = "#6B8E23" if is_correct else "#DC3545"
        
            with st.expander(f"{status_icon} Question {i}: {q['topic']}" + (" ✓ Correct" if is_correct else " ✗ Incorrect"), expanded=not is_correct):
                # Get display values to avoid nested f-string issues
                user_answer = q['choices'][r] if r is not None else '— (No answer selected)'
                question_text = q['stem']
                
                st.markdown(f"""
                <div style="background: #2d2d2d; border-radius: 12px; padding: 20px; border-left: 4px solid {border_color};">
                    <div style="font-size: 18px; color: #FFFFFF; margin-bottom: 15px; font-weight: 600;">{question_text}</div>
                    <div style="font-size: 14px; margin-bottom: 10px;">
                        <div style="color: #B3B3B3; margin-bottom: 5px;"><b>Your answer:</b></div>
                        <div style="color: {status_color}; font-size: 16px; padding: 10px; background: #1a1a1a; border-radius: 8px; margin-bottom: 10px;">
                            {user_answer}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if not is_correct:
                    correct_answer = q['choices'][q['shuffled_answer']]
                    st.markdown(f"""
                    <div style="font-size: 14px; margin-bottom: 10px;">
                        <div style="color: #B3B3B3; margin-bottom: 5px;"><b>Correct answer:</b></div>
                        <div style="color: #6B8E23; font-size: 16px; padding: 10px; background: #1a1a1a; border-radius: 8px; margin-bottom: 10px;">
                            {correct_answer}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
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
                st.session_state.quiz_responses = [None] * 18
                st.session_state.quiz_finished = False
                st.session_state.quiz_analyzed = False
                st.session_state.shuffled_questions = None
                st.session_state.hints_used = [False] * 18
                st.session_state.skipped_questions = []
                st.rerun()
