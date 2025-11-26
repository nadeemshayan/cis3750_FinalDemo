# 🗄️ Supabase Setup Guide - Fix Progress on Streamlit Cloud

## ✅ What's Been Fixed

1. ✅ **Added overall progress calculation** to Supabase methods
2. ✅ **Enabled Supabase** in `data_manager.py`
3. ✅ **Progress now persists** on Streamlit Cloud (once configured)

---

## 🚀 How to Configure Supabase on Streamlit Cloud

### Step 1: Get Your Supabase Credentials

You already have a Supabase project. Find these values:

1. **Go to:** https://supabase.com/dashboard
2. **Open your project** (the one for this app)
3. **Click "Settings" → "API"**
4. **Copy:**
   - `Project URL` → This is your `SUPABASE_URL`
   - `anon public` key → This is your `SUPABASE_KEY`

---

### Step 2: Add Secrets to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/
2. **Click on your app** (`cis3750_finaldemo`)
3. **Click the 3 dots** (⋮) → **"Settings"**
4. **Scroll down to "Secrets"** section
5. **Paste this format:**

```toml
[supabase]
url = "your-project-url-here"
key = "your-anon-public-key-here"
```

**Example:**
```toml
[supabase]
url = "https://abcdefghijklmnop.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsIn..."
```

6. **Click "Save"**
7. **App will automatically reboot**

---

### Step 3: Verify Supabase Tables Exist

Your Supabase database needs these tables:

#### Table 1: `users`
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    age_level TEXT,
    grade TEXT,
    share_code TEXT,
    teacher_code TEXT,
    parent_codes TEXT DEFAULT '[]',
    teacher_codes TEXT DEFAULT '[]'
);
```

#### Table 2: `progress`
```sql
CREATE TABLE progress (
    username TEXT PRIMARY KEY REFERENCES users(username),
    initial_quiz TEXT DEFAULT '{"completed": false, "score": 0, "total": 18, "weak_topics": [], "strong_topics": [], "date": null}',
    lessons TEXT DEFAULT '{}',
    lesson_quizzes TEXT DEFAULT '{}',
    practice_problems TEXT DEFAULT '{}',
    final_test TEXT DEFAULT '{"completed": false, "score": 0, "date": null}',
    badges TEXT DEFAULT '[]',
    certificates TEXT DEFAULT '[]',
    total_time_spent INTEGER DEFAULT 0,
    last_active TIMESTAMPTZ DEFAULT NOW(),
    current_level INTEGER DEFAULT 1,
    overall_progress INTEGER DEFAULT 0
);
```

**To create these:**
1. Go to **Supabase Dashboard**
2. Click **"SQL Editor"**
3. Paste the SQL above
4. Click **"Run"**

---

## 🧪 Testing After Setup

### Test 1: Check if Supabase is Enabled

**On Streamlit Cloud, check the logs:**

```
✅ Supabase enabled - Progress will persist on cloud!
```

❌ **If you see:**
```
⚠️ Supabase not configured, using JSON fallback
```

→ Secrets not configured correctly. Double-check Step 2.

---

### Test 2: Complete a Quiz

1. **Complete initial quiz**
2. **Check logs for:**
```
📊 Supabase Quiz Progress Update: Quiz=True, Lessons=0/6 → Overall=20%
✅ Saved to Supabase: username - initial
```

3. **Refresh the page**
4. **Progress should still be 20%** (persisted!)

---

### Test 3: Complete a Lesson

1. **Complete Lesson 1**
2. **Check logs for:**
```
📊 Supabase Lesson Progress Update: Quiz=True, Lessons=1/6 → Overall=30%
✅ Saved to Supabase: username - Lesson lesson1
```

3. **Refresh the page**
4. **Progress should still be 30%** (persisted!)

---

## 🔍 Troubleshooting

### Issue: "Supabase not configured" error

**Causes:**
1. Secrets not added to Streamlit Cloud
2. Secrets have wrong format
3. Supabase credentials are wrong

**Solution:**
- Re-check Step 2
- Make sure format is exactly:
  ```toml
  [supabase]
  url = "..."
  key = "..."
  ```
- No extra quotes, no extra spaces

---

### Issue: "Table does not exist" error

**Cause:** Supabase tables not created

**Solution:**
- Go through Step 3
- Create both `users` and `progress` tables
- Check table names are exact (lowercase)

---

### Issue: Progress still shows 0% after quiz

**Causes:**
1. Supabase not actually enabled (check logs)
2. Tables missing
3. Progress calculation not running

**Debug:**
- Check logs for `📊 Supabase Quiz Progress Update`
- If you see it with "Overall=20%" but UI shows 0%:
  - Hard refresh (Ctrl+Shift+R)
  - Check database to see if row was created

**Check database:**
1. Go to Supabase Dashboard
2. Click "Table Editor"
3. Select `progress` table
4. Find your username
5. Check `overall_progress` column value

---

## 📋 Complete Checklist

Before deploying:

- [ ] Have Supabase project URL
- [ ] Have Supabase anon key
- [ ] Added secrets to Streamlit Cloud settings
- [ ] Created `users` table in Supabase
- [ ] Created `progress` table in Supabase
- [ ] Rebooted Streamlit Cloud app
- [ ] See "✅ Supabase enabled" in logs
- [ ] Tested quiz completion
- [ ] Tested lesson completion
- [ ] Progress persists after refresh

---

## 🎯 Local vs Cloud Comparison

| Feature | Local (JSON) | Cloud (Supabase) |
|---------|-------------|------------------|
| Progress saves | ✅ Yes | ✅ Yes |
| Progress persists | ✅ Yes | ✅ Yes (once configured) |
| Shared across devices | ❌ No | ✅ Yes |
| Setup required | ❌ None | ✅ Configure secrets |
| Database | File system | PostgreSQL |

---

## ⚡ Quick Setup Summary

**If you already have Supabase set up:**

1. Get URL and key from Supabase dashboard
2. Add to Streamlit Cloud secrets:
   ```toml
   [supabase]
   url = "https://your-project.supabase.co"
   key = "your-anon-key"
   ```
3. Reboot app
4. Done! ✅

**Expected logs after setup:**
```
✅ Supabase enabled - Progress will persist on cloud!
📊 Supabase Quiz Progress Update: ... → Overall=20%
✅ Saved to Supabase: username - initial
```

---

## 🔗 Useful Links

- **Supabase Dashboard:** https://supabase.com/dashboard
- **Streamlit Cloud:** https://share.streamlit.io/
- **Your App:** https://nadeemshayan-cis3750-finaldemo.streamlit.app/ (or similar)

---

## 🆘 Still Having Issues?

**Report these details:**

1. Screenshot of Streamlit secrets configuration
2. Screenshot of Supabase tables
3. Copy/paste of app logs showing:
   - "Supabase enabled" message
   - Any error messages
4. What happens when you complete a quiz
5. What the UI shows vs what logs say
