# First-release preparation

The GitHub repository is a private staging repository until the license
and release metadata are confirmed. No GitHub release or
Zenodo record has been published. The proposed release is `v1.0.0`.

## Decisions before publication

- [x] Confirm software authors: Raphael Reinauer alone, as confirmed by the
      author on 2026-11-07. No ORCID ID was supplied.
- [ ] Confirm a software license and the right to license every included file.
- [ ] Add the chosen license as `LICENSE`.
- [x] Add root `CITATION.cff` using confirmed software authorship.
- [ ] Add the confirmed license, version `1.0.0`, and actual release date
      to `CITATION.cff` before publication.
- [x] Validate the preparation `CITATION.cff` with cffconvert 2.0.0 against
      schema 1.2.0. Revalidate after adding the release license/version/date.
- [ ] Have the authors review the mathematical scope and AI-use disclosure.
- [ ] Confirm the final manuscript revision corresponding to the release;
      the extraction manifest identifies the current source revision.

Do not put guessed ORCID IDs, an invented DOI, or provisional author credits
into release metadata. Keep a single metadata source: `CITATION.cff` is
enough for this release; adding `.zenodo.json` would override it in Zenodo.

## Verification

- [x] Create a fresh virtual environment and install `requirements.txt`.
- [x] Run `python run_checks.py` without optimization, including the symbolic
      eta certificate. Save the complete output as `verification.txt`.
- [x] Check that `python -O run_checks.py` and a `PYTHONOPTIMIZE=1` invocation
      both fail instead of reporting success.
- [x] Check the prepared files contain no virtual environment, credentials,
      private manuscript material, absolute research paths, or unrelated code.
- [x] Confirm the six extracted scripts agree with `provenance.json`.
- [ ] Commit the final state and record its commit hash in the release notes.

The supplied `verification.txt` records the preparation run. It should be
regenerated if any script or runtime dependency changes.

## GitHub and Zenodo

1. After the decisions above, make the GitHub repository public.
2. Sign in to Zenodo and link the GitHub account if needed. In the profile
   menu choose GitHub, sync repositories, and enable
   `raphaelreinauer/glr-c4xc4-checks` **before** publishing the GitHub release.
3. Create the final `v1.0.0` tag at the tested commit and publish a GitHub
   release using the release-note draft below. Do not move this published tag.
4. Wait for Zenodo to ingest the release. Check title, creators, license,
   resource type Software, version, and source archive against the release.
5. Record the DOI of this specific version. Add it to the paper's software
   reference and availability statement. A later documentation commit can
   add it to the README; do not change the archived source/tag to do so.
6. Future corrections should be new versioned releases, not a replacement
   of the source already cited by the paper.

Official instructions:

- [Enable the GitHub repository](https://help.zenodo.org/docs/github/enable-repository/)
- [Archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Describe software using CITATION.cff](https://help.zenodo.org/docs/github/describe-software/citation-file/)

If integration is unavailable, a manual Zenodo Software upload is an
alternative. Generate one ZIP from the final Git tag, not the working
directory, and upload that single source archive. Do not publish a second
record for the same release through both routes.

## Proposed Zenodo description

Exact-arithmetic verification scripts accompanying Appendix A of
*The Gromov–Lawson–Rosenberg Conjecture for the group Z/4 x Z/4*, by
Noé Bárcenas, Luis Eduardo García-Hernández, and Raphael Reinauer.

The six standalone Python scripts check eta fixed-point sums and Smith
normal forms, primitive symmetry and real Adams spectral-sequence
calculations, exact rational generating-function identities, and mixed
spin-index/Gysin images. The scripts are supplementary checks, not a
replacement for the paper's proofs. The README distinguishes finite-range
calculations from symbolic all-parameter certificates.

The package includes pinned dependencies, a runner that requires assertions,
and an extraction manifest. GitHub Copilot assisted in developing the scripts;
additional AI assistance was used for the repository documentation and runner.

Resource type: Software. Software creator: Raphael Reinauer.
Proposed license: MIT, awaiting approval.
Version: 1.0.0 once released. No DOI has been assigned during preparation.

## Proposed GitHub release notes

First release of the six exact-arithmetic checks listed in Appendix A.

- Eta fixed-point sums, actual target periods, Smith forms, and a symbolic
  universal 2-local diagonalization certificate.
- Primitive complex symmetry and real E3/third-differential rank checks.
- Exact rational identities and mixed spin-index/Gysin calculations.
- Pinned runtime dependencies, execution instructions, and verification output.

These checks support the written proofs. Finite tests are not claimed to
establish all-degree theorems. See README for the exact scope of each script.

Tested source commit: fill from the final release commit, not this draft.
