"""
Practice Problems with Intelligent Review Logic
Tracks attempts and recommends review after 3 incorrect attempts
"""

import streamlit as st
from data_manager import DataManager
import random
from ml_features import get_review_schedule, get_adaptive_difficulty, calculate_topic_confidence


# Practice problem bank organized by topic
PRACTICE_PROBLEMS = {
    "basic_derivatives": [
        {
            "id": "bd1",
            "question": "Find the derivative of f(x) = x⁵",
            "options": ["5x⁴", "x⁴", "5x⁶", "4x⁵"],
            "correct": 0,
            "explanation": "Using the power rule: if f(x) = xⁿ, then f'(x) = n·xⁿ⁻¹. So f'(x) = 5x⁴",
            "topic": "Power Rule",
            "difficulty": "easy"
        },
        {
            "id": "bd2",
            "question": "What is the derivative of f(x) = 3x² + 2x + 1?",
            "options": ["6x + 2", "3x + 2", "6x² + 2x", "3x² + 1"],
            "correct": 0,
            "explanation": "Apply the power rule term by term: 3(2x) + 2(1) + 0 = 6x + 2",
            "topic": "Power Rule",
            "difficulty": "easy"
        },
        {
            "id": "bd3",
            "question": "Find f'(x) if f(x) = 7",
            "options": ["0", "7", "7x", "x"],
            "correct": 0,
            "explanation": "The derivative of any constant is 0",
            "topic": "Constant Rule",
            "difficulty": "easy"
        },
        {
            "id": "bd4",
            "question": "Differentiate: f(x) = x⁸",
            "options": ["8x⁷", "x⁷", "8x⁸", "7x⁷"],
            "correct": 0,
            "explanation": "Power rule: d/dx(x⁸) = 8x⁷",
            "topic": "Power Rule",
            "difficulty": "easy"
        },
        {
            "id": "bd5",
            "question": "Find f'(x) if f(x) = 6x⁴ - 2x³ + x",
            "options": ["24x³ - 6x² + 1", "6x³ - 2x²", "24x³ - 6x²", "6x⁴ - 2x³"],
            "correct": 0,
            "explanation": "Power rule term by term: 24x³ - 6x² + 1",
            "topic": "Power Rule",
            "difficulty": "easy"
        },
        {
            "id": "bd6",
            "question": "What is d/dx[1/x]?",
            "options": ["-1/x²", "1/x²", "-x", "1/x"],
            "correct": 0,
            "explanation": "Rewrite as x⁻¹: d/dx = -1·x⁻² = -1/x²",
            "topic": "Power Rule",
            "difficulty": "medium"
        },
        {
            "id": "bd7",
            "question": "Differentiate: f(x) = √(x³)",
            "options": ["(3/2)√x", "3√x", "(3/2)x", "√(3x)"],
            "correct": 0,
            "explanation": "Rewrite as x^(3/2): d/dx = (3/2)x^(1/2) = (3/2)√x",
            "topic": "Power Rule",
            "difficulty": "medium"
        }
    ],
    "product_quotient": [
        {
            "id": "pq1",
            "question": "Find the derivative of f(x) = x²·sin(x) using the product rule",
            "options": ["2x·sin(x) + x²·cos(x)", "2x·cos(x)", "x²·sin(x)", "2x·sin(x)"],
            "correct": 0,
            "explanation": "Product rule: (uv)' = u'v + uv'. Here u = x², v = sin(x), so f'(x) = 2x·sin(x) + x²·cos(x)",
            "topic": "Product Rule",
            "difficulty": "medium"
        },
        {
            "id": "pq2",
            "question": "Find the derivative of f(x) = (x³)/(x+1)",
            "options": ["(2x³ + 3x²)/(x+1)²", "(3x²)/(x+1)", "x²", "(3x² + 3x²)/(x+1)²"],
            "correct": 0,
            "explanation": "Quotient rule: (u/v)' = (u'v - uv')/v². Here: (3x²(x+1) - x³(1))/(x+1)² = (2x³ + 3x²)/(x+1)²",
            "topic": "Quotient Rule",
            "difficulty": "medium"
        },
        {
            "id": "pq3",
            "question": "What is the derivative of f(x) = x·eˣ?",
            "options": ["eˣ + x·eˣ", "x·eˣ", "eˣ", "x·eˣ⁻¹"],
            "correct": 0,
            "explanation": "Product rule: f'(x) = 1·eˣ + x·eˣ = eˣ(1 + x)",
            "topic": "Product Rule",
            "difficulty": "medium"
        }
    ],
    "chain_rule": [
        {
            "id": "cr1",
            "question": "Find the derivative of f(x) = (x² + 1)³",
            "options": ["6x(x² + 1)²", "3(x² + 1)²", "3x²(x² + 1)²", "(x² + 1)²"],
            "correct": 0,
            "explanation": "Chain rule: outer derivative × inner derivative = 3(x² + 1)²·2x = 6x(x² + 1)²",
            "topic": "Chain Rule",
            "difficulty": "medium"
        },
        {
            "id": "cr2",
            "question": "What is the derivative of f(x) = sin(3x)?",
            "options": ["3cos(3x)", "cos(3x)", "3sin(3x)", "-3cos(3x)"],
            "correct": 0,
            "explanation": "Chain rule: cos(3x)·3 = 3cos(3x)",
            "topic": "Chain Rule",
            "difficulty": "medium"
        },
        {
            "id": "cr3",
            "question": "Find f'(x) if f(x) = e^(x²)",
            "options": ["2x·e^(x²)", "e^(x²)", "x²·e^(x²)", "2e^(x²)"],
            "correct": 0,
            "explanation": "Chain rule: e^(x²)·2x = 2x·e^(x²)",
            "topic": "Chain Rule",
            "difficulty": "hard"
        }
    ],
    "applications": [
        {
            "id": "ap1",
            "question": "A ball is thrown upward. Its height is h(t) = -16t² + 64t + 5. What is its velocity at t = 2?",
            "options": ["0 ft/s", "32 ft/s", "64 ft/s", "-32 ft/s"],
            "correct": 0,
            "explanation": "Velocity is the derivative: v(t) = h'(t) = -32t + 64. At t=2: v(2) = -32(2) + 64 = 0 ft/s",
            "topic": "Applications",
            "difficulty": "hard"
        },
        {
            "id": "ap2",
            "question": "To find the maximum of f(x) = -x² + 4x + 1, where should we look?",
            "options": ["Where f'(x) = 0", "Where f(x) = 0", "At x = 0", "Where f''(x) = 0"],
            "correct": 0,
            "explanation": "Critical points (maxima/minima) occur where f'(x) = 0",
            "topic": "Optimization",
            "difficulty": "medium"
        },
        {
            "id": "ap3",
            "question": "The cost function is C(x) = 100 + 50x. What is the marginal cost?",
            "options": ["50", "100", "50x", "150"],
            "correct": 0,
            "explanation": "Marginal cost is C'(x) = 50 (constant marginal cost)",
            "topic": "Applications",
            "difficulty": "easy"
        },
        {
            "id": "ap4",
            "question": "A square's side length increases at 2 cm/s. How fast does its area increase when side = 10 cm?",
            "options": ["40 cm²/s", "20 cm²/s", "100 cm²/s", "4 cm²/s"],
            "correct": 0,
            "explanation": "A = s². dA/dt = 2s(ds/dt) = 2(10)(2) = 40 cm²/s",
            "topic": "Related Rates",
            "difficulty": "hard"
        },
        {
            "id": "ap5",
            "question": "For f(x) = x³ - 3x + 1, where is f'(x) = 0?",
            "options": ["x = ±1", "x = 0", "x = 1", "x = 3"],
            "correct": 0,
            "explanation": "f'(x) = 3x² - 3 = 0, so 3x² = 3, x² = 1, x = ±1",
            "topic": "Critical Points",
            "difficulty": "medium"
        }
    ],
    "implicit_differentiation": [
        {
            "id": "im1",
            "question": "For x² + y² = 16, find dy/dx",
            "options": ["-x/y", "x/y", "-y/x", "2x/2y"],
            "correct": 0,
            "explanation": "Differentiate: 2x + 2y(dy/dx) = 0, so dy/dx = -x/y",
            "topic": "Implicit Diff",
            "difficulty": "easy"
        },
        {
            "id": "im2",
            "question": "For x³ + xy + y³ = 0, find dy/dx",
            "options": ["-(3x² + y)/(x + 3y²)", "(3x² + y)/(x + 3y²)", "-3x²/3y²", "-y/x"],
            "correct": 0,
            "explanation": "Differentiate: 3x² + y + x(dy/dx) + 3y²(dy/dx) = 0. Solve for dy/dx",
            "topic": "Implicit Diff",
            "difficulty": "hard"
        },
        {
            "id": "im3",
            "question": "For xy = 1, what is dy/dx?",
            "options": ["-y/x", "y/x", "-1/x²", "1/x²"],
            "correct": 0,
            "explanation": "Differentiate: y + x(dy/dx) = 0, so dy/dx = -y/x",
            "topic": "Implicit Diff",
            "difficulty": "easy"
        },
        {
            "id": "im4",
            "question": "For sin(xy) = x, find dy/dx",
            "options": ["[1 - y·cos(xy)]/[x·cos(xy)]", "1/cos(xy)", "-sin(xy)", "cos(xy)"],
            "correct": 0,
            "explanation": "Differentiate: cos(xy)·[y + x(dy/dx)] = 1. Solve for dy/dx",
            "topic": "Implicit Diff",
            "difficulty": "hard"
        },
        {
            "id": "im5",
            "question": "For x² - y² = 9, find dy/dx",
            "options": ["x/y", "-x/y", "y/x", "2x/2y"],
            "correct": 0,
            "explanation": "Differentiate: 2x - 2y(dy/dx) = 0, so dy/dx = x/y",
            "topic": "Implicit Diff",
            "difficulty": "easy"
        }
    ],
    "trigonometric": [
        {
            "id": "tr1",
            "question": "Find d/dx[sin(x)]",
            "options": ["cos(x)", "-cos(x)", "sin(x)", "-sin(x)"],
            "correct": 0,
            "explanation": "The derivative of sin(x) is cos(x)",
            "topic": "Trig Derivatives",
            "difficulty": "easy"
        },
        {
            "id": "tr2",
            "question": "What is d/dx[tan(x)]?",
            "options": ["sec²(x)", "sec(x)tan(x)", "1/cos²(x)", "Both A and C"],
            "correct": 3,
            "explanation": "d/dx[tan(x)] = sec²(x) = 1/cos²(x)",
            "topic": "Trig Derivatives",
            "difficulty": "easy"
        },
        {
            "id": "tr3",
            "question": "Differentiate: f(x) = x·sin(x)",
            "options": ["sin(x) + x·cos(x)", "x·cos(x)", "cos(x)", "sin(x)"],
            "correct": 0,
            "explanation": "Product rule: 1·sin(x) + x·cos(x)",
            "topic": "Trig Derivatives",
            "difficulty": "medium"
        },
        {
            "id": "tr4",
            "question": "Find d/dx[cos(3x)]",
            "options": ["-3sin(3x)", "sin(3x)", "-sin(3x)", "3cos(3x)"],
            "correct": 0,
            "explanation": "Chain rule: -sin(3x)·3 = -3sin(3x)",
            "topic": "Trig Derivatives",
            "difficulty": "medium"
        },
        {
            "id": "tr5",
            "question": "What is d/dx[sin²(x)]?",
            "options": ["2sin(x)cos(x)", "2sin(x)", "sin(2x)", "Both A and C"],
            "correct": 3,
            "explanation": "Chain rule: 2sin(x)·cos(x) = sin(2x)",
            "topic": "Trig Derivatives",
            "difficulty": "medium"
        }
    ],
    "exponential_log": [
        {
            "id": "el1",
            "question": "Find d/dx[eˣ]",
            "options": ["eˣ", "xeˣ⁻¹", "e", "ln(x)"],
            "correct": 0,
            "explanation": "The derivative of eˣ is eˣ",
            "topic": "Exponential",
            "difficulty": "easy"
        },
        {
            "id": "el2",
            "question": "What is d/dx[ln(x)]?",
            "options": ["1/x", "ln(x)", "x", "1"],
            "correct": 0,
            "explanation": "The derivative of ln(x) is 1/x",
            "topic": "Logarithmic",
            "difficulty": "easy"
        },
        {
            "id": "el3",
            "question": "Differentiate: f(x) = e^(2x)",
            "options": ["2e^(2x)", "e^(2x)", "2xe^(2x)", "e^(2x)/2"],
            "correct": 0,
            "explanation": "Chain rule: e^(2x)·2 = 2e^(2x)",
            "topic": "Exponential",
            "difficulty": "medium"
        },
        {
            "id": "el4",
            "question": "Find d/dx[ln(x²)]",
            "options": ["2/x", "1/x²", "2x", "ln(2x)"],
            "correct": 0,
            "explanation": "Chain rule: (1/x²)·2x = 2/x, or use log property: ln(x²) = 2ln(x), d/dx = 2/x",
            "topic": "Logarithmic",
            "difficulty": "medium"
        },
        {
            "id": "el5",
            "question": "Differentiate: f(x) = x·eˣ",
            "options": ["eˣ(1 + x)", "xeˣ", "eˣ", "(1+x)eˣ⁻¹"],
            "correct": 0,
            "explanation": "Product rule: 1·eˣ + x·eˣ = eˣ(1 + x)",
            "topic": "Exponential",
            "difficulty": "medium"
        },
        {
            "id": "el6",
            "question": "What is d/dx[ln(sin(x))]?",
            "options": ["cot(x)", "1/sin(x)", "cos(x)/sin(x)", "Both A and C"],
            "correct": 3,
            "explanation": "Chain rule: (1/sin(x))·cos(x) = cos(x)/sin(x) = cot(x)",
            "topic": "Logarithmic",
            "difficulty": "hard"
        }
    ]
}


def get_problem_by_id(problem_id: str):
    """Get a specific problem by ID"""
    for category, problems in PRACTICE_PROBLEMS.items():
        for problem in problems:
            if problem['id'] == problem_id:
                return problem
    return None


def get_problems_for_user(username: str, count: int = 5) -> list:
    """Get recommended problems based on user's weak topics"""
    progress = DataManager.get_user_progress(username)
    weak_topics = progress.get('initial_quiz', {}).get('weak_topics', [])
    
    # Flatten all problems
    all_problems = []
    for category, problems in PRACTICE_PROBLEMS.items():
        all_problems.extend(problems)
    
    # Prioritize problems matching weak topics
    recommended = []
    for problem in all_problems:
        if any(topic.lower() in problem['topic'].lower() for topic in weak_topics):
            recommended.append(problem)
    
    # Fill remaining with random problems
    while len(recommended) < count and all_problems:
        prob = random.choice(all_problems)
        if prob not in recommended:
            recommended.append(prob)
    
    return recommended[:count]


def track_attempt(username: str, problem_id: str, correct: bool):
    """Track practice problem attempts"""
    progress = DataManager.get_user_progress(username)
    practice_data = progress.get('practice_problems', {})
    
    if problem_id not in practice_data:
        practice_data[problem_id] = {
            "attempts": 0,
            "correct": 0,
            "incorrect": 0,
            "needs_review": False
        }
    
    practice_data[problem_id]["attempts"] += 1
    
    if correct:
        practice_data[problem_id]["correct"] += 1
        practice_data[problem_id]["needs_review"] = False
    else:
        practice_data[problem_id]["incorrect"] += 1
        # Mark for review after 3 incorrect attempts
        if practice_data[problem_id]["incorrect"] >= 3:
            practice_data[problem_id]["needs_review"] = True
    
    DataManager.update_progress(username, 'practice_problems', practice_data)
    
    return practice_data[problem_id]


def render_problem(problem, index, total):
    """Render a practice problem"""
    st.markdown(f"### Question {index + 1} of {total}")
    
    # Show difficulty badge
    difficulty_colors = {
        "easy": "🟢",
        "medium": "🟡",
        "hard": "🔴"
    }
    st.caption(f"{difficulty_colors.get(problem['difficulty'], '⚪')} {problem['difficulty'].title()} • Topic: {problem['topic']}")
    
    st.markdown(f"**{problem['question']}**")
    
    # Answer options
    answer_key = f"answer_{problem['id']}"
    selected = st.radio(
        "Select your answer:",
        problem['options'],
        key=answer_key,
        index=None
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        submit = st.button("Submit Answer", key=f"submit_{problem['id']}", type="primary")
    
    with col2:
        if st.button("💡 Show Hint", key=f"hint_{problem['id']}"):
            st.info(f"💡 Hint: This problem involves the **{problem['topic']}**")
    
    if submit:
        if selected is None:
            st.warning("Please select an answer!")
        else:
            correct = problem['options'].index(selected) == problem['correct']
            
            # Track attempt
            stats = track_attempt(st.session_state.username, problem['id'], correct)
            
            if correct:
                st.success("✅ Correct! Great job!")
                st.balloons()
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{problem['options'][problem['correct']]}**")
                
                if stats['needs_review']:
                    st.warning(f"⚠️ You've attempted this {stats['incorrect']} times. We recommend reviewing the **{problem['topic']}** lesson!")
            
            # Show explanation
            with st.expander("📖 Explanation"):
                st.markdown(problem['explanation'])
            
            # Award badge for first correct answer
            progress = DataManager.get_user_progress(st.session_state.username)
            correct_count = sum(1 for p in progress.get('practice_problems', {}).values() if p.get('correct', 0) > 0)
            if correct_count == 1:
                DataManager.award_badge(
                    st.session_state.username,
                    "Practice Makes Perfect! ✏️",
                    "Correctly answered your first practice problem"
                )


def main():
    # Home button at top
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("✏️ Practice Problems")
    with col2:
        if st.button("🏠 Home", key="practice_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    st.markdown("Reinforce your learning with targeted practice")
    
    username = st.session_state.username
    progress = DataManager.get_user_progress(username)
    practice_data = progress.get('practice_problems', {})
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_attempted = len(practice_data)
    total_correct = sum(1 for p in practice_data.values() if p.get('correct', 0) > 0)
    needs_review = sum(1 for p in practice_data.values() if p.get('needs_review', False))
    accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
    
    with col1:
        st.metric("Problems Attempted", total_attempted)
    with col2:
        st.metric("Correct", total_correct)
    with col3:
        st.metric("Accuracy", f"{accuracy:.0f}%")
    with col4:
        st.metric("Needs Review", needs_review, delta="⚠️" if needs_review > 0 else "✅")
    
    st.markdown("---")
    
    # Show problems that need review
    if needs_review > 0:
        st.warning(f"⚠️ You have {needs_review} problem(s) that need review")
        
        if st.button("📚 Review Recommended Lessons"):
            st.session_state.current_page = "lessons"
            st.rerun()
    
    # Filter options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        practice_mode = st.selectbox(
            "Practice Mode",
            ["Recommended for You", "By Topic", "Random Mix", "Review Mistakes"]
        )
    
    with col2:
        num_problems = st.selectbox("Number of Problems", [5, 10, 15, 20], index=0)
    
    st.markdown("---")
    
    # ML-powered spaced repetition info
    review_schedule = get_review_schedule(username)
    if review_schedule:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 4px solid #6B8E23; margin-bottom: 20px;">
            <div style="font-size: 14px; font-weight: 600; color: #FFFFFF; margin-bottom: 8px;">
                🔄 Spaced Repetition Active
            </div>
            <div style="font-size: 12px; color: #E0E0E0;">
                <strong>🤖 ML Analysis:</strong> {len(review_schedule)} topics need review based on SM-2 algorithm.
                We're intelligently spacing your practice to maximize long-term retention.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Get problems based on mode
    if practice_mode == "Recommended for You":
        problems = get_problems_for_user(username, num_problems)
        
        # Show ML explanation
        progress = DataManager.get_user_progress(username)
        weak_topics = progress.get('initial_quiz', {}).get('weak_topics', [])
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 4px solid #6B8E23; margin-bottom: 15px;">
            <div style="font-size: 13px; color: #E0E0E0;">
                <strong style="color: #FFFFFF;">🤖 Why these problems?</strong><br>
                {f"• Targeting your weak topics: {', '.join(weak_topics[:3])}<br>" if weak_topics else ""}
                • Adaptive difficulty based on your performance<br>
                • Optimized for your learning velocity<br>
                • Includes review problems from spaced repetition schedule
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif practice_mode == "By Topic":
        topic = st.selectbox("Select Topic", list(PRACTICE_PROBLEMS.keys()))
        problems = PRACTICE_PROBLEMS[topic][:num_problems]
        
        # Show ML analysis for this topic
        topic_map = {
            "basic_derivatives": "Basic Rules",
            "product_quotient": "Product Rule",
            "chain_rule": "Chain Rule",
            "applications": "Applications",
            "implicit_differentiation": "Implicit Diff.",
            "trigonometric": "Basic Rules",
            "exponential_log": "Basic Rules"
        }
        mapped_topic = topic_map.get(topic, "Basic Rules")
        confidence = calculate_topic_confidence(username, mapped_topic)
        difficulty = get_adaptive_difficulty(username, mapped_topic)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 4px solid #6B8E23; margin-bottom: 15px;">
            <div style="font-size: 13px; color: #E0E0E0;">
                <strong style="color: #FFFFFF;">🤖 Topic Analysis:</strong><br>
                • Current confidence: {confidence}%<br>
                • Recommended difficulty: {difficulty.upper()}<br>
                • These problems will help build mastery in this area
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif practice_mode == "Review Mistakes":
        # Get problems that need review
        problem_ids = [pid for pid, data in practice_data.items() if data.get('needs_review')]
        problems = [get_problem_by_id(pid) for pid in problem_ids if get_problem_by_id(pid)]
        if not problems:
            st.success("✅ No problems need review! You're doing great!")
            problems = get_problems_for_user(username, num_problems)
    else:  # Random Mix
        all_problems = []
        for problems_list in PRACTICE_PROBLEMS.values():
            all_problems.extend(problems_list)
        random.shuffle(all_problems)
        problems = all_problems[:num_problems]
    
    # Display problems
    if problems:
        for idx, problem in enumerate(problems):
            with st.container(border=True):
                render_problem(problem, idx, len(problems))
            st.markdown("---")
    else:
        st.info("No problems available. Try a different mode!")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Load More Problems", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 View My Stats", use_container_width=True):
            st.session_state.current_page = "progress"
            st.rerun()
    
    with col3:
        if st.button("📚 Back to Lessons", use_container_width=True):
            st.session_state.current_page = "lessons"
            st.rerun()


if __name__ == "__main__":
    main()
