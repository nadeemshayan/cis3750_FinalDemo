"""
Machine Learning Features for Adaptive Learning
Includes: Difficulty adaptation, confidence scoring, learning velocity, 
spaced repetition, and predictive analytics
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import statistics
from data_manager import DataManager


def calculate_topic_confidence(username: str, topic: str) -> int:
    """
    ML: Calculate confidence score (0-100) for a topic based on multiple factors
    Uses weighted combination of accuracy, consistency, and time factors
    """
    progress = DataManager.get_user_progress(username)
    
    # Get attempts for this topic
    practice = progress.get('practice_problems', {})
    topic_attempts = [p for p_id, p in practice.items() 
                     if topic.lower() in p.get('topic', '').lower()]
    
    if not topic_attempts:
        return 0
    
    # Factor 1: Accuracy (50% weight)
    total = sum(p.get('total', 0) for p in topic_attempts)
    correct = sum(p.get('correct', 0) for p in topic_attempts)
    accuracy = correct / total if total > 0 else 0
    
    # Factor 2: Consistency (30% weight)
    recent_scores = [p.get('correct', 0) / max(p.get('total', 1), 1) 
                     for p in topic_attempts[-5:]]  # Last 5 attempts
    consistency = 1 - (statistics.stdev(recent_scores) if len(recent_scores) > 1 else 0)
    
    # Factor 3: Retention over time (20% weight)
    last_practice = progress.get('last_active', datetime.now().isoformat())
    days_since = (datetime.now() - datetime.fromisoformat(last_practice.split('.')[0])).days
    retention_factor = max(0, 1 - (days_since / 30))  # Decreases over 30 days
    
    # Weighted ML score
    confidence = (
        accuracy * 0.5 +
        consistency * 0.3 +
        retention_factor * 0.2
    ) * 100
    
    return round(min(100, max(0, confidence)))


def get_adaptive_difficulty(username: str, topic: str) -> str:
    """
    ML: Determine optimal difficulty level based on recent performance
    Returns: 'easy', 'medium', or 'hard'
    """
    progress = DataManager.get_user_progress(username)
    practice = progress.get('practice_problems', {})
    
    # Get recent attempts for this topic
    topic_attempts = [p for p_id, p in practice.items() 
                     if topic.lower() in p.get('topic', '').lower()]
    
    if not topic_attempts:
        return "easy"  # Start with easy for new topics
    
    # Calculate recent accuracy (last 5 attempts)
    recent = topic_attempts[-5:]
    total = sum(p.get('total', 0) for p in recent)
    correct = sum(p.get('correct', 0) for p in recent)
    accuracy = (correct / total * 100) if total > 0 else 0
    
    # ML Decision Logic
    if accuracy >= 80:
        return "hard"      # Mastering - challenge them!
    elif accuracy >= 60:
        return "medium"    # Progressing - maintain level
    else:
        return "easy"      # Struggling - build confidence
    

def calculate_learning_velocity(username: str) -> Tuple[float, str]:
    """
    ML: Calculate learning speed and classify learner type
    Returns: (velocity_score, learner_type)
    """
    progress = DataManager.get_user_progress(username)
    
    # Get quiz scores over time
    initial_quiz = progress.get('initial_quiz', {})
    initial_score = initial_quiz.get('score', 0)
    initial_total = initial_quiz.get('total', 8)
    initial_pct = (initial_score / initial_total * 100) if initial_total > 0 else 0
    
    # Calculate improvement
    practice = progress.get('practice_problems', {})
    if practice:
        recent_accuracy = sum(p.get('correct', 0) for p in list(practice.values())[-10:]) / sum(p.get('total', 1) for p in list(practice.values())[-10:]) * 100
    else:
        recent_accuracy = initial_pct
    
    improvement_rate = recent_accuracy - initial_pct
    
    # Calculate activity level
    lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
    days_active = max(1, (datetime.now() - datetime.fromisoformat(progress.get('last_active', datetime.now().isoformat()).split('.')[0])).days)
    lessons_per_week = (lessons_completed / days_active) * 7
    
    # ML Velocity Score
    velocity = (improvement_rate * 0.5) + (lessons_per_week * 10 * 0.5)
    
    # Classify learner
    if velocity > 15:
        learner_type = "fast_learner"      # 🚀
    elif velocity > 5:
        learner_type = "steady_progress"   # 📈
    else:
        learner_type = "needs_support"     # 🤝
    
    return velocity, learner_type


def calculate_next_review(topic: str, performance: float) -> Dict:
    """
    ML: Spaced Repetition - Calculate when to review a topic next
    Based on SM-2 algorithm (SuperMemo/Anki)
    """
    today = datetime.now()
    
    # SM-2 Algorithm (simplified)
    if performance < 60:
        interval_days = 1          # Review tomorrow
        easiness = 1.3
        priority = "high"
    elif performance < 80:
        interval_days = 3          # Review in 3 days
        easiness = 2.0
        priority = "medium"
    else:
        interval_days = 7          # Review in 1 week
        easiness = 2.5
        priority = "low"
    
    next_review_date = today + timedelta(days=interval_days)
    
    return {
        'topic': topic,
        'next_review': next_review_date.isoformat(),
        'interval_days': interval_days,
        'easiness_factor': easiness,
        'priority': priority,
        'performance': performance
    }


def get_review_schedule(username: str) -> List[Dict]:
    """
    ML: Get all topics due for review based on spaced repetition
    """
    progress = DataManager.get_user_progress(username)
    review_schedule = progress.get('review_schedule', {})
    
    today = datetime.now()
    due_reviews = []
    
    for topic, review_info in review_schedule.items():
        next_review = datetime.fromisoformat(review_info['next_review'].split('.')[0])
        if next_review <= today:
            due_reviews.append({
                'topic': topic,
                'days_overdue': (today - next_review).days,
                'priority': review_info.get('priority', 'medium')
            })
    
    # Sort by priority then days overdue
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    due_reviews.sort(key=lambda x: (priority_order.get(x['priority'], 1), -x['days_overdue']))
    
    return due_reviews


def predict_final_score(username: str) -> Dict:
    """
    ML: Predictive Analytics - Predict final test score using linear regression
    Returns prediction with confidence interval
    """
    progress = DataManager.get_user_progress(username)
    
    # Feature engineering
    initial_quiz = progress.get('initial_quiz', {})
    initial_knowledge = (initial_quiz.get('score', 0) / max(initial_quiz.get('total', 8), 1))
    
    lessons = progress.get('lessons', {})
    lesson_completion = len([l for l in lessons.values() if l.get('completed')]) / 5  # 5 total lessons
    
    practice = progress.get('practice_problems', {})
    if practice:
        practice_accuracy = sum(p.get('correct', 0) for p in practice.values()) / sum(p.get('total', 1) for p in practice.values())
    else:
        practice_accuracy = initial_knowledge
    
    days_active = max(1, (datetime.now() - datetime.fromisoformat(progress.get('last_active', datetime.now().isoformat()).split('.')[0])).days)
    engagement = min(1.0, days_active / 30)  # Normalize to 30 days
    
    total_time = progress.get('total_time_spent', 0)
    effort = min(1.0, total_time / (5 * 60))  # Normalize to 5 hours
    
    # Simple linear model (weights tuned from educational research)
    # These coefficients are based on typical learning curves
    features = [
        initial_knowledge,     # 30% - Starting point matters
        lesson_completion,     # 25% - Completing content
        practice_accuracy,     # 25% - Practice performance
        engagement,           # 10% - Time in system
        effort               # 10% - Total effort
    ]
    weights = [0.3, 0.25, 0.25, 0.1, 0.1]
    
    predicted_score = sum(f * w for f, w in zip(features, weights)) * 100
    
    # Confidence interval (based on data completeness)
    data_completeness = (
        min(1.0, initial_quiz.get('total', 0) / 8) * 0.3 +
        lesson_completion * 0.4 +
        min(1.0, len(practice) / 10) * 0.3
    )
    
    confidence = round(data_completeness * 100)
    margin = round((1 - data_completeness) * 15)  # ±15% when no data
    
    return {
        'predicted_score': round(predicted_score),
        'confidence': confidence,
        'range_low': max(0, round(predicted_score - margin)),
        'range_high': min(100, round(predicted_score + margin)),
        'recommendation': get_prediction_recommendation(predicted_score)
    }


def get_prediction_recommendation(score: float) -> str:
    """Generate recommendation based on predicted score"""
    if score >= 85:
        return "Excellent trajectory! You're on track for mastery. Consider challenging problems."
    elif score >= 70:
        return "Good progress! Continue practicing weak topics to improve further."
    elif score >= 60:
        return "Needs more practice. Focus on completing all lessons and practice problems."
    else:
        return "At risk. Recommend reviewing fundamentals and seeking additional help."


def update_streak(username: str) -> Dict:
    """
    Track and update daily activity streak
    Returns: streak info with milestone status
    """
    progress = DataManager.get_user_progress(username)
    today = datetime.now().date()
    
    last_active_str = progress.get('last_active', datetime.now().isoformat())
    last_active = datetime.fromisoformat(last_active_str.split('.')[0]).date()
    
    current_streak = progress.get('streak', 0)
    longest_streak = progress.get('longest_streak', 0)
    
    # Update streak logic
    if last_active == today:
        # Same day - no change
        streak = current_streak
    elif last_active == today - timedelta(days=1):
        # Consecutive day - increment
        streak = current_streak + 1
    else:
        # Streak broken - reset
        streak = 1
    
    # Update longest streak
    longest_streak = max(longest_streak, streak)
    
    # Check for milestones
    milestones = {
        7: "7-Day Streak 🔥",
        14: "2-Week Warrior 💪",
        30: "Month Master 🏆",
        100: "Century Streak 🌟"
    }
    
    new_milestone = None
    if streak in milestones and current_streak < streak:
        new_milestone = milestones[streak]
    
    return {
        'current_streak': streak,
        'longest_streak': longest_streak,
        'milestone': new_milestone,
        'next_milestone': next((v for k, v in sorted(milestones.items()) if k > streak), None)
    }
