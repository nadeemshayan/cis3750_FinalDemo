# Verify Teacher-Student Connection

## Check in Supabase SQL Editor:

```sql
-- See which students have TEACH-5000 in their teacher_codes
SELECT 
    username, 
    role, 
    teacher_codes,
    email,
    grade
FROM users 
WHERE role = 'Student'
ORDER BY username;
```

This will show:
- All students
- Their teacher_codes arrays
- Who has TEACH-5000

## Expected Results:
Should see 4 students with TEACH-5000:
- shayann
- student2  
- livedemostudent1
- finalstudenttest

## If teacher_codes is empty for some students:
They need to join the class again via student dashboard.

## Quick Fix Query (if needed):
```sql
-- Add TEACH-5000 to a student's teacher_codes
UPDATE users 
SET teacher_codes = teacher_codes || '["TEACH-5000"]'::jsonb
WHERE username = 'livedemostudent1' AND role = 'Student';

UPDATE users 
SET teacher_codes = teacher_codes || '["TEACH-5000"]'::jsonb
WHERE username = 'finalstudenttest' AND role = 'Student';
```
