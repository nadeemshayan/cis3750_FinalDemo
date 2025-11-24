"""
Migration script: JSON → Supabase
Run this once to migrate your existing data
"""

import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.supabase_manager import get_supabase_client


def migrate_data():
    """Migrate data from JSON files to Supabase"""
    
    print("🚀 Starting migration to Supabase...")
    
    # Load JSON data
    data_dir = Path(__file__).parent.parent / "data"
    users_file = data_dir / "users.json"
    progress_file = data_dir / "progress.json"
    
    if not users_file.exists() or not progress_file.exists():
        print("❌ JSON files not found!")
        return
    
    with open(users_file, 'r') as f:
        users = json.load(f)
    
    with open(progress_file, 'r') as f:
        progress_data = json.load(f)
    
    supabase = get_supabase_client()
    
    # Migrate users
    print("\n📥 Migrating users...")
    for username, user_data in users.items():
        try:
            # Convert arrays to JSON strings for insertion
            user_insert = {
                "username": username,
                "password": user_data.get("password"),
                "email": user_data.get("email"),
                "role": user_data.get("role"),
                "created_at": user_data.get("created_at"),
                "age_level": user_data.get("age_level"),
                "grade": user_data.get("grade", ""),
                "share_code": user_data.get("share_code", ""),
                "teacher_code": user_data.get("teacher_code", ""),
                "parent_codes": json.dumps(user_data.get("parent_codes", [])),
                "teacher_codes": json.dumps(user_data.get("teacher_codes", []))
            }
            
            supabase.table('users').insert(user_insert).execute()
            print(f"  ✅ Migrated user: {username}")
        except Exception as e:
            print(f"  ⚠️  Skipped {username} (may already exist): {e}")
    
    # Migrate progress
    print("\n📥 Migrating progress...")
    for username, prog in progress_data.items():
        try:
            progress_insert = {
                "username": username,
                "initial_quiz": json.dumps(prog.get("initial_quiz", {})),
                "lessons": json.dumps(prog.get("lessons", {})),
                "lesson_quizzes": json.dumps(prog.get("lesson_quizzes", {})),
                "practice_problems": json.dumps(prog.get("practice_problems", {})),
                "final_test": json.dumps(prog.get("final_test", {})),
                "badges": json.dumps(prog.get("badges", [])),
                "certificates": json.dumps(prog.get("certificates", [])),
                "total_time_spent": prog.get("total_time_spent", 0),
                "last_active": prog.get("last_active"),
                "current_level": prog.get("current_level", 1),
                "overall_progress": prog.get("overall_progress", 0)
            }
            
            supabase.table('progress').insert(progress_insert).execute()
            print(f"  ✅ Migrated progress: {username}")
        except Exception as e:
            print(f"  ⚠️  Skipped {username} (may already exist): {e}")
    
    print("\n🎉 Migration complete!")
    print("\n⚠️  IMPORTANT: Test the app, then you can delete the /data folder")


if __name__ == "__main__":
    migrate_data()
