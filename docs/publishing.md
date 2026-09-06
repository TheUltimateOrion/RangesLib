# Publishing

`rangeslib` publishes to PyPI from GitHub Releases using PyPI Trusted
Publishing. No PyPI API token should be stored in GitHub secrets.

## Release flow

1. Update `[project].version` in `pyproject.toml`.
2. Update `docs/changelog.md`.
3. Commit and push to `main`.
4. The `Release` workflow validates the project and creates `v<version>` plus a
   GitHub Release.
5. The `Publish to PyPI` workflow builds the tagged release and publishes the
   distributions to PyPI.

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

## What the workflow publishes

The workflow runs only for non-prerelease GitHub Releases. It checks out the
release tag, builds the source distribution and wheel, then publishes everything
in `dist/` using `pypa/gh-action-pypi-publish`.

If the PyPI trusted publisher has not been configured yet, the workflow will
fail at the publish step without leaking credentials.
