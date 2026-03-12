export type LeaderboardRow = {
  host_slug: string;
  host_name: string;
  score_date: string;
  popularity_score: number;
  attention: number;
  discoverability: number;
  engagement: number;
  sentiment: number;
  crossover: number;
  momentum_7d: number | null;
  momentum_30d: number | null;
  youtube_views: number | null;
  google_trends_interest: number | null;
  serp_avg_rank: number | null;
  podcast_mentions: number | null;
};

export type HostDetail = {
  host_slug: string;
  host_name: string;
  leaderboard: LeaderboardRow;
  score_series: { day: string; value: number }[];
  trends_series: { day: string; value: number }[];
  youtube_series: { day: string; value: number }[];
  sentiment_series: { day: string; value: number }[];
  appearances: { day: string; source: string; title: string; confidence: number }[];
};

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function getJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${baseUrl}${path}`, { next: { revalidate: 60 } });
    if (!response.ok) {
      return fallback;
    }
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export function getLeaderboard() {
  return getJson<LeaderboardRow[]>("/api/leaderboard", []);
}

export function getHost(slug: string) {
  return getJson<HostDetail | null>(`/api/hosts/${slug}`, null);
}

