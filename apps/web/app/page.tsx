import { LeaderboardTable } from "../components/leaderboard-table";
import { getLeaderboard } from "../lib/api";

function formatCompact(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return "N/A";
  }
  return Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value);
}

export default async function HomePage() {
  const rows = await getLeaderboard();
  const leader = rows[0];
  const avgSentiment = rows.length
    ? rows.reduce((sum, row) => sum + row.sentiment, 0) / rows.length
    : null;
  const totalPodcastMentions = rows.reduce((sum, row) => sum + (row.podcast_mentions ?? 0), 0);
  const totalViews = rows.reduce((sum, row) => sum + (row.youtube_views ?? 0), 0);

  return (
    <main className="shell">
      <div className="frame">
        <header className="topbar">
          <div className="brandBlock">
            <span className="eyebrow">Internal Editorial Intelligence</span>
            <div className="brand">
              Blaze <span>Popularity Desk</span>
            </div>
          </div>
          <nav className="topnav">
            <a href="#leaderboard">Leaderboard</a>
            <a href="#signals">Signals</a>
            <a href="#coverage">Coverage</a>
          </nav>
        </header>

        <section className="hero">
          <div className="heroMain">
            <span className="pill">Blaze Media Host Index</span>
            <h1>The newsroom view of host momentum.</h1>
            <p>
              A Blaze-branded internal dashboard for tracking public attention, discoverability, engagement,
              sentiment, and crossover reach across YouTube, Google Trends, search visibility, and podcasts.
            </p>
          </div>
          <aside className="heroRail">
            <div className="railMetric">
              <span className="railLabel">Top Host Today</span>
              <strong>{leader?.host_name ?? "Waiting for data"}</strong>
              <span className="muted">
                Score {leader ? leader.popularity_score.toFixed(1) : "N/A"} with 7-day momentum{" "}
                {leader?.momentum_7d?.toFixed(1) ?? "N/A"}%
              </span>
            </div>
            <div className="railMetric">
              <span className="railLabel">Primary Inputs</span>
              <span className="muted">YouTube, Google Trends, SERP rank, podcast mentions, and sentiment docs</span>
            </div>
          </aside>
        </section>

        <section className="statsRow" id="signals">
          <div className="panel card statCard">
            <span className="subtleLabel">Tracked Hosts</span>
            <strong className="statValue">{rows.length}</strong>
            <span className="muted">Config-driven roster from `hosts.yaml`</span>
          </div>
          <div className="panel card statCard">
            <span className="subtleLabel">Combined YouTube Views</span>
            <strong className="statValue accentText">{formatCompact(totalViews)}</strong>
            <span className="muted">Latest daily channel totals across active hosts</span>
          </div>
          <div className="panel card statCard">
            <span className="subtleLabel">Average Sentiment</span>
            <strong className="statValue">{avgSentiment === null ? "N/A" : avgSentiment.toFixed(1)}</strong>
            <span className="muted">Normalized sentiment subscore, 0 to 100</span>
          </div>
          <div className="panel card statCard">
            <span className="subtleLabel">Podcast Mentions</span>
            <strong className="statValue">{totalPodcastMentions}</strong>
            <span className="muted">Latest host crossover mentions with confidence scoring</span>
          </div>
        </section>

        <section className="newsGrid" id="coverage">
          <article className="panel featurePanel">
            <span className="sectionKicker">Lead Story</span>
            <h2 className="featureHeadline">
              {leader ? `${leader.host_name} leads the internal popularity board.` : "Popularity board is ready for live feeds."}
            </h2>
            <p className="sectionMeta">
              The composite score weights attention, discoverability, engagement, sentiment, and crossover. Missing
              provider data degrades gracefully rather than breaking the dashboard.
            </p>
          </article>
          <aside className="panel card">
            <span className="sectionKicker">Score Recipe</span>
            <div className="timeline">
              <div className="timelineItem">
                <strong>Attention 30%</strong>
                <span className="muted">Audience reach across video and search interest.</span>
              </div>
              <div className="timelineItem">
                <strong>Discoverability 20%</strong>
                <span className="muted">Google Trends visibility and SERP ranking strength.</span>
              </div>
              <div className="timelineItem">
                <strong>Engagement 20%</strong>
                <span className="muted">Video reaction signals and recurring mention volume.</span>
              </div>
              <div className="timelineItem">
                <strong>Sentiment 15% and CrossOver 15%</strong>
                <span className="muted">Tone of public mentions and reach outside the core channel.</span>
              </div>
            </div>
          </aside>
        </section>

        <section id="leaderboard">
          <div className="sectionHeader">
            <div>
              <span className="sectionKicker">Leaderboard</span>
              <h2>Daily host standings</h2>
            </div>
            <div className="sectionMeta">
              Sort-ready popularity coverage designed for editorial and executive review. Each row links to a detail
              page with score history and appearance context.
            </div>
          </div>
          <LeaderboardTable rows={rows} />
        </section>

        <div className="footerNote">
          Visual direction is adapted from the editorial feel of <a href="https://www.theblaze.com">theblaze.com</a>:
          warm paper tones, bold serif typography, orange accenting, and sectioned newsroom framing.
        </div>
      </div>
    </main>
  );
}
