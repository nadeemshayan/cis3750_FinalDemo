"""
Parent dashboard - clean and consistent
"""
import streamlit as st
from data_manager import DataManager
from pages.dashboard.styles import apply_dashboard_styles


def render():
    """Render parent dashboard"""
    apply_dashboard_styles()
    
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px;">
            Parent Dashboard 👨‍👩‍👧‍👦
        </h1>
        <p style="font-size: 15px; color: #B3B3B3;">Monitor your children's learning progress</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%);">
            <div class="stat-number">0</div>
            <div class="stat-label">Connected Children</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%);">
            <div class="stat-number">0</div>
            <div class="stat-label">Avg Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #8B9F29 0%, #7BA428 100%);">
            <div class="stat-number">0</div>
            <div class="stat-label">Active This Week</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    st.subheader("👨‍👩‍👧‍👦 Manage Children")
    
    if st.button("➕ Connect Child Account", use_container_width=True):
        st.info("Enter your child's share code to connect their account")
        share_code = st.text_input("Share Code", placeholder="SHARE-1234")
        if st.button("Connect"):
            st.success("Feature coming soon!")
    
    st.markdown("---")
    
    st.info("📊 Detailed progress reports and activity monitoring coming soon!")
