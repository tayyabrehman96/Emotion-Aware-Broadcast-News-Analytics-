# Emotion-Aware Broadcast News Analytics

Repository accompanying the paper **"Emotion-Aware Broadcast News Analytics: An Integrated Deep Learning Pipeline for Topic Extraction, Sentiment Intensity Scaling, and Semantic-Preserving Regulation"** (submitted to Knowledge-Based Systems).

This codebase implements the experimental pipeline for segment-level topic modeling, sentiment analysis, and semantic-preserving intensity regulation on broadcast news content. It is provided for reproducibility and peer review.

---

## Repository structure

| Path | Description |
|------|-------------|
| `main.py` | **Main entry point** — runs the full pipeline: segmentation, topic labeling, sentiment analysis, rephrasing, and export. |
| `codes.py` | YouTube API integration (search, download) and video transcription (AssemblyAI). |
| `transcript_and_segmentation.py` | Video-to-segment pipeline using AssemblyAI (transcription + IAB-based segmentation). |
| `semantic_segmentation.py` | Text-based semantic segmentation (AI21 Semantic Text Splitter). |
| `modeling.py` | Topic modeling (LDA, Gensim) and taxonomy mapping with embeddings (spaCy, GloVe). |
| `sentiment_analysis.py` | Sentiment classification (zero-shot BART) and iterative rephrasing loop. |
| `rephrase.py` | Semantic-preserving rephrasing (Google Generative AI) to reduce emotional intensity. |
| `save_data.py` | Export of results to Excel (date, segment, topic, sentiment, scores). |
| `plot_data.py` | Plotting utilities for dataset summary and paper figures (run separately; outputs not in repo). |
| `run_plots_and_save_png.py` | Script to regenerate figures from saved data. |
| `generate_organic_dataset.py` | Helper to generate synthetic/organic dataset for testing. |
| `main.tex` | LaTeX source of the manuscript. |
| `example.bib` | Bibliography. |
| `requirements.txt` | Python dependencies. |
| `.env.example` | Template for API keys and configuration (copy to `.env`). |

Generated outputs (figures, Excel files, downloaded media) are excluded via `.gitignore`; reviewers may reproduce them using the instructions below.

---

## Requirements

- **Python** 3.10 or higher  
- **GPU** (optional but recommended for transformer inference)  
- **API keys** (see Setup)

---

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   # or:  .venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Configuration and API keys**  
   Copy `.env.example` to `.env` and set the required keys (see that file).  
   **Do not commit `.env`.** For production and review, use environment variables or a secrets manager.

   - YouTube Data API key (video search/download)  
   - AssemblyAI API key (transcription / IAB segmentation)  
   - Google Generative AI API key (rephrasing)  
   - AI21 API key (if using `semantic_segmentation.py` text splitter)

---

## Usage

**Run the full pipeline (main code)**

- Edit `main.py` to set the input video path or use the YouTube search/download flow (uncomment the relevant blocks).
- Ensure the Excel output path and any local paths match your environment.
- Run:
  ```bash
  python main.py
  ```
  This will: transcribe/segment input, label topics, run sentiment analysis, apply rephrasing where needed, and save results to the configured Excel file.

**Regenerate figures (optional)**

- After running the pipeline and saving data, use:
  ```bash
  python run_plots_and_save_png.py
  ```
  Output figures are written to disk and are not tracked in the repository.

---

## Models and tools

- **Transcription:** AssemblyAI (cloud).  
- **Segmentation:** AssemblyAI IAB categories (`transcript_and_segmentation.py`) or AI21 Semantic Text Splitter (`semantic_segmentation.py`).  
- **Topic modeling:** Gensim LDA + optional GloVe/spaCy for taxonomy mapping (`modeling.py`).  
- **Sentiment:** Hugging Face `facebook/bart-large-mnli` zero-shot pipeline.  
- **Rephrasing:** Google Generative AI (Gemini) for semantic-preserving attenuation.

Details and hyperparameters (e.g. threshold, number of rephrasing attempts) are described in the paper.

---

## Citation

If you use this code or build on this work, please cite:

```bibtex
@article{emotion-aware-news-analytics,
  title={Emotion-Aware Broadcast News Analytics: An Integrated Deep Learning Pipeline for Topic Extraction, Sentiment Intensity Scaling, and Semantic-Preserving Regulation},
  author={Rehman, Tayyab and Mustafa, Muzzamil},
  journal={Knowledge-Based Systems},
  year={2025},
  note={Submitted}
}
```

---

## License and data

Code is provided for research and review. Use of third-party APIs (YouTube, AssemblyAI, Google, AI21) is subject to their respective terms. Researchers are responsible for obtaining any required data and API keys and for compliance with applicable ethics and data-protection guidelines.
