import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

# Try to use Supabase, fall back to JSON for local dev
# NOW ENABLED - Supabase manager now has complete progress calculation
USE_SUPABASE = True
try:
    from database.supabase_manager import SupabaseDataManager
    print("✅ Supabase enabled - Progress will persist on cloud!")
except Exception as e:
    USE_SUPABASE = False
    print(f"⚠️ Supabase not configured ({e}), using JSON fallback")

# JSON fallback configuration
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
PROGRESS_FILE = DATA_DIR / "progress.json"
QUIZZES_FILE = DATA_DIR / "quizzes.json"
LESSONS_FILE = DATA_DIR / "lessons.json"


class DataManager:
    """Handles all data persistence operations - routes to Supabase or JSON"""
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def _load_json(filepath: Path) -> Dict:
        """Load data from JSON file"""
        if not filepath.exists():
            return {}
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    @staticmethod
    def _save_json(filepath: Path, data: Dict):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved to {filepath.name} - {len(data)} users")
    
    # --- User Management ---
    
    @staticmethod
    def register_user(username: str, password: str, email: str, role: str, **kwargs) -> tuple[bool, str]:
        """Register a new user"""
        # Use Supabase if available
        if USE_SUPABASE:
            return SupabaseDataManager.register_user(username, password, email, role, **kwargs)
        
        # JSON fallback
        users = DataManager._load_json(USERS_FILE)
        
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            "password": DataManager._hash_password(password),
            "email": email,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "age_level": kwargs.get("age_level", "High School"),
            "grade": kwargs.get("grade", ""),
            "share_code": kwargs.get("share_code", ""),
            "parent_codes": kwargs.get("parent_codes", []),
            "teacher_codes": kwargs.get("teacher_codes", [])
        }
        
        DataManager._save_json(USERS_FILE, users)
        
        # Initialize progress for new user
        DataManager.init_user_progress(username)
        
        return True, "Registration successful"
    
    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, Optional[Dict], str]:
        """Authenticate user login"""
        # Use Supabase if available
        if USE_SUPABASE:
            return SupabaseDataManager.login_user(username, password)
        
        # JSON fallback
        users = DataManager._load_json(USERS_FILE)
        
        if username not in users:
            return False, None, "User not found"
        
        user = users[username]
        if user["password"] != DataManager._hash_password(password):
            return False, None, "Incorrect password"
        
        return True, user, "Login successful"
    
    @staticmethod
    def get_user(username: str) -> Optional[Dict]:
        """Get user information"""
        # Use Supabase if available
        if USE_SUPABASE:
            return SupabaseDataManager.get_user(username)
        
        # JSON fallback
        users = DataManager._load_json(USERS_FILE)
        return users.get(username)
    
    @staticmethod
    def update_user(username: str, updates: Dict) -> bool:
        """Update user information"""
        users = DataManager._load_json(USERS_FILE)
        if username not in users:
            return False
        users[username].update(updates)
        DataManager._save_json(USERS_FILE, users)
        return True
    
    @staticmethod
    def reset_password(username: str, email: str, new_password: str) -> tuple[bool, str]:
        """Reset user password"""
        users = DataManager._load_json(USERS_FILE)
        
        if username not in users:
            return False, "User not found"
        
        if users[username]["email"] != email:
            return False, "Email doesn't match"
        
        users[username]["password"] = DataManager._hash_password(new_password)
        DataManager._save_json(USERS_FILE, users)
        return True, "Password reset successful"
    
    # --- Progress Management ---
    
    @staticmethod
    def init_user_progress(username: str):
        """Initialize progress tracking for a new user"""
        progress = DataManager._load_json(PROGRESS_FILE)
        
        if username not in progress:
            progress[username] = {
                "initial_quiz": {
                    "completed": False,
                    "score": 0,
                    "total": 18,
                    "weak_topics": [],
                    "strong_topics": [],
                    "date": None
                },
                "lessons": {},
                "lesson_quizzes": {},
                "practice_problems": {},
                "final_test": {
                    "completed": False,
                    "score": 0,
                    "date": None
                },
                "badges": [],
                "certificates": [],
                "total_time_spent": 0,
                "last_active": datetime.now().isoformat(),
                "current_level": 1,
                "overall_progress": 0
            }
            DataManager._save_json(PROGRESS_FILE, progress)
    
    @staticmethod
    def get_user_progress(username: str) -> Dict:
        """Get user progress data"""
        # Use Supabase if available
        if USE_SUPABASE:
            try:
                result = SupabaseDataManager.get_user_progress(username)
                print(f"📖 Supabase get_user_progress: {username} → Overall={result.get('overall_progress', 0)}%")
                return result
            except Exception as e:
                print(f"❌ Supabase get_user_progress failed: {e}")
                # Don't fall back, re-raise to show the error
                raise
        
        # JSON fallback
        progress_data = DataManager._load_json(PROGRESS_FILE)
        if username not in progress_data:
            DataManager.init_user_progress(username)
            progress_data = DataManager._load_json(PROGRESS_FILE)
        
        user_progress = progress_data.get(username, {})
        print(f"📖 Reading progress for {username}: Overall={user_progress.get('overall_progress', 0)}%, Quiz={user_progress.get('initial_quiz', {}).get('completed', False)}")
        return user_progress
    
    @staticmethod
    def update_progress(username: str, category: str, data: Dict):
        """Update specific category of user progress"""
        progress = DataManager._load_json(PROGRESS_FILE)
        if username not in progress:
            DataManager.init_user_progress(username)
            progress = DataManager._load_json(PROGRESS_FILE)
        
        if category in progress[username]:
            progress[username][category].update(data)
        else:
            progress[username][category] = data
        
        progress[username]["last_active"] = datetime.now().isoformat()
        DataManager._save_json(PROGRESS_FILE, progress)
    
    @staticmethod
    def save_quiz_results(username: str, quiz_type: str, score: int, total: int, 
                         weak_topics: List[str], strong_topics: List[str]):
        """Save quiz results"""
        # Use Supabase if available
        if USE_SUPABASE:
            try:
                print(f"💾 Attempting Supabase save: {username} - {quiz_type}")
                SupabaseDataManager.save_quiz_results(username, quiz_type, score, total, weak_topics, strong_topics)
                print(f"✅ Saved to Supabase: {username} - {quiz_type}")
                return  # Success, don't fall back to JSON
            except Exception as e:
                print(f"❌ Supabase save failed: {e}")
        
        # JSON fallback (always save to JSON too for safety)
        progress = DataManager._load_json(PROGRESS_FILE)
        if username not in progress:
            DataManager.init_user_progress(username)
            progress = DataManager._load_json(PROGRESS_FILE)
        
        quiz_data = {
            "completed": True,
            "score": score,
            "total": total,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "date": datetime.now().isoformat()
        }
        
        if quiz_type == "initial":
            progress[username]["initial_quiz"] = quiz_data
        else:
            progress[username]["lesson_quizzes"][quiz_type] = quiz_data
        
        # Update overall progress
        quiz_completed = progress[username].get("initial_quiz", {}).get("completed", False)
        lessons_completed = len([l for l in progress[username].get("lessons", {}).values() if l.get("completed")])
        practice_done = len(progress[username].get("practice_problems", {}))
        
        # Calculate overall progress (quiz 20%, lessons 60%, practice 20%)
        overall = 0
        if quiz_completed:
            overall += 20
        overall += (lessons_completed / 6) * 60 if lessons_completed > 0 else 0
        overall += (practice_done / 10) * 20 if practice_done > 0 else 0
        
        progress[username]["overall_progress"] = int(overall)
        print(f"📊 Quiz Progress Update: Quiz={quiz_completed}, Lessons={lessons_completed}/6, Practice={practice_done}/10 → Overall={int(overall)}%")
        
        DataManager._save_json(PROGRESS_FILE, progress)
        print(f"✅ Saved to JSON: {username} - Quiz completed: {quiz_data['completed']}")
    
    @staticmethod
    def save_lesson_progress(username: str, lesson_id: str, completed: bool, time_spent: int):
        """Save lesson completion progress"""
        # Use Supabase if available
        if USE_SUPABASE:
            try:
                print(f"💾 Attempting Supabase lesson save: {username} - {lesson_id}")
                SupabaseDataManager.save_lesson_progress(username, lesson_id, completed, time_spent)
                print(f"✅ Saved to Supabase: {username} - Lesson {lesson_id}")
                return  # Success, don't fall back to JSON
            except Exception as e:
                print(f"❌ Supabase lesson save failed: {e}")
        
        # JSON fallback (always save to JSON too for safety)
        progress = DataManager._load_json(PROGRESS_FILE)
        if username not in progress:
            DataManager.init_user_progress(username)
            progress = DataManager._load_json(PROGRESS_FILE)
        
        progress[username]["lessons"][lesson_id] = {
            "completed": completed,
            "time_spent": time_spent,
            "date": datetime.now().isoformat()
        }
        
        progress[username]["total_time_spent"] += time_spent
        
        # Update overall progress
        quiz_completed = progress[username].get("initial_quiz", {}).get("completed", False)
        lessons_completed = len([l for l in progress[username].get("lessons", {}).values() if l.get("completed")])
        practice_done = len(progress[username].get("practice_problems", {}))
        
        # Calculate overall progress (quiz 20%, lessons 60%, practice 20%)
        overall = 0
        if quiz_completed:
            overall += 20
        overall += (lessons_completed / 6) * 60 if lessons_completed > 0 else 0
        overall += (practice_done / 10) * 20 if practice_done > 0 else 0
        
        progress[username]["overall_progress"] = int(overall)
        print(f"📊 Progress Update: Quiz={quiz_completed}, Lessons={lessons_completed}/6, Practice={practice_done}/10 → Overall={int(overall)}%")
        
        DataManager._save_json(PROGRESS_FILE, progress)
    
    @staticmethod
    def award_badge(username: str, badge_name: str, badge_description: str):
        """Award a badge to user"""
        # Use Supabase if available
        if USE_SUPABASE:
            try:
                SupabaseDataManager.award_badge(username, badge_name, badge_description)
                print(f"✅ Saved to Supabase: {username} - Badge: {badge_name}")
            except Exception as e:
                print(f"⚠️ Supabase save failed: {e}, falling back to JSON")
        
        # JSON fallback (always save to JSON too for safety)
        progress = DataManager._load_json(PROGRESS_FILE)
        if username not in progress:
            DataManager.init_user_progress(username)
            progress = DataManager._load_json(PROGRESS_FILE)
        
        # Check if badge already exists by name
        earned_badge_names = [b.get('name') for b in progress[username].get("badges", [])]
        if badge_name not in earned_badge_names:
            badge = {
                "name": badge_name,
                "description": badge_description,
                "date": datetime.now().isoformat()
            }
            progress[username]["badges"].append(badge)
            DataManager._save_json(PROGRESS_FILE, progress)
    
    @staticmethod
    def award_certificate(username: str, cert_name: str, cert_description: str):
        """Award a certificate to user"""
        progress = DataManager._load_json(PROGRESS_FILE)
        if username not in progress:
            DataManager.init_user_progress(username)
            progress = DataManager._load_json(PROGRESS_FILE)
        
        cert = {
            "name": cert_name,
            "description": cert_description,
            "date": datetime.now().isoformat()
        }
        
        if cert not in progress[username]["certificates"]:
            progress[username]["certificates"].append(cert)
            DataManager._save_json(PROGRESS_FILE, progress)
    
    @staticmethod
    def link_student_to_teacher(student_username: str, teacher_code: str) -> tuple:
        """
        Link a student to a teacher's class using teacher code
        Returns: (success: bool, message: str)
        """
        users = DataManager._load_json(USERS_FILE)
        
        # Check if student exists
        if student_username not in users:
            return False, "Student account not found"
        
        # Find teacher with this code
        teacher_username = None
        for username, user_data in users.items():
            if user_data.get('teacher_code') == teacher_code:
                teacher_username = username
                break
        
        if not teacher_username:
            return False, f"Teacher with code '{teacher_code}' not found"
        
        # Add teacher code to student's list
        if 'teacher_codes' not in users[student_username]:
            users[student_username]['teacher_codes'] = []
        
        if teacher_code in users[student_username]['teacher_codes']:
            return False, "Already enrolled in this class"
        
        users[student_username]['teacher_codes'].append(teacher_code)
        
        # Add student to teacher's class list (if field exists)
        if 'students' not in users[teacher_username]:
            users[teacher_username]['students'] = []
        
        if student_username not in users[teacher_username]['students']:
            users[teacher_username]['students'].append(student_username)
        
        DataManager._save_json(USERS_FILE, users)
        print(f"✅ Linked {student_username} to teacher {teacher_username} (code: {teacher_code})")
        
        return True, f"Successfully joined {teacher_username}'s class!"
    
    @staticmethod
    def link_parent_to_child(parent_username: str, child_share_code: str) -> tuple:
        """
        Link a parent to their child's account using share code
        Returns: (success: bool, message: str)
        """
        # Try Supabase first
        if USE_SUPABASE:
            try:
                return SupabaseDataManager.link_parent_to_child(parent_username, child_share_code)
            except Exception as e:
                print(f"⚠️ Supabase link failed, falling back to JSON: {e}")
        
        # JSON fallback
        users = DataManager._load_json(USERS_FILE)
        
        # Check if parent exists
        if parent_username not in users:
            return False, "Parent account not found"
        
        # Find child with this share code
        child_username = None
        for username, user_data in users.items():
            if user_data.get('share_code') == child_share_code:
                child_username = username
                break
        
        if not child_username:
            return False, f"Student with share code '{child_share_code}' not found"
        
        # Add child to parent's list
        if 'children' not in users[parent_username]:
            users[parent_username]['children'] = []
        
        if child_username in users[parent_username]['children']:
            return False, "Child already linked"
        
        users[parent_username]['children'].append(child_username)
        
        # Add parent code to child's list
        if 'parent_codes' not in users[child_username]:
            users[child_username]['parent_codes'] = []
        
        if parent_username not in users[child_username]['parent_codes']:
            users[child_username]['parent_codes'].append(parent_username)
        
        DataManager._save_json(USERS_FILE, users)
        print(f"✅ Linked {parent_username} to child {child_username} (code: {child_share_code})")
        
        return True, f"Successfully linked to {child_username}!"
    
    @staticmethod
    def get_teacher_students(teacher_username: str) -> List[str]:
        """Get list of students enrolled in teacher's class"""
        users = DataManager._load_json(USERS_FILE)
        teacher_data = users.get(teacher_username, {})
        return teacher_data.get('students', [])
    
    @staticmethod
    def get_all_students() -> List[str]:
        """Get list of all student usernames"""
        users = DataManager._load_json(USERS_FILE)
        return [username for username, data in users.items() if data["role"] == "Student"]
    
    @staticmethod
    def get_students_by_teacher_code(teacher_code: str) -> List[Dict]:
        """Get students who joined with a teacher's code"""
        users = DataManager._load_json(USERS_FILE)
        progress = DataManager._load_json(PROGRESS_FILE)
        
        students = []
        for username, user_data in users.items():
            if user_data["role"] == "Student" and teacher_code in user_data.get("teacher_codes", []):
                student_progress = progress.get(username, {})
                students.append({
                    "username": username,
                    "email": user_data["email"],
                    "progress": student_progress.get("overall_progress", 0),
                    "last_active": student_progress.get("last_active", "Never")
                })
        
        return students
    
    @staticmethod
    def get_children_by_parent_code(parent_share_codes: List[str]) -> List[Dict]:
        """Get children data for parent based on share codes"""
        users = DataManager._load_json(USERS_FILE)
        progress = DataManager._load_json(PROGRESS_FILE)
        
        children = []
        for username, user_data in users.items():
            if user_data["role"] == "Student" and user_data.get("share_code") in parent_share_codes:
                student_progress = progress.get(username, {})
                children.append({
                    "username": username,
                    "share_code": user_data.get("share_code"),
                    "progress": student_progress.get("overall_progress", 0),
                    "weak_topics": student_progress.get("initial_quiz", {}).get("weak_topics", []),
                    "strong_topics": student_progress.get("initial_quiz", {}).get("strong_topics", []),
                    "last_active": student_progress.get("last_active", "Never")
                })
        
        return children
