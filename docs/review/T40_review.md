# Review: T40

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### N1. Expected edge counts are hardcoded snapshots

`docs/provenance_split_protocol.md` Section 4.5 hardcodes expected edge counts (e.g., Field.Subfield: 116 extends, 36 instance_of, 152 total) derived from the current source graph `stats.json`. These numbers are correct at the time of this review (verified independently against both `stats.json` files), but if source graphs are ever regenerated or if the `candidate_graphs` directory is rebuilt, these hardcoded values will silently become stale.

**Assessment**: Acceptable for a frozen config protocol. The parenthetical "(from source graph stats.json)" partially indicates the source. No action required now, but T41 should verify actual output edge counts against these expected values and flag any mismatch.

### N2. `_t40_frozen` marker is convention-only

The `_t40_frozen: true` field in both configs is a human-readable marker. The `split_relations_by_provenance.py` script does not validate or enforce this field. A downstream consumer could modify the config without any technical guardrail.

**Assessment**: Acceptable at current governance level. The marker serves its purpose as a documentation signal. Adding code-level enforcement would be over-engineering for this stage.

### N3. `hierarchy_mixed = full source graph` identity is an invariant that must be verified, not assumed

The protocol correctly documents that for both current candidates, `hierarchy_mixed` is identical to the full source graph (since neither has `uses` edges). However, this identity is a contingent property of the current data, not a logical necessity. If a future source graph contains `uses` edges, `hierarchy_mixed` will be a proper subset.

**Assessment**: The protocol already notes this in Section 1 ("Key constraint") and Section 6.3 ("Critical Constraint for T41/T42"). Adequately documented. T41/T42 should programmatically verify node/edge count identity rather than assuming it.

### N4. `docs/05_decision_log.md` changes in the working tree are from prior tasks

The git diff shows changes to `docs/05_decision_log.md` (D022-D025), but these entries document T32/T33/T34 and M3 review decisions, not T40. The T40 worker correctly did not add a decision log entry because T40 produced no key decisions.

**Assessment**: No issue. This is pre-existing dirty working tree state from prior task sessions.

## Missing Tests

None required. T40 is a config-freeze and protocol documentation task. The verification command checks keyword presence across the protocol and configs. Independent verification confirms:

1. Expected edge counts match actual `stats.json` values exactly.
2. The split script (`split_relations_by_provenance.py`) correctly reads the T40 config schema and produces the documented output files.
3. No source code was modified.
4. No historical configs were overwritten.

## Suspicious Implementation Details

None found. Specific checks:

1. **No mock/stub/hardcode**: Both configs are real JSON files pointing to real source graph directories. The protocol references real edge counts verified against `stats.json`.
2. **No fake execution**: The worker correctly did not run the split generation script. Actual split generation is deferred to T41.
3. **No data semantic manipulation**: The `origin_map` (`extends → explicit`, `instance_of → synthesized`) is the natural, documented mapping consistent with Lean's compilation model.
4. **No over-engineering**: The protocol covers exactly what T41/T42 needs (semantics, config index, output convention, expected counts, usage guide, integrity rules) without speculative extensions.

## Recommended Next Action

Captain should mark T40 as complete and advance to T41. T41 worker must:

1. Run the frozen T40 configs through `split_relations_by_provenance.py` to actually generate the six provenance-split graph directories.
2. Verify output edge counts match the expected values in the protocol (Section 4.5).
3. Run structural diagnostics on each of the six split graphs per `docs/diagnostics_protocol.md`.
4. Pay special attention to comparing depth/leaf-ratio/hyperbolicity proxy across explicit-only vs synthesized-only vs hierarchy_mixed.
5. Programmatically verify the `hierarchy_mixed = full source graph` identity for both candidates.
