-- Migration: add-carryover-to-entries
-- Supabase: run in SQL Editor.
-- SQLite local dev: delete calendar.db and let the app rebuild it on next start.

ALTER TABLE entries ADD COLUMN carried_over BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE entries ADD COLUMN original_date DATE;
