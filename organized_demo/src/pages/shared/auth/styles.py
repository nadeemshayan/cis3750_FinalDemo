"""
Shared styles for authentication pages
"""

AUTH_STYLES = """
<style>
    /* Hide sidebar completely on auth pages */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Hide sidebar toggle button */
    button[kind="header"] {
        display: none !important;
    }
    
    /* Force all buttons to be olive green on auth pages */
    .stButton>button, .stFormSubmitButton>button {
        background: #6B8E23 !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
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
    
    /* Auth container */
    .auth-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 0px 20px 20px 20px;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .logo-container img {
        width: 120px;
        height: 120px;
        margin-bottom: 16px;
        animation: bounce 1s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .app-title {
        font-size: 36px;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        text-align: center;
        margin-bottom: 6px;
        margin-top: 6px;
        letter-spacing: -0.8px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    
    .app-subtitle {
        font-size: 15px;
        color: #B3B3B3 !important;
        text-align: center;
        margin-bottom: 20px;
        line-height: 1.4;
        font-weight: 500;
    }
    
    .auth-card {
        background: linear-gradient(145deg, #2d2d2d 0%, #252525 100%) !important;
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        border: 2px solid #404040;
    }
    
    .form-header {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        margin-top: 0px;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    .link-button {
        background: none;
        border: none;
        color: #1CB0F6;
        font-weight: 700;
        cursor: pointer;
        text-decoration: underline;
        padding: 0;
        font-size: 15px;
    }
</style>
"""


def apply_auth_styles():
    """Apply authentication page styles"""
    import streamlit as st
    st.markdown(AUTH_STYLES, unsafe_allow_html=True)
