from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trace a Lean repo with LeanDojo and materialize a real trace sample."
    )
    parser.add_argument("--repo-url", required=True, help="GitHub URL of the Lean repo.")
    parser.add_argument("--commit", required=True, help="Commit hash to trace.")
    parser.add_argument("--dst-dir", required=True, type=Path, help="Output directory for traced repo.")
    return parser.parse_args()


def main() -> None:
    try:
        from lean_dojo import LeanGitRepo, trace
    except ImportError as exc:  # noqa: BLE001
        raise SystemExit(
            "LeanDojo is not installed in the current Python environment. "
            "Install it first, then rerun this script."
        ) from exc

    args = parse_args()
    repo = LeanGitRepo(args.repo_url, args.commit)
    trace(repo, dst_dir=str(args.dst_dir))
    print(f"[done] traced repo written to: {args.dst_dir}")


if __name__ == "__main__":
    main()
