import argparse
import json
from datetime import UTC, datetime
import os

import jinja2
import requests
import yaml
from packaging.version import parse as parse_version


def get_github_releases(repo, github_token=None):
    """
    Fetches all release information from GitHub for a given repository.
    """
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    response = requests.get(url, headers=headers)

    if response.status_code == 403 or response.status_code == 429:
        print(
            f"Error: GitHub API rate limit exceeded or forbidden for {repo}. Status code: {response.status_code}"
        )
        exit(1)
    elif response.status_code != 200:
        print(
            f"Error: Failed to fetch GitHub releases for {repo}. Status code: {response.status_code}"
        )
        return None, None

    releases = response.json()
    stable_release = next((r for r in releases if not r["prerelease"]), None)

    latest_stable = None
    if stable_release:
        latest_stable = {
            "version": stable_release["tag_name"],
            "published_at": stable_release["published_at"],
            "url": stable_release["html_url"],
        }

    return latest_stable, None


def get_pypi_releases(package_name):
    """Fetches the latest stable and pre-release information from PyPI for a given package."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Error: Failed to fetch PyPI releases for {package_name}. Status code: {response.status_code}"
        )
        return None, None

    data = response.json()
    releases = data.get("releases", {})

    latest_stable = None
    latest_prerelease = None

    for version_str, version_data in releases.items():
        if not version_data:  # Skip empty release data
            continue

        version = parse_version(version_str)
        published_at = version_data[0].get(
            "upload_time_iso_8601"
        )  # Take the first upload time

        if not published_at:  # Skip if no upload time
            continue

        release_info = {
            "version": version_str,
            "published_at": published_at,
            "url": f"https://pypi.org/project/{package_name}/{version_str}/",
        }

        if version.is_prerelease:
            if (
                latest_prerelease is None
                or parse_version(latest_prerelease["version"]) < version
            ):
                latest_prerelease = release_info
        else:
            if (
                latest_stable is None
                or parse_version(latest_stable["version"]) < version
            ):
                latest_stable = release_info

    return latest_stable, latest_prerelease


def get_conda_forge_releases(package_name):
    """Fetches the latest version from conda-forge for a given package."""
    url = f"https://api.anaconda.org/package/conda-forge/{package_name}"
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Error: Failed to fetch Conda-Forge releases for {package_name}. Status code: {response.status_code}"
        )
        return None

    data = response.json()
    latest_version = data.get("latest_version")
    if latest_version:
        return {
            "version": latest_version,
            "url": f"https://anaconda.org/conda-forge/{package_name}",
        }
    return None


def main():
    """Main function to update release information."""
    parser = argparse.ArgumentParser(
        description="Update Open Data Cube release information."
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Only re-render the HTML from releases.json, do not fetch new data.",
    )
    args = parser.parse_args()

    if args.render_only:
        with open("releases.json", "r") as f:
            release_data = json.load(f)
    else:
        with open("packages.yaml") as f:
            packages = yaml.safe_load(f)

        github_token = os.environ.get("GITHUB_TOKEN")
        github_cache = {}

        release_data = []
        for package in packages:
            github_repo = package["github"]
            if github_repo not in github_cache:
                github_cache[github_repo] = get_github_releases(
                    github_repo, github_token
                )
            github_stable, _ = github_cache[github_repo]

            pypi_stable, pypi_prerelease = get_pypi_releases(package["pypi_name"])
            conda_forge_release = get_conda_forge_releases(package["pypi_name"])

            release_info = {
                "name": package["name"],
                "pypi_name": package["pypi_name"],
                "github_repo": package["github"],
                "pypi_stable_version": pypi_stable["version"] if pypi_stable else "N/A",
                "pypi_stable_url": pypi_stable["url"]
                if pypi_stable
                else f"https://pypi.org/project/{package['pypi_name']}/",
                "pypi_stable_published_at": pypi_stable["published_at"]
                if pypi_stable
                else "N/A",
                "pypi_prerelease": pypi_prerelease,
                "github_stable_version": github_stable["version"]
                if github_stable
                else "N/A",
                "github_stable_url": github_stable["url"]
                if github_stable
                else f"https://github.com/{package['github']}",
                "github_stable_published_at": github_stable["published_at"]
                if github_stable
                else "N/A",
                "conda_forge_version": conda_forge_release["version"]
                if conda_forge_release
                else "N/A",
                "conda_forge_url": conda_forge_release["url"]
                if conda_forge_release
                else f"https://anaconda.org/conda-forge/{package['pypi_name']}",
            }

            release_data.append(release_info)

        with open("releases.json", "w") as f:
            json.dump(release_data, f, indent=2)

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)

    def version_compare_filter(version1, version2):
        return parse_version(version1) > parse_version(version2)

    def to_datetime_filter(date_str):
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    def date_filter(dt_obj, fmt):
        return dt_obj.strftime(fmt)

    template_env.filters["version_compare"] = version_compare_filter
    template_env.filters["to_datetime"] = to_datetime_filter
    template_env.filters["date"] = date_filter

    # Render the combined table template
    template_combined = template_env.get_template("template.html")
    with open("index.html", "w") as f:
        f.write(template_combined.render(releases=release_data, now=datetime.now(UTC)))


if __name__ == "__main__":
    main()
