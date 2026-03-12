import Link from "next/link";

import type { LeaderboardRow } from "../lib/api";

function formatNumber(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return "N/A";
  }
  return Intl.NumberFormat("en-US", { maximumFractionDigits: 1 }).format(value);
}

export function LeaderboardTable({ rows }: { rows: LeaderboardRow[] }) {
  if (rows.length === 0) {
    return (
      <div className="panel card">
        <h2>Leaderboard unavailable</h2>
        <p className="muted">
          The UI stays online even when providers or the API are unavailable. Seed data or start the API to populate
          this table.
        </p>
      </div>
    );
  }

  return (
    <div className="panel tableWrap">
      <table>
        <thead>
          <tr>
            <th>Host</th>
            <th>Score</th>
            <th>7d</th>
            <th>30d</th>
            <th>Sentiment</th>
            <th>YouTube Views</th>
            <th>Google Trends</th>
            <th>SERP Rank</th>
            <th>Podcast Mentions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row.host_slug}>
              <td>
                <div className="hostCell">
                  <span className="hostRank">Rank #{index + 1}</span>
                  <Link className="hostName" href={`/hosts/${row.host_slug}`}>
                    {row.host_name}
                  </Link>
                  <div className="badgeRow">
                    <span className="metricBadge">Attention {formatNumber(row.attention)}</span>
                    <span className="metricBadge">Engagement {formatNumber(row.engagement)}</span>
                  </div>
                </div>
              </td>
              <td className="score">{formatNumber(row.popularity_score)}</td>
              <td className={`delta ${row.momentum_7d !== null && row.momentum_7d < 0 ? "deltaDown" : "deltaUp"}`}>
                {row.momentum_7d === null ? "N/A" : `${formatNumber(row.momentum_7d)}%`}
              </td>
              <td className={`delta ${row.momentum_30d !== null && row.momentum_30d < 0 ? "deltaDown" : "deltaUp"}`}>
                {row.momentum_30d === null ? "N/A" : `${formatNumber(row.momentum_30d)}%`}
              </td>
              <td>{formatNumber(row.sentiment)}</td>
              <td>{formatNumber(row.youtube_views)}</td>
              <td>{formatNumber(row.google_trends_interest)}</td>
              <td>{formatNumber(row.serp_avg_rank)}</td>
              <td>{formatNumber(row.podcast_mentions)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
