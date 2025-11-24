# 🧠 BrainyYack - Intelligent Tutoring System

**An ML-Powered Adaptive Learning Platform for Calculus Derivatives**

[![Status](https://img.shields.io/badge/status-demo%20ready-success)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Group 11 - CIS3750 F25**
> Muskan Manwani • Ainsley Williams • Shayan Nadeem • Shaun Chua • Dominic Szymanski • Oliver Catania • Rajin Uddin Al-Faiz

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Architecture](#architecture)
- [Testing](#testing)
- [Demo Guide](#demo-guide)
- [Contributing](#contributing)

---

## 🎯 Overview

BrainyYack is an intelligent tutoring system that revolutionizes how students learn calculus derivatives through:

- **🎯 Adaptive Learning**: Personalized lesson recommendations based on quiz performance
- **🎮 Gamification**: Badges, points, and achievements to maintain engagement
- **👥 Multi-Role Platform**: Separate interfaces for students, teachers, and parents
- **📊 Data-Driven Insights**: Comprehensive analytics and progress tracking
- **🎨 Modern UI**: Clean, professional dark-mode interface

### The Problem We Solve

Traditional math education is **one-size-fits-all**. Students struggle with:
- Generic content that doesn't match their level
- Lack of immediate feedback
- No tracking of weak areas
- Boring, unmotivating interfaces

### Our Solution

BrainyYack provides:
- ✅ **Personalized learning paths** based on individual performance
- ✅ **Instant feedback** on every answer
- ✅ **Automatic weak topic identification** with targeted practice
- ✅ **Engaging gamified experience** that motivates learning

---

## ✨ Features

### For Students

#### 🔍 Initial Assessment
- 8-question diagnostic quiz covering 6 core topics
- Randomized answer choices (prevents cheating)
- Hint system for guidance
- Skip functionality for flexibility
- Immediate results with explanations

#### 📚 Adaptive Lessons
- Lessons recommended based on weak areas
- Progressive difficulty
- Interactive content
- Time tracking
- Completion badges

#### ✏️ Practice System
- Problems prioritized by weak topics
- Immediate feedback
- Detailed explanations
- Progress tracking

#### 🏆 Gamification
- **Badges**: Welcome Aboard, Quiz Master, Lesson Master, Practice Warrior
- **Points System**: Earn points for achievements
- **Progress Tracking**: Visual indicators of completion

#### 📊 Analytics
- Overall progress percentage
- Topic mastery breakdown
- Time spent learning
- Badges earned
- Weak vs strong topics

### For Teachers

#### 👥 Class Management
- View all students
- Individual student analytics
- Class-wide performance metrics
- Common struggle topics

#### 📈 Analytics Dashboard
- Student engagement levels
- Average scores
- Time spent per topic
- Lesson completion rates
- Exportable reports

#### 🎯 Insights
- Identify at-risk students
- Recommend interventions
- Track improvement over time

### For Parents

#### 👶 Child Monitoring
- Link children via share codes
- View progress in real-time
- See weak/strong topics
- Track time spent
- Achievement milestones

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/cis3750-f25/project-setup-group-11.git
cd final_demo
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run streamlit_app.py
```

4. **Access the app**
```
Open browser to: http://localhost:8501
```

### First Time Setup

**Create a Student Account:**
1. Click "Create account"
2. Fill in details
3. Select "Student" role
4. Register
5. Login

**Start Learning:**
1. Take Initial Quiz
2. View Results
3. Check Recommended Lessons
4. Begin Learning!

---

## 📚 Documentation

Comprehensive guides available:

### Core Documentation
- **[QUICK_START.md](QUICK_START.md)** - Get running in 1 minute
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Complete testing procedures
- **[DEMO_READINESS_REPORT.md](DEMO_READINESS_REPORT.md)** - Demo preparation
- **[IMPROVEMENTS_CHECKLIST.md](IMPROVEMENTS_CHECKLIST.md)** - Future enhancements

### Quick References
- **Setup**: See [QUICK_START.md](QUICK_START.md)
- **Testing**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Demo Prep**: See [DEMO_READINESS_REPORT.md](DEMO_READINESS_REPORT.md)

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Streamlit 1.28+ (UI framework)
- Custom CSS (styling)
- Plotly & Altair (charts)

**Backend:**
- Python 3.8+
- Pandas & NumPy (data processing)
- Supabase Client (database)

**Database:**
- Supabase (PostgreSQL) - Production
- JSON Files - Development/Fallback

### Project Structure
```
final_demo/
├── streamlit_app.py          # Main entry point
├── app_main.py                # Core application logic
├── data_manager.py            # Data persistence layer
├── requirements.txt           # Python dependencies
│
├── .streamlit/
│   ├── secrets.toml          # Supabase credentials (DO NOT COMMIT)
│   └── secrets.toml.example  # Template for secrets
│
├── assets/
│   └── logo.png              # App logo
│
├── components/
│   └── sidebar/
│       └── __init__.py       # Navigation sidebar
│
├── database/
│   ├── setup_supabase.sql    # Database schema
│   ├── supabase_manager.py   # Supabase data manager
│   └── migrate_to_supabase.py # Migration script
│
├── pages/
│   ├── auth/                 # Authentication pages
│   │   ├── login.py
│   │   ├── register.py
│   │   └── forgot_password.py
│   │
│   ├── dashboard/            # Role-specific dashboards
│   │   ├── student.py
│   │   ├── teacher.py
│   │   └── parent.py
│   │
│   ├── initial_quiz.py       # Diagnostic quiz
│   ├── lessons_enhanced.py   # Adaptive lessons
│   ├── practice_problems.py  # Practice system
│   ├── achievements.py       # Badges & certificates
│   └── progress_tracker.py   # Analytics
│
├── data/                     # JSON fallback storage
│   ├── users.json
│   └── progress.json
│
└── docs/                     # Documentation
    ├── TESTING_GUIDE.md
    ├── QUICK_START.md
    └── DEMO_READINESS_REPORT.md
```

### Data Flow

```
User Input → Streamlit UI → Data Manager → Database (Supabase/JSON) → Storage
                                ↓
                         ML Logic (Adaptive)
                                ↓
                    Recommendations → UI Updates
```

### Database Schema

**Users Table:**
- id, username, password (hashed), email, role
- age_level, grade, share_code, teacher_code
- parent_codes, teacher_codes, created_at

**Progress Table:**
- id, username (FK)
- initial_quiz (JSONB)
- lessons (JSONB)
- lesson_quizzes (JSONB)
- practice_problems (JSONB)
- final_test (JSONB)
- badges (JSONB)
- certificates (JSONB)
- total_time_spent, last_active
- current_level, overall_progress

---

## 🧪 Testing

### Run Full Test Suite

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing procedures.

### Quick Test (5 Minutes)

1. **Start app**: `streamlit run streamlit_app.py`
2. **Register** student account
3. **Take** initial quiz (intentionally get some wrong)
4. **Check** badges unlocked
5. **View** dashboard recommendations
6. **Verify** data persists after refresh

### Critical Checks

- [ ] Quiz answers are shuffled
- [ ] No HTML tags in explanations
- [ ] Colors are olive green (#6B8E23)
- [ ] Badges unlock properly
- [ ] Progress saves
- [ ] Home buttons present

---

## 🎬 Demo Guide

### Perfect 10-Minute Demo

**Minutes 0-2: Introduction**
- Introduce problem (one-size-fits-all education)
- Present solution (adaptive learning)

**Minutes 2-5: Student Journey**
- Register account → Get badge
- Take quiz → Show shuffled answers
- View results → Weak topics identified
- Dashboard → Personalized recommendations

**Minutes 5-8: Key Features**
- Adaptive lessons
- Gamification system
- Progress tracking
- Analytics dashboard

**Minutes 8-10: Stakeholder Views**
- Teacher analytics
- Parent monitoring
- Multi-role platform value

**Conclusion:**
- Recap key benefits
- Future roadmap
- Q&A

### Demo Tips

✅ **DO:**
- Prepare test accounts beforehand
- Zoom browser to 125%
- Intentionally answer some questions wrong (shows adaptive features)
- Highlight the ML/adaptive aspects
- Show enthusiasm!

❌ **DON'T:**
- Create accounts during demo (takes time)
- Show error cases
- Dive too deep into technical details
- Apologize for missing features

---

## 🛠️ Configuration

### Supabase Setup (Production)

1. Create Supabase project at [supabase.com](https://supabase.com)
2. Run SQL from `database/setup_supabase.sql`
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
4. Add credentials:
```toml
[supabase]
url = "https://YOUR_PROJECT.supabase.co"
key = "YOUR_ANON_KEY"
```

### JSON Fallback (Development)

No configuration needed! App automatically uses JSON files in `data/` folder.

---

## 📊 Performance

- **Page Load**: < 2 seconds
- **Quiz Submit**: < 1 second
- **Database Save**: < 500ms
- **Memory**: ~150 MB
- **Concurrent Users**: Tested up to 10

---

## 🔒 Security

- ✅ Password hashing (SHA-256)
- ✅ Session-based authentication
- ✅ Input validation
- ✅ SQL injection protection (Supabase)
- ✅ No plaintext password storage
- ❌ Email verification (future feature)
- ❌ Rate limiting (future feature)

---

## 🐛 Known Issues

### Minor (Non-Blocking)
1. No loading states during operations
2. Not optimized for mobile
3. No email verification
4. Limited error messages

See [IMPROVEMENTS_CHECKLIST.md](IMPROVEMENTS_CHECKLIST.md) for full list.

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅ (COMPLETE)
- [x] User authentication
- [x] Initial quiz with adaptive logic
- [x] Lesson system
- [x] Badge system
- [x] Progress tracking
- [x] Multi-role support

### Phase 2: Enhancements (Next 3 Months)
- [ ] Spaced repetition algorithm
- [ ] Video lessons
- [ ] Mobile responsiveness
- [ ] Email notifications
- [ ] Advanced analytics

### Phase 3: Scale (6 Months)
- [ ] AI tutor chat
- [ ] LMS integration
- [ ] Multi-language support
- [ ] Mobile app

---

## 👥 Team

**Group 11 - CIS3750 F25**

| Name | Role | GitHub |
|------|------|--------|
| Muskan Manwani | Developer | [@Muskan-guelph](https://github.com/Muskan-guelph) |
| Ainsley Williams | Developer | [@Ainsley212](https://github.com/Ainsley212) |
| Shayan Nadeem | Developer | [@nadeemshayan](https://github.com/nadeemshayan) |
| Shaun Chua | Developer | [@Chuas9786](https://github.com/Chuas9786) |
| Dominic Szymanski | Developer | [@Szymand](https://github.com/Szymand) |
| Oliver Catania | Developer | [@0catania](https://github.com/0catania) |
| Rajin Uddin Al-Faiz | Developer | [@razinn70](https://github.com/razinn70) |

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- University of Guelph - CIS3750 Course
- Streamlit Community
- Supabase Team
- Open Source Contributors

---

## 📞 Support

### Issues
Report bugs or request features via GitHub Issues

### Questions
Contact team via course email: cis3750@socs.uoguelph.ca

---

## 📊 Project Stats

- **Lines of Code**: ~8,000+
- **Components**: 20+
- **Features**: 30+
- **Test Scenarios**: 50+
- **Development Time**: 1 semester
- **Team Size**: 7 members

---

## 🎯 Success Metrics

**Educational Impact:**
- Personalized learning paths
- Immediate feedback
- Data-driven insights
- Increased engagement

**Technical Achievement:**
- Full-stack application
- Production database integration
- Clean, professional UI
- Comprehensive testing

**Team Collaboration:**
- Git workflow
- Code reviews
- Documentation
- Agile practices

---

## 🏆 Key Achievements

✅ Fully functional ITS from scratch
✅ ML-powered adaptive learning
✅ Clean, modern UI/UX
✅ Multi-role platform
✅ Production-ready database
✅ Comprehensive testing
✅ Professional documentation
✅ Demo-ready presentation

---

## 🚀 Getting Started Now

**For Evaluators:**
1. Read [QUICK_START.md](QUICK_START.md)
2. Run the app
3. Test student journey
4. Review [DEMO_READINESS_REPORT.md](DEMO_READINESS_REPORT.md)

**For Developers:**
1. Read [Architecture](#architecture)
2. Set up environment
3. Review [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. Check [IMPROVEMENTS_CHECKLIST.md](IMPROVEMENTS_CHECKLIST.md)

**For Users:**
1. Install from [Quick Start](#quick-start)
2. Create account
3. Take quiz
4. Start learning!

---

## ⭐ Star Us!

If you find this project helpful, please give it a star on GitHub!

---

**Built with ❤️ by Group 11**

*Making calculus education adaptive, engaging, and effective.*

---

**Last Updated**: November 24, 2025
**Version**: 1.0.0 (Demo Ready)
**Status**: ✅ Production Ready
