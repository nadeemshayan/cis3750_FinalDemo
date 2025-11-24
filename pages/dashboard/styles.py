"""
Shared styles for dashboard pages - OLIVE GREEN THEME
"""

DASHBOARD_STYLES = """
<style>
    /* Force olive green for ALL buttons */
    .stButton>button, .stFormSubmitButton>button {
        background: #6B8E23 !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 0 #556B2F !important;
        text-transform: none !important;
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
    
    /* Premium cards - DARK MODE */
    .dashboard-card {
        background: #2d2d2d;
        border-radius: 20px;
        padding: 24px;
        border: 2px solid #404040;
        transition: all 0.3s ease;
        margin-bottom: 16px;
    }
    
    .dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
        border-color: #6B8E23;
    }
    
    /* Stats display - OLIVE GREEN */
    .stat-card {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);
        border-radius: 16px;
        color: white;
        box-shadow: 0 4px 0 #556B2F;
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
    
    /* Action buttons - DARK MODE */
    .action-button {
        background: #2d2d2d;
        border: 2px solid #404040;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #FFFFFF;
    }
    
    .action-button:hover {
        border-color: #6B8E23;
        transform: scale(1.05);
    }
    
    /* Progress bars - OLIVE GREEN */
    .stProgress > div > div {
        background-color: #6B8E23 !important;
    }
</style>
"""


def apply_dashboard_styles():
    """Apply consistent olive green dashboard styles"""
    import streamlit as st
    st.markdown(DASHBOARD_STYLES, unsafe_allow_html=True)
