# 🔍 Debug Logs Guide - What to Look For

## ✅ All Errors Fixed!

1. ✅ **AttributeError (NoneType)** - Fixed with null check
2. ✅ **KeyError in quiz display** - Fixed with pre-computed values
3. ✅ **Quiz answers not showing** - Fixed nested f-string issue

## 📊 How to Read the Debug Logs

### When You Complete the Initial Quiz

**In your terminal/console, you should see this sequence:**

```
📊 Quiz Submission: Answered=15/18, Correct=12/18, Skipped=3
🎓 Saving initial quiz: yourname, Score: 12/18, Weak: [...], Strong: [...]
📊 Quiz Progress Update: Quiz=True, Lessons=0/6, Practice=0/10 → Overall=20%
💾 Saved to progress.json - 3 users
✅ Initial quiz saved successfully
```

**What each line means:**

1. **📊 Quiz Submission** 
   - Shows how many you answered vs skipped
   - Shows your correct count
   - **Skipped questions are NOT counted as correct**

2. **🎓 Saving initial quiz**
   - Confirms save is being attempted
   - Shows your score and weak/strong topics

3. **📊 Quiz Progress Update**
   - Shows the calculation: Quiz + Lessons + Practice = Overall
   - Should show "Overall=20%" after first quiz

4. **💾 Saved to progress.json**
   - Confirms file was written
   - Shows how many users in the file

5. **✅ Initial quiz saved successfully**
   - Final confirmation

---

### When You View Dashboard/Sidebar

**You should see:**

```
📖 Reading progress for yourname: Overall=20%, Quiz=True
🔍 Dashboard loading progress for yourname: 20%
🔍 Sidebar loading progress for yourname: 20%
```

**What each line means:**

1. **📖 Reading progress**
   - Shows what was loaded from file
   - Should match what you just saved

2. **🔍 Dashboard/Sidebar loading**
   - Shows what's being displayed
   - Should match what was read

---

## 🐛 Troubleshooting - If Progress is Still 0%

### Check 1: Did the Quiz Save?

**Look for these lines after submitting quiz:**
```
📊 Quiz Progress Update: ... → Overall=20%
💾 Saved to progress.json
✅ Initial quiz saved successfully
```

❌ **If you DON'T see these:**
- Quiz save didn't run
- Check if you're logged in (not guest)
- Check username in session

✅ **If you DO see these:**
- Quiz saved correctly
- Problem is in reading/displaying

---

### Check 2: Is the File Being Read?

**Look for this when loading dashboard:**
```
📖 Reading progress for yourname: Overall=20%, Quiz=True
```

❌ **If it shows Overall=0%:**
- File was saved but read back as 0%
- Possible file permission issue on Streamlit Cloud
- Or username mismatch

✅ **If it shows Overall=20%:**
- File read correctly
- Problem is in display

---

### Check 3: Is the UI Displaying It?

**Look for these when dashboard loads:**
```
🔍 Dashboard loading progress: 20%
🔍 Sidebar loading progress: 20%
```

❌ **If these show 0% but read showed 20%:**
- Data is correct, but UI not updating
- Try hard refresh (Ctrl+Shift+R)

✅ **If these show 20%:**
- Everything working!
- Check the actual UI

---

## 🎯 Common Scenarios

### Scenario 1: "I see 20% in logs but 0% on screen"

**Solution:**
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. On Streamlit Cloud: Click "Reboot app" in menu

---

### Scenario 2: "I see all the save logs but read shows 0%"

**Possible causes:**
1. **Username mismatch**
   - Saving under one name
   - Reading under different name
   - Check: Look at username in each log line

2. **File permissions on Streamlit Cloud**
   - Cloud environment may not persist files
   - Need to use Supabase for cloud (currently disabled)

**Solution for Streamlit Cloud:**
- The app needs Supabase enabled for cloud deployment
- JSON files don't persist on Streamlit Cloud
- Either:
  - Test locally (JSON works)
  - Or enable Supabase (need to complete the implementation)

---

### Scenario 3: "I don't see ANY debug logs"

**Causes:**
1. Code not deployed yet
2. Using old version
3. Looking at wrong terminal

**Solution:**
1. Verify you pulled latest code
2. Check Streamlit Cloud logs (click "Manage app" → "Logs")
3. For local: Check terminal where you ran `streamlit run`

---

## 📋 Complete Test Checklist

**After completing initial quiz:**

- [ ] See: "📊 Quiz Submission: Answered=X/18, Correct=Y/18"
- [ ] See: "🎓 Saving initial quiz: username, Score: Y/18"
- [ ] See: "📊 Quiz Progress Update: ... → Overall=20%"
- [ ] See: "💾 Saved to progress.json - X users"
- [ ] See: "✅ Initial quiz saved successfully"

**When loading dashboard:**

- [ ] See: "📖 Reading progress for username: Overall=20%"
- [ ] See: "🔍 Dashboard loading progress: 20%"
- [ ] See: "🔍 Sidebar loading progress: 20%"
- [ ] Dashboard tile shows 20%
- [ ] Sidebar bar shows 20%

---

## ⚠️ Known Limitation: Streamlit Cloud

**Important:** JSON files don't persist on Streamlit Cloud!

The `/data/` folder is:
- ✅ **Works locally** - Files save and load perfectly
- ❌ **Doesn't work on cloud** - Files reset on each deploy

**For Streamlit Cloud deployment, you need:**
1. Enable Supabase (database)
2. Complete Supabase implementation (missing methods)
3. Configure secrets on Streamlit Cloud

**Current workaround:**
- Test locally for now
- Or complete Supabase setup

---

## 🚀 What to Report

If issues persist, copy/paste from terminal:

**After completing quiz:**
```
[paste all lines with 📊 🎓 💾 ✅]
```

**After loading dashboard:**
```
[paste all lines with 📖 🔍]
```

**Include:**
1. Your username
2. Whether testing locally or on Streamlit Cloud
3. What the UI actually shows
4. What the logs say it should show
