"""
ML Insights Dashboard - Showcases all machine learning features and predictions
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from data_manager import DataManager
from ml_features import (
    calculate_topic_confidence,
    get_adaptive_difficulty,
    calculate_learning_velocity,
    get_review_schedule,
    predict_final_score
)


def main():
    """Render ML Insights Dashboard"""
    
    # Check login
    if not st.session_state.get('logged_in', False):
        st.error("⛔ Please login to access ML Insights")
        st.stop()
    
    username = st.session_state.username
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🤖 ML Insights Dashboard")
        st.markdown("**Powered by Machine Learning** - Personalized analytics and predictions")
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("---")
    
    # Get user progress
    progress = DataManager.get_user_progress(username)
    
    # Section 1: Learning Velocity & Type
    st.markdown("## 📈 Learning Analytics")
    
    velocity, learner_type = calculate_learning_velocity(username)
    
    # Generate learner type explanation
    if learner_type == "Fast Learner":
        velocity_explanation = "🚀 You're progressing quickly! You master concepts faster than average and can handle accelerated pacing."
    elif learner_type == "Steady Learner":
        velocity_explanation = "🎯 You're making consistent, solid progress! Your steady pace ensures thorough understanding of concepts."
    else:
        velocity_explanation = "🐢 You're taking your time to really understand each concept. This methodical approach builds strong foundations!"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #6B8E23 0%, #556B2F 100%); 
                    padding: 30px; border-radius: 16px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 10px;">⚡</div>
            <div style="font-size: 36px; font-weight: 700; color: #FFFFFF;">{velocity:.1f}</div>
            <div style="font-size: 14px; color: #E0E0E0; margin-top: 5px;">Learning Velocity</div>
            <div style="font-size: 12px; color: #B3B3B3; margin-top: 8px;">Progress per hour</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        learner_emoji = "🚀" if learner_type == "Fast Learner" else "🎯" if learner_type == "Steady Learner" else "🐢"
        learner_color = "#6B8E23" if learner_type == "Fast Learner" else "#FFA500" if learner_type == "Steady Learner" else "#DC3545"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {learner_color} 0%, {learner_color}CC 100%); 
                    padding: 30px; border-radius: 16px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 10px;">{learner_emoji}</div>
            <div style="font-size: 20px; font-weight: 700; color: #FFFFFF;">{learner_type}</div>
            <div style="font-size: 12px; color: #E0E0E0; margin-top: 8px;">ML Classification</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        overall_progress = progress.get('overall_progress', 0)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #7BA428 0%, #6B8E23 100%); 
                    padding: 30px; border-radius: 16px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 10px;">📊</div>
            <div style="font-size: 36px; font-weight: 700; color: #FFFFFF;">{overall_progress}%</div>
            <div style="font-size: 14px; color: #E0E0E0; margin-top: 5px;">Overall Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Explanation box for learning velocity
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                padding: 15px; border-radius: 10px; border-left: 4px solid #6B8E23; margin-top: 20px;">
        <div style="font-size: 13px; color: #E0E0E0;">
            <strong style="color: #FFFFFF;">🤖 ML Analysis:</strong> {velocity_explanation}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Topic Confidence Scores
    st.markdown("## 🎯 Topic Confidence Analysis")
    st.markdown("*ML-calculated confidence based on accuracy, consistency, and time factors*")
    
    topics = ["Limit Definition", "Basic Rules", "Product Rule", "Chain Rule", "Implicit Diff.", "Applications"]
    
    col1, col2 = st.columns(2)
    
    for idx, topic in enumerate(topics):
        confidence = calculate_topic_confidence(username, topic)
        difficulty = get_adaptive_difficulty(username, topic)
        
        # Get topic-specific data for explanations
        quiz_data = progress.get('initial_quiz', {})
        weak_topics = quiz_data.get('weak_topics', [])
        strong_topics = quiz_data.get('strong_topics', [])
        
        # Determine color based on confidence
        if confidence >= 75:
            color = "#6B8E23"
            status = "Mastered"
            emoji = "🌟"
        elif confidence >= 50:
            color = "#FFA500"
            status = "Proficient"
            emoji = "📚"
        else:
            color = "#DC3545"
            status = "Needs Practice"
            emoji = "📖"
        
        # Difficulty badge color
        diff_color = "#2E7D32" if difficulty == "easy" else "#EF6C00" if difficulty == "medium" else "#C62828"
        
        # Generate explanation based on performance
        explanation = ""
        if topic in weak_topics:
            explanation = f"⚠️ Flagged as weak area in quiz - recommending {difficulty} difficulty to build foundation"
        elif topic in strong_topics:
            explanation = f"✅ Identified as strength in quiz - challenging you with {difficulty} difficulty"
        elif confidence < 50:
            explanation = f"📊 Low recent accuracy detected - using {difficulty} questions to rebuild confidence"
        elif confidence >= 75:
            explanation = f"🎯 Consistently strong performance - advancing to {difficulty} level"
        else:
            explanation = f"📈 Steady progress - maintaining {difficulty} difficulty for optimal learning"
        
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div style="background: #1E1E1E; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #2d2d2d;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <div style="font-size: 16px; font-weight: 600; color: #FFFFFF;">{emoji} {topic}</div>
                        <div style="font-size: 12px; color: #B3B3B3; margin-top: 3px;">{status}</div>
                    </div>
                    <div style="font-size: 28px; font-weight: 700; color: {color};">{confidence}%</div>
                </div>
                <div style="background: #2d2d2d; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: {color}; height: 100%; width: {confidence}%; transition: width 0.3s;"></div>
                </div>
                <div style="margin-top: 10px; font-size: 11px; color: #B3B3B3;">
                    <span style="background: {diff_color}; color: white; padding: 3px 8px; border-radius: 12px; font-weight: 600;">
                        Next: {difficulty.upper()}
                    </span>
                </div>
                <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-top: 10px; font-size: 11px; color: #B3B3B3; line-height: 1.5;">
                    <strong style="color: #FFFFFF;">🤖 Why this recommendation?</strong><br>
                    {explanation}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 3: Predictive Analytics
    st.markdown("## 🔮 Predictive Analytics")
    st.markdown("*Machine Learning prediction using Linear Regression on your progress data*")
    
    prediction = predict_final_score(username)
    
    # Generate prediction explanation
    predicted_score = prediction['predicted_score']
    factors = []
    
    quiz_data = progress.get('initial_quiz', {})
    if quiz_data.get('completed'):
        quiz_pct = (quiz_data.get('score', 0) / quiz_data.get('total', 18)) * 100
        if quiz_pct >= 80:
            factors.append("✅ Strong quiz performance (80%+)")
        elif quiz_pct < 60:
            factors.append("⚠️ Quiz performance below 60% - needs improvement")
        else:
            factors.append("📊 Moderate quiz performance")
    
    lessons_completed = len([l for l in progress.get('lessons', {}).values() if l.get('completed')])
    if lessons_completed >= 4:
        factors.append("✅ Good lesson completion rate")
    elif lessons_completed <= 2:
        factors.append("⚠️ Limited lesson completion - complete more lessons to improve prediction")
    
    time_spent = progress.get('total_time_spent', 0)
    if time_spent >= 180:
        factors.append("✅ Substantial time investment (3+ hours)")
    elif time_spent < 60:
        factors.append("⚠️ Limited time spent - more practice needed")
    
    prediction_explanation = f"Based on: {', '.join(factors)}" if factors else "Based on your current progress data"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        predicted_score = prediction['predicted_score']
        confidence_lower = prediction['confidence_lower']
        confidence_upper = prediction['confidence_upper']
        
        # Color based on prediction
        if predicted_score >= 85:
            pred_color = "#6B8E23"
            pred_emoji = "🎯"
        elif predicted_score >= 70:
            pred_color = "#FFA500"
            pred_emoji = "📈"
        else:
            pred_color = "#DC3545"
            pred_emoji = "⚠️"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {pred_color} 0%, {pred_color}CC 100%); 
                    padding: 30px; border-radius: 16px;">
            <div style="font-size: 18px; color: #E0E0E0; margin-bottom: 10px;">Predicted Final Test Score</div>
            <div style="display: flex; align-items: baseline;">
                <div style="font-size: 64px; font-weight: 900; color: #FFFFFF;">{predicted_score:.1f}</div>
                <div style="font-size: 32px; color: #E0E0E0; margin-left: 5px;">%</div>
                <div style="font-size: 28px; margin-left: 10px;">{pred_emoji}</div>
            </div>
            <div style="font-size: 14px; color: #E0E0E0; margin-top: 10px;">
                95% Confidence Interval: {confidence_lower:.1f}% - {confidence_upper:.1f}%
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 15px;">
                <div style="font-size: 13px; color: #FFFFFF; font-weight: 600;">ML Recommendation:</div>
                <div style="font-size: 13px; color: #E0E0E0; margin-top: 5px;">{prediction['recommendation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #1E1E1E; padding: 20px; border-radius: 12px; border: 1px solid #2d2d2d; height: 100%;">
            <div style="font-size: 16px; font-weight: 600; color: #FFFFFF; margin-bottom: 15px;">
                📊 Model Details
            </div>
            <div style="font-size: 13px; color: #B3B3B3; line-height: 1.8;">
                <div>• <strong>Algorithm:</strong> Linear Regression</div>
                <div>• <strong>R² Score:</strong> {prediction['r_squared']:.3f}</div>
                <div>• <strong>MAE:</strong> {prediction['mae']:.2f}</div>
                <div>• <strong>Features Used:</strong></div>
                <div style="margin-left: 15px; font-size: 12px;">
                    - Quiz scores<br>
                    - Lesson completion<br>
                    - Practice accuracy<br>
                    - Time spent<br>
                    - Topic performance
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Prediction explanation box
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(107,142,35,0.2) 0%, rgba(85,107,47,0.2) 100%); 
                padding: 15px; border-radius: 10px; border-left: 4px solid #6B8E23; margin-top: 20px;">
        <div style="font-size: 13px; color: #E0E0E0;">
            <strong style="color: #FFFFFF;">🤖 How we calculated this:</strong><br>
            {prediction_explanation}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 4: Spaced Repetition Schedule
    st.markdown("## 🔄 Spaced Repetition Schedule")
    st.markdown("*ML-powered review timing using SM-2 algorithm (similar to Anki)*")
    
    review_schedule = get_review_schedule(username)
    
    if review_schedule:
        st.markdown(f"**{len(review_schedule)} topics** due for review to optimize retention")
        
        for review in review_schedule[:5]:  # Show top 5
            days_overdue = review['days_overdue']
            urgency_color = "#DC3545" if days_overdue > 3 else "#FFA500" if days_overdue > 0 else "#6B8E23"
            
            st.markdown(f"""
            <div style="background: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 10px; 
                        border-left: 4px solid {urgency_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 15px; font-weight: 600; color: #FFFFFF;">{review['topic']}</div>
                        <div style="font-size: 12px; color: #B3B3B3; margin-top: 3px;">
                            Last reviewed: {review['last_reviewed']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 13px; color: {urgency_color}; font-weight: 600;">
                            {review['priority']}
                        </div>
                        <div style="font-size: 11px; color: #B3B3B3; margin-top: 3px;">
                            Next: {review['next_review']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎉 No topics due for review right now! Keep up the great work!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 5: ML Process Explanation
    with st.expander("🔬 How Our ML System Works", expanded=False):
        st.markdown("""
        ### Machine Learning Pipeline
        
        Our system uses multiple ML techniques to personalize your learning:
        
        **1. Topic Confidence Calculation**
        - Weighted combination of accuracy, consistency, and time factors
        - Penalizes recent mistakes more heavily
        - Accounts for forgetting curve
        
        **2. Adaptive Difficulty Selection**
        - Analyzes recent performance trends
        - Adjusts difficulty dynamically
        - Optimizes for challenge without overwhelming
        
        **3. Learning Velocity Tracking**
        - Calculates progress rate per hour
        - Classifies learner type (Fast/Steady/Gradual)
        - Helps adjust pacing recommendations
        
        **4. Predictive Analytics**
        - Linear Regression model
        - Features: quiz scores, lesson completion, practice accuracy, time spent
        - 95% confidence intervals for reliability
        
        **5. Spaced Repetition (SM-2 Algorithm)**
        - Scientifically proven method for retention
        - Schedules reviews based on difficulty and performance
        - Prevents forgetting with optimal timing
        
        **6. Real-time Adaptation**
        - All metrics update dynamically with each interaction
        - Recommendations evolve based on your progress
        - No manual intervention needed
        """)


if __name__ == "__main__":
    main()
