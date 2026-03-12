CREATE TABLE IF NOT EXISTS hosts (
  id SERIAL PRIMARY KEY,
  slug VARCHAR(120) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  config_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS host_aliases (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  alias VARCHAR(255) NOT NULL,
  alias_type VARCHAR(50) NOT NULL DEFAULT 'name',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_host_alias UNIQUE (host_id, alias)
);

CREATE TABLE IF NOT EXISTS platform_accounts (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  platform VARCHAR(50) NOT NULL,
  account_id VARCHAR(255) NOT NULL,
  username VARCHAR(255),
  url VARCHAR(500),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_platform_account UNIQUE (host_id, platform, account_id)
);

CREATE TABLE IF NOT EXISTS youtube_channel_daily (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  day DATE NOT NULL,
  views INTEGER NOT NULL DEFAULT 0,
  subscribers INTEGER,
  videos_published INTEGER NOT NULL DEFAULT 0,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_youtube_channel_daily UNIQUE (host_id, day)
);

CREATE TABLE IF NOT EXISTS youtube_video_daily (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  video_id VARCHAR(255) NOT NULL,
  day DATE NOT NULL,
  title VARCHAR(500) NOT NULL,
  views INTEGER NOT NULL DEFAULT 0,
  likes INTEGER NOT NULL DEFAULT 0,
  comments INTEGER NOT NULL DEFAULT 0,
  engagement_rate DOUBLE PRECISION,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_youtube_video_daily UNIQUE (host_id, video_id, day)
);

CREATE TABLE IF NOT EXISTS google_trends_daily (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  day DATE NOT NULL,
  interest_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_google_trends_daily UNIQUE (host_id, day)
);

CREATE TABLE IF NOT EXISTS serp_rank_daily (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  keyword VARCHAR(255) NOT NULL,
  day DATE NOT NULL,
  average_rank DOUBLE PRECISION NOT NULL,
  best_rank INTEGER,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 1.0,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_serp_rank_daily UNIQUE (host_id, keyword, day)
);

CREATE TABLE IF NOT EXISTS podcast_mentions_daily (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  episode_id VARCHAR(255) NOT NULL,
  day DATE NOT NULL,
  podcast_name VARCHAR(255) NOT NULL,
  episode_title VARCHAR(500) NOT NULL,
  mention_count INTEGER NOT NULL DEFAULT 1,
  confidence DOUBLE PRECISION NOT NULL,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_podcast_mentions_daily UNIQUE (host_id, episode_id, day)
);

CREATE TABLE IF NOT EXISTS sentiment_documents (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  source VARCHAR(50) NOT NULL,
  source_document_id VARCHAR(255) NOT NULL,
  published_at TIMESTAMPTZ NOT NULL,
  day DATE NOT NULL,
  title VARCHAR(500) NOT NULL,
  excerpt TEXT,
  sentiment_label VARCHAR(30),
  sentiment_score DOUBLE PRECISION,
  confidence DOUBLE PRECISION NOT NULL,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS host_scores_daily (
  id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
  day DATE NOT NULL,
  attention DOUBLE PRECISION NOT NULL,
  discoverability DOUBLE PRECISION NOT NULL,
  engagement DOUBLE PRECISION NOT NULL,
  sentiment DOUBLE PRECISION NOT NULL,
  crossover DOUBLE PRECISION NOT NULL,
  popularity_score DOUBLE PRECISION NOT NULL,
  momentum_7d DOUBLE PRECISION,
  momentum_30d DOUBLE PRECISION,
  source_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_host_scores_daily UNIQUE (host_id, day)
);

CREATE TABLE IF NOT EXISTS raw_source_events (
  id SERIAL PRIMARY KEY,
  provider VARCHAR(50) NOT NULL,
  source_type VARCHAR(50) NOT NULL,
  cache_key VARCHAR(255),
  event_at TIMESTAMPTZ NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS provider_cache_entries (
  id SERIAL PRIMARY KEY,
  provider VARCHAR(50) NOT NULL,
  cache_key VARCHAR(255) NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_provider_cache_entry UNIQUE (provider, cache_key)
);

