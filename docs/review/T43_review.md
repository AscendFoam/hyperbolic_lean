# Review: T43

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### N1. FS synthesized_only GCN MAP value is incorrect in Section 5.1 table

The table in Section 5.1 shows:

```
| Field.Subfield | 0.6857 ± 0.1140* | 0.6857 ± 0.1140 | — |
```

Both the GCN and HGCN columns show 0.6857 ± 0.1140 with delta "—". However, the T42 aggregate.json for `provenance_gcn_field_subfield_synthesized_only_t42` records GCN MAP mean = 1.0000, std = 0.0000. The value 0.6857 is the HGCN MAP, incorrectly duplicated into the GCN column.

The correct row should show GCN MAP ≈ 1.0000 ± 0.0000 (aggregate) with delta "GCN +0.3143". The `*` marker has no explicit footnote in the table.

**Assessment**: This is a copy-paste error. The surrounding narrative text correctly states "GCN matches or outperforms HGCN on the flat synthesized graphs" and Section 5.2 correctly notes the aggregate is 1.0000. The synthesized_only is explicitly labeled as controlled diagnostic, not primary evidence, so the main provenance-conditional conclusion is unaffected. However, the table is factually wrong and should be corrected before external publication.

### N2. `.claude/settings.json` modified again

Same pattern as T14, T31, T42, and other tasks — an automatic tool artifact, not an intentional worker change.

**Assessment**: Rejected/excluded from commit per established precedent. This file is not in T43's Allowed Files.

### N3. R04 status remains "Mitigated" with provenance-conditional qualification

This was flagged as N4 in the T42 review. The T43 worker kept the "Mitigated" status with thorough provenance-conditional qualification text. The original risk scope was "relation layer 过浅, 双曲价值不足" — about the overall relation layer. On the full graph (hierarchy_mixed), the conclusion is still "GCN ahead."

**Assessment**: The qualification text is now more precise than in T42, and T43's formal summary strengthens the conditional framing. The mitigation text explicitly states "R04 的缓解是 provenance-conditional 的，不是对整体 relation layer 的无条件结论." This is defensible. Whether "Partially Mitigated" would be more precise is a classification judgment call that doesn't affect the validity of T43's work.

## Missing Tests

None required. T43 is a summary and governance task with no code changes. Both verification commands from the task package produce the expected keyword matches:

1. `rg -n "explicit_only|synthesized_only|hierarchy_mixed|primary evidence|controlled diagnostic|reproducibility check|4/5 seeds|aggregate|per-seed|conditional" docs\experiment_reports\provenance_summary.md` — all keywords present, with correct contextual usage.

2. `rg -n "T43|provenance_summary|Current Unique Task|R28|conditional" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md` — all governance docs have T43 references.

Independent verification confirms:

1. **Main deliverable exists**: `docs/experiment_reports/provenance_summary.md` is a 10-section report synthesizing T41 structural diagnostics and T42 provenance-aware seed sweeps.

2. **Three-way provenance split roles correctly assigned**: explicit_only = primary evidence (Section 4), synthesized_only = controlled diagnostic (Section 5), hierarchy_mixed = reproducibility check (Section 6). All three roles are explicitly stated with bold labels in the report.

3. **Primary evidence numbers match T42**: FS explicit_only GCN MAP 0.5256 ± 0.0800, HGCN MAP 0.6503 ± 0.0481, delta +0.1247 ✓. OR explicit_only GCN MAP 0.5836 ± 0.0978, HGCN MAP 0.6393 ± 0.0656, delta +0.0557 ✓.

4. **Hop bucket numbers match T42**: FS hop_4_plus delta +0.2471 ✓, OR hop_4_plus delta +0.2708 ✓.

5. **Precision constraint — 4/5 seeds**: Section 4.2 explicitly states "computed over **4 of 5 seeds**" for FS hop_4_plus ✓.

6. **Precision constraint — aggregate/per-seed discrepancy**: Section 5.2 explicitly describes the discrepancy (aggregate 1.0000 vs per-seed 0.8100/0.9029) and registers it as a follow-up item ✓.

7. **Reproducibility check numbers match T32/T33**: hierarchy_mixed MAP values byte-identical ✓.

8. **Governance docs updated**: D029 added to decision log, task board updated with T43 execution note and T42 completion, handoff updated with items 70-71 and Section 8 rewrite, risks updated (R04, R06, R27 → Mitigated; R28 added; Open Questions 3, 4, 5 updated).

9. **No code changes**: Only documentation and governance files were modified.

10. **No T40/T41/T42 semantics modified**: No provenance split directories, configs, artifact data, or frozen protocol documents were changed.

## Suspicious Implementation Details

None found. Specific checks:

1. **No over-engineering**: The report covers exactly what the task package requires — synthesizing T41 and T42 into a provenance-conditional conclusion with precision notes. No speculative extensions.

2. **Correct provenance hierarchy respected**: explicit_only as primary, synthesized_only as controlled diagnostic, hierarchy_mixed as reproducibility check — all three roles clearly stated and correctly handled.

3. **No proxy-as-theorem**: The report frames results as "provenance-conditional" rather than claiming universal model superiority.

4. **Variance is honest**: High-std values (e.g., FS GCN explicit_only MAP std = 0.0800) are reported without suppression.

5. **No new experiments**: The worker correctly confined work to summary and governance updates.

6. **Candidate graph size limitation acknowledged**: Section 9.4 explicitly notes both graphs are small (133–253 nodes) and generalization requires further evidence.

## Recommended Next Action

Captain should mark T43 as complete and close Milestone 4. The project is now ready for Milestone 5 (T50: paper contribution skeleton). Before external publication, fix N1 (FS synthesized_only table value) and resolve R28 (aggregate/per-seed discrepancy root cause).
