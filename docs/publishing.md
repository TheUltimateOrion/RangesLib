# Publishing

`rangeslib` publishes to PyPI using PyPI Trusted Publishing. No PyPI API token
should be stored in GitHub secrets.

## Release flow

1. Update `[project].version` in `pyproject.toml`.
2. Update `docs/changelog.md`.
3. Commit and push to `main`.
4. The `Release` workflow validates the project and creates `v<version>` plus a
   GitHub Release.
5. The `Release` workflow starts `publish.yml` with that tag.
6. `publish.yml` builds the tagged distribution and publishes it to PyPI.

GitHub does not trigger a `release: published` workflow from a release created
with `GITHUB_TOKEN`, so `.github/workflows/release.yml` explicitly dispatches
`.github/workflows/publish.yml` for normal version bumps.

## PyPI setup

Before the first publish, configure a trusted publisher on PyPI for this
project.

Use these values:

| Field | Value |
| --- | --- |
| Owner | `TheUltimateOrion` |
| Repository name | `RangesLib` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

The GitHub workflow uses the `pypi` environment. You may add environment
protection rules in GitHub if you want manual approval before publishing.

## Publishing an existing release manually

If a GitHub Release already exists but was not published to PyPI, run the
`Publish to PyPI` workflow manually from the GitHub Actions tab and provide the
tag name, for example `v0.6.0`.

This uses the same trusted publisher configuration as the normal release flow.

## What the workflows publish

The workflows check out the release tag, build the source distribution and
wheel, then publish everything in `dist/` using
`pypa/gh-action-pypi-publish`.

If the PyPI trusted publisher has not been configured yet, the workflow will
fail at the publish step without leaking credentials.
