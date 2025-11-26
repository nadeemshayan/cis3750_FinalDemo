"""
Generate Demo Class Data
Creates a teacher account with 30 demo students with varied performance
"""
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from data_manager import DataManager

# Demo teacher credentials
DEMO_TEACHER = {
    'username': 'demo_teacher',
    'password': 'teacher123',
    'email': 'teacher@demo.com',
    'role': 'Teacher',
    'teacher_code': 'DEMO-TEACH'
}

# Common first and last names for generating realistic student names
FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'William', 'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia',
    'Lucas', 'Harper', 'Henry', 'Evelyn', 'Alexander', 'Abigail', 'Michael',
    'Emily', 'Daniel', 'Elizabeth', 'Matthew', 'Sofia', 'Jackson', 'Avery', 'Sebastian'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
    'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson'
]

# Calculus topics from quiz
TOPICS = [
    "Limit Definition",
    "Basic Rules", 
    "Product Rule",
    "Chain Rule",
    "Implicit Diff.",
    "Applications",
    "Quotient Rule"
]

def generate_student_name():
    """Generate a random student name"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first}_{last}".lower()

def generate_email(name):
    """Generate email from name"""
    return f"{name}@student.demo.com"

def create_demo_teacher():
    """Create demo teacher account"""
    print("Creating demo teacher account...")
    success, msg = DataManager.register_user(
        DEMO_TEACHER['username'],
        DEMO_TEACHER['password'],
        DEMO_TEACHER['email'],
        DEMO_TEACHER['role'],
        teacher_code=DEMO_TEACHER['teacher_code']
    )
    
    if success or "already exists" in msg:
        print(f"✓ Demo teacher ready: {DEMO_TEACHER['username']} (Code: {DEMO_TEACHER['teacher_code']})")
        return True
    else:
        print(f"✗ Failed to create teacher: {msg}")
        return False

def create_demo_student(performance_level='medium'):
    """
    Create a demo student with realistic data
    performance_level: 'high', 'medium', or 'low'
    """
    # Generate unique name
    max_attempts = 50
    for _ in range(max_attempts):
        name = generate_student_name()
        if not DataManager.get_user(name):
            break
    else:
        # If we can't find unique name, add number
        name = f"{generate_student_name()}{random.randint(1, 999)}"
    
    email = generate_email(name)
    password = 'demo123'
    
    # Register student
    success, msg = DataManager.register_user(
        name,
        password,
        email,
        'Student',
        age_level='High School',
        grade=random.choice(['Grade 11', 'Grade 12']),
        teacher_codes=[DEMO_TEACHER['teacher_code']]
    )
    
    if not success:
        print(f"  ✗ Failed to create {name}: {msg}")
        return None
    
    # Generate performance data based on level
    if performance_level == 'high':
        quiz_score = random.randint(7, 8)  # 7-8 out of 8
        quiz_total = 8
        overall_progress = random.randint(70, 95)
        lessons_completed = random.randint(4, 6)
        total_time = random.randint(180, 360)  # 3-6 hours
        weak_topics = random.sample(TOPICS, k=random.randint(0, 1))
        strong_topics = random.sample(TOPICS, k=random.randint(3, 5))
        practice_attempts = random.randint(15, 30)
        practice_accuracy = random.uniform(0.75, 0.95)
    
    elif performance_level == 'low':
        quiz_score = random.randint(2, 4)  # 2-4 out of 8
        quiz_total = 8
        overall_progress = random.randint(10, 35)
        lessons_completed = random.randint(0, 2)
        total_time = random.randint(30, 120)  # 30min-2hours
        weak_topics = random.sample(TOPICS, k=random.randint(3, 5))
        strong_topics = random.sample(TOPICS, k=random.randint(0, 1))
        practice_attempts = random.randint(3, 10)
        practice_accuracy = random.uniform(0.25, 0.50)
    
    else:  # medium
        quiz_score = random.randint(5, 6)  # 5-6 out of 8
        quiz_total = 8
        overall_progress = random.randint(40, 70)
        lessons_completed = random.randint(2, 4)
        total_time = random.randint(120, 240)  # 2-4 hours
        weak_topics = random.sample(TOPICS, k=random.randint(1, 3))
        strong_topics = random.sample(TOPICS, k=random.randint(1, 3))
        practice_attempts = random.randint(10, 20)
        practice_accuracy = random.uniform(0.50, 0.75)
    
    # Save quiz results
    DataManager.save_quiz_results(
        name,
        "initial",
        quiz_score,
        quiz_total,
        weak_topics,
        strong_topics
    )
    
    # Update overall progress
    progress = DataManager.get_user_progress(name)
    progress['overall_progress'] = overall_progress
    progress['total_time_spent'] = total_time
    
    # Add lesson completion data
    lesson_ids = ['limit_definition', 'basic_rules', 'product_rule', 'chain_rule', 'quotient_rule', 'implicit_diff']
    for i in range(lessons_completed):
        if i < len(lesson_ids):
            progress['lessons'][lesson_ids[i]] = {
                'completed': True,
                'score': random.randint(70, 100),
                'time_spent': random.randint(15, 45),
                'timestamp': (datetime.now() - timedelta(days=random.randint(1, 14))).isoformat()
            }
    
    # Add practice problems
    for i in range(practice_attempts):
        topic = random.choice(TOPICS)
        is_correct = random.random() < practice_accuracy
        problem_id = f"practice_{i}_{random.randint(1000, 9999)}"
        
        progress['practice_problems'][problem_id] = {
            'topic': topic,
            'correct': 1 if is_correct else 0,
            'total': 1,
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 14))).isoformat(),
            'time_spent': random.randint(2, 10)
        }
    
    # Update last active
    progress['last_active'] = (datetime.now() - timedelta(days=random.randint(0, 3))).isoformat()
    
    # Save progress
    DataManager.save_user_progress(name, progress)
    
    # Award badges based on performance
    if quiz_score >= 6:
        DataManager.award_badge(name, "Quiz Master 🎯", "Scored 75% or higher on initial quiz")
    else:
        DataManager.award_badge(name, "Quiz Starter 📝", "Completed initial quiz")
    
    if lessons_completed >= 3:
        DataManager.award_badge(name, "Learning Enthusiast 📚", "Completed 3+ lessons")
    
    if practice_attempts >= 15:
        DataManager.award_badge(name, "Practice Champion 💪", "Attempted 15+ practice problems")
    
    return {
        'username': name,
        'performance': performance_level,
        'quiz_score': f"{quiz_score}/{quiz_total}",
        'progress': f"{overall_progress}%"
    }

def create_demo_parent(student_username):
    """Create a parent account linked to a student"""
    parent_name = f"parent_of_{student_username}"
    email = f"{parent_name}@parent.demo.com"
    password = 'demo123'
    
    # Register parent
    success, msg = DataManager.register_user(
        parent_name,
        password,
        email,
        'Parent',
        age_level='Adult'
    )
    
    if not success and "already exists" not in msg:
        return None
    
    # Link to student
    result = DataManager.link_parent_to_child(parent_name, student_username)
    
    return {
        'username': parent_name,
        'linked_child': student_username
    }

def generate_demo_class():
    """Generate complete demo class with 30 students"""
    print("\n" + "="*60)
    print("GENERATING DEMO CLASS DATA")
    print("="*60 + "\n")
    
    # Create teacher
    if not create_demo_teacher():
        return
    
    print(f"\nCreating 30 demo students...")
    print("-" * 60)
    
    students_created = []
    parents_created = []
    
    # Create distribution: 8 high, 17 medium, 5 low performers
    performance_distribution = (
        ['high'] * 8 +
        ['medium'] * 17 +
        ['low'] * 5
    )
    random.shuffle(performance_distribution)
    
    for i, perf_level in enumerate(performance_distribution, 1):
        student = create_demo_student(perf_level)
        if student:
            students_created.append(student)
            icon = "🌟" if perf_level == "high" else "📚" if perf_level == "medium" else "📖"
            print(f"{i:2d}. {icon} {student['username']:20s} | {student['performance']:6s} | Quiz: {student['quiz_score']} | Progress: {student['progress']}")
            
            # Create parent for some students (about 50%)
            if random.random() < 0.5:
                parent = create_demo_parent(student['username'])
                if parent:
                    parents_created.append(parent)
    
    print("-" * 60)
    print(f"\n✓ Successfully created {len(students_created)} students!\n")
    print(f"✓ Created {len(parents_created)} parent accounts!\n")
    
    # Summary
    print("="*60)
    print("DEMO CLASS SUMMARY")
    print("="*60)
    print(f"\n📧 Teacher Login:")
    print(f"   Username: {DEMO_TEACHER['username']}")
    print(f"   Password: {DEMO_TEACHER['password']}")
    print(f"   Teacher Code: {DEMO_TEACHER['teacher_code']}")
    print(f"\n👥 Students: {len(students_created)}")
    print(f"   🌟 High Performers: {sum(1 for s in students_created if s['performance'] == 'high')}")
    print(f"   📚 Medium Performers: {sum(1 for s in students_created if s['performance'] == 'medium')}")
    print(f"   📖 Low Performers: {sum(1 for s in students_created if s['performance'] == 'low')}")
    print(f"\n� Parents: {len(parents_created)}")
    if parents_created:
        print(f"   Example: {parents_created[0]['username']}")
    print(f"\n💡 All accounts use password: demo123")
    print(f"💡 Parent usernames: parent_of_[student_name]")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    generate_demo_class()
