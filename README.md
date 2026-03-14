# Emotion-Aware Broadcast News Analytics

Repository accompanying the paper **"Emotion-Aware Broadcast News Analytics: An Integrated Deep Learning Pipeline for Topic Extraction, Sentiment Intensity Scaling, and Semantic-Preserving Regulation"** (submitted to Knowledge-Based Systems).

This repository contains **only the implementation**: main code, model/training logic, API integration, and numbered result images. It does not include the paper source (LaTeX/BibTeX).

---

## Repository structure

| Path | Description |
|------|-------------|
| `main.py` | **Main entry point** — full pipeline: segmentation, topic labeling, sentiment analysis, rephrasing, export. |
| `codes.py` | YouTube API (search, download) and video transcription (AssemblyAI). |
| `transcript_and_segmentation.py` | Video-to-segment pipeline (AssemblyAI transcription + IAB segmentation). |
| `semantic_segmentation.py` | Text-based semantic segmentation (AI21 Semantic Text Splitter). |
| `modeling.py` | Topic modeling (LDA, Gensim) and taxonomy mapping (spaCy, GloVe). |
| `sentiment_analysis.py` | Sentiment classification (zero-shot BART) and iterative rephrasing loop. |
| `rephrase.py` | Semantic-preserving rephrasing (Google Generative AI). |
| `save_data.py` | Export to Excel (date, segment, topic, sentiment, scores). |
| `plot_data.py` | Plotting utilities for dataset summary and figures. |
| `run_plots_and_save_png.py` | Regenerate numbered figures from saved data. |
| `generate_organic_dataset.py` | Helper to generate synthetic dataset for testing. |
| `results_images/` | **Numbered result images** (e.g. `figure1.png`, `figure2.png`) — add your outputs here. |
| `requirements.txt` | Python dependencies. |
| `.env.example` | Template for API keys (copy to `.env`). |

Other generated outputs (Excel, downloads) remain untracked; only `results_images/*.png` and `*.jpg` are committed.

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

**Regenerate result images**

- After running the pipeline and saving data:
  ```bash
  python run_plots_and_save_png.py
  ```
  Save the generated figures as `figure1.png`, `figure2.png`, etc. in `results_images/` to include them in the repo.

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
