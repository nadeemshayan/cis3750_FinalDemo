# Demo Class Setup Instructions

## Overview
The demo class generator creates a fully functional teacher account with 30 demo students (and parent accounts for ~15 students) with realistic, varied performance data.

## Running the Generator

### Option 1: Through Streamlit (Recommended)
```bash
streamlit run generate_demo_class.py
```
This will run the generator and create all demo accounts.

### Option 2: Standalone Python (if JSON fallback is needed)
If you want to bypass Supabase and use JSON storage only:
1. Edit `data_manager.py` line 9: Change `USE_SUPABASE = True` to `USE_SUPABASE = False`
2. Run: `python3 generate_demo_class.py`

## Demo Accounts Created

### Teacher Account
- **Username**: `demo_teacher`
- **Password**: `teacher123`
- **Teacher Code**: `DEMO-TEACH`
- **Purpose**: View all 30 students in teacher analytics dashboard

### Student Accounts (30 total)
- **Usernames**: Random combinations like `emma_smith`, `liam_johnson`, etc.
- **Password**: `demo123` (for all students)
- **Performance Distribution**:
  - 8 High Performers (70-95% progress, quiz scores 7-8/8)
  - 17 Medium Performers (40-70% progress, quiz scores 5-6/8)
  - 5 Low Performers (10-35% progress, quiz scores 2-4/8)

### Parent Accounts (~15 total)
- **Usernames**: `parent_of_[student_name]`
- **Password**: `demo123` (for all parents)
- **Purpose**: View linked child's progress
- **Example**: `parent_of_emma_smith` → linked to student `emma_smith`

## Generated Data for Each Student

Each demo student has:
- ✅ Completed initial quiz with varied scores
- 📚 Completed 0-6 lessons (based on performance level)
- ⏱️ 30-360 minutes of study time
- 🎯 3-30 practice problem attempts with varied accuracy
- 🏆 Earned badges based on achievements
- 📈 Realistic weak/strong topic distributions
- 📅 Activity timestamps spread over 2 weeks

## Testing the Demo

### As Teacher:
1. Login as `demo_teacher` / `teacher123`
2. Navigate to **Teacher Dashboard**
3. Click **"View Student Analytics"**
4. See all 30 students with:
   - Individual performance metrics
   - Class-wide statistics
   - ML-powered risk assessments
   - Topic performance analysis

### As Student:
1. Login as any student (e.g., `emma_smith` / `demo123`)
2. See their completed quiz, lessons, and progress
3. Navigate through achievements to see earned badges
4. Test lesson completion and practice problems

### As Parent:
1. Login as any parent (e.g., `parent_of_emma_smith` / `demo123`)
2. View your child's:
   - Overall progress
   - Quiz results with weak/strong topics
   - Lesson completion status
   - Activity timeline
   - Earned badges

## Features Demonstrated

### 1. **Quiz System** ✅
- Initial quiz saves results correctly
- Achievements/badges awarded based on scores
- Progress unlocks lessons

### 2. **Lesson System** ✅
- Lessons unlock based on quiz completion
- Practice problems link at bottom of each lesson
- Lesson quizzes route correctly

### 3. **Teacher Dashboard** ✅
- Shows real student count and statistics
- Recent student activity display
- Analytics page with ML-powered insights

### 4. **Parent Dashboard** ✅
- Displays child's progress (not parent's own progress)
- Detailed performance metrics
- Activity tracking and engagement stats

### 5. **Achievements System** ✅
- Uses actual user data (not hardcoded)
- Badges awarded based on real accomplishments
- Certificate tracking

## Troubleshooting

### If Supabase Error Occurs:
The generator will fall back to JSON storage automatically. If you see Supabase errors:
1. The data will still be saved to local JSON files in the `data/` folder
2. You can continue using the app normally with JSON storage

### If Demo Data Needs Reset:
Delete these files:
```bash
rm data/users.json
rm data/progress.json
```
Then run the generator again.

### Checking Created Accounts:
View the generated accounts:
```bash
cat data/users.json | python3 -m json.tool
```

## Next Steps

After generating demo data:
1. Login as `demo_teacher` to see the full teacher experience
2. Login as various students to see different performance levels
3. Login as a parent to test parent-child linking
4. Test the ML-adaptive features with different student profiles

## Notes

- All passwords are `demo123` for easy testing
- Parent accounts are automatically linked to their students
- Student data includes realistic timestamps over 2 weeks
- ML features will show different recommendations based on performance
- The demo can be regenerated anytime to get fresh data
