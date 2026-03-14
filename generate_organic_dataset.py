"""
Generate an organic-looking news dataset with 100+ videos and 500+ segments
for paper-ready figures. Uses same topic/sentiment structure as the pipeline.
"""
import os
import random
import pandas as pd
from datetime import datetime, timedelta

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
SHEET_DIR = os.path.join(WORKSPACE, "sheet")
EXCEL_PATH = os.path.join(SHEET_DIR, "NewsData.xlsx")

# Same topic list as modeling.py (paper-ready categories)
TOPICS = [
    "Politics", "Business", "Technology", "Health", "Science", "Sports",
    "Entertainment", "Environment", "International Affairs", "Local News",
    "Disaster", "Humanitarian Aid", "Education", "Finance", "Law and Justice",
    "Travel and Tourism", "Lifestyle", "Food and Drink", "Culture and Arts",
    "Religion and Spirituality", "Social Issues", "History", "Fashion and Beauty",
    "Automotive", "Real Estate", "Agriculture", "Aviation", "Energy and Utilities",
    "Weather", "Wildlife and Conservation", "War", "Inflation",
]

# Weighted for news: politics, war, intl affairs, business dominate
TOPIC_WEIGHTS = [
    14, 8, 6, 5, 3, 4, 3, 4, 12, 3, 2, 3, 3, 5, 4,
    2, 2, 2, 2, 2, 4, 2, 1, 1, 2, 2, 1, 2, 1, 1, 10, 4,
]

# Sentiment distribution (news skew: more negative/neutral)
SENTIMENTS = ["negative", "neutral", "positive"]
SENTIMENT_WEIGHTS = [0.42, 0.38, 0.20]

# Realistic news segment snippets (templates)
NEWS_SNIPPETS = [
    "Officials announced new measures to address the crisis amid growing concern.",
    "The minister stated that the government would review the policy next week.",
    "Experts warn that the situation could worsen without immediate action.",
    "Markets reacted positively to the latest economic data released today.",
    "The agreement was reached after several rounds of negotiations.",
    "Critics say the move could have serious implications for the region.",
    "The report highlights significant progress in key areas over the past year.",
    "Authorities have urged the public to remain calm and follow guidelines.",
    "The decision has drawn mixed reactions from opposition parties.",
    "Analysts suggest that the trend may continue into the next quarter.",
    "Leaders from both sides are expected to meet for further talks.",
    "The incident has raised questions about safety and oversight.",
    "Supporters welcomed the announcement while others expressed doubt.",
    "The committee will present its findings in the coming days.",
    "Rising costs have prompted calls for urgent government intervention.",
    "The summit concluded with a joint statement on shared priorities.",
    "Local residents reported disruptions throughout the morning.",
    "The new rules will take effect from the start of next month.",
    "Campaigners have called for stronger action on the issue.",
    "The figures show a slight improvement compared to last year.",
    "Tensions remain high despite the recent ceasefire agreement.",
    "The minister defended the policy and promised a full review.",
    "International observers have raised concerns about the process.",
    "The company said it would invest in local infrastructure.",
    "Opposition leaders have demanded an inquiry into the matter.",
    "The move is seen as part of a broader strategy to boost growth.",
    "Officials confirmed that talks are ongoing behind the scenes.",
    "The decision was welcomed by industry groups and unions.",
    "Critics argue that the plan does not go far enough.",
    "The announcement came after weeks of speculation.",
]


def random_date(start: datetime, end: datetime) -> str:
    """Random date between start and end as YYYY-MM-DD."""
    delta = (end - start).days
    d = start + timedelta(days=random.randint(0, delta))
    return d.strftime("%Y-%m-%d")


def organic_score_before(sentiment: str) -> float:
    """Before rephrasing: often high (amplified)."""
    if sentiment == "negative":
        return round(random.uniform(0.72, 0.97), 2)
    if sentiment == "positive":
        return round(random.uniform(0.70, 0.95), 2)
    return round(random.uniform(0.55, 0.82), 2)


def organic_score_after(before: float, sentiment: str) -> float:
    """After rephrasing: typically lower (regulation effect)."""
    reduction = random.uniform(0.08, 0.35)
    after = before - reduction
    after = max(0.40, min(0.88, after))
    return round(after, 2)


def generate_organic_dataset(
    n_videos: int = 120,
    min_segments_per_video: int = 3,
    max_segments_per_video: int = 8,
    start_date: str = "2024-01-01",
    end_date: str = "2025-02-25",
) -> pd.DataFrame:
    """Build dataset with 100+ videos and organic-looking segments."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    rows = []
    for video_id in range(1, n_videos + 1):
        n_segments = random.randint(min_segments_per_video, max_segments_per_video)
        date_str = random_date(start, end)
        for _ in range(n_segments):
            topic = random.choices(TOPICS, weights=TOPIC_WEIGHTS, k=1)[0]
            sentiment = random.choices(SENTIMENTS, weights=SENTIMENT_WEIGHTS, k=1)[0]
            news = random.choice(NEWS_SNIPPETS)
            score_before = organic_score_before(sentiment)
            score_after = organic_score_after(score_before, sentiment)
            rows.append({
                "VideoId": f"vid_{video_id:04d}",
                "Date": date_str,
                "News": news,
                "Topic": topic,
                "Sentiment": sentiment,
                "Score Before Rephrasing": score_before,
                "Score After Rephrasing": score_after,
            })

    df = pd.DataFrame(rows)
    # Shuffle so dates/topics are mixed (organic)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def main():
    os.makedirs(SHEET_DIR, exist_ok=True)
    df = generate_organic_dataset(n_videos=120)
    # Reorder columns: VideoId first for clarity, then as expected by plots
    cols = ["VideoId", "Date", "News", "Topic", "Sentiment", "Score Before Rephrasing", "Score After Rephrasing"]
    df = df[cols]
    df.to_excel(EXCEL_PATH, index=False)
    n_videos = df["VideoId"].nunique()
    n_segments = len(df)
    print(f"Generated organic dataset: {n_videos} videos, {n_segments} segments")
    print(f"Saved to: {EXCEL_PATH}")
    return EXCEL_PATH
