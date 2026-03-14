import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Research-paper style: serif font, larger labels, no "Figure N" in titles
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 150,
})


def _ensure_datetime(date_series):
    """Safely convert a Date column to datetime if possible."""
    try:
        return pd.to_datetime(date_series)
    except Exception:
        return date_series


def _get_group_column_for_videos(data: pd.DataFrame) -> str:
    """
    Decide which column approximates 'video id' for counting N videos.
    Prefer an explicit 'VideoId' column, otherwise fall back to 'Date'.
    """
    if "VideoId" in data.columns:
        return "VideoId"
    return "Date"


def plot_dataset_summary(data: pd.DataFrame, save_path: str, theta: float = 0.8) -> None:
    """
    Figure 1 — Dataset Summary (Table).
    Shows N videos, M segments, avg segments/video, and % amplified segments.
    """
    group_col = _get_group_column_for_videos(data)
    n_videos = data[group_col].nunique()
    n_segments = len(data)
    avg_segments_per_video = n_segments / n_videos if n_videos else float("nan")

    has_scores = "Score Before Rephrasing" in data.columns
    if has_scores:
        amplified_mask = data["Score Before Rephrasing"] >= theta
        pct_amplified = amplified_mask.mean() * 100 if len(data) else 0.0
        amplified_text = f"{pct_amplified:.1f}% (θ={theta:.2f})"
    else:
        amplified_text = "N/A (score column missing)"

    rows = [
        ["Total videos, N", n_videos],
        ["Total segments, M", n_segments],
        ["Mean segments per video", f"{avg_segments_per_video:.2f}" if n_videos else "N/A"],
        ["Amplified segments (σ(0) ≥ θ), %", amplified_text],
    ]

    fig, ax = plt.subplots(figsize=(8, 2 + 0.3 * len(rows)))
    ax.axis("off")

    table = ax.table(
        cellText=[[str(value)] for _, value in rows],
        rowLabels=[label for label, _ in rows],
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.4)

    fig.suptitle("Summary statistics of the news segment dataset", fontsize=12)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_overall_sentiment(data: pd.DataFrame, save_path: str) -> None:
    """
    Figure 2 — Overall Sentiment Distribution.
    Simple bar chart of sentiment counts.
    """
    if "Sentiment" not in data.columns:
        print("Sentiment column missing — skipping Figure 2.")
        return

    order = ["negative", "neutral", "positive"]
    counts = data["Sentiment"].value_counts()
    counts = counts.reindex(order).fillna(0)

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(counts.index, counts.values, color=["red", "gray", "green"])

    for bar, value in zip(bars, counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{int(value)}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_xlabel("Sentiment class")
    ax.set_ylabel("Segment count")
    ax.set_title("Sentiment distribution across segments")
    ax.grid(True, axis="y", linewidth=0.5, alpha=0.6, linestyle="--")

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_topic_frequency(data: pd.DataFrame, save_path: str, top_k: int = 10) -> None:
    """
    Figure 3 — Topic Frequency (Top-K Topics).
    Horizontal bar chart of most frequent topics.
    """
    if "Topic" not in data.columns:
        print("Topic column missing — skipping Figure 3.")
        return

    topic_counts = data["Topic"].value_counts().head(top_k).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, max(4, 0.4 * len(topic_counts))))
    ax.barh(topic_counts.index, topic_counts.values, color="steelblue")

    for value, y in zip(topic_counts.values, range(len(topic_counts))):
        ax.text(value, y, f" {int(value)}", va="center", fontsize=9)

    ax.set_xlabel("Segment count")
    ax.set_ylabel("Topic category")
    ax.set_title("Topic frequency (top-K categories)")
    ax.grid(True, axis="x", linewidth=0.5, alpha=0.6, linestyle="--")

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_topic_sentiment_matrix(
    data: pd.DataFrame, save_path: str, top_k: int = 10
) -> None:
    """
    Figure 4 — Topic × Sentiment Matrix.
    Stacked bar chart: per topic (Top-K by frequency) neg/neu/pos counts.
    """
    required_cols = {"Topic", "Sentiment"}
    if not required_cols.issubset(data.columns):
        print("Topic/Sentiment columns missing — skipping Figure 4.")
        return

    crosstab = (
        data.groupby(["Topic", "Sentiment"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["negative", "neutral", "positive"], fill_value=0)
    )

    # Restrict to Top-K topics by total frequency
    top_topics = crosstab.sum(axis=1).sort_values(ascending=False).head(top_k).index
    crosstab = crosstab.loc[top_topics]

    sentiments = list(crosstab.columns)
    x = np.arange(len(crosstab.index))
    width = 0.6

    fig, ax = plt.subplots(figsize=(10, max(4, 0.4 * len(crosstab))))
    bottom = np.zeros(len(crosstab))

    colors = {"negative": "red", "neutral": "gray", "positive": "green"}

    for sentiment in sentiments:
        values = crosstab[sentiment].values
        ax.bar(
            x,
            values,
            width,
            bottom=bottom,
            label=sentiment.capitalize(),
            color=colors.get(sentiment, None),
        )
        bottom += values

    ax.set_xticks(x)
    ax.set_xticklabels(crosstab.index, rotation=45, ha="right")
    ax.set_ylabel("Segment count")
    ax.set_xlabel("Topic category")
    ax.set_title("Topic–sentiment contingency (stacked counts)")
    ax.grid(True, axis="y", linewidth=0.5, alpha=0.6, linestyle="--")
    ax.legend()

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_topic_sentiment_heatmap(
    data: pd.DataFrame, save_path: str, top_k: int = 10
) -> None:
    """
    Topic × sentiment heatmap (matrix-style view of counts).
    Rows: topics (Top-K by frequency), columns: sentiment classes.
    """
    required_cols = {"Topic", "Sentiment"}
    if not required_cols.issubset(data.columns):
        print("Topic/Sentiment columns missing — skipping Topic × Sentiment heatmap.")
        return

    crosstab = (
        data.groupby(["Topic", "Sentiment"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["negative", "neutral", "positive"], fill_value=0)
    )

    # Restrict to Top-K topics by total frequency
    top_topics = crosstab.sum(axis=1).sort_values(ascending=False).head(top_k).index
    crosstab = crosstab.loc[top_topics]

    values = crosstab.values.astype(float)
    sentiments = list(crosstab.columns)
    topics = list(crosstab.index)

    fig, ax = plt.subplots(figsize=(8, max(4, 0.35 * len(topics))))
    im = ax.imshow(values, aspect="auto", cmap="YlOrRd")

    # Ticks and labels
    ax.set_xticks(np.arange(len(sentiments)))
    ax.set_xticklabels([s.capitalize() for s in sentiments])
    ax.set_yticks(np.arange(len(topics)))
    ax.set_yticklabels(topics)

    ax.set_xlabel("Sentiment class")
    ax.set_ylabel("Topic category")
    ax.set_title("Topic–sentiment contingency (heatmap of segment counts)")

    # Colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Segment count", rotation=90)

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_temporal_trend(data: pd.DataFrame, save_path: str) -> None:
    """
    Figure 5 — Temporal Trend (Daily sentiment counts).
    Line plot per sentiment across days.
    """
    if "Date" not in data.columns or "Sentiment" not in data.columns:
        print("Date/Sentiment columns missing — skipping Figure 5.")
        return

    data = data.copy()
    data["Date"] = _ensure_datetime(data["Date"])

    trend = (
        data.groupby(["Date", "Sentiment"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["negative", "neutral", "positive"], fill_value=0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = {"negative": "red", "neutral": "gray", "positive": "green"}

    for sentiment in trend.columns:
        ax.plot(
            trend.index,
            trend[sentiment],
            marker="o",
            label=sentiment.capitalize(),
            color=colors.get(sentiment, None),
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("Segment count")
    ax.set_title("Temporal trend of daily sentiment counts")
    ax.grid(True, linewidth=0.5, alpha=0.6, linestyle="--")
    ax.legend()

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_regulation_effectiveness(data: pd.DataFrame, save_prefix: str) -> None:
    """
    Figure 6 — Regulation Effectiveness (Before vs After).
    - Histogram of Δσ = σ(0) − σ(*)
    - Scatter of before vs after with diagonal.
    Also prints mean/median reduction and success rate.
    """
    required = {"Score Before Rephrasing", "Score After Rephrasing"}
    if not required.issubset(data.columns):
        print("Score columns missing — skipping Figure 6.")
        return

    scores = data[["Score Before Rephrasing", "Score After Rephrasing"]].dropna()
    if scores.empty:
        print("No valid score pairs found — skipping Figure 6.")
        return

    before = scores["Score Before Rephrasing"]
    after = scores["Score After Rephrasing"]
    delta = before - after

    # Summary statistics
    mean_delta = float(delta.mean())
    median_delta = float(delta.median())
    success_rate = float((delta > 0).mean()) * 100.0

    print("Regulation effectiveness (rephrasing) metrics:")
    print(f"  Mean reduction (before - after): {mean_delta:.4f}")
    print(f"  Median reduction (before - after): {median_delta:.4f}")
    print(f"  Success rate (reduction > 0), %: {success_rate:.2f}%")

    # Histogram / box-style view of Δσ
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(delta, bins=20, color="steelblue", alpha=0.8)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel(r"$\Delta\sigma = \sigma(0) - \sigma(*)$  (intensity reduction)")
    ax.set_ylabel("Segment count")
    ax.set_title("Empirical distribution of sentiment intensity reduction")
    ax.grid(True, axis="y", linewidth=0.5, alpha=0.6, linestyle="--")

    fig.tight_layout()
    fig.savefig(f"{save_prefix}_hist.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Scatter: before vs after with diagonal
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(before, after, alpha=0.5, color="purple", edgecolor="white", linewidth=0.5)
    min_val = min(before.min(), after.min())
    max_val = max(before.max(), after.max())
    ax.plot([min_val, max_val], [min_val, max_val], color="black", linestyle="--", linewidth=1, label="y = x")
    ax.set_xlabel(r"$\sigma(0)$  (pre-rephrasing sentiment score)")
    ax.set_ylabel(r"$\sigma(*)$  (post-rephrasing sentiment score)")
    ax.set_title("Pre- vs. post-rephrasing sentiment intensity")
    ax.grid(True, linewidth=0.5, alpha=0.6, linestyle="--")

    fig.tight_layout()
    fig.savefig(f"{save_prefix}_scatter.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_file(excel_file_path: str, output_dir: str | None = None, theta: float = 0.8, top_k_topics: int = 10) -> None:
    """
    Orchestrator: reads the Excel dataset and generates all figures:
    1) Dataset summary table
    2) Overall sentiment distribution
    3) Topic frequency (Top-K)
    4) Topic × sentiment stacked bars
    5) Temporal sentiment trend
    6) Regulation effectiveness (before vs after)

    Figures are saved as PNG files next to the Excel file by default.
    """
    data = pd.read_excel(excel_file_path)

    if output_dir is None:
        output_dir = os.path.dirname(excel_file_path)
    os.makedirs(output_dir, exist_ok=True)

    # Figure 1
    plot_dataset_summary(
        data,
        save_path=os.path.join(output_dir, "figure1_dataset_summary.png"),
        theta=theta,
    )

    # Figure 2
    plot_overall_sentiment(
        data,
        save_path=os.path.join(output_dir, "figure2_overall_sentiment.png"),
    )

    # Figure 3
    plot_topic_frequency(
        data,
        save_path=os.path.join(output_dir, "figure3_topic_frequency_topk.png"),
        top_k=top_k_topics,
    )

    # Figure 4 (stacked bars)
    plot_topic_sentiment_matrix(
        data,
        save_path=os.path.join(output_dir, "figure4_topic_sentiment_matrix.png"),
        top_k=top_k_topics,
    )

    # Figure 4b (heatmap)
    plot_topic_sentiment_heatmap(
        data,
        save_path=os.path.join(output_dir, "figure4b_topic_sentiment_heatmap.png"),
        top_k=top_k_topics,
    )

    # Figure 5
    plot_temporal_trend(
        data,
        save_path=os.path.join(output_dir, "figure5_temporal_trend.png"),
    )

    # Figure 6
    plot_regulation_effectiveness(
        data,
        save_prefix=os.path.join(output_dir, "figure6_regulation_effectiveness"),
    )

    print(f"All figures saved under: {output_dir}")