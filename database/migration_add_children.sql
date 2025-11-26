-- Migration: Add 'children' column to users table
-- Run this in Supabase SQL Editor

-- Add children column if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS children JSONB DEFAULT '[]'::jsonb;

-- Verify the change
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
AND column_name = 'children';
