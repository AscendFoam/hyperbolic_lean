# Review: T63

Verdict: PASS_WITH_WARNINGS

## Blocking Issues

None.

## Non-Blocking Issues

### N1. `.claude/settings.json` appears in working-copy diff

The file shows 16 new permission entries added during the T63 session (conda, kpsewhich, pdflatex, bibtex, rg, PIL checks, etc.). The T63 task package explicitly lists `.claude/settings.json` under Forbidden Scope.

**Mitigating factor**: These entries are Claude Code's auto-permission registration (the runtime writes approved commands to settings.json when the user approves tool calls). The worker did not intentionally edit this file. The content is purely permission patterns, no project logic changed.

**Recommendation**: Revert `.claude/settings.json` to the committed state (`git checkout HEAD -- .claude/settings.json`) before the next task. Do not commit it.

### N2. Figure F2 (`F2_hop_depth_delta.png`) could not be visually verified

MCP image analysis returned error 400 ("图片输入格式/解析错误"). PIL was unavailable in the local Python environment to programmatically verify DPI or dimensions. The file exists on disk (77 KB) and is referenced correctly in `main.tex`, but the reviewer could not independently confirm the chart content matches the spec in `docs/paper_figures_and_tables.md` Section 2 (Figure F2).

**Recommendation**: A human reviewer should visually inspect F2 before submission. Verify the line chart shows HGCN−GCN MAP delta by hop depth with correct values (hop_2: FS≈+0.009/OR≈+0.011; hop_3: FS≈+0.020/OR≈+0.026; hop_4_plus: FS≈+0.031/OR≈+0.039), dagger marker on FS hop_4_plus, and zero-line.

### N3. Figure F1 minor visual artifacts

Image analysis of `F1_provenance_structure.png` revealed:
- Inconsistent y-axis scales across the three panels (explicit_only, synthesized_only, hierarchy_mixed), which may mislead readers comparing across panels.
- A formatting artifact ("1 1" label) visible in the hierarchy_mixed panel, likely a truncated or overlapping annotation.
- Data values themselves appear correct per T41 structural diagnostics.

**Recommendation**: Before submission, regenerate F1 with consistent y-axis ranges (e.g., all panels sharing the same y-max) and fix the "1 1" label.

## Missing Tests

None beyond verification gaps noted above.

T63 is a conversion/rendering task. The verification commands specified in the task package were run by the worker:
- `pdflatex` + `bibtex` compilation: confirmed by presence of `main.pdf`, `main.aux`, `main.bbl`, `main.log` on disk.
- `rg` pattern check: worker reports all required patterns present; reviewer independently confirmed `\documentclass`, `\includegraphics`, `\bibliography`, `\bibliographystyle` in `main.tex`.
- Section count: `rg -c` reports 6 `\section` and 18 `\subsection` commands, matching the worker's claim and the source markdown structure.

## Suspicious Implementation Details

None found.

- All numeric values in `main.tex` are frozen from reviewed T32/T33/T41/T42/T43 artifacts. Spot-checked key values (GCN+0.3143, 1.0000±0.0000 baseline, hop-bucket deltas) against `docs/paper_draft.md` — matches.
- `references.bib` contains 10 entries, all real and citable works (Poincaré embeddings, HGCN, Hyperbolic GCN, DeepMath, TacticToe, LeanDojo, etc.).
- No mock, stub, hardcoded, or placeholder content detected in the LaTeX source.
- The rendering scripts produced actual PNG files (not placeholder images).

## Governance Check

| Check | Result |
| --- | --- |
| Task goal met | Yes — LaTeX source tree + 2 core figures delivered |
| Stayed within Allowed Files | Yes — all created files under `paper/itp/` |
| Avoided Forbidden Scope | **Partial** — `.claude/settings.json` modified (see N1) |
| No mock/stub/hardcode | Pass |
| Docs match reality | Pass — worker summary and README accurately describe deliverables |
| Existing behavior preserved | Pass — no changes to pipeline, data, or experiment code |
| Risks correctly maintained | Pass — R25, R30, R08, R34 all remain Active in `08_risks_and_open_questions.md` |

## Recommended Next Action

1. **Revert** `.claude/settings.json` to the committed state before committing T63 changes.
2. **Human visual inspection** of `F2_hop_depth_delta.png` against the Figure F2 spec.
3. **Consider regenerating** `F1_provenance_structure.png` with consistent y-axis scales across panels.
4. After these cleanup items, T63 output is ready for inclusion in the submission bundle.
