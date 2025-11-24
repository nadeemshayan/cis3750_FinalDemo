import streamlit as st

def home_button():
    st.markdown("""
    <style>
        .home-button-container {
            position: fixed;
            top: 70px;
            right: 20px;
            z-index: 999;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col3:
        if st.button("🏠 Home", key="nav_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()


def page_header(title, subtitle=None):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <h1 style="font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 8px;">
                {title}
            </h1>
            {f'<p style="font-size: 15px; color: #B3B3B3;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🏠 Home", key="page_header_home", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("---")
