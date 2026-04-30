from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trace a Lean repo with LeanDojo and materialize a real trace sample."
    )
    parser.add_argument("--config", type=Path, help="Optional JSON config path.")
    parser.add_argument("--repo-url", help="GitHub URL of the Lean repo.")
    parser.add_argument("--commit", help="Commit hash to trace.")
    parser.add_argument("--dst-dir", type=Path, help="Output directory for traced repo.")
    parser.add_argument(
        "--build-deps",
        dest="build_deps",
        action="store_true",
        help="Whether to trace dependency packages as well.",
    )
    parser.add_argument(
        "--no-build-deps",
        dest="build_deps",
        action="store_false",
        help="Trace only the target repo and skip dependency extraction when possible.",
    )
    parser.add_argument(
        "--num-procs",
        type=int,
        help="Override LeanDojo NUM_PROCS to control memory usage during tracing.",
    )
    parser.set_defaults(build_deps=None)
    return parser.parse_args()


def load_config(path: Path | None) -> dict:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_trace_args(args: argparse.Namespace) -> tuple[str, str, Path, bool, int | None]:
    config = load_config(args.config)
    repo_url = args.repo_url or config.get("repo_url")
    commit = args.commit or config.get("commit")
    dst_dir_value = args.dst_dir or config.get("dst_dir")
    build_deps = args.build_deps
    if build_deps is None:
        build_deps = bool(config.get("build_deps", True))
    num_procs = args.num_procs if args.num_procs is not None else config.get("num_procs")
    if not repo_url or not commit or not dst_dir_value:
        raise SystemExit(
            "Missing trace arguments. Provide either --config or the full set of "
            "--repo-url, --commit, and --dst-dir."
        )
    if num_procs is not None:
        try:
            num_procs = int(num_procs)
        except (TypeError, ValueError) as exc:
            raise SystemExit("num_procs must be an integer.") from exc
        if num_procs <= 0:
            raise SystemExit("num_procs must be positive.")
    return repo_url, commit, Path(dst_dir_value), bool(build_deps), num_procs


def patch_leandojo_windows_git_detection() -> None:
    """Patch LeanDojo's POSIX-only git repo check when running on Windows."""
    if os.name != "nt":
        return

    def _is_git_repo(path: Path) -> bool:
        try:
            subprocess.run(
                ["git", "-C", str(Path(path).resolve()), "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except Exception:  # noqa: BLE001
            return False

    import lean_dojo.utils as lean_dojo_utils
    from lean_dojo.data_extraction import lean as lean_module
    from lean_dojo.data_extraction import traced_data as traced_data_module

    lean_dojo_utils.is_git_repo = _is_git_repo
    lean_module.is_git_repo = _is_git_repo
    traced_data_module.is_git_repo = _is_git_repo


def apply_num_procs_override(num_procs: int | None) -> None:
    if num_procs is None:
        return
    os.environ["NUM_PROCS"] = str(num_procs)


def main() -> None:
    args = parse_args()
    repo_url, commit, dst_dir, build_deps, num_procs = resolve_trace_args(args)
    apply_num_procs_override(num_procs)

    try:
        from lean_dojo import LeanGitRepo, trace
    except ImportError as exc:  # noqa: BLE001
        raise SystemExit(
            "LeanDojo is not installed in the current Python environment. "
            "Install it first, then rerun this script."
        ) from exc

    patch_leandojo_windows_git_detection()
    repo = LeanGitRepo(repo_url, commit)
    trace(repo, dst_dir=str(dst_dir), build_deps=build_deps)
    print(f"[done] traced repo written to: {dst_dir}")


if __name__ == "__main__":
    main()
