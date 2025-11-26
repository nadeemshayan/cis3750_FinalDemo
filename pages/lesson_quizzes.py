"""
Lesson Quizzes - Clean, beautiful, ML-adaptive
"""
import streamlit as st
from data_manager import DataManager
import random
from datetime import datetime

# Lesson metadata
LESSONS = {
    "lesson1": {
        "title": "Lesson 1: Basic Derivative Rules",
        "color": "#6B8E23",
        "topics": ["Power Rule", "Constant Rule", "Sum Rule"]
    },
    "lesson2": {
        "title": "Lesson 2: Product & Quotient Rules", 
        "color": "#7BA428",
        "topics": ["Product Rule", "Quotient Rule"]
    },
    "lesson3": {
        "title": "Lesson 3: Chain Rule",
        "color": "#8AB833",
        "topics": ["Chain Rule", "Composite Functions"]
    },
    "lesson4": {
        "title": "Lesson 4: Trigonometric Derivatives",
        "color": "#6B8E23",
        "topics": ["sin, cos derivatives", "tan, cot derivatives"]
    },
    "lesson5": {
        "title": "Lesson 5: Exponential & Logarithmic",
        "color": "#7BA428",
        "topics": ["e^x derivatives", "ln(x) derivatives"]
    },
    "lesson6": {
        "title": "Lesson 6: Applications",
        "color": "#8AB833",
        "topics": ["Related Rates", "Optimization", "Motion"]
    }
}

# Question bank - 10 questions per lesson
QUESTION_BANKS = {
    "lesson1": [
        {"q": "What is the derivative of x³?", "choices": ["3x²", "x²", "3x", "x³"], "answer": 0, "difficulty": "easy"},
        {"q": "What is the derivative of 5?", "choices": ["0", "5", "5x", "1"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(x⁴)?", "choices": ["4x³", "x³", "4x⁴", "x⁴"], "answer": 0, "difficulty": "easy"},
        {"q": "What is the derivative of 2x?", "choices": ["2", "2x", "x", "0"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(x² + x)?", "choices": ["2x + 1", "2x", "x + 1", "2x² + x"], "answer": 0, "difficulty": "medium"},
        {"q": "What is the derivative of 3x² - 5x + 7?", "choices": ["6x - 5", "6x - 5x", "3x - 5", "6x²"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx(x⁵ - 2x³ + x):", "choices": ["5x⁴ - 6x² + 1", "5x⁴ - 2x²", "x⁴ - 2x² + 1", "5x⁴ - 6x²"], "answer": 0, "difficulty": "medium"},
        {"q": "What is the derivative of √x?", "choices": ["1/(2√x)", "2√x", "√x/2", "1/√x"], "answer": 0, "difficulty": "hard"},
        {"q": "Find d/dx(1/x²):", "choices": ["-2/x³", "2/x³", "-1/x²", "1/x³"], "answer": 0, "difficulty": "hard"},
        {"q": "What is d/dx(x^(2/3))?", "choices": ["(2/3)x^(-1/3)", "(2/3)x^(2/3)", "x^(-1/3)", "(3/2)x^(1/3)"], "answer": 0, "difficulty": "hard"},
    ],
    "lesson2": [
        {"q": "Using product rule, find d/dx(x·x²):", "choices": ["3x²", "2x²", "x³", "x²"], "answer": 0, "difficulty": "easy"},
        {"q": "What is the product rule formula?", "choices": ["uv' + vu'", "uv'", "u'v'", "(uv)'"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx(x² · x³):", "choices": ["5x⁴", "6x⁵", "5x⁵", "x⁵"], "answer": 0, "difficulty": "easy"},
        {"q": "What is the quotient rule formula?", "choices": ["(vu' - uv')/v²", "(u'v - uv')/v²", "u'/v'", "(uv')/v²"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx(x · sin x):", "choices": ["x·cos x + sin x", "x·cos x", "cos x + sin x", "x·sin x"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx((x²)(e^x)):", "choices": ["e^x(x² + 2x)", "2x·e^x", "x²·e^x", "e^x(2x)"], "answer": 0, "difficulty": "medium"},
        {"q": "What is d/dx(x/x²)?", "choices": ["-1/x²", "1/x²", "0", "1/x"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx((3x² + 1)(2x - 5)):", "choices": ["12x² - 30x + 2", "6x - 5", "12x² + 2", "6x² - 15x"], "answer": 0, "difficulty": "hard"},
        {"q": "Find d/dx(x²/sin x):", "choices": ["(2x·sin x - x²·cos x)/sin² x", "2x/cos x", "2x/sin x", "x²/cos x"], "answer": 0, "difficulty": "hard"},
        {"q": "Using product rule, find d/dx(x³·ln x):", "choices": ["x²(3ln x + 1)", "3x²·ln x", "x³/x + 3x²·ln x", "3x²"], "answer": 0, "difficulty": "hard"},
    ],
    "lesson3": [
        {"q": "What is the chain rule formula?", "choices": ["f'(g(x))·g'(x)", "f'(x)·g'(x)", "f(g'(x))", "f'(x) + g'(x)"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx((x²)³):", "choices": ["6x⁵", "3x⁵", "6x²", "2x⁵"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(sin(2x))?", "choices": ["2cos(2x)", "cos(2x)", "2sin(2x)", "-2cos(2x)"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx((3x + 1)²):", "choices": ["6(3x + 1)", "2(3x + 1)", "6x + 1", "3(3x + 1)"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(e^(2x))?", "choices": ["2e^(2x)", "e^(2x)", "2e^x", "e^(2x²)"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx(sin(x²)):", "choices": ["2x·cos(x²)", "cos(x²)", "2x·sin(x²)", "sin(2x)"], "answer": 0, "difficulty": "medium"},
        {"q": "What is d/dx((x² + 1)⁵)?", "choices": ["10x(x² + 1)⁴", "5(x² + 1)⁴", "10x⁴", "5x(x² + 1)⁴"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx(ln(x³)):", "choices": ["3/x", "1/x³", "3x²", "ln(3x²)"], "answer": 0, "difficulty": "hard"},
        {"q": "What is d/dx(e^(sin x))?", "choices": ["e^(sin x)·cos x", "e^(sin x)", "e^(cos x)", "cos x"], "answer": 0, "difficulty": "hard"},
        {"q": "Find d/dx(sin(cos x)):", "choices": ["-sin x·cos(cos x)", "cos(cos x)", "-cos(cos x)", "sin x·cos(cos x)"], "answer": 0, "difficulty": "hard"},
    ],
    "lesson4": [
        {"q": "What is d/dx(sin x)?", "choices": ["cos x", "-cos x", "sin x", "-sin x"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(cos x)?", "choices": ["-sin x", "sin x", "cos x", "-cos x"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(tan x)?", "choices": ["sec² x", "sec x·tan x", "csc² x", "cos² x"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx(sin x + cos x):", "choices": ["cos x - sin x", "sin x - cos x", "cos x + sin x", "-sin x - cos x"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(sin(2x))?", "choices": ["2cos(2x)", "cos(2x)", "-2sin(2x)", "2sin(2x)"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx(x·sin x):", "choices": ["x·cos x + sin x", "x·cos x", "cos x", "sin x + cos x"], "answer": 0, "difficulty": "medium"},
        {"q": "What is d/dx(sin² x)?", "choices": ["2sin x·cos x", "sin(2x)", "cos² x", "2sin x"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx(tan(x²)):", "choices": ["2x·sec²(x²)", "sec²(x²)", "2x·tan(x²)", "sec²(2x)"], "answer": 0, "difficulty": "hard"},
        {"q": "What is d/dx(sec x)?", "choices": ["sec x·tan x", "sec² x", "-csc x·cot x", "tan x"], "answer": 0, "difficulty": "hard"},
        {"q": "Find d/dx(sin x/cos x):", "choices": ["sec² x", "1", "tan x", "sec x"], "answer": 0, "difficulty": "hard"},
    ],
    "lesson5": [
        {"q": "What is d/dx(e^x)?", "choices": ["e^x", "xe^(x-1)", "e", "x·e^x"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(ln x)?", "choices": ["1/x", "ln x", "x", "1/ln x"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx(2e^x):", "choices": ["2e^x", "e^x", "2e", "2x·e^x"], "answer": 0, "difficulty": "easy"},
        {"q": "What is d/dx(ln(2x))?", "choices": ["1/x", "2/x", "1/(2x)", "ln 2"], "answer": 0, "difficulty": "easy"},
        {"q": "Find d/dx(e^(2x)):", "choices": ["2e^(2x)", "e^(2x)", "2e^x", "e^(2x²)"], "answer": 0, "difficulty": "medium"},
        {"q": "What is d/dx(x·e^x)?", "choices": ["e^x(x + 1)", "x·e^x", "e^x", "x·e^(x+1)"], "answer": 0, "difficulty": "medium"},
        {"q": "Find d/dx(ln(x²)):", "choices": ["2/x", "1/x²", "2x", "ln(2x)"], "answer": 0, "difficulty": "medium"},
        {"q": "What is d/dx(e^(x²))?", "choices": ["2x·e^(x²)", "e^(x²)", "2e^(x²)", "x²·e^(x²-1)"], "answer": 0, "difficulty": "hard"},
        {"q": "Find d/dx(ln(sin x)):", "choices": ["cot x", "1/sin x", "cos x/sin x", "1/cos x"], "answer": 0, "difficulty": "hard"},
        {"q": "What is d/dx(x^x)?", "choices": ["x^x(ln x + 1)", "x·x^(x-1)", "x^x·ln x", "x^x"], "answer": 0, "difficulty": "hard"},
    ],
    "lesson6": [
        {"q": "If s(t) = t², what is velocity v(t)?", "choices": ["2t", "t²", "t", "2"], "answer": 0, "difficulty": "easy"},
        {"q": "If v(t) is velocity, what is v'(t)?", "choices": ["acceleration", "position", "jerk", "speed"], "answer": 0, "difficulty": "easy"},
        {"q": "For optimization, where do max/min occur?", "choices": ["Where f'(x) = 0", "Where f(x) = 0", "Endpoints only", "Where f''(x) = 0"], "answer": 0, "difficulty": "easy"},
        {"q": "If position s = t³, find acceleration at t=2:", "choices": ["12", "6", "8", "4"], "answer": 0, "difficulty": "easy"},
        {"q": "A ladder slides down a wall. This is an example of:", "choices": ["Related rates", "Optimization", "Linear motion", "Integration"], "answer": 0, "difficulty": "medium"},
        {"q": "To maximize area, what do we do with A'(x)?", "choices": ["Set it equal to 0", "Set it equal to 1", "Integrate it", "Differentiate it"], "answer": 0, "difficulty": "medium"},
        {"q": "If f'(c) = 0 and f''(c) > 0, then f has a:", "choices": ["local minimum at c", "local maximum at c", "inflection point at c", "discontinuity at c"], "answer": 0, "difficulty": "medium"},
        {"q": "For h(t) = -16t² + 64t, when is max height?", "choices": ["t = 2", "t = 4", "t = 0", "t = 1"], "answer": 0, "difficulty": "hard"},
        {"q": "If C(x) = 100 + 2x is cost, what is marginal cost?", "choices": ["2", "100", "2x", "102"], "answer": 0, "difficulty": "hard"},
        {"q": "A box with square base, volume 32. Minimize surface area. If side = x, height h = 32/x². What is S'(x)?", "choices": ["2x - 64/x²", "2x + 64/x²", "x² - 32/x", "2x"], "answer": 0, "difficulty": "hard"},
    ]
}


def main():
    """Main lesson quiz page"""
    st.markdown("""
    <style>
        /* Dark theme consistency */
        .main-title {
            font-size: 36px;
            font-weight: 900;
            color: #FFFFFF;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 16px;
            color: #B3B3B3;
            margin-bottom: 30px;
        }
        .lesson-card {
            background: linear-gradient(135deg, rgba(107, 142, 35, 0.15) 0%, rgba(107, 142, 35, 0.05) 100%);
            border: 2px solid rgba(107, 142, 35, 0.4);
            border-left: 5px solid #6B8E23;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .question-card {
            background: #2d2d2d;
            border: 2px solid #404040;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
        }
        .question-number {
            color: #6B8E23;
            font-weight: 700;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .question-text {
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .difficulty-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            margin-left: 10px;
        }
        .diff-easy { background: #58CC02; color: #000; }
        .diff-medium { background: #FFC800; color: #000; }
        .diff-hard { background: #FF4B4B; color: #FFF; }
        .result-box {
            background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            margin: 20px 0;
        }
        .result-score {
            font-size: 72px;
            font-weight: 900;
            color: #FFFFFF;
        }
        .result-text {
            font-size: 18px;
            color: #E0E0E0;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-title">📝 Lesson Quizzes</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Test your knowledge with 10-question ML-adaptive quizzes</div>', unsafe_allow_html=True)
    
    # Get username
    username = st.session_state.get('username', 'guest')
    
    # Lesson selection
    lesson_options = [LESSONS[key]["title"] for key in LESSONS.keys()]
    lesson_keys = list(LESSONS.keys())
    
    # Check if coming from a specific lesson
    default_index = 0
    came_from_lesson = False
    if 'quiz_lesson_id' in st.session_state:
        target_lesson = st.session_state['quiz_lesson_id']
        if target_lesson in lesson_keys:
            default_index = lesson_keys.index(target_lesson)
            came_from_lesson = True
        del st.session_state['quiz_lesson_id']  # Clear it after use
    
    # Show indicator if auto-selected
    if came_from_lesson:
        st.success(f"✅ Auto-selected quiz for {LESSONS[lesson_keys[default_index]]['title']}")
    
    selected_title = st.selectbox(
        "**Choose a lesson:**",
        options=lesson_options,
        index=default_index,
        key="lesson_selector"
    )
    
    lesson_key = lesson_keys[lesson_options.index(selected_title)]
    lesson = LESSONS[lesson_key]
    questions = QUESTION_BANKS[lesson_key]
    
    # Lesson header
    st.markdown(f"""
    <div class="lesson-card">
        <h2 style="color: #90EE90; margin: 0 0 12px 0; font-weight: 800;">{lesson['title']}</h2>
        <p style="color: #E0E0E0; margin: 0 0 15px 0; font-size: 15px;">
            <strong>Topics:</strong> {', '.join(lesson['topics'])}
        </p>
        <p style="color: #B8E986; margin: 0; font-size: 14px; line-height: 1.6;">
            🤖 <strong style="color: #90EE90;">ML-Adaptive Quiz:</strong> This quiz intelligently selects 10 questions based on your performance. Master easy questions to unlock harder ones!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user's past performance for adaptive selection
    progress = DataManager.get_user_progress(username)
    lesson_history = progress.get('lesson_quizzes', {}).get(lesson_key, {})
    past_score = lesson_history.get('best_score_pct', 0)
    
    # Adaptive question selection (10 questions)
    easy_q = [q for q in questions if q['difficulty'] == 'easy']
    medium_q = [q for q in questions if q['difficulty'] == 'medium']
    hard_q = [q for q in questions if q['difficulty'] == 'hard']
    
    selected_questions = []
    if past_score == 0:  # First attempt
        selected_questions.extend(random.sample(easy_q, min(4, len(easy_q))))
        selected_questions.extend(random.sample(medium_q, min(4, len(medium_q))))
        selected_questions.extend(random.sample(hard_q, min(2, len(hard_q))))
    elif past_score < 50:  # Struggling
        selected_questions.extend(random.sample(easy_q, min(5, len(easy_q))))
        selected_questions.extend(random.sample(medium_q, min(3, len(medium_q))))
        selected_questions.extend(random.sample(hard_q, min(2, len(hard_q))))
    elif past_score < 80:  # Improving
        selected_questions.extend(random.sample(easy_q, min(3, len(easy_q))))
        selected_questions.extend(random.sample(medium_q, min(4, len(medium_q))))
        selected_questions.extend(random.sample(hard_q, min(3, len(hard_q))))
    else:  # Mastering
        selected_questions.extend(random.sample(easy_q, min(2, len(easy_q))))
        selected_questions.extend(random.sample(medium_q, min(3, len(medium_q))))
        selected_questions.extend(random.sample(hard_q, min(5, len(hard_q))))
    
    # Fill to 10 if needed
    while len(selected_questions) < 10 and len(selected_questions) < len(questions):
        remaining = [q for q in questions if q not in selected_questions]
        if remaining:
            selected_questions.append(random.choice(remaining))
    
    selected_questions = selected_questions[:10]
    
    # Shuffle
    random.shuffle(selected_questions)
    
    # Show adaptive info
    st.info(f"🤖 **Adaptive Selection:** Based on your performance (best: {past_score}%), we've selected 10 questions tailored to your skill level.")
    
    # Display questions - NO pre-filled answers
    answers = {}
    for idx, q in enumerate(selected_questions, 1):
        diff_class = f"diff-{q['difficulty']}"
        
        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">
                Question {idx}
                <span class="difficulty-badge {diff_class}">{q['difficulty']}</span>
            </div>
            <div class="question-text">{q['q']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Radio buttons with unique keys - NO default index
        answer = st.radio(
            f"Select your answer for Question {idx}:",
            options=q['choices'],
            key=f"q_{lesson_key}_{idx}_{q['q'][:20]}",  # Unique key per question
            label_visibility="collapsed",
            index=None  # NO PRE-SELECTION
        )
        answers[idx] = answer
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
        # Check if all answered
        if None in answers.values() or len([a for a in answers.values() if a]) < 10:
            st.error("⚠️ Please answer all 10 questions before submitting!")
        else:
            # Grade quiz
            correct = 0
            easy_correct = 0
            medium_correct = 0
            hard_correct = 0
            easy_total = 0
            medium_total = 0
            hard_total = 0
            
            for idx, q in enumerate(selected_questions, 1):
                user_answer = answers[idx]
                is_correct = q['choices'].index(user_answer) == q['answer']
                
                if is_correct:
                    correct += 1
                
                if q['difficulty'] == 'easy':
                    easy_total += 1
                    if is_correct:
                        easy_correct += 1
                elif q['difficulty'] == 'medium':
                    medium_total += 1
                    if is_correct:
                        medium_correct += 1
                else:
                    hard_total += 1
                    if is_correct:
                        hard_correct += 1
            
            score_pct = int((correct / 10) * 100)
            
            # Save to progress
            if username != 'guest':
                best_score = max(score_pct, lesson_history.get('best_score_pct', 0))
                attempts = lesson_history.get('attempts', 0) + 1
                
                DataManager.save_quiz_results(
                    username=username,
                    quiz_type=lesson_key,
                    score=correct,
                    total=10,
                    weak_topics=[],
                    strong_topics=[]
                )
                
                # Update with detailed stats
                progress = DataManager.get_user_progress(username)
                if 'lesson_quizzes' not in progress:
                    progress['lesson_quizzes'] = {}
                progress['lesson_quizzes'][lesson_key] = {
                    'completed': True,
                    'score': correct,
                    'total': 10,
                    'score_pct': score_pct,
                    'best_score_pct': best_score,
                    'attempts': attempts,
                    'easy': f"{easy_correct}/{easy_total}",
                    'medium': f"{medium_correct}/{medium_total}",
                    'hard': f"{hard_correct}/{hard_total}",
                    'date': datetime.now().isoformat()
                }
                DataManager._save_json(DataManager.PROGRESS_FILE, progress)
            
            # Show results
            performance = "🌟 Mastering!" if score_pct >= 80 else "📈 Improving!" if score_pct >= 60 else "📚 Keep Learning!"
            
            st.markdown(f"""
            <div class="result-box">
                <div class="result-score">{score_pct}%</div>
                <div class="result-text">
                    You scored {correct} out of 10 correct
                </div>
                <div class="result-text" style="font-size: 24px; font-weight: 700; margin-top: 15px;">
                    {performance}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Easy", f"{easy_correct}/{easy_total}", delta=None)
            with col2:
                st.metric("Medium", f"{medium_correct}/{medium_total}", delta=None)
            with col3:
                st.metric("Hard", f"{hard_correct}/{hard_total}", delta=None)
            
            # ML Insights
            if score_pct >= 80:
                insight = "🎯 **Excellent!** You're mastering this topic. Keep challenging yourself with advanced problems."
                next_step = "Try the next lesson or practice more difficult problems."
            elif score_pct >= 60:
                insight = "💪 **Good progress!** You understand the fundamentals. Focus on medium and hard questions."
                next_step = "Review the lesson content and retry for a higher score."
            else:
                insight = "📖 **Keep practicing!** Review the lesson material and focus on understanding core concepts."
                next_step = "Revisit the lesson content, then try again with easier questions."
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                        padding: 20px; border-radius: 12px; border-left: 4px solid #6B8E23; margin: 20px 0;">
                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">
                    🤖 ML Insights
                </div>
                <div style="font-size: 14px; color: #E0E0E0; margin-bottom: 8px;">
                    {insight}
                </div>
                <div style="font-size: 14px; color: #B3B3B3;">
                    <strong>Next Steps:</strong> {next_step}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show improvement if retaking
            if username != 'guest' and attempts > 1:
                if score_pct > lesson_history.get('best_score_pct', 0):
                    improvement = score_pct - lesson_history.get('best_score_pct', 0)
                    st.success(f"🎉 **New Personal Best!** You improved by {improvement}%!")
                elif score_pct == best_score and score_pct >= 80:
                    st.success(f"🏆 **Consistent Excellence!** Attempt #{attempts} - Best: {best_score}%")
                else:
                    st.info(f"📊 Attempt #{attempts} - Your best: {best_score}%")
            
            if score_pct == 100:
                st.balloons()
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀️ Back to Lessons"):
            st.session_state.current_page = "lessons"
            st.rerun()
    with col2:
        if st.button("🏠 Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with col3:
        if st.button("🔄 Retry Quiz"):
            st.rerun()


if __name__ == "__main__":
    main()
