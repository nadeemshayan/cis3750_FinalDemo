# 🧪 Complete Testing Guide for BrainyYack ITS

**Purpose**: Test all features across Student, Parent, and Teacher roles  
**Date**: November 24, 2025

---

## 🚀 QUICK START - How to Test

### Step 1: Start the App
```bash
cd /Users/shayannadeem/Desktop/School/Fourth\ Year/CIS3750/project-setup-group-11/final_demo
streamlit run streamlit_app.py
```

### Step 2: Create Test Accounts
You'll need 3 accounts to test everything:
1. **Student Account** (test_student)
2. **Teacher Account** (test_teacher)  
3. **Parent Account** (test_parent)

---

## 📋 TESTING SCENARIOS

### Scenario 1: Student Journey (15 minutes)

#### Test: Account Creation & Initial Setup
1. **Register as Student**
   - Username: `test_student`
   - Password: `test123`
   - Email: `student@test.com`
   - Role: **Student**
   - Age Level: High School
   - Grade: 12th

2. **Expected Results**:
   - ✅ "Welcome Aboard! 👋" badge immediately awarded
   - ✅ Redirected to login
   - ✅ After login, see student dashboard

3. **Check Dashboard**:
   - Should see: 0% progress, 0 lessons, 1 badge, 0% quiz
   - Should see: Your Share Code (e.g., SHARE-XXXX)
   - Should see: "No parents linked yet"
   - Should see: "Not in any class yet"

#### Test: Initial Quiz
1. **Click "📝 Take Initial Quiz"**
2. **Complete Quiz** (intentionally get 2-3 wrong):
   - Question 1: Choose correct answer
   - Question 2: Choose correct answer  
   - Question 3: Choose **WRONG** answer
   - Question 4: Choose **WRONG** answer
   - Question 5: Choose correct answer
   - Continue through all 8 questions

3. **Use Features**:
   - Click "💡 Show Hint" on one question
   - Click "⏭️ Skip" on one question

4. **Expected Results**:
   - ✅ See results page with score (e.g., 60%)
   - ✅ See "Weak Topics" identified
   - ✅ See "Strong Topics" identified
   - ✅ "Quiz Starter" OR "Quiz Master" badge awarded
   - ✅ Terminal shows: `✅ Saved to JSON: test_student`

5. **Refresh Dashboard**:
   - Should now show: Quiz score updated
   - Should show: "📌 Work on: [weak topics]"
   - Should have: 2 badges total

#### Test: Account Linking - Join Teacher
1. **Go to Dashboard** (should already be there)
2. **Scroll to "🔗 Account Connections"**
3. **Under "👨‍🏫 Teacher Access"**:
   - Enter: `TEACH-5000` (teacher's code)
   - Click "🎓 Join Class"

4. **Expected Results**:
   - ✅ Success message
   - ✅ Balloons animation
   - ✅ (Refresh) Should show "✅ Linked to: TEACH-5000"

#### Test: Lessons
1. **Click "📚 Browse Lessons"**
2. **Expected Results**:
   - ✅ Lessons are unlocked (not showing "Complete quiz")
   - ✅ Recommended lesson matches your weak topic

#### Test: Practice Problems
1. **Click "✏️ Practice Problems"**
2. **Do 3-5 problems**
3. **Expected Results**:
   - ✅ Problems prioritize weak topics
   - ✅ Answers tracked
   - ✅ Explanations show

#### Test: Settings
1. **Click "⚙️ Settings" in sidebar**
2. **Check "Account Info" tab**:
   - ✅ See your username
   - ✅ See share code
   - ✅ See linked teachers

3. **Test Password Change**:
   - Go to "Security" tab
   - Try changing password
   - ✅ Should ask for confirmation

---

### Scenario 2: Teacher Journey (10 minutes)

#### Test: Teacher Account
1. **Logout** (if logged in as student)
2. **Register as Teacher**:
   - Username: `test_teacher`
   - Password: `test123`
   - Email: `teacher@test.com`
   - Role: **Teacher**

3. **Expected Results**:
   - ✅ See teacher dashboard
   - ✅ Shows "Your Teacher Code: TEACH-XXXX"

4. **Check Class List**:
   - Should show: 0 students (or 1 if student linked in Scenario 1)
   - If student linked:
     - ✅ See `test_student` in class list
     - ✅ Can view their progress
     - ✅ Can see their quiz results
     - ✅ Can see their badges

#### Test: Student Analytics
1. **Click "📊 View Student Analytics"**
2. **Expected Results**:
   - ✅ See all students in your class
   - ✅ See their progress percentages
   - ✅ See weak topics highlighted
   - ✅ See activity status

---

### Scenario 3: Parent Journey (10 minutes)

#### Test: Parent Account
1. **Logout**
2. **Register as Parent**:
   - Username: `test_parent`
   - Password: `test123`
   - Email: `parent@test.com`
   - Role: **Parent**

3. **Expected Results**:
   - ✅ See parent dashboard
   - ✅ Shows "0 Connected Children"

#### Test: Link Child
1. **Go to "➕ Connect New Child"**
2. **Enter Share Code**:
   - Use `test_student`'s share code from Scenario 1
   - Click "Connect"

3. **Expected Results**:
   - ✅ Success message
   - ✅ (Refresh) Shows "1 Connected Children"

4. **View Child Progress**:
   - ✅ See detailed report for `test_student`
   - ✅ See their quiz score
   - ✅ See their weak/strong topics
   - ✅ See lessons completed
   - ✅ See badges earned
   - ✅ See activity status (🟢 Active today)

#### Test: Detailed Tabs
1. **Click through tabs**:
   - **📝 Quiz Results**: See score, topics
   - **📚 Lessons**: See completion status
   - **⚡ Activity**: See last active, streak, practice stats
   - **🏆 Achievements**: See all badges

2. **Expected Results**:
   - ✅ All data matches student's actual progress
   - ✅ No "My Progress" - should say child's name
   - ✅ Shows child-specific data, not parent's data

---

## ✅ VERIFICATION CHECKLIST

### Data Consistency
- [ ] Student's quiz results same in all views (student, teacher, parent)
- [ ] Badges visible to student, teacher, and parent
- [ ] Weak topics consistent across all dashboards
- [ ] Activity status accurate (last active date)

### Account Linking
- [ ] Student can join teacher's class
- [ ] Teacher sees student in class list
- [ ] Parent can link child via share code
- [ ] Parent sees child's data (not parent's own progress)

### Database Persistence
- [ ] Logout and login → data persists
- [ ] Refresh page → data persists
- [ ] Check `data/progress.json` → quiz data saved
- [ ] Check `data/users.json` → codes saved

### UI/UX
- [ ] All pages have home buttons
- [ ] Settings page works
- [ ] Confirmations for destructive actions
- [ ] Loading states show (spinners)
- [ ] Success messages clear

---

## 🐛 COMMON ISSUES & FIXES

### Issue 1: "Take Initial Quiz" still showing after completion
**Cause**: Database not saving  
**Fix**: Check terminal for "✅ Saved to JSON" message  
**Verify**: Look in `data/progress.json` for your username

### Issue 2: Parent seeing own progress instead of child's
**Cause**: Fixed! Used to pull parent data, now pulls child data  
**Verify**: Parent dashboard should show child's username in report

### Issue 3: Achievements locked after quiz
**Cause**: Fixed! Achievements page now checks and awards badges  
**Verify**: Go to Achievements page, should see unlocked badges

### Issue 4: Teacher can't see students
**Cause**: Students need to join using teacher code  
**Fix**: Student must enter teacher code on their dashboard

### Issue 5: Share codes not working
**Cause**: Need to implement linking logic in DataManager  
**Current Status**: UI ready, backend connection needed

---

## 📊 WHAT EACH ROLE SHOULD SEE

### Student Dashboard Should Show:
- ✅ Own progress stats
- ✅ Own share code (for parents)
- ✅ Teacher codes joined
- ✅ Ability to join more teachers
- ✅ Current weak topics
- ✅ Current streak

### Parent Dashboard Should Show:
- ✅ Connected children count
- ✅ Average progress across children
- ✅ Each child's detailed report:
  - Quiz results
  - Lessons completed
  - Badges earned
  - Activity status
  - Practice stats
- ✅ Ability to connect more children

### Teacher Dashboard Should Show:
- ✅ Total students in class
- ✅ Class average progress
- ✅ Teacher code to share
- ✅ Individual student progress
- ✅ Class-wide weak topics
- ✅ Student activity levels

---

## 🧪 ADVANCED TESTING

### Test: Random Quiz Questions
1. Student takes quiz
2. Note which questions appear
3. Retake quiz
4. **Expected**: Different questions each time (random from 30-question bank)

### Test: Difficulty Adaptation
1. Student does 5 easy practice problems (get all correct)
2. **Expected**: Next problems should be harder
3. Student does 5 hard problems (get most wrong)
4. **Expected**: Next problems should be easier

### Test: Streaks
1. Login today
2. Come back tomorrow
3. **Expected**: Streak increments to 1 day
4. Skip a day
5. **Expected**: Streak resets to 1

---

## 🎯 SUCCESS CRITERIA

Your app is working if:
1. ✅ Student can take quiz and see results save
2. ✅ Student can join teacher's class
3. ✅ Teacher can see that student in class list
4. ✅ Parent can link child and see child's progress
5. ✅ All three roles see same data for the student
6. ✅ Badges unlock properly
7. ✅ Settings page works
8. ✅ Data persists across sessions

---

## 📝 TESTING NOTES TEMPLATE

Use this to track your testing:

```
Date: ___________
Tester: ___________

Student Account Tests:
[ ] Registration works
[ ] Quiz saves results
[ ] Weak topics identified
[ ] Can join teacher
[ ] Badges unlock
[ ] Settings accessible

Teacher Account Tests:
[ ] Can see class list
[ ] Student appears after joining
[ ] Can view student progress
[ ] Analytics work

Parent Account Tests:
[ ] Can link child
[ ] Sees child's data (not own)
[ ] All tabs show child info
[ ] Activity tracking accurate

Issues Found:
1. ___________
2. ___________
3. ___________

Overall Status: ⭕ Pass / ❌ Fail
```

---

## 🚀 QUICK TEST (5 minutes)

If short on time, test this critical path:

1. **Register student** → Take quiz → Check dashboard updates ✅
2. **Register parent** → Try to link child ✅
3. **Check parent sees child's quiz results** ✅

If these 3 work, core functionality is good!

---

**Generated**: November 24, 2025  
**For**: BrainyYack ITS v2.0  
**Test Coverage**: Student, Parent, Teacher roles + All major features
