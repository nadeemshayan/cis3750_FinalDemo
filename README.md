# BrainyYack ITS - Intelligent Tutoring System

**ML-Powered Adaptive Learning Platform for Calculus Derivatives**

---

## 🚀 Quick Start

### Run Locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Deploy to Streamlit Cloud
1. Push to GitHub
2. Go to share.streamlit.io
3. Deploy from your repo
4. Add Supabase secrets (optional)

---

## 📁 Folder Structure

```
final_demo/
├── streamlit_app.py          # Main entry point
├── app_main.py                # Core app logic
├── data_manager.py            # Data layer (Supabase/JSON)
├── requirements.txt           # Python dependencies
│
├── .streamlit/
│   └── secrets.toml.example  # Supabase config template
│
├── assets/
│   └── logo.png              # App logo
│
├── components/
│   └── sidebar/              # Navigation sidebar
│
├── database/
│   ├── supabase_manager.py   # Supabase connector
│   ├── setup_supabase.sql    # Database schema
│   └── migrate_to_supabase.py
│
├── data/                      # Local JSON storage (fallback)
│   ├── users.json
│   └── progress.json
│
└── pages/                     # All app pages
    ├── auth/                  # Login, register, password reset
    ├── dashboard/             # Student, teacher, parent dashboards
    ├── quiz/                  # Quiz styling
    ├── initial_quiz.py        # Diagnostic assessment
    ├── lessons_enhanced.py    # Adaptive lessons
    ├── practice_problems.py   # Practice system
    ├── achievements.py        # Badges & achievements
    ├── progress_tracker.py    # Analytics
    └── final_test.py          # Final assessment
```

---

## 🔌 Database Options

### Option 1: Supabase (Cloud - Production)
1. Create project at supabase.com
2. Run `database/setup_supabase.sql`
3. Add secrets to Streamlit Cloud:
```toml
[supabase]
url = "https://your-project.supabase.co"
key = "your-anon-key"
```

### Option 2: JSON Files (Local - Development)
- No setup needed!
- App automatically uses `data/users.json` and `data/progress.json`
- Perfect for testing and demos

---

## ✨ Features

- ✅ User authentication (Student, Teacher, Parent)
- ✅ Adaptive initial quiz with shuffled answers
- ✅ Personalized lesson recommendations
- ✅ Badge & achievement system
- ✅ Progress tracking & analytics
- ✅ Practice problems
- ✅ Multi-role dashboards

---

## 📦 Requirements

- Python 3.8+
- Streamlit 1.28+
- Supabase (optional)

---

**Built by Group 11 - CIS3750**
