import Link from "next/link";

type Props = { params: Promise<{ ids: string }> };

export default async function ComparePage({ params }: Props) {
  const { ids } = await params;
  const hosts = ids.split(",").filter(Boolean).slice(0, 5);

  return (
    <main className="shell">
      <div className="frame">
        <header className="topbar">
          <div className="brandBlock">
            <span className="eyebrow">Editorial Compare</span>
            <div className="brand">
              Blaze <span>Popularity Desk</span>
            </div>
          </div>
          <nav className="topnav">
            <Link href="/">Leaderboard</Link>
          </nav>
        </header>

        <section className="hero">
          <div className="heroMain">
            <span className="pill">Compare Hosts</span>
            <h1>Head-to-head momentum.</h1>
            <p>
              This route is ready for richer comparative overlays. For now it gives the Blaze-branded shell and the
              selected host roster so we can plug in multi-host charts next.
            </p>
            <Link href="/">Back to leaderboard</Link>
          </div>
          <aside className="heroRail">
            <div className="railMetric">
              <span className="railLabel">Selected</span>
              <strong>{hosts.length}</strong>
              <span className="muted">Supports 2 to 5 hosts per comparison set</span>
            </div>
          </aside>
        </section>

        <section className="panel card compareList">
          {hosts.length === 0 ? <p className="muted">No hosts selected.</p> : null}
          {hosts.map((host) => (
            <div className="compareCard" key={host}>
              <strong>{host}</strong>
              <span className="metricBadge">Comparison slot ready</span>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
