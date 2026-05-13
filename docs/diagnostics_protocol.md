# Diagnostics Protocol

> 更新时间：2026-05-13
>
> 状态：T22 reviewed heuristic diagnostics protocol。本文用于筛查 traced hierarchy graph 是否适合进入下一轮 benchmark / training；它不是理论结论，也不是最终 benchmark 排名。

## 1. Purpose

本文把 `T20` 与 `T21` 已审阅诊断中的经验判断固化成统一模板，避免后续 worker：

1. 只看 raw hierarchy score 就直接提升候选优先级。
2. 把 shallow forest / star forest 误写成“适合验证双曲优势”的图。
3. 把临时审计语言误写成正式 benchmark 结论。

## 2. Required Inputs

每次诊断至少收集以下字段：

- `relation nodes`
- `relation positive edges`
- `largest_relation_component`
- `longest chain`
- `leaf ratio`
- `multi-parent count`
- `ancestor_added_nodes`

从上面派生两个门控量：

```text
component ratio = largest_relation_component / relation nodes
closure expansion ratio = ancestor_added_nodes / relation nodes
```

说明：

- `relation positive edges` 是当前 positive scale 代理量。
- `component ratio` 衡量连续性。
- `closure expansion ratio` 衡量该候选对 ancestor closure 的依赖程度。

## 3. Heuristic Flags

以下阈值是经验模板，不是理论边界；只服务于当前 traced Lean / Mathlib hierarchy diagnostics。

### 3.1 Shallow Forest Flag

满足任一条件即可标记为 `shallow forest risk`：

1. `longest chain <= 4`
2. `longest chain <= 6` 且 `leaf ratio >= 0.70`
3. `component ratio < 0.50` 且 `leaf ratio >= 0.70`

### 3.2 Star-Forest Flag

满足全部条件时标记为 `star-forest risk`：

1. `longest chain <= 3`
2. `leaf ratio >= 0.75`
3. `multi-parent count` 很低，或结构观察显示大量节点直接挂到少数中心节点

### 3.3 Positive-Scale Flag

按 `relation positive edges` 分层：

- `< 100`: 太小，只适合作为诊断参考
- `100-249`: 可作 controlled probe
- `>= 250`: 才有资格进入默认 follow-up 候选讨论
- `>= 800`: 可单独考虑为 depth stress-test 的大规模候选

### 3.4 Continuity Flag

按 `component ratio` 分层：

- `< 0.50`: 碎片化明显
- `0.50-0.64`: 可接受但仍有连续性风险
- `>= 0.65`: 连续性较好

### 3.5 Closure-Expansion Flag

按 `closure expansion ratio` 分层：

- `<= 0.60`: closure 负担可接受
- `0.60-0.80`: closure 偏重，需要在报告中显式提示
- `> 0.80`: closure-heavy，不宜直接当默认 benchmark

## 4. Candidate Role Gates

### 4.1 Default Follow-Up Candidate

默认下一轮 benchmark 候选需要同时满足：

1. `longest chain >= 8`
2. `relation positive edges >= 250`
3. `component ratio >= 0.65`
4. `leaf ratio <= 0.60`
5. `closure expansion ratio <= 0.60`
6. 不触发 `star-forest risk`

### 4.2 Depth Stress-Test

如果满足：

1. `longest chain >= 10`
2. `relation positive edges >= 800`
3. 但 `component ratio < 0.65` 或 `leaf ratio > 0.60`

则标记为 `depth stress-test`，而不是默认 benchmark。

### 4.3 Controlled Probe

如果满足：

1. `longest chain >= 8`
2. `relation positive edges` 在 `100-249`
3. `component ratio >= 0.40`
4. `leaf ratio <= 0.60`

则可标记为 `controlled probe`。若 `closure expansion ratio > 0.60`，必须额外注明 `closure-heavy`。

### 4.4 Diagnostic-Only

满足任一条件即可归为 `diagnostic-only`：

1. 触发 `star-forest risk`
2. `longest chain <= 4`
3. `relation positive edges < 100`
4. `leaf ratio >= 0.75` 且没有足够 positive scale 抵消结构风险

## 5. Current Calibration Against Reviewed Candidates

基于 `docs/candidate_graph_audit.md` 当前 reviewed 数值，模板应给出以下角色：

| candidate | expected role | reason |
| --- | --- | --- |
| `Mathlib.Algebra.Order.Ring` | default follow-up candidate | depth、positive scale、continuity 最平衡 |
| `Mathlib.Algebra.Order` | depth stress-test | depth 与 scale 很强，但碎片化且 leaf-heavy |
| `Mathlib.Algebra.Ring.Subring` | controlled probe | 深度足够但规模较小，且 closure-heavy |
| `Mathlib.Algebra.Field.Subfield` | controlled probe | 深度足够但规模较小，且 closure-heavy |
| `Batteries.*` top candidates | diagnostic-only | too shallow and too small |

这组映射是当前模板校准点，不是永久排序。

## 6. Required Report Language

诊断报告必须显式写出：

1. 这是 `heuristic` 判断，不是正式 benchmark 结论。
2. 该图属于 `default follow-up candidate`、`depth stress-test`、`controlled probe` 或 `diagnostic-only` 中哪一类。
3. 如果图因为 `positive scale`、`component ratio` 或 `closure expansion ratio` 被降级，必须写出降级原因。
4. 不得把 `reviewed diagnostic priority` 直接写成“最终 benchmark 排序”。

## 7. Report Template

```md
## Diagnostic Gate Summary

- Scope: existing diagnostics only / no retraining / no new benchmark claim.
- Candidate:
- Role:
- Heuristic status: pass / pass-with-risk / diagnostic-only

| metric | value | heuristic band | note |
| --- | ---: | --- | --- |
| relation nodes |  |  |  |
| relation positive edges |  | <100 / 100-249 / >=250 / >=800 |  |
| longest chain |  | <=4 / 5-7 / >=8 / >=10 |  |
| leaf ratio |  | >=0.75 risk / 0.60-0.74 caution / <=0.60 better |  |
| component ratio |  | <0.50 risk / 0.50-0.64 caution / >=0.65 better |  |
| ancestor_added_nodes |  |  |  |
| closure expansion ratio |  | <=0.60 / 0.60-0.80 / >0.80 |  |

### Judgment

- Shallow forest risk:
- Star-forest risk:
- Positive-scale assessment:
- Continuity assessment:
- Closure assessment:

### Recommended Use

- Default follow-up candidate / depth stress-test / controlled probe / diagnostic-only
- Not a final benchmark conclusion.
```

## 8. Governance Notes

1. 后续若 `T30+` 训练结果、`T40+` provenance split 或更大 traced graph 改变结构分布，应重新校准这些阈值。
2. 本文不会替代 `docs/06_eval_protocol.md` 的主协议；它只是结构诊断的配套门控。
3. 本文不关闭 `R14` 或 `R16`，只把它们从“口头经验”提升为“显式模板”。
