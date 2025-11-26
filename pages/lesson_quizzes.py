import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import random

sys.path.insert(0, str(Path(__file__).parent.parent))
from data_manager import DataManager

def apply_quiz_styles():
    """Apply custom styles for lesson quizzes"""
    st.markdown(
    """
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #F5FBF8;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

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

    .quiz-card {
        background-color: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .quiz-header-card {
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        color: #1a1a1a;
    }

    .lesson-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 14px;
        font-size: 14px;
        font-weight: 600;
        background-color: white;
        margin-bottom: 10px;
    }

    .quiz-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .quiz-goal {
        font-size: 16px;
        color: #444;
        font-style: italic;
        margin-bottom: 5px;
    }

    .quiz-meta {
        font-size: 14px;
        color: #666;
    }

    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        font-size: 14px;
        color: #666;
    }

    .difficulty-badge {
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .difficulty-easy {
        background-color: #E8F5E9;
        color: #2E7D32;
    }

    .difficulty-medium {
        background-color: #FFF3E0;
        color: #EF6C00;
    }

    .difficulty-hard {
        background-color: #FFEBEE;
        color: #C62828;
    }

    .question-stem {
        font-size: 17px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 10px;
    }

    .result-box {
        background: linear-gradient(135deg, #D4F4DD 0%, #B8F4D3 100%);
        border-radius: 18px;
        padding: 25px;
        margin-top: 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    .result-score {
        font-size: 40px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 5px;
    }

    .result-text {
        font-size: 15px;
        color: #444;
    }

    .per-question-result {
        font-size: 14px;
        margin-top: 4px;
    }

    .per-question-correct {
        color: #2E7D32;
    }

    .per-question-wrong {
        color: #C62828;
    }

    .stButton > button {
        border-radius: 15px;
        padding: 10px 22px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# left vertical icons to match other pages
st.markdown(
    """
<div style="position: fixed; left: 20px; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 20px; z-index: 1000;">
    <div style="width: 50px; height: 50px; background-color: white;
                border: 2px solid #e0e0e0; border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 24px; cursor: pointer;">🏠</div>
    <div style="width: 50px; height: 50px; background-color: white;
                border: 2px solid #e0e0e0; border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 24px; cursor: pointer;">📚</div>
    <div style="width: 50px; height: 50px; background-color: #1a1a1a;
                border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 24px; cursor: pointer;">🎯</div>
    <div style="width: 50px; height: 50px; background-color: white;
                border: 2px solid #e0e0e0; border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 24px; cursor: pointer;">📊</div>
</div>
""",
    unsafe_allow_html=True,
)

# ------------- lesson meta and banks -------------

LESSON_META = {
    "lesson1": {
        "label": "Lesson 1 · Limit Definition",
        "title": "Limit Definition of the Derivative",
        "goal": "Check that you can use the limit definition in simple cases.",
        "gradient": "linear-gradient(135deg, #FFD4D4 0%, #FFE5E5 100%)",
        "badge_color": "#DC143C",
    },
    "lesson2": {
        "label": "Lesson 2 · Basic Rules",
        "title": "Basic Differentiation Rules",
        "goal": "Power rule and simple combinations.",
        "gradient": "linear-gradient(135deg, #FFE5D0 0%, #FFF0E0 100%)",
        "badge_color": "#FF8C00",
    },
    "lesson3": {
        "label": "Lesson 3 · Product Rule",
        "title": "Product Rule",
        "goal": "Differentiate products of functions.",
        "gradient": "linear-gradient(135deg, #E5D4FF 0%, #F0E8FF 100%)",
        "badge_color": "#6B46C1",
    },
    "lesson4": {
        "label": "Lesson 4 · Chain Rule",
        "title": "Chain Rule",
        "goal": "Work with composite functions.",
        "gradient": "linear-gradient(135deg, #D4FFE5 0%, #E5FFF0 100%)",
        "badge_color": "#10B981",
    },
    "lesson5": {
        "label": "Lesson 5 · Implicit Differentiation",
        "title": "Implicit Differentiation",
        "goal": "Differentiate relations that mix x and y.",
        "gradient": "linear-gradient(135deg, #D4E8FF 0%, #E5F2FF 100%)",
        "badge_color": "#2196F3",
    },
    "lesson6": {
        "label": "Lesson 6 · Applications",
        "title": "Applications of Derivatives",
        "goal": "Use derivatives in concrete problems.",
        "gradient": "linear-gradient(135deg, #FFF4D4 0%, #FFFAE5 100%)",
        "badge_color": "#F59E0B",
    },
}

# Each question has id, difficulty, stem, choices, answer index
# There are three levels per lesson so you can expand this to sixty later

QUESTION_BANKS = {
    "lesson1": [
        # easy
        {
            "id": "L1_E1",
            "difficulty": "easy",
            "stem": "For f(x) = x², which expression is the difference quotient at x = a?",
            "choices": [
                "(f(a+h) − f(a))/h",
                "(f(a) − f(h))/a",
                "(f(a+h) − f(h))/a",
                "(f(a) − f(a−h))/h",
            ],
            "answer": 0,
        },
        {
            "id": "L1_E2",
            "difficulty": "easy",
            "stem": "The derivative at x = a is the limit of the secant slope as",
            "choices": [
                "h → 0",
                "h → 1",
                "x → ∞",
                "a → 0",
            ],
            "answer": 0,
        },
        {
            "id": "L1_E3",
            "difficulty": "easy",
            "stem": "The derivative of f at a point is best described as",
            "choices": [
                "the slope of the tangent line",
                "the area under the curve",
                "the x coordinate of the point",
                "the y intercept of the graph",
            ],
            "answer": 0,
        },
        # medium
        {
            "id": "L1_M1",
            "difficulty": "medium",
            "stem": "Use the limit definition to find f'(a) for f(x) = x².",
            "choices": ["2a", "a²", "a", "4a"],
            "answer": 0,
        },
        {
            "id": "L1_M2",
            "difficulty": "medium",
            "stem": "Use the limit definition to find f'(a) for f(x) = 3x.",
            "choices": ["3", "3a", "a", "0"],
            "answer": 0,
        },
        {
            "id": "L1_M3",
            "difficulty": "medium",
            "stem": "If f'(2) = 5, what does that tell you about the graph of f at x = 2?",
            "choices": [
                "The tangent line at x = 2 has slope 5.",
                "The tangent line at x = 5 has slope 2.",
                "The point (2,5) is on the graph.",
                "The graph crosses the x axis at x = 5.",
            ],
            "answer": 0,
        },
        # hard
        {
            "id": "L1_H1",
            "difficulty": "hard",
            "stem": "For f(x) = √x, use the limit definition to find f'(a).",
            "choices": [
                "1/(2√a)",
                "√a",
                "1/√a",
                "2√a",
            ],
            "answer": 0,
        },
        {
            "id": "L1_H2",
            "difficulty": "hard",
            "stem": "For f(x) = |x|, what can you say about f'(0)?",
            "choices": [
                "The derivative does not exist at 0.",
                "f'(0) = 0.",
                "f'(0) = 1.",
                "f'(0) = −1.",
            ],
            "answer": 0,
        },
        {
            "id": "L1_H3",
            "difficulty": "hard",
            "stem": "Which statement is true?",
            "choices": [
                "If f is differentiable at a then f is continuous at a.",
                "If f is continuous at a then f is differentiable at a.",
                "Every function is differentiable everywhere.",
                "Differentiability and continuity are unrelated.",
            ],
            "answer": 0,
        },
    ],
    "lesson2": [
        # easy
        {
            "id": "L2_E1",
            "difficulty": "easy",
            "stem": "Differentiate f(x) = x³.",
            "choices": ["3x²", "x²", "3x³", "x"],
            "answer": 0,
        },
        {
            "id": "L2_E2",
            "difficulty": "easy",
            "stem": "Differentiate f(x) = 7.",
            "choices": ["0", "7", "1", "x"],
            "answer": 0,
        },
        {
            "id": "L2_E3",
            "difficulty": "easy",
            "stem": "Differentiate f(x) = 4x.",
            "choices": ["4", "x", "4x²", "0"],
            "answer": 0,
        },
        # medium
        {
            "id": "L2_M1",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = 5x³ − 4x + 7.",
            "choices": ["15x² − 4", "5x² − 4", "15x³ − 4", "15x² − 4x"],
            "answer": 0,
        },
        {
            "id": "L2_M2",
            "difficulty": "medium",
            "stem": "Write f'(x) if f(x) = 2x^(1/2) + x^(−2).",
            "choices": [
                "x^(−1/2) − 2x^(−3)",
                "2x^(−1/2) − 2x^(−2)",
                "x^(1/2) − 2x^(−3)",
                "x^(−1/2) − x^(−3)",
            ],
            "answer": 0,
        },
        {
            "id": "L2_M3",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = 3x⁴ − x².",
            "choices": ["12x³ − 2x", "12x² − 2x", "3x³ − 2x", "12x³ − x"],
            "answer": 0,
        },
        # hard
        {
            "id": "L2_H1",
            "difficulty": "hard",
            "stem": "Find f'(x) for f(x) = x^(3/2).",
            "choices": [
                "(3/2)x^(1/2)",
                "(1/2)x^(−1/2)",
                "(3/2)x^(−1/2)",
                "3x^(1/2)",
            ],
            "answer": 0,
        },
        {
            "id": "L2_H2",
            "difficulty": "hard",
            "stem": "Differentiate f(x) = (2/x³) − √x.",
            "choices": [
                "-6/x⁴ − 1/(2√x)",
                "-6/x² − 1/(2√x)",
                "6/x⁴ − 1/(2√x)",
                "6/x³ − 1/(2√x)",
            ],
            "answer": 0,
        },
        {
            "id": "L2_H3",
            "difficulty": "hard",
            "stem": "If f(x) = x⁴ − 3x², what is f'(2)?",
            "choices": ["20", "10", "32", "8"],
            "answer": 0,
        },
    ],
    "lesson3": [
        # easy
        {
            "id": "L3_E1",
            "difficulty": "easy",
            "stem": "State the product rule for f(x) = u(x)v(x).",
            "choices": [
                "f' = u'v + uv'",
                "f' = u'v'",
                "f' = uv",
                "f' = u + v",
            ],
            "answer": 0,
        },
        {
            "id": "L3_E2",
            "difficulty": "easy",
            "stem": "In words, the product rule is",
            "choices": [
                "derivative of first times second plus first times derivative of second",
                "multiply the two derivatives",
                "add the original functions",
                "take the derivative of the ratio",
            ],
            "answer": 0,
        },
        {
            "id": "L3_E3",
            "difficulty": "easy",
            "stem": "Which is a product that needs the product rule?",
            "choices": [
                "x² sin x",
                "x² + sin x",
                "sin(x²)",
                "1/x",
            ],
            "answer": 0,
        },
        # medium
        {
            "id": "L3_M1",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = x² sin x.",
            "choices": [
                "2x sin x + x² cos x",
                "2x sin x",
                "x² cos x",
                "cos x",
            ],
            "answer": 0,
        },
        {
            "id": "L3_M2",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = x³ e^x.",
            "choices": [
                "3x² e^x + x³ e^x",
                "3x² e^x",
                "x³ e^x",
                "e^x",
            ],
            "answer": 0,
        },
        {
            "id": "L3_M3",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = (2x)(ln x).",
            "choices": [
                "2 ln x + 2",
                "2 ln x",
                "2/x + ln x",
                "2x/x",
            ],
            "answer": 0,
        },
        # hard
        {
            "id": "L3_H1",
            "difficulty": "hard",
            "stem": "Differentiate f(x) = x² e^x sin x (treat as product of three).",
            "choices": [
                "x² e^x cos x + 2x e^x sin x + x² e^x sin x",
                "2x e^x sin x",
                "x² e^x cos x",
                "2x e^x cos x",
            ],
            "answer": 0,
        },
        {
            "id": "L3_H2",
            "difficulty": "hard",
            "stem": "Differentiate f(x) = (x² + 1)(x³ − x).",
            "choices": [
                "2x(x³ − x) + (x² + 1)(3x² − 1)",
                "2x(x³ − x) + 3x² − 1",
                "(x² + 1)(3x² − 1)",
                "2x + 3x² − 1",
            ],
            "answer": 0,
        },
        {
            "id": "L3_H3",
            "difficulty": "hard",
            "stem": "Which mistake is most common when students misapply the product rule?",
            "choices": [
                "Using u'v' instead of u'v + uv'.",
                "Taking no derivative at all.",
                "Only differentiating v.",
                "Only differentiating u and v in the numerator.",
            ],
            "answer": 0,
        },
    ],
    "lesson4": [
        # easy
        {
            "id": "L4_E1",
            "difficulty": "easy",
            "stem": "State the chain rule for f(x) = f(g(x)).",
            "choices": [
                "f'(g(x)) g'(x)",
                "f'(x) g'(x)",
                "f(g'(x))",
                "g'(x)/f(x)",
            ],
            "answer": 0,
        },
        {
            "id": "L4_E2",
            "difficulty": "easy",
            "stem": "In words, the chain rule says",
            "choices": [
                "derivative of the outer times derivative of the inner",
                "add the derivatives of each part",
                "divide the derivatives",
                "multiply the original functions",
            ],
            "answer": 0,
        },
        {
            "id": "L4_E3",
            "difficulty": "easy",
            "stem": "Which function clearly needs the chain rule?",
            "choices": [
                "(3x² + 1)⁴",
                "x² + 1",
                "3x²",
                "x⁴",
            ],
            "answer": 0,
        },
        # medium
        {
            "id": "L4_M1",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = (3x² + 1)⁴.",
            "choices": [
                "24x(3x² + 1)³",
                "4(3x² + 1)³",
                "12x(3x² + 1)⁴",
                "(3x² + 1)³",
            ],
            "answer": 0,
        },
        {
            "id": "L4_M2",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = sin(5x²).",
            "choices": [
                "10x cos(5x²)",
                "cos(5x²)",
                "5 cos(5x²)",
                "10x sin(5x²)",
            ],
            "answer": 0,
        },
        {
            "id": "L4_M3",
            "difficulty": "medium",
            "stem": "Differentiate f(x) = e^(2x).",
            "choices": [
                "2e^(2x)",
                "e^(2x)",
                "2e^x",
                "e^x",
            ],
            "answer": 0,
        },
        # hard
        {
            "id": "L4_H1",
            "difficulty": "hard",
            "stem": "Differentiate f(x) = sin(cos(x²)).",
            "choices": [
                "cos(cos(x²)) (−sin(x²)) 2x",
                "cos(cos(x²)) 2x",
                "sin(cos(x²)) 2x",
                "cos(x²) (−sin(x²))",
            ],
            "answer": 0,
        },
        {
            "id": "L4_H2",
            "difficulty": "hard",
            "stem": "Differentiate f(x) = √(4x² + 1).",
            "choices": [
                "(4x)/(√(4x² + 1))",
                "2√(4x² + 1)",
                "1/(2√(4x² + 1))",
                "4/(√(4x² + 1))",
            ],
            "answer": 0,
        },
        {
            "id": "L4_H3",
            "difficulty": "hard",
            "stem": "Differentiate f(x) = (5x³ − x)¹⁰.",
            "choices": [
                "10(5x³ − x)⁹(15x² − 1)",
                "10(5x³ − x)⁹",
                "15x² − 1",
                "(5x³ − x)¹⁰(15x² − 1)",
            ],
            "answer": 0,
        },
    ],
    "lesson5": [
        # easy
        {
            "id": "L5_E1",
            "difficulty": "easy",
            "stem": "In implicit differentiation, whenever you differentiate y you must",
            "choices": [
                "multiply by dy/dx",
                "set it equal to zero",
                "leave it unchanged",
                "treat it as a constant",
            ],
            "answer": 0,
        },
        {
            "id": "L5_E2",
            "difficulty": "easy",
            "stem": "Implicit differentiation is used when",
            "choices": [
                "y is not isolated as a function of x",
                "x is constant",
                "y never appears",
                "the function is linear",
            ],
            "answer": 0,
        },
        {
            "id": "L5_E3",
            "difficulty": "easy",
            "stem": "Differentiate x² with respect to x.",
            "choices": ["2x", "x²", "2", "0"],
            "answer": 0,
        },
        # medium
        {
            "id": "L5_M1",
            "difficulty": "medium",
            "stem": "For x² + y² = 25, find dy/dx.",
            "choices": [
                "−x/y",
                "x/y",
                "−y/x",
                "y/x",
            ],
            "answer": 0,
        },
        {
            "id": "L5_M2",
            "difficulty": "medium",
            "stem": "For xy = 1, what is dy/dx?",
            "choices": [
                "−y/x",
                "−x/y",
                "1/(xy)",
                "x/y",
            ],
            "answer": 0,
        },
        {
            "id": "L5_M3",
            "difficulty": "medium",
            "stem": "For x² + xy + y² = 7, which line is correct after differentiating?",
            "choices": [
                "2x + y + x dy/dx + 2y dy/dx = 0",
                "2x + 2y dy/dx = 0",
                "2x + y dy/dx + 2y = 0",
                "x + y + 2y dy/dx = 0",
            ],
            "answer": 0,
        },
        # hard
        {
            "id": "L5_H1",
            "difficulty": "hard",
            "stem": "From 2x + y + x dy/dx + 2y dy/dx = 0, solve for dy/dx.",
            "choices": [
                "dy/dx = (−2x − y)/(x + 2y)",
                "dy/dx = (2x + y)/(x + 2y)",
                "dy/dx = (−2x − y)/(2x + y)",
                "dy/dx = (2x + y)/(2x + y)",
            ],
            "answer": 0,
        },
        {
            "id": "L5_H2",
            "difficulty": "hard",
            "stem": "For x² − y² = 1, what is dy/dx?",
            "choices": [
                "x/y",
                "−x/y",
                "−y/x",
                "y/x",
            ],
            "answer": 0,
        },
        {
            "id": "L5_H3",
            "difficulty": "hard",
            "stem": "For sin(x + y) = x, which equation is correct after differentiating?",
            "choices": [
                "cos(x + y)(1 + dy/dx) = 1",
                "cos(x + y) dy/dx = 1",
                "sin(x + y)(1 + dy/dx) = 1",
                "cos(x + y) = 1 + dy/dx",
            ],
            "answer": 0,
        },
    ],
    "lesson6": [
        # easy
        {
            "id": "L6_E1",
            "difficulty": "easy",
            "stem": "The slope of the tangent line to y = f(x) at x = a is",
            "choices": [
                "f'(a)",
                "f(a)",
                "a",
                "f(a)/a",
            ],
            "answer": 0,
        },
        {
            "id": "L6_E2",
            "difficulty": "easy",
            "stem": "If s(t) is position, then s'(t) represents",
            "choices": [
                "velocity",
                "acceleration",
                "distance",
                "time",
            ],
            "answer": 0,
        },
        {
            "id": "L6_E3",
            "difficulty": "easy",
            "stem": "If v(t) is velocity, then v'(t) is",
            "choices": [
                "acceleration",
                "position",
                "displacement",
                "time",
            ],
            "answer": 0,
        },
        # medium
        {
            "id": "L6_M1",
            "difficulty": "medium",
            "stem": "Find the equation of the tangent line to f(x) = x² at x = 2.",
            "choices": [
                "y = 4x − 4",
                "y = 2x + 4",
                "y = x²",
                "y = 4x + 4",
            ],
            "answer": 0,
        },
        {
            "id": "L6_M2",
            "difficulty": "medium",
            "stem": "For s(t) = t³ − 6t² + 9t, find v(t).",
            "choices": [
                "3t² − 12t + 9",
                "3t² − 6t + 9",
                "t² − 6t + 9",
                "3t³ − 12t² + 9",
            ],
            "answer": 0,
        },
        {
            "id": "L6_M3",
            "difficulty": "medium",
            "stem": "For h(t) = −16t² + 64t + 5, when does the maximum height occur?",
            "choices": [
                "t = 2",
                "t = 0",
                "t = 4",
                "t = 1",
            ],
            "answer": 0,
        },
        # hard
        {
            "id": "L6_H1",
            "difficulty": "hard",
            "stem": "For h(t) = −16t² + 64t + 5, what is the maximum height?",
            "choices": [
                "69",
                "64",
                "5",
                "80",
            ],
            "answer": 0,
        },
        {
            "id": "L6_H2",
            "difficulty": "hard",
            "stem": "If C(q) is cost and C'(q) is marginal cost, then C'(100) ≈ 25 means",
            "choices": [
                "producing one more unit at q = 100 costs about 25",
                "total cost at q = 100 is 25",
                "average cost at q = 100 is 25",
                "the company makes 25 units",
            ],
            "answer": 0,
        },
        {
            "id": "L6_H3",
            "difficulty": "hard",
            "stem": "You are told that f'(x) changes sign from positive to negative at x = 3. What does this say about f?",
            "choices": [
                "f has a local maximum at x = 3",
                "f has a local minimum at x = 3",
                "f is always decreasing",
                "f is always increasing",
            ],
            "answer": 0,
        },
    ],
}

def main():
    """Main function for lesson quizzes"""
    apply_quiz_styles()
    
    # ------------- header -------------
    
    st.markdown(
        '<h1 class="main-header">Lesson Quizzes</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">Each quiz uses an easy, medium, hard bank for its lesson. You can add more questions to the banks when you need the full sixty.</p>',
        unsafe_allow_html=True,
    )

lesson_labels = [meta["label"] for meta in LESSON_META.values()]
lesson_keys = list(LESSON_META.keys())

selected_label = st.selectbox(
    "Choose a lesson to quiz yourself on",
    options=lesson_labels,
)

selected_key = lesson_keys[lesson_labels.index(selected_label)]
meta = LESSON_META[selected_key]
questions = QUESTION_BANKS[selected_key]

# ------------- lesson header card -------------

st.markdown(
    f"""
<div class="quiz-header-card" style="background: {meta['gradient']};">
    <div class="lesson-badge" style="color: {meta['badge_color']};">
        {meta['label']}
    </div>
    <div class="quiz-title">{meta['title']}</div>
    <div class="quiz-goal">{meta['goal']}</div>
    <div class="quiz-meta">🤖 <strong>ML-Adaptive Quiz:</strong> This quiz intelligently selects 5 questions based on your performance. Master easy questions to unlock harder ones!</div>
</div>
""",
    unsafe_allow_html=True,
)

# adaptive question selection
def select_adaptive_questions(lesson_key, all_questions, username):
    # get past performance
    progress = DataManager.get_user_progress(username) if username else {}
    lesson_history = progress.get('lesson_quizzes', {}).get(lesson_key, {})
    
    easy_q = [q for q in all_questions if q['difficulty'] == 'easy']
    medium_q = [q for q in all_questions if q['difficulty'] == 'medium']
    hard_q = [q for q in all_questions if q['difficulty'] == 'hard']
    
    selected = []
    past_score = lesson_history.get('best_score_pct', 0)
    
    if past_score == 0:
        # first try - start easier
        selected.extend(random.sample(easy_q, min(2, len(easy_q))))
        selected.extend(random.sample(medium_q, min(2, len(medium_q))))
        selected.extend(random.sample(hard_q, min(1, len(hard_q))))
    elif past_score < 60:
        selected.extend(random.sample(easy_q, min(2, len(easy_q))))
        selected.extend(random.sample(medium_q, min(2, len(medium_q))))
        selected.extend(random.sample(hard_q, min(1, len(hard_q))))
    elif past_score < 80:
        selected.extend(random.sample(easy_q, min(1, len(easy_q))))
        selected.extend(random.sample(medium_q, min(2, len(medium_q))))
        selected.extend(random.sample(hard_q, min(2, len(hard_q))))
    else:
        selected.extend(random.sample(easy_q, min(1, len(easy_q))))
        selected.extend(random.sample(medium_q, min(1, len(medium_q))))
        selected.extend(random.sample(hard_q, min(3, len(hard_q))))
    
    while len(selected) < 5 and len(all_questions) > len(selected):
        remaining = [q for q in all_questions if q not in selected]
        if remaining:
            selected.append(random.choice(remaining))
    
    return selected[:5]

username = st.session_state.get('username', 'guest')

# select questions
questions = select_adaptive_questions(selected_key, questions, username)

st.info(f"🤖 **Adaptive Selection:** Based on your performance, we've selected {len(questions)} questions tailored to your skill level.")

answers = {}
correct_flags = {}

for idx, q in enumerate(questions, start=1):
    difficulty = q["difficulty"]
    diff_class = (
        "difficulty-easy"
        if difficulty == "easy"
        else "difficulty-medium"
        if difficulty == "medium"
        else "difficulty-hard"
    )

    st.markdown(
        f"""
<div class="quiz-card">
    <div class="question-header">
        <div>Question {idx}</div>
        <div class="difficulty-badge {diff_class}">{difficulty.capitalize()}</div>
    </div>
    <div class="question-stem">{q['stem']}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    choice = st.radio(
        "",
        q["choices"],
        key=f"{selected_key}_{q['id']}",
        label_visibility="collapsed",
    )
    answers[q["id"]] = choice

submit = st.button("Submit lesson quiz")

if submit:
    total = len(questions)
    correct_count = 0
    easy_correct = 0
    easy_total = 0
    medium_correct = 0
    medium_total = 0
    hard_correct = 0
    hard_total = 0
    topic_performance = {}

    for q in questions:
        picked = answers.get(q["id"])
        picked_index = q["choices"].index(picked) if picked in q["choices"] else None
        is_correct = picked_index == q["answer"]
        correct_flags[q["id"]] = is_correct

        if q["difficulty"] == "easy":
            easy_total += 1
            if is_correct:
                easy_correct += 1
        elif q["difficulty"] == "medium":
            medium_total += 1
            if is_correct:
                medium_correct += 1
        else:
            hard_total += 1
            if is_correct:
                hard_correct += 1

        if is_correct:
            correct_count += 1

    pct = round(100 * correct_count / total) if total > 0 else 0
    
    # save results
    if username != 'guest':
        DataManager.update_progress(
            username,
            'lesson_quizzes',
            {
                selected_key: {
                    'completed': True,
                    'score': correct_count,
                    'total': total,
                    'score_pct': pct,
                    'best_score_pct': max(pct, DataManager.get_user_progress(username).get('lesson_quizzes', {}).get(selected_key, {}).get('best_score_pct', 0)),
                    'easy_score': f"{easy_correct}/{easy_total}",
                    'medium_score': f"{medium_correct}/{medium_total}",
                    'hard_score': f"{hard_correct}/{hard_total}",
                    'date': datetime.now().isoformat(),
                    'attempts': DataManager.get_user_progress(username).get('lesson_quizzes', {}).get(selected_key, {}).get('attempts', 0) + 1
                }
            }
        )

    performance_level = "Mastering" if pct >= 80 else "Improving" if pct >= 60 else "Learning"
    difficulty_trend = ""
    next_steps = ""
    
    if easy_total > 0 and easy_correct == easy_total and medium_correct >= medium_total * 0.8:
        difficulty_trend = "📈 Strong foundation! You're ready for more challenging questions."
        next_steps = "Your next quiz will include more hard questions to challenge you."
    elif easy_correct < easy_total * 0.6:
        difficulty_trend = "📚 Focus on fundamentals. Review the lesson content for this topic."
        next_steps = "Your next quiz will focus on easier questions to build your foundation."
    elif hard_total > 0 and hard_correct >= hard_total * 0.6:
        difficulty_trend = "🌟 Excellent! You're mastering advanced concepts."
        next_steps = "Keep challenging yourself with complex problems!"
    else:
        difficulty_trend = "💪 Good progress! Keep practicing to improve."
        next_steps = "Your next quiz will adapt to help you improve further."
    
    st.markdown(
        f"""
<div class="result-box">
    <div class="result-score">{pct}%</div>
    <div class="result-text">
        You answered {correct_count} out of {total} correctly. <strong>{performance_level}!</strong>
    </div>
    <div class="result-text" style="margin-top: 10px;">
        Easy: {easy_correct}/{easy_total}  
        Medium: {medium_correct}/{medium_total}  
        Hard: {hard_correct}/{hard_total}
    </div>
    <div style="margin-top: 15px; padding: 15px; background: rgba(255,255,255,0.3); border-radius: 10px;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">🤖 ML Insights:</div>
        <div style="font-size: 13px; margin-bottom: 5px;">{difficulty_trend}</div>
        <div style="font-size: 13px; color: #555;"><strong>Next Steps:</strong> {next_steps}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    
    # Show improvement over attempts
    if username != 'guest':
        attempts = DataManager.get_user_progress(username).get('lesson_quizzes', {}).get(selected_key, {}).get('attempts', 1)
        best_score = DataManager.get_user_progress(username).get('lesson_quizzes', {}).get(selected_key, {}).get('best_score_pct', pct)
        if attempts > 1:
            if pct > best_score - 10:
                st.success(f"📊 **Progress Tracking:** This is attempt #{attempts}. Best score: {best_score}%")
            if pct == best_score and pct >= 80:
                st.balloons()
                st.success("🎉 **New Personal Best!** You're mastering this lesson!")
            elif pct > best_score:
                st.success(f"🎉 **Improvement!** You scored {pct - best_score}% better than your previous best!")

    for idx, q in enumerate(questions, start=1):
        picked = answers.get(q["id"])
        picked_index = q["choices"].index(picked) if picked in q["choices"] else None
        is_correct = picked_index == q["answer"]

        css_class = (
            "per-question-correct" if is_correct else "per-question-wrong"
        )
        label = "Correct" if is_correct else "Check this one again"

        st.markdown(
            f"""
<div class="per-question-result {css_class}">
    Question {idx}: {label}
</div>
""",
            unsafe_allow_html=True,
        )


st.markdown("---")
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("Back to lessons"):
        if "current_page" in st.session_state:
            st.session_state.current_page = "lessons"
            st.rerun()
with col_b:
    if st.button("Back to home"):
        if "current_page" in st.session_state:
            st.session_state.current_page = "dashboard"
            st.rerun()
with col_c:
    if st.button("Retry quiz", type="primary"):
        st.rerun()

if __name__ == "__main__":
    main()
