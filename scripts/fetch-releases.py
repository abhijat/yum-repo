import dataclasses
import enum
import os.path
import time

import requests

RELEASE_URL = "https://api.github.com/repos/dragonflydb/dragonfly/releases"


class AssetKind(enum.Enum):
    RPM = 1
    DEB = 2


@dataclasses.dataclass
class Package:
    kind: AssetKind
    download_url: str
    version: str
    filename: str

    @staticmethod
    def from_url(url: str) -> "Package":
        tokens = url.split('/')
        filename = tokens[-1]
        kind = AssetKind.RPM if filename.endswith(".rpm") else AssetKind.DEB
        return Package(kind=kind, download_url=url, version=tokens[-2], filename=filename)

    def storage_path(self, root: str) -> str:
        match self.kind:
            case AssetKind.RPM:
                return os.path.join(root, "rpm", self.version)
            case AssetKind.DEB:
                return os.path.join(root, "deb", self.version)


def collect_download_urls() -> list[Package]:
    packages = []
    # TODO retry logic
    response = requests.get(RELEASE_URL)
    releases = response.json()
    for release in releases[:5]:
        for asset in release["assets"]:
            if asset["name"].endswith(".rpm") or asset["name"].endswith(".deb"):
                packages.append(Package.from_url(asset["browser_download_url"]))
    return packages


def download_packages(root: str, packages: list[Package]):
    for package in packages:
        print(f"Downloading {package.download_url}")
        path = package.storage_path(root)
        if not os.path.exists(path):
            os.makedirs(path)

        target = os.path.join(path, package.filename)
        # TODO retry logic
        response = requests.get(package.download_url)
        with open(target, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {package.download_url}")
        time.sleep(0.5)


def main():
    packages = collect_download_urls()
    download_packages("_site", packages)


if __name__ == '__main__':
    main()
