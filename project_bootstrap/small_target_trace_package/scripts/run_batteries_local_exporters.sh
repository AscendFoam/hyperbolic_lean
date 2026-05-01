#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="/mnt/d/Codes/Math/hyperbolic_lean"
TRACED_REPO_ROOT="$WORKSPACE_ROOT/data/raw/leandojo_trace/traced_batteries_v420_small/batteries"
SOURCE_LEAN_DIR="$WORKSPACE_ROOT/project_bootstrap/leandojo_graph_scaffold/lean"
LOCAL_TOOL_DIR="$TRACED_REPO_ROOT/.codex_local_exporters"
LOCAL_OUTPUT_DIR="$TRACED_REPO_ROOT/.codex_local_export_output"
WORKSPACE_REL_OUT="$WORKSPACE_ROOT/data/interim/lean_meta_relations/batteries_precise_hierarchy_v1"
WORKSPACE_DECL_INDEX_OUT="$WORKSPACE_ROOT/data/interim/normalized_trace/batteries_declaration_index.tsv"
WORKSPACE_LOG_DIR="$WORKSPACE_ROOT/artifacts/logs/batteries_local_exporters"

mkdir -p "$WORKSPACE_LOG_DIR"
rm -rf "$LOCAL_TOOL_DIR" "$LOCAL_OUTPUT_DIR"
mkdir -p "$LOCAL_TOOL_DIR" "$LOCAL_OUTPUT_DIR"

cp "$SOURCE_LEAN_DIR/ExportPreciseHierarchy.lean" "$LOCAL_TOOL_DIR/ExportPreciseHierarchy.lean"
cp "$SOURCE_LEAN_DIR/ExportDeclarationIndex.lean" "$LOCAL_TOOL_DIR/ExportDeclarationIndex.lean"
cp "$SOURCE_LEAN_DIR/PrintPreciseHierarchyStats.lean" "$LOCAL_TOOL_DIR/PrintPreciseHierarchyStats.lean"

cd "$TRACED_REPO_ROOT"
export PATH="$HOME/.elan/bin:$PATH"

echo "[local-export] traced_repo=$TRACED_REPO_ROOT"
echo "[local-export] tool_dir=$LOCAL_TOOL_DIR"
echo "[local-export] output_dir=$LOCAL_OUTPUT_DIR"
echo "[local-export] lake=$(command -v lake)"
echo "[local-export] lean=$(command -v lean || true)"

PRECISE_LOG="$WORKSPACE_LOG_DIR/export_precise_hierarchy.log"
DECL_LOG="$WORKSPACE_LOG_DIR/export_declaration_index.log"
STATS_LOG="$WORKSPACE_LOG_DIR/print_precise_stats.log"

set +e
lake env lean --run "$LOCAL_TOOL_DIR/PrintPreciseHierarchyStats.lean" Batteries \
  >"$STATS_LOG" 2>&1
STATS_EXIT=$?
lake env lean --run "$LOCAL_TOOL_DIR/ExportPreciseHierarchy.lean" Batteries "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1" \
  >"$PRECISE_LOG" 2>&1
PRECISE_EXIT=$?
lake env lean --run "$LOCAL_TOOL_DIR/ExportDeclarationIndex.lean" Batteries "$LOCAL_OUTPUT_DIR/batteries_declaration_index.tsv" \
  >"$DECL_LOG" 2>&1
DECL_EXIT=$?
set -e

echo "[local-export] stats_exit=$STATS_EXIT"
echo "[local-export] precise_exit=$PRECISE_EXIT"
echo "[local-export] decl_exit=$DECL_EXIT"

if [[ -d "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1" ]]; then
  find "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1" -maxdepth 2 -type f | sed -n '1,20p'
fi
if [[ -f "$LOCAL_OUTPUT_DIR/batteries_declaration_index.tsv" ]]; then
  ls -l "$LOCAL_OUTPUT_DIR/batteries_declaration_index.tsv"
fi

if [[ ! -f "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1/nodes.tsv" ]] || [[ ! -f "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1/relations.tsv" ]]; then
  echo "[local-export][error] precise hierarchy outputs missing"
  echo "[local-export][error] inspect log: $PRECISE_LOG"
  exit 1
fi

if [[ ! -f "$LOCAL_OUTPUT_DIR/batteries_declaration_index.tsv" ]]; then
  echo "[local-export][error] declaration index output missing"
  echo "[local-export][error] inspect log: $DECL_LOG"
  exit 1
fi

rm -rf "$WORKSPACE_REL_OUT"
mkdir -p "$WORKSPACE_REL_OUT"
cp "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1/nodes.tsv" "$WORKSPACE_REL_OUT/nodes.tsv"
cp "$LOCAL_OUTPUT_DIR/batteries_precise_hierarchy_v1/relations.tsv" "$WORKSPACE_REL_OUT/relations.tsv"
cp "$LOCAL_OUTPUT_DIR/batteries_declaration_index.tsv" "$WORKSPACE_DECL_INDEX_OUT"

echo "[local-export][done] precise hierarchy copied to: $WORKSPACE_REL_OUT"
echo "[local-export][done] declaration index copied to: $WORKSPACE_DECL_INDEX_OUT"
echo "[local-export][done] logs:"
echo "  $STATS_LOG"
echo "  $PRECISE_LOG"
echo "  $DECL_LOG"
