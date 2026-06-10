-- Drop translation columns from questions table
-- We're going English-only for content; UI i18n remains
ALTER TABLE questions DROP COLUMN IF EXISTS body_translations;
ALTER TABLE questions DROP COLUMN IF EXISTS options_translations;
