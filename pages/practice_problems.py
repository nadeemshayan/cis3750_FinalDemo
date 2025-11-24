"""
Practice Problems with Intelligent Review Logic
Tracks attempts and recommends review after 3 incorrect attempts
"""

import streamlit as st
from data_manager import DataManager
import random


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
    
    # Get problems based on mode
    if practice_mode == "Recommended for You":
        problems = get_problems_for_user(username, num_problems)
        st.info("🎯 These problems are selected based on your quiz results and learning progress")
    elif practice_mode == "By Topic":
        topic = st.selectbox("Select Topic", list(PRACTICE_PROBLEMS.keys()))
        problems = PRACTICE_PROBLEMS[topic][:num_problems]
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
