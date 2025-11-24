"""
Supabase Data Manager - Cloud-persistent storage
Replaces JSON files with PostgreSQL database via Supabase
"""

import streamlit as st
from supabase import create_client, Client
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    try:
        # Try to get from Streamlit secrets (production)
        supabase_url = st.secrets["supabase"]["url"]
        supabase_key = st.secrets["supabase"]["key"]
    except:
        # Fallback to environment variables or raise error
        import os
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            st.error("⚠️ Supabase credentials not found! Please configure secrets.")
            st.stop()
    
    return create_client(supabase_url, supabase_key)


class SupabaseDataManager:
    """Handles all data persistence via Supabase"""
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # --- User Management ---
    
    @staticmethod
    def register_user(username: str, password: str, email: str, role: str, **kwargs) -> tuple[bool, str]:
        """Register a new user"""
        supabase = get_supabase_client()
        
        # Check if username exists
        response = supabase.table('users').select('username').eq('username', username).execute()
        if response.data:
            return False, "Username already exists"
        
        # Insert new user
        user_data = {
            "username": username,
            "password": SupabaseDataManager._hash_password(password),
            "email": email,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "age_level": kwargs.get("age_level", "High School"),
            "grade": kwargs.get("grade", ""),
            "share_code": kwargs.get("share_code", ""),
            "teacher_code": kwargs.get("teacher_code", ""),
            "parent_codes": json.dumps(kwargs.get("parent_codes", [])),
            "teacher_codes": json.dumps(kwargs.get("teacher_codes", []))
        }
        
        try:
            supabase.table('users').insert(user_data).execute()
            
            # Initialize progress for new user
            SupabaseDataManager.init_user_progress(username)
            
            return True, "Registration successful"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, Optional[Dict], str]:
        """Authenticate user login"""
        supabase = get_supabase_client()
        
        # Get user
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if not response.data:
            return False, None, "User not found"
        
        user = response.data[0]
        
        # Verify password
        if user["password"] != SupabaseDataManager._hash_password(password):
            return False, None, "Incorrect password"
        
        # Parse JSON fields
        user['parent_codes'] = json.loads(user.get('parent_codes', '[]'))
        user['teacher_codes'] = json.loads(user.get('teacher_codes', '[]'))
        
        return True, user, "Login successful"
    
    @staticmethod
    def get_user(username: str) -> Optional[Dict]:
        """Get user information"""
        supabase = get_supabase_client()
        
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if response.data:
            user = response.data[0]
            # Parse JSON fields
            user['parent_codes'] = json.loads(user.get('parent_codes', '[]'))
            user['teacher_codes'] = json.loads(user.get('teacher_codes', '[]'))
            return user
        return None
    
    @staticmethod
    def update_user(username: str, updates: Dict) -> bool:
        """Update user information"""
        supabase = get_supabase_client()
        
        try:
            # Convert lists to JSON strings if present
            if 'parent_codes' in updates:
                updates['parent_codes'] = json.dumps(updates['parent_codes'])
            if 'teacher_codes' in updates:
                updates['teacher_codes'] = json.dumps(updates['teacher_codes'])
            
            supabase.table('users').update(updates).eq('username', username).execute()
            return True
        except:
            return False
    
    # --- Progress Management ---
    
    @staticmethod
    def init_user_progress(username: str):
        """Initialize progress tracking for a new user"""
        supabase = get_supabase_client()
        
        progress_data = {
            "username": username,
            "initial_quiz": json.dumps({
                "completed": False,
                "score": 0,
                "total": 8,
                "weak_topics": [],
                "strong_topics": [],
                "date": None
            }),
            "lessons": json.dumps({}),
            "lesson_quizzes": json.dumps({}),
            "practice_problems": json.dumps({}),
            "final_test": json.dumps({
                "completed": False,
                "score": 0,
                "date": None
            }),
            "badges": json.dumps([]),
            "certificates": json.dumps([]),
            "total_time_spent": 0,
            "last_active": datetime.now().isoformat(),
            "current_level": 1,
            "overall_progress": 0
        }
        
        try:
            supabase.table('progress').insert(progress_data).execute()
        except:
            pass  # Progress already exists
    
    @staticmethod
    def get_user_progress(username: str) -> Dict:
        """Get user progress data"""
        supabase = get_supabase_client()
        
        response = supabase.table('progress').select('*').eq('username', username).execute()
        
        if response.data:
            progress = response.data[0]
            # Parse JSON fields
            progress['initial_quiz'] = json.loads(progress.get('initial_quiz', '{}'))
            progress['lessons'] = json.loads(progress.get('lessons', '{}'))
            progress['lesson_quizzes'] = json.loads(progress.get('lesson_quizzes', '{}'))
            progress['practice_problems'] = json.loads(progress.get('practice_problems', '{}'))
            progress['final_test'] = json.loads(progress.get('final_test', '{}'))
            progress['badges'] = json.loads(progress.get('badges', '[]'))
            progress['certificates'] = json.loads(progress.get('certificates', '[]'))
            return progress
        
        # Return default if not found
        return {
            "initial_quiz": {"completed": False, "score": 0, "total": 8, "weak_topics": [], "strong_topics": [], "date": None},
            "lessons": {},
            "lesson_quizzes": {},
            "practice_problems": {},
            "final_test": {"completed": False, "score": 0, "date": None},
            "badges": [],
            "certificates": [],
            "total_time_spent": 0,
            "last_active": datetime.now().isoformat(),
            "current_level": 1,
            "overall_progress": 0
        }
    
    @staticmethod
    def update_user_progress(username: str, progress_data: Dict) -> bool:
        """Update user progress"""
        supabase = get_supabase_client()
        
        try:
            # Convert complex objects to JSON strings
            update_data = {}
            for key, value in progress_data.items():
                if key in ['initial_quiz', 'lessons', 'lesson_quizzes', 'practice_problems', 
                          'final_test', 'badges', 'certificates']:
                    update_data[key] = json.dumps(value)
                else:
                    update_data[key] = value
            
            update_data['last_active'] = datetime.now().isoformat()
            
            supabase.table('progress').update(update_data).eq('username', username).execute()
            return True
        except Exception as e:
            st.error(f"Error updating progress: {e}")
            return False
    
    # --- Additional Methods (keeping same signatures as original) ---
    
    @staticmethod
    def save_quiz_results(username: str, score: int, total: int, weak_topics: List[str], strong_topics: List[str]):
        """Save initial quiz results"""
        progress = SupabaseDataManager.get_user_progress(username)
        progress['initial_quiz'] = {
            "completed": True,
            "score": score,
            "total": total,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "date": datetime.now().isoformat()
        }
        SupabaseDataManager.update_user_progress(username, progress)
    
    @staticmethod
    def update_lesson_progress(username: str, lesson_id: str, completed: bool, time_spent: int):
        """Update lesson progress"""
        progress = SupabaseDataManager.get_user_progress(username)
        if 'lessons' not in progress:
            progress['lessons'] = {}
        
        progress['lessons'][lesson_id] = {
            "completed": completed,
            "time_spent": time_spent,
            "progress": 1.0 if completed else 0.5,
            "date": datetime.now().isoformat()
        }
        
        SupabaseDataManager.update_user_progress(username, progress)
    
    @staticmethod
    def award_badge(username: str, badge_name: str, description: str):
        """Award a badge to user"""
        progress = SupabaseDataManager.get_user_progress(username)
        if badge_name not in progress.get('badges', []):
            progress['badges'].append(badge_name)
            SupabaseDataManager.update_user_progress(username, progress)
    
    @staticmethod
    def reset_password(username: str, email: str, new_password: str) -> bool:
        """Reset user password"""
        supabase = get_supabase_client()
        
        try:
            # Verify user exists with that email
            response = supabase.table('users').select('*').eq('username', username).eq('email', email).execute()
            
            if not response.data:
                return False
            
            # Update password
            supabase.table('users').update({
                'password': SupabaseDataManager._hash_password(new_password)
            }).eq('username', username).execute()
            
            return True
        except:
            return False
