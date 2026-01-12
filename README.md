[![Update Releases](https://github.com/opendatacube/release-tracker/actions/workflows/update.yml/badge.svg)](https://github.com/opendatacube/release-tracker/actions/workflows/update.yml)

# Open Data Cube Release Tracker

This repository tracks the latest releases of Open Data Cube packages from PyPI, GitHub and Conda-forge.

**The live release tracker is available at: [https://opendatacube.github.io/release-tracker/](https://opendatacube.github.io/release-tracker/)**

The `update_releases.py` script fetches the latest version information and generates the `releases.json` and `index.html` files. The GitHub Actions workflow in `.github/workflows/update.yml` automates this process.

<!-- START_ODC_RELEASE_TABLE -->
| Package | PyPI Version | PyPI Release Date | Conda-forge Version | Conda-forge Release Date |
|---|---|---|---|---|
| [datacube-core](https://pypi.org/project/datacube/1.9.12/) | 1.9.12 | 2025-12-22 | 1.9.12 | N/A |
| [odc-stac](https://pypi.org/project/odc-stac/0.5.0/) | 0.5.0 | 2025-12-10 | 0.5.0 | N/A |
| [odc-stats](https://pypi.org/project/odc-stats/1.9.7/) | 1.9.7 | 2025-11-03 | 1.0.47 | N/A |
| [odc-geo](https://pypi.org/project/odc-geo/0.5.0/) | 0.5.0 | 2025-12-09 | 0.5.0 | N/A |
| [odc-algo](https://pypi.org/project/odc-algo/1.1.1/) | 1.1.1 | 2025-09-07 | 1.1.1 | N/A |
| [datacube-alchemist](https://pypi.org/project/datacube-alchemist/0.6.7/) | 0.6.7 | 2023-09-01 | N/A | N/A |
| [datacube-ows](https://pypi.org/project/datacube-ows/1.9.7/) | 1.9.7 | 2025-12-22 | N/A | N/A |
| [datacube-explorer](https://pypi.org/project/datacube-explorer/3.1.2/) | 3.1.2 | 2025-12-22 | N/A | N/A |
| [odc-loader](https://pypi.org/project/odc-loader/0.6.2/) | 0.6.2 | 2026-01-09 | 0.6.2 | N/A |
| [odc-dscache](https://pypi.org/project/odc-dscache/1.9.1/) | 1.9.1 | 2025-07-10 | 1.9.1 | N/A |
| [eo-datasets](https://pypi.org/project/eodatasets3/1.9.3/) | 1.9.3 | 2025-05-20 | 1.9.3 | N/A |
| [odc-io](https://pypi.org/project/odc-io/0.2.2/) | 0.2.2 | 2023-11-15 | 0.2.2 | N/A |
| [odc-cloud](https://pypi.org/project/odc-cloud/0.2.5/) | 0.2.5 | 2024-01-17 | 0.2.5 | N/A |
| [odc-ui](https://pypi.org/project/odc-ui/0.2.1/) | 0.2.1 | 2023-11-15 | N/A | N/A |
| [odc-apps-cloud](https://pypi.org/project/odc-apps-cloud/0.2.3/) | 0.2.3 | 2023-11-15 | N/A | N/A |
| [odc-apps-dc-tools](https://pypi.org/project/odc-apps-dc-tools/1.9.7/) | 1.9.7 | 2025-12-22 | 1.9.7 | N/A |
<!-- END_ODC_RELEASE_TABLE -->

# Styling

You can re-render `index.html` more quickly by running `uv run python update_releases.py`, which uses the local JSON data.

This is useful for updating the template or styles
