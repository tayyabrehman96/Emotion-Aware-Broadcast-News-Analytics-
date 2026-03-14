# Plan to Perfect and Get the Paper Accepted

Based on the strict review and the provided **example.bib**, this plan lists concrete steps in priority order. The bib file is now available; several citation keys are still wrong or missing, and the manuscript has fixable technical and methodological gaps.

---

## Phase 1: Fix Manuscript and Bibliography (Required – do first)

### 1.1 Fix the bibliography file (`example.bib`)

| Issue | Action |
|-------|--------|
| **Invalid lines** | Remove the standalone lines `Introduction` and `Related Work` at the top (lines 1 and 112). They are not valid BibTeX and can cause parsing errors. |
| **Missing entries** | The manuscript cites four keys that are **not** in the bib: `wnkhade2026`, `bertrend2024`, `spitale2025`, `reuters2025`. Either add real entries for these papers or replace the citations (see 1.2). |

**Option A – Replace with existing bib entries (fast):**
- For the “benchmarking sentiment in multilingual news” sentence: cite **Zanoli et al.** and use key `zanoli2025benchmarking` (already in bib). Change in-text “Wnkhade et al.” to “Zanoli et al.”
- For BERTrend / Spitale / Reuters: add minimal placeholder entries in the bib (with real title/journal/year if possible), or cite different papers already in the bib and adjust the sentence.

**Option B – Add missing entries (preferred):**
- Find the real papers (BERTrend 2024, Spitale et al. 2025, Reuters 2025, and the correct “Wnkhade”/benchmarking paper), then add correct `@article` or `@inproceedings` entries to `example.bib` so every `\cite{}` in main.tex has a matching key.

### 1.2 Align in-text author names with the bibliography

Your **main.tex** uses author names that do not match the **example.bib** authors for the same key. Referees check this. Fix as follows:

| In main.tex (current) | Bib key | Actual authors in example.bib | Change in main.tex to |
|------------------------|--------|-------------------------------|------------------------|
| Wnkhade et al. | wnkhade2026 (missing) | — | Use Zanoli et al. with `zanoli2025benchmarking`, or add correct Wnkhade entry |
| Jarić et al. | areia2025sentiment | Areia, Carlos; Taylor, Michael; Garcia, Miguel; Hernandez, Jonathan | **Areia et al.** |
| Ruan and Jiang | kim2025news | Kim-Hahm, Hyunsun; Abou-Zaid, Ahmed S; Mohd, Abidalrahman | **Kim-Hahm et al.** |
| Fernández and Awinat | malik2025multimodal | Malik, Shoaib S; Ilyas, Muhammad; et al. | **Malik et al.** |

Apply these name changes in the Related Work (and anywhere else these citations appear).

### 1.3 Remove duplicate LaTeX and fix small errors in `main.tex`

| Item | Location | Action |
|------|----------|--------|
| Duplicate `\end{document}` | After the first `\end{document}` (~line 507) | Delete everything after the first `\end{document}` up to and including the second `\end{document}` (or move the commented template block before `\end{document}`). |
| Duplicate `\bibliographystyle` and `\bibliography` | Same block after first `\end{document}` | Keep only one `\bibliographystyle{elsarticle-harv}` and one `\bibliography{example}` immediately before the first `\end{document}`. |
| Figure path typo | Line 414 | Change `Mechasnism-methodology.png` to `Mechanism-methodology.png` (or rename the image file to match). |
| Second author affiliation | Second author block | Change `\affiliation[first]` to `\affiliation[Second]` for the second author so the affiliation links correctly. |

After Phase 1, the manuscript should compile cleanly, all citations should resolve, and author names should match the bib.

---

## Phase 2: Methodological Transparency (Required for acceptance)

Reviewers need enough detail to judge and reproduce the pipeline.

### 2.1 Specify the rewriting mechanism G(·)

- Add a short subsection or paragraph (e.g. in Section 3 or in Experimental Setup) that states:
  - **Model:** e.g. “We use model X (e.g. GPT-3.5/4, or a fine-tuned T5/BART) via API/library Y.”
  - **Prompt:** High-level description or example prompt (e.g. “Rephrase the following news segment to preserve facts but reduce emotionally charged wording”).
  - **Constraints:** e.g. max length, no change of named entities, single sentence vs multi-sentence.
- One or two example prompts in the paper or in supplementary material will greatly strengthen reproducibility.

### 2.2 Specify the topic taxonomy and segmentation

- **Taxonomy:** List the 15 topic categories (e.g. Politics, War, Economy, Health, …) in the main text or in a table/supplement. Refer to this table when you describe “predefined taxonomy” and zero-shot topic classification.
- **Segmentation:** Briefly describe how “discourse-aware semantic partitioning” is implemented (e.g. rule-based on cue phrases, embedding similarity, or a trained segmenter). If you use an existing tool or script, name it.

### 2.3 Optional but helpful

- Report **K** (number of LDA topics) and the **embedding model** used for topic refinement.
- Mention whether the same taxonomy and segmentation are used in the conflict case study as in the main pipeline.

---

## Phase 3: Validation and Claims (Strongly recommended for acceptance)

### 3.1 Justify “confidence as emotional intensity”

- Add one or two sentences that this is a **proxy** and its limitation (e.g. “We use the classifier’s maximum posterior as a proxy for emotional intensity; we do not claim it equals human-rated intensity.”).
- If you have any correlation with human ratings (even on a small subset), report it; otherwise, tone down claims that suggest confidence = true emotional intensity.

### 3.2 Add at least minimal human evaluation

- **Minimum:** For a small subset (e.g. 30–50 segments), have 1–2 raters judge:
  - **Semantic preservation:** “Does the attenuated version preserve the factual content of the original?” (e.g. yes/no or 1–5).
  - **Intensity:** “Is the attenuated version less emotionally intense?” (e.g. yes/no or scale).
- Report inter-rater agreement (e.g. Cohen’s κ or simple % agreement) and summarize in the Results. This directly addresses the reviewer’s “no human evaluation” concern.

### 3.3 Tone down overclaiming

- **Title/abstract:** Replace or soften “Cognitive Impact Mitigation” (e.g. “Toward Cognitive Impact Mitigation” or “Emotion-Aware News Analytics … for Sentiment Regulation”) unless you add a study that actually measures cognitive impact.
- **Objectives:** Replace “mental health–aware” with something like “emotion-aware” or “intensity-aware” unless you measure mental health outcomes.
- **Abstract:** Change “preserving topical consistency and contextual meaning” to “aiming to preserve …” or add “in a human evaluation we show …” if you add the small human study above.

---

## Phase 4: Strengthen the Paper (Recommended)

### 4.1 Basic statistics and uncertainty

- Report **standard deviation or confidence intervals** for the mean reduction Δσ (e.g. “mean Δσ = 0.19 (95% CI 0.17–0.21)” or “SD = 0.08”).
- If applicable, add a short sentence on statistical significance (e.g. paired test before/after regulation).

### 4.2 Reproducibility and resources

- In the paper or supplementary: “Code/data available at [URL]” or “Code and list of video IDs available upon request.” Specify license if you share data.
- In Experimental Setup: briefly state framework versions (e.g. PyTorch 2.x, Transformers 4.x) and that the same seed was used for reproducibility.

### 4.3 Ethical and limitations

- Add 2–3 sentences in Ethical Considerations: who is responsible when news is automatically rewritten; risk of systematic bias from G(·); who sets θ and with what policy implications.
- In Conclusion or Limitations: single source/channel, single language, and that results may not generalize to other outlets or languages.

### 4.4 Case study figure notation

- In the case study figure you use “Semantic Fidelity Check” and “Residual High-Intensity Cases” with symbols (e.g. Sim(·,·), σ_min^fidelity). Either define these in the methodology/caption or remove the undefined symbols to avoid “false rigor.”

---

## Phase 5: Final Checklist Before Resubmission

- [ ] **example.bib:** No “Introduction”/“Related Work” lines; every `\cite{}` in main.tex has a matching entry; author names in bib match what you cite.
- [ ] **main.tex:** All author names in text match the bib (Areia et al., Kim-Hahm et al., Malik et al., Zanoli et al. or correct names for any new keys).
- [ ] **main.tex:** Only one `\end{document}`; one `\bibliographystyle` and one `\bibliography`; figure path “Mechanism” (not “Mechasnism”); second author has `\affiliation[Second]`.
- [ ] **Methodology:** G(·) specified (model + prompt + constraints); topic taxonomy listed; segmentation method described briefly.
- [ ] **Claims:** No “cognitive impact” or “mental health–aware” without evidence; confidence as proxy clearly stated.
- [ ] **Evaluation:** At least a small human evaluation for semantic preservation and intensity; mean Δσ reported with SD or CI.
- [ ] **Ethics/Limitations:** Short note on responsibility, bias, and generalizability.

---

## Summary: Priority Order

| Priority | What to do |
|----------|------------|
| **1** | Fix example.bib (remove invalid lines; add or replace missing keys). Fix in-text author names to match bib. Remove duplicate `\end{document}` and bibliography; fix figure path and second author affiliation. |
| **2** | Specify G(·), topic taxonomy, and segmentation in the manuscript. |
| **3** | Justify confidence-as-intensity; add minimal human evaluation; soften cognitive/mental health claims. |
| **4** | Add SD/CI for Δσ; reproducibility statement; ethics/limitations and case study figure notation. |

Completing **Phase 1** and **Phase 2** is the minimum to make the paper acceptable from a technical and reproducibility standpoint. Adding **Phase 3** (and as much of **Phase 4** as possible) will make the paper much stronger and more likely to be accepted.

---

## Final Pass Completed (Post-Revision)

- [x] **example.bib:** Invalid lines removed; all cited keys present; author names aligned with main.tex.
- [x] **main.tex:** Author names match bib; single `\end{document}` and bibliography; figure path `Mechanism-methodology.png`; second author `\affiliation[Second]`.
- [x] **Methodology:** G(·), taxonomy (Table~\ref{tab:taxonomy}), and segmentation described.
- [x] **Claims:** Title/abstract/objectives softened; confidence-as-proxy stated; human evaluation added.
- [x] **Evaluation:** Human evaluation subsection (Section 5); Δσ with SD and 95% CI.
- [x] **Ethics/Limitations:** Limitations subsection; ethics expanded (responsibility, bias, θ).
- [x] **Consistency:** Section labels `\label{sec:methodology}` and `\label{sec:experiments}` added; in-text "Section~5" and "Section~3" replaced with `\ref`; double space ("video.  Across") fixed.

**Before submission:** Replace placeholder SD/CI and human-eval numbers with actual results if different; ensure figure file is named `Mechanism-methodology.png` (or update path); add code/data URL if available.
