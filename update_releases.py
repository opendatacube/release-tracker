
import json
import os
from datetime import datetime

import jinja2
import requests
import yaml

def get_github_latest_release(repo):
    """
    Fetches the latest release information from GitHub for a given repository.
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "version": data["tag_name"],
            "published_at": data["published_at"],
        }
    return None

def get_pypi_latest_release(package_name):
    """
    Fetches the latest release information from PyPI for a given package.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "version": data["info"]["version"],
        }
    return None

def main():
    """
    Main function to update release information.
    """
    with open("packages.yaml", "r") as f:
        packages = yaml.safe_load(f)

    release_data = []
    for package in packages:
        github_release = get_github_latest_release(package["github"])
        pypi_release = get_pypi_latest_release(package["pypi_name"])

        release_info = {
            "name": package["name"],
            "pypi_version": pypi_release["version"] if pypi_release else "N/A",
            "github_version": github_release["version"] if github_release else "N/A",
        }

        if github_release:
            published_at = datetime.fromisoformat(github_release["published_at"].replace("Z", "+00:00"))
            release_info["github_release_age_days"] = (datetime.utcnow() - published_at.replace(tzinfo=None)).days

        release_data.append(release_info)

    with open("releases.json", "w") as f:
        json.dump(release_data, f, indent=2)

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("template.html")

    with open("index.html", "w") as f:
        f.write(template.render(releases=release_data))

if __name__ == "__main__":
    main()
