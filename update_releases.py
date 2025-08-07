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
        print(f"Error: GitHub API rate limit exceeded or forbidden for {repo}. Status code: {response.status_code}")
        exit(1)
    elif response.status_code != 200:
        print(f"Error: Failed to fetch GitHub releases for {repo}. Status code: {response.status_code}")
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


def main():
    """Main function to update release information."""
    with open("packages.yaml") as f:
        packages = yaml.safe_load(f)

    github_token = os.environ.get("GITHUB_TOKEN")

    release_data = []
    for package in packages:
        github_stable, _ = get_github_releases(package["github"], github_token)
        pypi_stable, pypi_prerelease = get_pypi_releases(package["pypi_name"])

        release_info = {
            "name": package["name"],
            "pypi_name": package["pypi_name"],
            "github_repo": package["github"],
            "pypi_stable_version": pypi_stable["version"] if pypi_stable else "N/A",
            "pypi_stable_url": pypi_stable["url"]
            if pypi_stable
            else f"https://pypi.org/project/{package['pypi_name']}/",
            "github_stable_version": github_stable["version"]
            if github_stable
            else "N/A",
            "github_stable_url": github_stable["url"]
            if github_stable
            else f"https://github.com/{package['github']}",
        }

        if pypi_stable and pypi_stable["published_at"]:
            published_at = datetime.fromisoformat(pypi_stable["published_at"])
            release_info["pypi_stable_age_days"] = (
                datetime.now(UTC) - published_at
            ).days
        else:
            release_info["pypi_stable_age_days"] = "N/A"

        if pypi_prerelease and pypi_prerelease["published_at"]:
            pypi_prerelease_published_at = datetime.fromisoformat(
                pypi_prerelease["published_at"]
            )
            pypi_prerelease_age_days = (
                datetime.now(UTC) - pypi_prerelease_published_at
            ).days

            if pypi_stable and parse_version(
                pypi_prerelease["version"]
            ) > parse_version(pypi_stable["version"]):
                release_info["pypi_stable_version"] += (
                    f'<br><span class="prerelease">{pypi_prerelease["version"]} ({pypi_prerelease_age_days} days old)</span>'
                )

        if github_stable and github_stable["published_at"]:
            published_at = datetime.fromisoformat(
                github_stable["published_at"].replace("Z", "+00:00")
            )
            release_info["github_stable_age_days"] = (
                datetime.now(UTC) - published_at
            ).days
        else:
            release_info["github_stable_age_days"] = "N/A"

        release_data.append(release_info)

    with open("releases.json", "w") as f:
        json.dump(release_data, f, indent=2)

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)

    # Render the combined table template
    template_combined = template_env.get_template("template.html")
    with open("index.html", "w") as f:
        f.write(template_combined.render(releases=release_data))


if __name__ == "__main__":
    main()
