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
        
        # Parse JSONB fields (Supabase returns them as objects, not strings)
        parent_codes = user.get('parent_codes', [])
        user['parent_codes'] = parent_codes if isinstance(parent_codes, list) else json.loads(parent_codes) if parent_codes else []
        
        teacher_codes = user.get('teacher_codes', [])
        user['teacher_codes'] = teacher_codes if isinstance(teacher_codes, list) else json.loads(teacher_codes) if teacher_codes else []
        
        children = user.get('children', [])
        user['children'] = children if isinstance(children, list) else json.loads(children) if children else []
        
        return True, user, "Login successful"
    
    @staticmethod
    def get_user(username: str) -> Optional[Dict]:
        """Get user information"""
        supabase = get_supabase_client()
        
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if response.data:
            user = response.data[0]
            # Parse JSONB fields (Supabase returns them as objects, not strings)
            parent_codes = user.get('parent_codes', [])
            user['parent_codes'] = parent_codes if isinstance(parent_codes, list) else json.loads(parent_codes) if parent_codes else []
            
            teacher_codes = user.get('teacher_codes', [])
            user['teacher_codes'] = teacher_codes if isinstance(teacher_codes, list) else json.loads(teacher_codes) if teacher_codes else []
            
            children = user.get('children', [])
            user['children'] = children if isinstance(children, list) else json.loads(children) if children else []
            
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
                "total": 18,
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
            "initial_quiz": {"completed": False, "score": 0, "total": 18, "weak_topics": [], "strong_topics": [], "date": None},
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
    def save_quiz_results(username: str, quiz_type: str, score: int, total: int, weak_topics: List[str], strong_topics: List[str]):
        """Save quiz results (initial or lesson quiz)"""
        progress = SupabaseDataManager.get_user_progress(username)
        
        quiz_data = {
            "completed": True,
            "score": score,
            "total": total,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "date": datetime.now().isoformat()
        }
        
        if quiz_type == "initial":
            progress['initial_quiz'] = quiz_data
        else:
            if 'lesson_quizzes' not in progress:
                progress['lesson_quizzes'] = {}
            progress['lesson_quizzes'][quiz_type] = quiz_data
        
        # Update overall progress (quiz 20%, lessons 60%, practice 20%)
        quiz_completed = progress.get("initial_quiz", {}).get("completed", False)
        lessons_completed = len([l for l in progress.get("lessons", {}).values() if l.get("completed")])
        practice_done = len(progress.get("practice_problems", {}))
        
        overall = 0
        if quiz_completed:
            overall += 20
        overall += (lessons_completed / 6) * 60 if lessons_completed > 0 else 0
        overall += (practice_done / 10) * 20 if practice_done > 0 else 0
        
        progress["overall_progress"] = int(overall)
        print(f"📊 Supabase Quiz Progress Update: Quiz={quiz_completed}, Lessons={lessons_completed}/6, Practice={practice_done}/10 → Overall={int(overall)}%")
        
        SupabaseDataManager.update_user_progress(username, progress)
    
    @staticmethod
    def save_lesson_progress(username: str, lesson_id: str, completed: bool = False, time_spent: int = 0):
        """Save lesson progress (matches DataManager API)"""
        progress = SupabaseDataManager.get_user_progress(username)
        if 'lessons' not in progress:
            progress['lessons'] = {}
        
        progress['lessons'][lesson_id] = {
            "completed": completed,
            "time_spent": time_spent,
            "progress": 1.0 if completed else 0.5,
            "date": datetime.now().isoformat()
        }
        
        # Update total time spent
        progress['total_time_spent'] = progress.get('total_time_spent', 0) + time_spent
        
        # Update overall progress (quiz 20%, lessons 60%, practice 20%)
        quiz_completed = progress.get("initial_quiz", {}).get("completed", False)
        lessons_completed = len([l for l in progress.get("lessons", {}).values() if l.get("completed")])
        practice_done = len(progress.get("practice_problems", {}))
        
        overall = 0
        if quiz_completed:
            overall += 20
        overall += (lessons_completed / 6) * 60 if lessons_completed > 0 else 0
        overall += (practice_done / 10) * 20 if practice_done > 0 else 0
        
        progress["overall_progress"] = int(overall)
        print(f"📊 Supabase Lesson Progress Update: Quiz={quiz_completed}, Lessons={lessons_completed}/6, Practice={practice_done}/10 → Overall={int(overall)}%")
        
        SupabaseDataManager.update_user_progress(username, progress)
    
    @staticmethod
    def update_lesson_progress(username: str, lesson_id: str, completed: bool, time_spent: int):
        """Update lesson progress (legacy method)"""
        SupabaseDataManager.save_lesson_progress(username, lesson_id, completed, time_spent)
    
    @staticmethod
    def award_badge(username: str, badge_name: str, description: str):
        """Award a badge to user"""
        progress = SupabaseDataManager.get_user_progress(username)
        badges = progress.get('badges', [])
        
        # Check if badge already exists by name
        earned_badge_names = [b.get('name') if isinstance(b, dict) else b for b in badges]
        if badge_name not in earned_badge_names:
            badge = {
                "name": badge_name,
                "description": description,
                "date": datetime.now().isoformat()
            }
            badges.append(badge)
            progress['badges'] = badges
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
        except Exception as e:
            print(f"Error resetting password: {e}")
            return False
    
    @staticmethod
    def link_parent_to_child(parent_username: str, child_share_code: str) -> tuple:
        """
        Link a parent to their child's account using share code
        Returns: (success: bool, message: str)
        """
        supabase = get_supabase_client()
        
        try:
            # Check if parent exists
            parent_response = supabase.table('users').select('*').eq('username', parent_username).execute()
            if not parent_response.data:
                return False, "Parent account not found"
            
            parent_data = parent_response.data[0]
            
            # Find child with this share code
            child_response = supabase.table('users').select('*').eq('share_code', child_share_code).execute()
            if not child_response.data:
                return False, f"Student with share code '{child_share_code}' not found"
            
            child_data = child_response.data[0]
            child_username = child_data['username']
            
            # Get current children list
            children = parent_data.get('children', [])
            if not isinstance(children, list):
                children = []
            
            # Check if already linked
            if child_username in children:
                return False, "Child already linked"
            
            # Add child to parent's list
            children.append(child_username)
            supabase.table('users').update({
                'children': children
            }).eq('username', parent_username).execute()
            
            # Add parent to child's parent_codes list
            parent_codes = child_data.get('parent_codes', [])
            if not isinstance(parent_codes, list):
                parent_codes = []
            
            if parent_username not in parent_codes:
                parent_codes.append(parent_username)
                supabase.table('users').update({
                    'parent_codes': parent_codes
                }).eq('username', child_username).execute()
            
            return True, f"Successfully linked to {child_username}'s account!"
        
        except Exception as e:
            print(f"Error linking parent to child: {e}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def link_student_to_teacher(student_username: str, teacher_code: str) -> tuple:
        """
        Link a student to a teacher's class using teacher code
        Returns: (success: bool, message: str)
        """
        supabase = get_supabase_client()
        
        try:
            # Check if student exists
            student_response = supabase.table('users').select('*').eq('username', student_username).execute()
            if not student_response.data:
                return False, "Student account not found"
            
            student_data = student_response.data[0]
            
            # Find teacher with this code
            teacher_response = supabase.table('users').select('*').eq('teacher_code', teacher_code).execute()
            if not teacher_response.data:
                return False, f"Teacher with code '{teacher_code}' not found"
            
            teacher_data = teacher_response.data[0]
            teacher_username = teacher_data['username']
            
            # Get student's teacher_codes list
            teacher_codes = student_data.get('teacher_codes', [])
            if not isinstance(teacher_codes, list):
                teacher_codes = []
            
            # Check if already enrolled
            if teacher_code in teacher_codes:
                return False, "Already enrolled in this class"
            
            # Add teacher code to student's list
            teacher_codes.append(teacher_code)
            supabase.table('users').update({
                'teacher_codes': teacher_codes
            }).eq('username', student_username).execute()
            
            print(f"✅ Linked {student_username} to teacher {teacher_username} (code: {teacher_code})")
            return True, f"Successfully joined {teacher_username}'s class!"
        
        except Exception as e:
            print(f"Error linking student to teacher: {e}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_students_by_teacher_code(teacher_code: str) -> List[Dict]:
        """Get students who joined with a teacher's code"""
        supabase = get_supabase_client()
        
        try:
            # Get all students
            students_response = supabase.table('users').select('*').eq('role', 'Student').execute()
            
            students = []
            for user in students_response.data:
                # Check if teacher_code is in student's teacher_codes array
                teacher_codes = user.get('teacher_codes', [])
                if not isinstance(teacher_codes, list):
                    teacher_codes = json.loads(teacher_codes) if teacher_codes else []
                
                if teacher_code in teacher_codes:
                    # Get student's progress
                    progress_response = supabase.table('progress').select('*').eq('username', user['username']).execute()
                    progress_data = progress_response.data[0] if progress_response.data else {}
                    
                    students.append({
                        "username": user['username'],
                        "email": user['email'],
                        "progress": progress_data.get('overall_progress', 0),
                        "last_active": progress_data.get('last_active', 'Never')
                    })
            
            return students
        
        except Exception as e:
            print(f"Error getting students by teacher code: {e}")
            return []
