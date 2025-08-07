# Open DataCube Release Tracker

This repository tracks the latest releases of Open DataCube packages from PyPI and GitHub.

The `update_releases.py` script fetches the latest version information and generates the `releases.json` and `index.html` files.

The GitHub Actions workflow in `.github/workflows/update.yml` automates this process.

# Styling

You can rerender `index.html` more quickly by running `uv run python update_releases.py`, which uses the local JSON data.

This is useful for updating the template or styles
