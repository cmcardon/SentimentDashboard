# Scoring

## Subscores

All subscores are clamped to the 0 to 100 range.

- `Attention`: audience reach, currently driven by YouTube views and trend volume
- `Discoverability`: search visibility and Google Trends discoverability
- `Engagement`: reactions and recurring mention volume
- `Sentiment`: normalized from document sentiment scores in the -1 to 1 range
- `CrossOver`: presence outside the host's primary channel, such as podcasts and broader search interest

## Composite popularity score

```text
Popularity =
  0.30 * Attention +
  0.20 * Discoverability +
  0.20 * Engagement +
  0.15 * Sentiment +
  0.15 * CrossOver
```

## Momentum

- `7-day momentum`: percent change between the current popularity score and the score 7 days earlier
- `30-day momentum`: percent change between the current popularity score and the score 30 days earlier

## Reproducibility

- Raw payloads are stored in `raw_source_events`
- Source-specific facts are persisted by host and day
- Final scores are deterministic from those persisted facts

