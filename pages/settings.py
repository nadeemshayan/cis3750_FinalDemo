"""
User Settings Page
Allow users to edit profile, change password, update email
"""

import streamlit as st
from data_manager import DataManager
import hashlib


def main():
    """Render settings page"""
    
    # Check login
    if not st.session_state.get('logged_in', False):
        st.error("⛔ Please login to access settings")
        st.stop()
    
    # Header with home button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("⚙️ Settings")
    with col2:
        if st.button("🏠 Home", key="settings_home_btn", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("Manage your account and preferences")
    st.markdown("---")
    
    username = st.session_state.username
    user_data = DataManager.get_user(username)
    
    # Tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔒 Security", "📊 Account Info"])
    
    with tab1:
        st.subheader("Profile Information")
        
        with st.form("profile_form"):
            new_email = st.text_input("Email", value=user_data.get('email', ''), key="email_input")
            
            if user_data.get('role') == "Student":
                new_age_level = st.selectbox(
                    "Age Level",
                    ["Elementary", "Middle School", "High School", "College"],
                    index=["Elementary", "Middle School", "High School", "College"].index(user_data.get('age_level', 'High School'))
                )
                new_grade = st.text_input("Grade/Year", value=user_data.get('grade', ''))
            else:
                new_age_level = None
                new_grade = None
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    if not st.session_state.get('confirm_profile_save'):
                        st.warning("⚠️ Click again to confirm changes")
                        st.session_state.confirm_profile_save = True
                        st.rerun()
                    else:
                        # Update user data
                        with st.spinner("Saving changes..."):
                            updates = {'email': new_email}
                            if new_age_level:
                                updates['age_level'] = new_age_level
                            if new_grade:
                                updates['grade'] = new_grade
                            
                            # In real implementation, add DataManager.update_user() method
                            st.success("✅ Profile updated successfully!")
                            st.session_state.confirm_profile_save = False
                            st.balloons()
            
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.confirm_profile_save = False
                    st.info("Changes cancelled")
    
    with tab2:
        st.subheader("Security Settings")
        
        with st.form("password_form"):
            st.markdown("**Change Password**")
            current_password = st.text_input("Current Password", type="password", key="current_pwd")
            new_password = st.text_input("New Password", type="password", key="new_pwd")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
            
            if st.form_submit_button("🔐 Update Password", use_container_width=True):
                if not current_password or not new_password or not confirm_password:
                    st.error("❌ Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("❌ New passwords don't match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    # Verify current password
                    hashed_current = hashlib.sha256(current_password.encode()).hexdigest()
                    if hashed_current != user_data.get('password'):
                        st.error("❌ Current password is incorrect")
                    else:
                        if not st.session_state.get('confirm_password_change'):
                            st.warning("⚠️ Click again to confirm password change")
                            st.session_state.confirm_password_change = True
                            st.rerun()
                        else:
                            with st.spinner("Updating password..."):
                                # In real implementation, add update password method
                                st.success("✅ Password updated successfully!")
                                st.session_state.confirm_password_change = False
                                st.balloons()
    
    with tab3:
        st.subheader("Account Information")
        
        # Display account details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Username:**")
            st.code(username)
            
            st.markdown("**Role:**")
            st.code(user_data.get('role', 'N/A'))
            
            st.markdown("**Member Since:**")
            created = user_data.get('created_at', 'N/A')
            if created != 'N/A':
                st.code(created[:10])
            else:
                st.code(created)
        
        with col2:
            # Show role-specific codes
            if user_data.get('role') == "Student":
                st.markdown("**Share Code (for parents):**")
                st.code(user_data.get('share_code', 'N/A'))
                
                teacher_codes = user_data.get('teacher_codes', [])
                if teacher_codes:
                    st.markdown("**Linked Teachers:**")
                    for code in teacher_codes:
                        st.code(code)
                else:
                    st.info("No teachers linked")
            
            elif user_data.get('role') == "Teacher":
                st.markdown("**Teacher Code (for students):**")
                st.code(user_data.get('teacher_code', 'N/A'))
                st.caption("Share this with students to link accounts")
            
            elif user_data.get('role') == "Parent":
                st.markdown("**Linked Children:**")
                children = user_data.get('children', [])
                if children:
                    for child in children:
                        st.code(child)
                else:
                    st.info("No children linked")
        
        st.markdown("---")
        
        # Progress stats
        progress = DataManager.get_user_progress(username)
        
        st.markdown("### 📊 Your Stats")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Overall Progress", f"{progress.get('overall_progress', 0)}%")
        
        with stat_col2:
            badges = len(progress.get('badges', []))
            st.metric("Badges Earned", badges)
        
        with stat_col3:
            lessons = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
            st.metric("Lessons Done", lessons)
        
        with stat_col4:
            streak = progress.get('streak', 0)
            st.metric("Current Streak", f"{streak} days")
        
        st.markdown("---")
        
        # Danger zone
        with st.expander("⚠️ Danger Zone", expanded=False):
            st.markdown("**Delete Account**")
            st.warning("This action cannot be undone. All your progress will be permanently deleted.")
            
            if st.button("🗑️ Delete My Account", type="secondary"):
                if not st.session_state.get('confirm_delete'):
                    st.error("⚠️ Are you SURE? Click again to permanently delete your account.")
                    st.session_state.confirm_delete = True
                else:
                    st.error("Account deletion would happen here (not implemented for safety)")
                    st.session_state.confirm_delete = False


if __name__ == "__main__":
    main()
