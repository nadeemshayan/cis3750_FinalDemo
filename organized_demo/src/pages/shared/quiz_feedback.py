import streamlit as st

# -------------------------
# CALCULUS QUIZ FEEDBACK - Modern Design
# -------------------------

st.set_page_config(page_title="Quiz Feedback - Derivatives", layout="wide", page_icon="📊", initial_sidebar_state="collapsed")

# -------------------------
# Static Data
# -------------------------
student_name = "John"
quiz_title = "An Introduction to Derivatives"
score = 75
questions_total = 8
correct = 6
wrong = 2

mastery = {
    "Limit Definition": 100,
    "Basic Rules": 100,
    "Product Rule": 100,
    "Chain Rule": 50,
    "Implicit Diff.": 0,
    "Applications": 0
}

# Concept cards - areas where student needs improvement
areas_to_improve = [
    {
        "topic": "Chain Rule",
        "score": 50,
        "issue": "Missed applying inner derivative.",
        "tip": "Remember: d/dx [f(g(x))] = f'(g(x)) * g'(x).",
        "color": "#FFE5D0"
    },
    {
        "topic": "Implicit Differentiation",
        "score": 0,
        "issue": "Forgot dy/dx term.",
        "tip": "Add dy/dx whenever differentiating y-terms.",
        "color": "#FFD4D4"
    },
    {
        "topic": "Applications",
        "score": 0,
        "issue": "Used wrong point for tangent.",
        "tip": "Plug x₀ and f(x₀) into line equation y = m(x-x₀)+y₀.",
        "color": "#D4FFE5"
    }
]

# Mastered concepts
mastered_concepts = [
    {
        "topic": "Limit Definition",
        "score": 100,
        "color": "#D4F4DD"
    },
    {
        "topic": "Basic Rules",
        "score": 100,
        "color": "#E5D4FF"
    },
    {
        "topic": "Product Rule",
        "score": 100,
        "color": "#D4E8FF"
    }
]

wrong_answers = [
    {
        "question": "Implicit Differentiation: For x² + y² = 25, what is dy/dx?",
        "your_answer": "−y/x",
        "correct_answer": "−x/y",
        "explanation": "Differentiate both sides: 2x + 2y(dy/dx) = 0 → dy/dx = -2x/(2y) = -x/y. You inverted the fraction."
    },
    {
        "question": "Applications: At x=2, the slope of the tangent to f(x)=x² is:",
        "your_answer": "2",
        "correct_answer": "4",
        "explanation": "f'(x) = 2x, so at x=2, the slope is f'(2) = 2(2) = 4. You forgot to substitute x=2 into the derivative."
    }
]

# -------------------------
# STYLE SECTION
# -------------------------

st.markdown("""
<style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background-color: #F5FBF8;
    }
    
    /* Hide default sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Header styling */
    .main-header {
        font-size: 48px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 20px;
        color: #666;
        margin-bottom: 30px;
    }
    
    /* Score card styling */
    .score-card {
        background-color: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 250px;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .score-number {
        font-size: 56px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 10px 0;
    }
    
    .score-label {
        font-size: 16px;
        color: #666;
        font-weight: 500;
    }
    
    /* Concept card styling */
    .concept-card {
        border-radius: 20px;
        padding: 25px;
        min-height: 180px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    
    .concept-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .concept-topic {
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 12px;
    }
    
    .concept-score {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .concept-issue {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }
    
    .concept-tip {
        font-size: 13px;
        color: #2D7A4F;
        background-color: rgba(45, 122, 79, 0.1);
        padding: 8px 12px;
        border-radius: 10px;
        margin-top: 10px;
    }
    
    /* Question card styling */
    .question-card {
        background-color: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    .question-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 15px;
    }
    
    .answer-row {
        margin: 10px 0;
        font-size: 15px;
    }
    
    .wrong-answer {
        color: #DC3545;
        font-weight: 500;
    }
    
    .correct-answer {
        color: #28A745;
        font-weight: 500;
    }
    
    .explanation {
        background-color: #F8F9FA;
        padding: 12px 15px;
        border-radius: 12px;
        margin-top: 10px;
        font-size: 14px;
        color: #555;
        font-style: italic;
    }
    
    /* Profile sidebar */
    .profile-card {
        background-color: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 20px;
    }
    
    .profile-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0 auto 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 32px;
        font-weight: 700;
    }
    
    .profile-name {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    
    .section-header {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 20px;
        margin-top: 30px;
        color: #1a1a1a;
    }
    
    .result-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 15px;
        background-color: #D4F4DD;
        color: #2D7A4F;
        font-size: 14px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    .warning-badge {
        background-color: #FFE5D0;
        color: #FF6B35;
    }
    
    /* Progress section */
    .progress-item {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .progress-label {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }
    
    .progress-bar-container {
        background-color: #F0F0F0;
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Force equal height columns */
    [data-testid="column"] {
        height: 100%;
    }
    
    [data-testid="stVerticalBlock"] {
        height: 100%;
    }
    
</style>
""", unsafe_allow_html=True)

# -------------------------
# MAIN LAYOUT
# -------------------------

# Create main columns - left content area and right sidebar
left_col, right_col = st.columns([3, 1])

with left_col:
    # Main Navigation Icons (left sidebar simulation)
    st.markdown("""
    <div style="position: fixed; left: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 20px; z-index: 1000;">
        <div style="width: 50px; height: 50px; background-color: #1a1a1a; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">🏠</div>
        <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">�</div>
        <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">📝</div>
        <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">�</div>
        <div style="width: 50px; height: 50px; background-color: white; border: 2px solid #e0e0e0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer;">⚙️</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(f'<h1 class="main-header">Great job, {student_name}!</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Here\'s your feedback for <b>{quiz_title}</b></p>', unsafe_allow_html=True)
    
    # Score overview cards
    score_cols = st.columns(3)
    with score_cols[0]:
        st.markdown(f"""
        <div class="score-card" style="background: linear-gradient(135deg, #D4F4DD 0%, #B8F4D3 100%);">
            <div class="score-label">Your Score</div>
            <div class="score-number">{score}%</div>
            <div class="score-label">{correct}/{questions_total} Correct</div>
            <div class="result-badge">Good Job!</div>
        </div>
        """, unsafe_allow_html=True)
    
    with score_cols[1]:
        mastered_count = sum(1 for v in mastery.values() if v >= 70)
        st.markdown(f"""
        <div class="score-card" style="background-color: white;">
            <div class="score-label">Mastered Topics</div>
            <div class="score-number">{mastered_count}</div>
            <div class="score-label">out of {len(mastery)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with score_cols[2]:
        needs_work = sum(1 for v in mastery.values() if v < 70)
        st.markdown(f"""
        <div class="score-card" style="background-color: white;">
            <div class="score-label">Needs Practice</div>
            <div class="score-number">{needs_work}</div>
            <div class="score-label">topics below 70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Areas to Improve Section
    st.markdown('<p class="section-header">📉 Areas to Improve</p>', unsafe_allow_html=True)
    
    improve_cols = st.columns(3)
    for idx, area in enumerate(areas_to_improve):
        with improve_cols[idx % 3]:
            st.markdown(f"""
            <div class="concept-card" style="background-color: {area['color']};">
                <div class="concept-score">{area['score']}%</div>
                <div class="concept-topic">{area['topic']}</div>
                <div class="concept-issue">❌ {area['issue']}</div>
                <div class="concept-tip">💡 {area['tip']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Mastered Concepts Section  
    st.markdown('<p class="section-header">✅ Mastered Concepts</p>', unsafe_allow_html=True)
    
    master_cols = st.columns(3)
    for idx, concept in enumerate(mastered_concepts):
        with master_cols[idx % 3]:
            st.markdown(f"""
            <div class="concept-card" style="background-color: {concept['color']}; height: 120px;">
                <div class="concept-score">{concept['score']}%</div>
                <div class="concept-topic">{concept['topic']}</div>
                <div class="result-badge" style="position: absolute; bottom: 20px; left: 25px;">Excellent!</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Wrong/Partial Questions Section
    st.markdown('<p class="section-header">❗ Questions to Review</p>', unsafe_allow_html=True)
    
    for idx, q in enumerate(wrong_answers, 1):
        st.markdown(f"""
        <div class="question-card">
            <div class="question-title">Question {idx}: {q['question']}</div>
            <div class="answer-row">
                <span class="wrong-answer">Your answer:</span> {q['your_answer']}
            </div>
            <div class="answer-row">
                <span class="correct-answer">Correct answer:</span> {q['correct_answer']}
            </div>
            <div class="explanation">
                💭 {q['explanation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Next Steps
    st.markdown('<p class="section-header">🎯 Next Steps</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="question-card">
        <div style="font-size: 15px; line-height: 1.8;">
            ✓ Practice 3 new <b>Chain Rule</b> problems — label outer vs inner explicitly.<br>
            ✓ Re-do <b>implicit differentiation</b> with both sides differentiated.<br>
            ✓ Revisit <b>tangent-line formula</b> practice at x=1,2,3 for various curves.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    # Add spacing to align with left column content
    st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)
    
    # Performance breakdown
    st.markdown('<p class="section-header" style="font-size: 16px;">Topic Breakdown</p>', unsafe_allow_html=True)
    
    for topic, score_val in mastery.items():
        color = "#28A745" if score_val >= 70 else "#FF6B35"
        st.markdown(f"""
        <div class="progress-item">
            <div class="progress-label">{topic}</div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {score_val}%; background-color: {color};"></div>
            </div>
            <div style="text-align: right; margin-top: 5px; font-size: 14px; font-weight: 600; color: {color};">{score_val}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quiz Stats
    st.markdown('<p class="section-header" style="font-size: 16px; margin-top: 25px;">Quiz Stats</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="profile-card">
        <div style="text-align: left;">
            <div style="margin-bottom: 15px;">
                <div style="font-size: 14px; color: #666;">Total Questions</div>
                <div style="font-size: 24px; font-weight: 700; color: #1a1a1a;">{questions_total}</div>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="font-size: 14px; color: #666;">Correct Answers</div>
                <div style="font-size: 24px; font-weight: 700; color: #28A745;">{correct}</div>
            </div>
            <div>
                <div style="font-size: 14px; color: #666;">Incorrect Answers</div>
                <div style="font-size: 24px; font-weight: 700; color: #DC3545;">{wrong}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
