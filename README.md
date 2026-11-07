# GLR checks for C4 x C4

Exact-arithmetic verification scripts accompanying Appendix A of
*The Gromov–Lawson–Rosenberg Conjecture for the group Z/4 x Z/4*, by
Noé Bárcenas, Luis Eduardo García-Hernández, and Raphael Reinauer.

These are reproducibility checks, not a replacement for the mathematical
proofs. In particular, finite-range checks do not establish all-degree
statements. The geometric interpretation of the matrices and the nonzero
spectral-sequence differential are inputs from the paper.

This repository is being prepared for its first release. The software author
is Raphael Reinauer. The license still needs confirmation. No Zenodo DOI has
been issued for this package, and no public release is claimed here.

## Run the checks

Python 3.10 or newer is required. The reference environment uses Python
3.12.13 and the exact package versions in `requirements.txt`.

From the repository root, on macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_checks.py
```

On Windows, replace `.venv/bin/python` by `.venv\Scripts\python.exe`.

The runner executes all six scripts, including the symbolic eta
certificate. It stops with a nonzero exit code if a script fails. Successful
completion ends with:

```text
PASS: all six scripts completed; symbolic eta certificate included.
```

To omit only the symbolic eta certificate:

```sh
.venv/bin/python run_checks.py --skip-symbolic
```

Every script can also be run separately, for example:

```sh
.venv/bin/python checks/eta_matrix_repair.py --symbolic
.venv/bin/python checks/check_mixed_geometry_spin_indices.py
```

Do not use `python -O`, `python -OO`, or `PYTHONOPTIMIZE`: the checks use
Python assertions. The runner rejects an optimized interpreter. Direct
invocations of the individual scripts do not have this safeguard.

No Sage, GAP, numerical floating-point calculation, external data file, or
network connection is needed to run the checks after installing dependencies.

## What is checked

Section numbers below refer to the November 2026 manuscript. The filenames
match Appendix A.

| Script in `checks/` | Paper | Scope |
| --- | --- | --- |
| `eta_matrix_repair.py` | §6.2 | Exact fixed-point sums for even m = 2,...,40; Smith calculations for d = 0,...,20; constant six-slope bundle matrix. With `--symbolic`, a universal 2-local diagonalization for every positive a divisible by four. |
| `check_ku_d3_symmetry.py` | §5.3 | A finite primitive source/target calculation and exhaustive symmetry test. This selects the unique nonzero invariant functional; it does not establish that the actual differential is nonzero. |
| `check_real_e3_and_d3_lower_bounds.py` | §§5.2, 5.4–5.5 | The actual R2/d2 construction, d2 squared zero, kernel/image quotients, and exhibited third-differential ranks in stems 2,...,31. |
| `check_E3_rational_identities.py` | §5.4 | Exact polynomial/rational identities giving the all-degree generating function and the eight quadratic residue formulas. Not finite fitting. |
| `check_mixed_spin_index.py` | §8.6 | Integral index diagonals, forced h0 corrections, and triangular first-row spanning for N = 2,...,64. |
| `check_mixed_geometry_spin_indices.py` | §§8.5–8.6 | Full mixed spin-index/Gysin computations for N = 1,...,5, in dimensions 6, 10, 14, 18, 22. The A-hat series is truncated to the degree required for these dimensions. The extra real degree-six class is handled in the paper. |

The eta, E3 rational-identity, and mixed-geometry scripts use `python-flint`.
The symbolic eta option also uses SymPy, whose dependency is mpmath. The
remaining three scripts use only the Python standard library.

## Provenance and AI assistance

The six checks were extracted from the manuscript's accompanying source
package. Their mathematical code is unchanged; the eta script's original
machine-local interpreter instruction was replaced by a reference to this
README. Source hashes and the extraction manifest are in
`publication/provenance.json`.

GitHub Copilot was used to assist in developing the verification scripts.
The repository documentation and test runner were prepared with additional
AI assistance. Automated checks do not replace the authors' mathematical
review or responsibility for the submitted software.

## Citation, license, and release

The repository is at
<https://github.com/raphaelreinauer/glr-c4xc4-checks>.

Software citation metadata is in `CITATION.cff`. The software author is
Raphael Reinauer; the accompanying paper has the three authors named above.
License terms must be confirmed before the first release is published.
MIT is proposed, but no reuse license has yet been granted.

The release checklist, proposed Zenodo description, and release notes are in
`publication/RELEASE.md`. The planned first release is `v1.0.0`; this is not
a published version or an assigned DOI. Once archived, cite the DOI of the
specific release used, not only the changing GitHub branch.
