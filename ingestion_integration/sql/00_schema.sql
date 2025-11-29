CREATE TABLE IF NOT EXISTS dim_experience (
  experience_id      TEXT PRIMARY KEY,
  host_id            TEXT NOT NULL,
  department         TEXT NOT NULL,
  host_verified      BOOLEAN NOT NULL,
  is_active          BOOLEAN NOT NULL,
  categories         TEXT[] NOT NULL,
  price_cop          BIGINT,
  group_size_max     INT,
  created_at_utc     TIMESTAMPTZ NOT NULL,
  updated_at_utc     TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS fact_availability_slot (
  experience_id      TEXT NOT NULL REFERENCES dim_experience(experience_id),
  start_utc          TIMESTAMPTZ NOT NULL,
  end_utc            TIMESTAMPTZ NOT NULL,
  capacity_total     INT NOT NULL,
  capacity_remaining INT NOT NULL,
  PRIMARY KEY (experience_id, start_utc, end_utc)
);

CREATE TABLE IF NOT EXISTS fact_booking (
  booking_id         TEXT PRIMARY KEY,
  experience_id      TEXT NOT NULL REFERENCES dim_experience(experience_id),
  host_id            TEXT NOT NULL,
  traveler_id        TEXT,
  people_count       INT NOT NULL,
  amount_cop         BIGINT,
  created_at_utc     TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_feature_usage_monthly (
  feature_key        TEXT NOT NULL,
  yyyymm             TEXT NOT NULL,     -- 'YYYY-MM'
  count              BIGINT NOT NULL,
  PRIMARY KEY (feature_key, yyyymm)
);

CREATE TABLE IF NOT EXISTS fact_messaging_global_usage (
  last_chat_started_at TEXT,
  total_chats_started INT NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_dim_experience_active_dept
  ON dim_experience (is_active, department);

CREATE INDEX IF NOT EXISTS ix_dim_experience_categories
  ON dim_experience USING GIN (categories);

CREATE INDEX IF NOT EXISTS ix_fact_availability_slot_time
  ON fact_availability_slot (start_utc, end_utc);

CREATE INDEX IF NOT EXISTS ix_fact_booking_created
  ON fact_booking (created_at_utc);
