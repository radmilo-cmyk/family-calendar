-- Migration: chores-checklist-and-defaults
-- Run this in the Supabase SQL Editor before deploying the new code.
-- SQLite (local dev) is handled automatically by create_all() on startup.

ALTER TABLE entries ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE;
ALTER TABLE entries ADD COLUMN IF NOT EXISTS done_by VARCHAR;

CREATE TABLE IF NOT EXISTS default_chores (
    id SERIAL PRIMARY KEY,
    content VARCHAR NOT NULL,
    position INTEGER DEFAULT 0 NOT NULL
);
