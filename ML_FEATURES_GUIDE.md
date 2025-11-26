# Machine Learning Features Guide

## Overview
BrainyYack incorporates multiple ML algorithms to personalize the learning experience. This guide documents all ML features and where they're visible in the UI.

---

## 🤖 ML Features Implemented

### 1. **Topic Confidence Calculation**
**Location**: `ml_features.py::calculate_topic_confidence()`

**Algorithm**: Weighted confidence scoring
- **Accuracy weight**: 40% - Recent quiz/practice performance
- **Consistency weight**: 30% - Performance variance over time
- **Time factor**: 20% - Recent vs old attempts (forgetting curve)
- **Recency bias**: 10% - Penalizes old mistakes less

**UI Display**:
- 🎯 **ML Insights Dashboard** - Shows confidence % for each topic with color-coded progress bars
- 📊 Student Dashboard - Topic focus areas

---

### 2. **Adaptive Difficulty Selection**
**Location**: `ml_features.py::get_adaptive_difficulty()`

**Algorithm**: Performance-based difficulty adjustment
- Analyzes last 5 attempts per topic
- Returns: 'easy', 'medium', or 'hard'
- Logic:
  - 80%+ accuracy → Hard questions
  - 60-80% accuracy → Medium questions
  - <60% accuracy → Easy questions

**UI Display**:
- 🎯 **ML Insights Dashboard** - "Next: EASY/MEDIUM/HARD" badges for each topic
- 📝 **Lesson Quizzes** - Adaptively selects questions based on past performance

---

### 3. **Learning Velocity Tracking**
**Location**: `ml_features.py::calculate_learning_velocity()`

**Algorithm**: Progress rate calculation
- Velocity = Overall Progress / Total Time Spent (hours)
- Classification:
  - **Fast Learner**: velocity > 15
  - **Steady Learner**: velocity 8-15
  - **Gradual Learner**: velocity < 8

**UI Display**:
- 🎯 **ML Insights Dashboard** - Large velocity score with learner type classification
- Icons: 🚀 Fast / 🎯 Steady / 🐢 Gradual

---

### 4. **Spaced Repetition (SM-2 Algorithm)**
**Location**: `ml_features.py::calculate_next_review()`

**Algorithm**: SuperMemo-2 algorithm (used by Anki)
- Calculates optimal review intervals based on:
  - Ease Factor (2.5 default, adjusted by performance)
  - Repetition number
  - Previous interval
- Formula: `interval = previous_interval * ease_factor`

**UI Display**:
- 🎯 **ML Insights Dashboard** - "Spaced Repetition Schedule" section
- Shows topics due for review with:
  - Days overdue (color-coded: red > orange > green)
  - Last reviewed date
  - Next review date
  - Priority level (High/Medium/Low)

---

### 5. **Predictive Analytics (Linear Regression)**
**Location**: `ml_features.py::predict_final_score()`

**Algorithm**: Scikit-learn Linear Regression
- **Features**:
  1. Quiz percentage
  2. Lessons completed percentage
  3. Practice accuracy
  4. Time investment (hours)
  5. Strong topics count
  6. Weak topics count

- **Output**:
  - Predicted final test score
  - 95% confidence interval
  - Model metrics (R², MAE)

**UI Display**:
- 🎯 **ML Insights Dashboard** - Large prediction card showing:
  - Predicted score (color-coded)
  - Confidence interval range
  - ML recommendation text
  - Model details (algorithm, R² score, MAE)

---

### 6. **Personalized Lesson Recommendations**
**Location**: `ml_features.py::get_recommended_lesson()` (used in `lessons_enhanced.py`)

**Algorithm**: Topic-based matching
- Analyzes weak topics from initial quiz
- Matches to lesson topics
- Prioritizes prerequisites

**UI Display**:
- 📚 **Lessons Page** - "🤖 AI-Recommended Lesson" section at top
- Green gradient box explaining ML analysis
- Shows which weak topics the lesson addresses

---

### 7. **Real-time Activity Tracking**
**Location**: `ml_features.py::update_streak()`

**Algorithm**: Daily activity tracking
- Tracks consecutive days active
- Milestone detection (7, 30, 100 days)
- Longest streak recording

**UI Display**:
- 📊 Student Dashboard - Streak counter
- 🏆 Achievements - Streak-based badges

---

## 🎨 ML Features in the UI

### Main Dashboard (Student)
```
┌─────────────────────────────────────────┐
│ Hey username! 👋                        │
│ Ready to master derivatives with        │
│ ML-powered tutoring?                    │
├─────────────────────────────────────────┤
│ [Quick Actions]                         │
│ 📝 Quiz  📚 Lessons  ✏️ Practice  🤖 ML │
└─────────────────────────────────────────┘
```

### ML Insights Dashboard (`/ml_insights`)
```
┌─────────────────────────────────────────┐
│ 🤖 ML Insights Dashboard                │
│ Powered by Machine Learning             │
├─────────────────────────────────────────┤
│ 📈 Learning Analytics                   │
│ [Velocity] [Learner Type] [Progress]    │
├─────────────────────────────────────────┤
│ 🎯 Topic Confidence Analysis            │
│ [6 topics with confidence bars]         │
│ Each shows: confidence %, status,       │
│              next difficulty level       │
├─────────────────────────────────────────┤
│ 🔮 Predictive Analytics                 │
│ [Predicted Score] [Model Details]       │
│ Shows Linear Regression prediction      │
├─────────────────────────────────────────┤
│ 🔄 Spaced Repetition Schedule          │
│ [Topics due for review]                 │
│ SM-2 algorithm timing                   │
└─────────────────────────────────────────┘
```

### Lessons Page (`/lessons`)
```
┌─────────────────────────────────────────┐
│ 🤖 AI-Recommended Lesson                │
│ ┌─────────────────────────────────────┐ │
│ │ 🤖 ML Analysis: Based on quiz       │ │
│ │ ⭐ [Lesson Title]                   │ │
│ │ Targets your areas for improvement  │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Lesson Quizzes (`/lesson_quizzes`)
```
┌─────────────────────────────────────────┐
│ 🤖 ML-Adaptive Quiz:                    │
│ This quiz intelligently selects 5       │
│ questions based on your performance     │
├─────────────────────────────────────────┤
│ After submission:                       │
│ ┌─────────────────────────────────────┐ │
│ │ 🤖 ML Insights:                     │ │
│ │ [Difficulty trend analysis]         │ │
│ │ [Next steps recommendation]         │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 📊 ML Data Flow

```
User Action → DataManager → Progress Storage (Supabase/JSON)
                                    ↓
                            ML Features Module
                            ├─ calculate_topic_confidence()
                            ├─ get_adaptive_difficulty()
                            ├─ calculate_learning_velocity()
                            ├─ predict_final_score()
                            └─ get_review_schedule()
                                    ↓
                            UI Components
                            ├─ ML Insights Dashboard
                            ├─ Lesson Recommendations
                            ├─ Adaptive Quizzes
                            └─ Progress Tracking
```

---

## 🚀 Accessing ML Features

### For Students:
1. **Quick Access**: Click "🤖 ML Insights" button on dashboard
2. **In Lessons**: See AI-recommended lesson at top based on weak topics
3. **In Quizzes**: Adaptive question selection message shown
4. **In Results**: ML analysis of performance trends

### For Teachers:
1. **Student Analytics Page**: ML-powered risk assessment
2. **Class Insights**: Aggregate ML predictions
3. **Individual Reports**: Per-student ML metrics

---

## 🔧 Technical Stack

- **Python Libraries**:
  - `numpy` - Numerical computations
  - `scikit-learn` - Linear Regression model
  - Custom algorithms for confidence, velocity, and spaced repetition

- **Data Sources**:
  - Initial quiz results
  - Lesson completion data
  - Practice problem performance
  - Time spent metrics

- **Storage**:
  - Supabase (primary)
  - JSON fallback
  - Real-time updates

---

## 💡 Future ML Enhancements

1. **Deep Learning Models**: Neural networks for more accurate predictions
2. **Collaborative Filtering**: Recommend based on similar students
3. **Natural Language Processing**: Analyze written responses
4. **Computer Vision**: Evaluate hand-written work
5. **Reinforcement Learning**: Optimize quiz difficulty in real-time

---

## 📚 References

- SM-2 Algorithm: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
- Spaced Repetition: https://en.wikipedia.org/wiki/Spaced_repetition
- Linear Regression: https://scikit-learn.org/stable/modules/linear_model.html
- Adaptive Learning: https://en.wikipedia.org/wiki/Adaptive_learning
