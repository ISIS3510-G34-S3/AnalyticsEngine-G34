-- Tracks watermarks for incremental loads
CREATE TABLE IF NOT EXISTS ingestion_state (
  source_key TEXT PRIMARY KEY,              -- e.g., 'bookings'
  highwater  TIMESTAMPTZ NOT NULL           -- latest createdAt_utc ingested
);
