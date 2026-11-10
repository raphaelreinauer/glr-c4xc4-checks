# Release and archival workflow

Software author: Raphael Reinauer. License: MIT, copyright (c) 2026
Raphael Reinauer. The `v1.0.0` release metadata is dated 2026-11-10.
Version `v1.0.0` was published on GitHub and archived on Zenodo on
2026-11-10. Both records were checked after publication.

- [GitHub release](https://github.com/raphaelreinauer/glr-c4xc4-checks/releases/tag/v1.0.0)
- Version-specific DOI: [10.5281/zenodo.24116313](https://doi.org/10.5281/zenodo.24116313)
- All-version concept DOI: [10.5281/zenodo.24116312](https://doi.org/10.5281/zenodo.24116312)
- Archived source commit: `8e4e5918b4cb14cb6d70574be46233c7a04f74fb`
- Archived ZIP SHA-256: `47200ff493780e018b0c420e29775a5ac7d247994daceb341acebddb2e2661bf`

The Zenodo archive was downloaded and all 17 tracked files were compared
byte for byte with the tagged commit. The six checks and the assertion
safeguards passed locally, and GitHub Actions passed at the tagged commit.
Use the version-specific DOI for the paper's software citation. Subsequent
documentation changes on `main` do not alter the frozen `v1.0.0` tag.

## Before publishing a release

1. Confirm the version, release date, author, and license in `CITATION.cff`
   match the release. Validate it with `cffconvert --validate`.
2. Create a fresh virtual environment, install `requirements.txt`, and run
   `python run_checks.py` with assertions enabled. Include the symbolic eta
   certificate and save the complete output as `verification.txt`.
3. Check that `python -O run_checks.py` and a `PYTHONOPTIMIZE=1` invocation
   fail rather than report success.
4. Check the release contains no credentials, virtual environment, private
   manuscript material, absolute research paths, or unrelated code. Check
   the six scripts against `publication/provenance.json`.
5. Review the README's mathematical scope and AI-use disclosure. Finite-range
   checks must not be described as proofs in all dimensions.
6. Commit the tested files and create the version tag at that commit. For
   the first release, use `v1.0.0` and the notes in
   `publication/github-release-notes.md`.

The supplied `verification.txt` records a completed local run. Regenerate
it if any script or runtime dependency changes. This workflow does not
assert that the paper's other authors have performed the software checks.

Keep citation metadata in `CITATION.cff`. Do not add guessed ORCID IDs or
an invented DOI. A `.zenodo.json` file would override `CITATION.cff` in
Zenodo's GitHub integration, so avoid maintaining conflicting metadata.

## GitHub and Zenodo

Choose one archival route for each release.

### GitHub integration

1. Make the GitHub repository public. In Zenodo, link the GitHub account,
   sync repositories, and enable `raphaelreinauer/glr-c4xc4-checks`
   before publishing the GitHub release.
2. Publish the release at the tested version tag. Do not move a published tag.
3. Wait for Zenodo to ingest the release. Check the title, creator, license,
   resource type Software, version, and archived source against the release.

### Manual archive

If the integration is unavailable, create a Zenodo Software record using
one ZIP generated from the tested Git tag, not from the working directory.
Use the same author, MIT license, version, and release date as `CITATION.cff`.
Check the uploaded archive before publishing the record. Do not also create
an integration-generated record for the same release.

### After archiving

Record the DOI of the specific version in the paper's software reference
and availability statement. A later documentation commit can add it to
the README; do not move the archived tag to do so. Future software corrections
should use new versioned releases, not replace the source cited by the paper.

Official instructions:

- [Enable the GitHub repository](https://help.zenodo.org/docs/github/enable-repository/)
- [Archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Describe software using CITATION.cff](https://help.zenodo.org/docs/github/describe-software/citation-file/)

## Zenodo description

Exact-arithmetic verification scripts accompanying Appendix A of
*The Gromov–Lawson–Rosenberg Conjecture for the group Z/4 x Z/4*, by
Noé Bárcenas, Luis Eduardo García-Hernández, and Raphael Reinauer.

The six standalone Python scripts check eta fixed-point sums and Smith
normal forms, primitive symmetry and real Adams spectral-sequence
calculations, exact rational generating-function identities, and mixed
spin-index/Gysin images. They are supplementary checks, not a replacement
for the paper's proofs. The README distinguishes finite-range calculations
from symbolic all-parameter certificates.

The package includes pinned dependencies, a runner that requires assertions,
and an extraction manifest. GitHub Copilot assisted in developing the scripts;
additional AI assistance was used for the repository documentation and runner.

Software creator: Raphael Reinauer. License: MIT.
Version: 1.0.0. Release date: 2026-11-10.

This software is a personal project by Raphael Reinauer.

Copyright (c) 2026 Raphael Reinauer
