"""
Quiz styling - consistent with dashboard
"""

QUIZ_STYLES = """
<style>
    /* Force dark mode for quiz */
    .stApp {
        background-color: #1a1a1a !important;
    }
    
    /* All text white */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #FFFFFF !important;
    }
    
    /* Quiz card styling */
    .quiz-card {
        background: #2d2d2d;
        border-radius: 20px;
        padding: 32px;
        border: 2px solid #404040;
        margin: 20px 0;
    }
    
    /* Question styling */
    .quiz-question {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        line-height: 1.4;
    }
    
    /* Radio buttons - olive green */
    .stRadio > label {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    
    /* Force all buttons olive green */
    .stButton>button, .stFormSubmitButton>button {
        background: #6B8E23 !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 0 #556B2F !important;
    }
    
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 0 #556B2F !important;
        background: #7BA428 !important;
    }
    
    .stButton>button:active, .stFormSubmitButton>button:active {
        transform: translateY(2px) !important;
        box-shadow: 0 2px 0 #556B2F !important;
    }
    
    /* Progress bar - olive green */
    .stProgress > div > div {
        background-color: #6B8E23 !important;
    }
    
    /* Stats cards */
    .stat-box {
        background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 0 #556B2F;
        margin: 10px 0;
    }
    
    .stat-number {
        font-size: 48px;
        font-weight: 900;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .stat-label {
        font-size: 14px;
        font-weight: 600;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 12px !important;
    }
    
    /* Question card */
    .question-card {
        background: #2d2d2d;
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        border: 2px solid #404040;
    }
    
    .question-topic {
        display: inline-block;
        background: #6B8E23;
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
    }
    
    .question-stem {
        font-size: 20px;
        font-weight: 600;
        color: #FFFFFF;
        line-height: 1.6;
        margin-top: 12px;
    }
    
    .question-number {
        font-size: 14px;
        color: #B3B3B3;
        font-weight: 600;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Progress bar container */
    .progress-container {
        width: 100%;
        height: 8px;
        background: #404040;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #6B8E23 0%, #7BA428 100%);
        transition: width 0.3s ease;
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);
        border-radius: 20px;
        padding: 48px;
        text-align: center;
        color: white;
        margin: 30px 0;
        box-shadow: 0 8px 0 #556B2F;
    }
    
    .result-label {
        font-size: 18px;
        font-weight: 600;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .result-score {
        font-size: 72px;
        font-weight: 900;
        margin: 20px 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
</style>
"""


def apply_quiz_styles():
    """Apply consistent quiz styling"""
    import streamlit as st
    st.markdown(QUIZ_STYLES, unsafe_allow_html=True)
