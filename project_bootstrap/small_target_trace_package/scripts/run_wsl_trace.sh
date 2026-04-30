#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: run_wsl_trace.sh <config-json>" >&2
  exit 1
fi

REPO_ROOT="/mnt/d/Codes/Math/hyperbolic_lean"
CONFIG_PATH="$1"
PYTHON_BIN="$HOME/.venvs/lean-dojo-420/bin/python3"

cd "$REPO_ROOT"
export PATH="$HOME/.elan/bin:$PATH"
export PYTHONPATH="$REPO_ROOT/project_bootstrap/leandojo_graph_scaffold/src"

echo "[wsl] repo_root=$REPO_ROOT"
echo "[wsl] config=$CONFIG_PATH"
echo "[wsl] python=$PYTHON_BIN"
echo "[wsl] lake=$(command -v lake)"
echo "[wsl] git=$(command -v git)"

"$PYTHON_BIN" "$REPO_ROOT/project_bootstrap/leandojo_graph_scaffold/src/trace_repo_with_leandojo.py" \
  --config "$CONFIG_PATH"
