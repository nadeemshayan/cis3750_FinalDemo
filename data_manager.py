import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

# Try to use Supabase, fall back to JSON for local dev
USE_SUPABASE = True
try:
    from database.supabase_manager import SupabaseDataManager
except:
    USE_SUPABASE = False
    print("⚠️ Supabase not configured, using JSON fallback")

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
                    "total": 8,
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
            return SupabaseDataManager.get_user_progress(username)
        
        # JSON fallback
        progress_data = DataManager._load_json(PROGRESS_FILE)
        if username not in progress_data:
            DataManager.init_user_progress(username)
            progress_data = DataManager._load_json(PROGRESS_FILE)
        return progress_data.get(username, {})
    
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
                SupabaseDataManager.save_quiz_results(username, quiz_type, score, total, weak_topics, strong_topics)
                print(f"✅ Saved to Supabase: {username} - {quiz_type}")
            except Exception as e:
                print(f"⚠️ Supabase save failed: {e}, falling back to JSON")
        
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
        
        DataManager._save_json(PROGRESS_FILE, progress)
        print(f"✅ Saved to JSON: {username} - Quiz completed: {quiz_data['completed']}")
    
    @staticmethod
    def save_lesson_progress(username: str, lesson_id: str, completed: bool, time_spent: int):
        """Save lesson completion progress"""
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
        DataManager._save_json(PROGRESS_FILE, progress)
    
    @staticmethod
    def award_badge(username: str, badge_name: str, badge_description: str):
        """Award a badge to user"""
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
    def award_certificate(username: str, cert_name: str, course: str):
        """Award a certificate to user"""
        progress = DataManager._load_json(PROGRESS_FILE)
        if username not in progress:
            DataManager.init_user_progress(username)
            progress = DataManager._load_json(PROGRESS_FILE)
        
        certificate = {
            "name": cert_name,
            "course": course,
            "date": datetime.now().isoformat()
        }
        
        progress[username]["certificates"].append(certificate)
        DataManager._save_json(PROGRESS_FILE, progress)
    
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
