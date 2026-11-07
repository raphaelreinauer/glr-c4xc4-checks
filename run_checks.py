#!/usr/bin/env python3
"""Run the six Appendix A checks with assertions enabled."""

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
CHECKS = (
    "eta_matrix_checks.py",
    "check_ku_d3_symmetry.py",
    "check_real_e3_and_d3_lower_bounds.py",
    "check_E3_rational_identities.py",
    "check_mixed_spin_index.py",
    "check_mixed_geometry_spin_indices.py",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-symbolic", action="store_true",
        help="omit the all-parameter eta certificate (finite eta tests still run)",
    )
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    if not __debug__ or sys.flags.optimize:
        parser.error("assertions are disabled; remove -O/-OO and PYTHONOPTIMIZE")

    dependencies = ("python-flint",) if args.skip_symbolic else (
        "python-flint", "sympy", "mpmath"
    )
    print(f"Python {sys.version.split()[0]}", flush=True)
    try:
        for package in dependencies:
            print(f"{package} {version(package)}", flush=True)
    except PackageNotFoundError as error:
        parser.error(f"missing dependency {error.name}; install requirements.txt")

    for name in CHECKS:
        relative = Path("checks") / name
        options = ["--symbolic"] if (
            name == "eta_matrix_checks.py" and not args.skip_symbolic
        ) else []
        print(f"\n=== {relative.as_posix()} {' '.join(options)} ===".rstrip(), flush=True)
        try:
            subprocess.run(
                [sys.executable, "-u", str(ROOT / relative), *options],
                cwd=ROOT, check=True,
            )
        except subprocess.CalledProcessError as error:
            print(f"FAIL: {relative.as_posix()} exited with {error.returncode}",
                  file=sys.stderr, flush=True)
            return 1

    certificate = "omitted" if args.skip_symbolic else "included"
    print(f"\nPASS: all six scripts completed; symbolic eta certificate {certificate}.",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
