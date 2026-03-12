import Link from "next/link";

import { getHost } from "../../../lib/api";

type Props = { params: Promise<{ slug: string }> };

function miniBars(points: { value: number }[]) {
  const sample = points.slice(-12);
  const max = Math.max(...sample.map((point) => point.value), 1);
  return sample.map((point, index) => ({
    key: `${index}-${point.value}`,
    height: Math.max(12, Math.round((point.value / max) * 100)),
    value: point.value,
  }));
}

export default async function HostPage({ params }: Props) {
  const { slug } = await params;
  const host = await getHost(slug);

  if (!host) {
    return (
      <main className="shell">
        <div className="panel card">
          <p className="muted">Host data is not available right now.</p>
          <Link href="/">Back to leaderboard</Link>
        </div>
      </main>
    );
  }

  const charts = [
    { label: "Popularity Score", value: host.leaderboard.popularity_score },
    { label: "Attention", value: host.leaderboard.attention },
    { label: "Discoverability", value: host.leaderboard.discoverability },
    { label: "Engagement", value: host.leaderboard.engagement },
    { label: "Sentiment", value: host.leaderboard.sentiment },
    { label: "CrossOver", value: host.leaderboard.crossover },
  ];
  const scoreBars = miniBars(host.score_series);
  const trendsBars = miniBars(host.trends_series);
  const youtubeBars = miniBars(host.youtube_series);

  return (
    <main className="shell">
      <div className="frame">
        <header className="topbar">
          <div className="brandBlock">
            <span className="eyebrow">Host Dossier</span>
            <div className="brand">
              Blaze <span>Popularity Desk</span>
            </div>
          </div>
          <nav className="topnav">
            <Link href="/">Leaderboard</Link>
            <Link href={`/compare/${host.host_slug}`}>Compare</Link>
          </nav>
        </header>

        <section className="hostHero">
          <div className="heroMain">
            <span className="pill">{host.host_name}</span>
            <h1>{host.host_name}</h1>
            <p>
              Score history, source performance, sentiment tone, and recent crossover appearances gathered from the
              host-day facts persisted by the ingestion layer.
            </p>
            <Link href="/">Back to leaderboard</Link>
          </div>

          <aside className="heroRail">
            <div className="railMetric">
              <span className="railLabel">Current Score</span>
              <strong>{host.leaderboard.popularity_score.toFixed(1)}</strong>
              <span className="muted">7-day momentum {host.leaderboard.momentum_7d?.toFixed(1) ?? "N/A"}%</span>
            </div>
            <div className="railMetric">
              <span className="railLabel">Latest Search Signal</span>
              <strong>{host.leaderboard.google_trends_interest?.toFixed(1) ?? "N/A"}</strong>
              <span className="muted">Google Trends interest on the latest scoring day</span>
            </div>
          </aside>
        </section>

        <section className="sectionHeader">
          <div>
            <span className="sectionKicker">Score Breakdown</span>
            <h2>How this host is performing</h2>
          </div>
          <div className="sectionMeta">
            Each subscore is clamped to 0-100, then blended into the composite popularity score using the documented
            weights from `docs/scoring.md`.
          </div>
        </section>

        <section className="grid cards">
          {charts.map((chart) => (
            <div className="panel card scoreStrip" key={chart.label}>
              <div className="subtleLabel">{chart.label}</div>
              <h2>{chart.value.toFixed(1)}</h2>
              <div className="barTrack">
                <div className="bar" style={{ width: `${Math.max(6, chart.value)}%` }} />
              </div>
            </div>
          ))}
        </section>

        <section className="newsGrid">
          <div className="panel card chartStack">
            <span className="sectionKicker">Trend View</span>
            <div className="sparklineRow">
              <span>Popularity Score</span>
              <div className="sparklineBars">
                {scoreBars.map((bar) => (
                  <div key={bar.key} className="sparklineBar" style={{ height: `${bar.height}%` }} />
                ))}
              </div>
              <strong>{host.leaderboard.popularity_score.toFixed(1)}</strong>
            </div>
            <div className="sparklineRow">
              <span>Google Trends</span>
              <div className="sparklineBars">
                {trendsBars.map((bar) => (
                  <div key={bar.key} className="sparklineBar" style={{ height: `${bar.height}%` }} />
                ))}
              </div>
              <strong>{host.leaderboard.google_trends_interest?.toFixed(1) ?? "N/A"}</strong>
            </div>
            <div className="sparklineRow">
              <span>YouTube Daily Views</span>
              <div className="sparklineBars">
                {youtubeBars.map((bar) => (
                  <div key={bar.key} className="sparklineBar" style={{ height: `${bar.height}%` }} />
                ))}
              </div>
              <strong>{host.leaderboard.youtube_views?.toLocaleString() ?? "N/A"}</strong>
            </div>
          </div>

          <aside className="panel card">
            <span className="sectionKicker">Recent Appearances</span>
            <div className="timeline">
              {host.appearances.slice(0, 10).map((appearance) => (
                <div className="timelineItem" key={`${appearance.day}-${appearance.title}`}>
                  <strong>{appearance.title}</strong>
                  <span className="muted">
                    {appearance.day} • {appearance.source} • confidence {appearance.confidence.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}
