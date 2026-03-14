# Strict Journal Review: *Emotion-Aware News Analytics: A Deep NLP Framework for Topic Extraction, Sentiment Scaling, and Cognitive Impact Mitigation*

**Manuscript:** `main.tex`  
**Target journal:** Journal of Information Processing Systems  
**Review type:** Critical / strict  

---

## 1. Summary of the Work

The manuscript proposes an **Emotion-Aware Multi-modal News Analytics Framework** that:
- Ingests broadcast news videos (YouTube), transcribes them (ASR), segments transcripts semantically, applies LDA + embedding-based topic assignment, transformer-based sentiment classification, and an **emotional amplification** proxy (sentiment confidence score).
- Introduces a **sentiment attenuation** mechanism: when confidence ≥ threshold (θ = 0.80), segments are iteratively rephrased (up to R = 5 times) and the version with lowest sentiment confidence is kept.
- Reports experiments on **120 videos** over **15 months**, yielding **639 segments**, with ~**45.2%** “amplified,” mean pre-regulation score **0.81**, post **0.62**, mean reduction **Δσ = 0.19**.

---

## 2. Statistics of the Work (As Reported)

| Quantity | Value |
|----------|--------|
| Observation window | 15 months (Jan 2024 – Mar 2025) |
| Total videos (N) | 120 |
| Total segments (M) | 639 |
| Mean segments per video | 5.33 |
| Sentiment: Negative | 245 (38.3%) |
| Sentiment: Neutral | 253 (39.6%) |
| Sentiment: Positive | 141 (22.1%) |
| Amplified segments (σ⁽⁰⁾ ≥ 0.80) | 289 (45.2%) |
| Mean pre-regulation score | 0.81 |
| Mean post-regulation score | 0.62 |
| Mean reduction Δσ | 0.19 |
| Topic categories | 15 |
| Conflict (War) case study segments | 62 |
| Conflict segments exceeding θ | >60% |
| Max rewriting iterations R | 5 |
| Amplification threshold θ | 0.80 |

---

## 3. Flaws and Critical Issues (Strict Review)

### 3.1 Citation–Author Mismatches (Serious)

- **Wnkhade et al.** cited as `\cite{wnkhade2026}` — key suggests different author; year 2026 is future-dated.
- **Jarić et al.** cited but key is `areia2025sentiment` — author key does not match.
- **Ruan and Jiang** cited but key is `kim2025news` — clear mismatch.
- **Fernández and Awinat** cited but key is `malik2025multimodal` — clear mismatch.

**Verdict:** Suggests either misattribution or placeholder/wrong keys. Unacceptable for publication without correction and verification of every citation.

### 3.2 Bibliography and Reproducibility

- Manuscript references `\bibliography{example}` but **no `example.bib`** is provided in the submission context. Referee cannot verify references.
- **Duplicate blocks:** `\bibliographystyle`, `\bibliography`, and a second `\end{document}` appear after the first `\end{document}` (around lines 507–518 and 731–759), which is invalid and indicates poor manuscript hygiene.

### 3.3 Conceptual and Methodological Weaknesses

- **Confidence as “emotional intensity”:** The paper treats **classifier confidence** (max softmax probability) as a proxy for “emotional amplification.” This is a strong, largely **unjustified** assumption. Confidence reflects model certainty, not necessarily strength of emotion in the text. No validation (e.g., correlation with human intensity ratings) is provided.
- **No human evaluation:** There is no human assessment of (i) semantic preservation after rewriting, (ii) perceived emotional intensity, or (iii) quality/readability of attenuated text. All claims about “semantic-preserving” regulation rest on the design, not on empirical evidence.
- **Single source, single channel:** Data from one YouTube channel (implied) over 15 months. No multi-source or cross-outlet validation. Generalizability to “digital news ecosystems” is overstated.
- **Black-box rephrasing:** The function G(·) (rewriting) is not specified. Model (e.g., which LLM/API), prompts, and constraints are not given. Reproducibility of the attenuation mechanism is impossible.
- **Topic taxonomy:** “Fifteen news categories” and “predefined taxonomy” are mentioned but the actual taxonomy (e.g., list of labels) is not provided. LDA + embedding refinement is described but key implementation details (K, embedding model, similarity aggregation) are vague.
- **Segmentation:** “Discourse-aware semantic partitioning” is claimed but the method (model, rules, or algorithm) is not specified. Segment boundaries could heavily affect topic and sentiment statistics.

### 3.4 Presentation and Technical Errors

- **Figure path typo:** `Mechasnism-methodology.png` (line 414) — “Mechasnism” should be “Mechanism”; build will fail if the file is named correctly.
- **Author/affiliation mismatch:** Second author has `\author[Second]` but `\affiliation[first]` — should be `\affiliation[Second]` for correct tagging.
- **Redundant/unused notation:** In the case study figure, “Semantic Fidelity Check” and “Residual High-Intensity Cases” use symbols (e.g., Sim(·,·), σ_min^fidelity) that are **not defined or used** in the methodology or algorithms. This creates false rigor.

### 3.5 Overclaiming and Wording

- “Cognitive impact mitigation” in the title and “mental health–aware” in the objectives imply a link to cognitive/mental health outcomes. The work does not measure any cognitive or health variable; it only modifies text and reports confidence scores. This is **overclaiming**.
- Abstract claims “preserving topical consistency and contextual meaning” without any quantitative or human evaluation of preservation.
- “Scalable” is asserted without reporting runtimes, throughput, or cost (e.g., API calls for G(·)).

### 3.6 Ethical and Scope

- Ethical considerations are brief and generic. No discussion of (i) editorial responsibility when automatically rewriting news, (ii) risk of systematic bias by G(·), or (iii) who decides θ and the policy implications of “regulation.”

---

## 4. Weaknesses (Structured)

1. **Validation:** No human evaluation of attenuation quality, semantic preservation, or emotional intensity; no external benchmark or baseline (e.g., non-attenuated vs attenuated in a user study).
2. **Reproducibility:** Missing bibliography file; rewriting mechanism G(·) and topic taxonomy not specified; segmentation method not detailed; code/data not indicated.
3. **Generalizability:** Single data source; one language (implied); one ASR/sentiment/topic setup.
4. **Theoretical link:** Confidence ≡ emotional intensity is assumed, not validated; no link to psychology or communication theory beyond citation.
5. **Evaluation depth:** No significance testing, confidence intervals, or ablations (e.g., effect of R, θ, or choice of G).
6. **Manuscript quality:** Citation errors, duplicate blocks, typo in figure path, author/affiliation inconsistency.

---

## 5. Strengths

1. **Problem:** Addressing both detection and “regulation” of emotional intensity in broadcast news is timely and relevant.
2. **Structure:** Pipeline (ASR → segmentation → topic → sentiment → attenuation → storage) is clearly laid out and algorithm boxes help readability.
3. **Formalism:** Notation is largely consistent; equations for LDA, similarity, attenuation loop, and dataset D are clear.
4. **Case study:** Conflict-centric (War) case study is a good choice and the discussion of “reducible exaggeration” vs “intrinsic severity” is thoughtful.
5. **Figures/tables:** Tables for notation, dataset profile, and experimental setup are useful; temporal and topic–sentiment visualizations support the narrative.
6. **Writing:** Generally clear and professional; related work is broad and recent (2023–2026).

---

## 6. Verdict (Strict)

- **Recommendation:** **Major revision (reject-and-resubmit)**. The manuscript is not acceptable in its current form for the same reasons a strict referee would require major revisions: citation errors, missing bibliography, unreproducible core component (G(·)), no human or external validation, and overclaiming (cognitive/mental health impact).
- **Minimum for acceptance:**  
  - Fix all citation–author correspondences and provide a complete, correct `.bib`.  
  - Remove duplicate `\end{document}` and bibliography blocks; fix figure path and author/affiliation.  
  - Specify G(·) (model, prompts, constraints) and the topic taxonomy; describe segmentation.  
  - Add human evaluation of semantic preservation and/or perceived intensity for a subset of attenuated segments.  
  - Tone down claims (e.g., “cognitive impact mitigation,” “mental health–aware”) or add matching empirical evidence.  
  - Add basic uncertainty quantification (e.g., CIs or variance for Δσ) and, if possible, multi-source or cross-channel validation.

---

## 7. Minor Points (Checklist for Revisions)

- [ ] Replace “Mechasnism” with “Mechanism” in figure filename or path.
- [ ] Set second author’s affiliation to `[Second]`.
- [ ] Define or remove symbols in the case study figure (e.g., Sim, σ_min^fidelity).
- [ ] Ensure all cited references exist in `example.bib` and keys match in-text author names and years.
- [ ] Remove or comment duplicate `\bibliographystyle`, `\bibliography`, and the second `\end{document}`.

---

*End of review.*
