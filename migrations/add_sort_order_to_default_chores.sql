-- Migration: add-sort-order-to-default-chores
-- Run this in the Supabase SQL Editor before deploying.
-- SQLite local dev: delete calendar.db and let the app rebuild it on next start.

ALTER TABLE default_chores RENAME COLUMN position TO sort_order;

-- Backfill: set sequential sort_order values based on existing id order
UPDATE default_chores SET sort_order = subq.new_order
FROM (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) - 1 AS new_order
    FROM default_chores
) subq
WHERE default_chores.id = subq.id;
