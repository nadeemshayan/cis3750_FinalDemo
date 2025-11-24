-- Supabase Database Schema for BrainyYack
-- Run this SQL in your Supabase SQL Editor

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    age_level TEXT,
    grade TEXT,
    share_code TEXT,
    teacher_code TEXT,
    parent_codes JSONB DEFAULT '[]'::jsonb,
    teacher_codes JSONB DEFAULT '[]'::jsonb
);

-- Progress table
CREATE TABLE IF NOT EXISTS progress (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    initial_quiz JSONB DEFAULT '{}'::jsonb,
    lessons JSONB DEFAULT '{}'::jsonb,
    lesson_quizzes JSONB DEFAULT '{}'::jsonb,
    practice_problems JSONB DEFAULT '{}'::jsonb,
    final_test JSONB DEFAULT '{}'::jsonb,
    badges JSONB DEFAULT '[]'::jsonb,
    certificates JSONB DEFAULT '[]'::jsonb,
    total_time_spent INTEGER DEFAULT 0,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    current_level INTEGER DEFAULT 1,
    overall_progress INTEGER DEFAULT 0
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_progress_username ON progress(username);

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE progress ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for now - you can restrict later)
CREATE POLICY "Enable read access for all users" ON users FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON users FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON users FOR UPDATE USING (true);

CREATE POLICY "Enable read access for all users" ON progress FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON progress FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON progress FOR UPDATE USING (true);
