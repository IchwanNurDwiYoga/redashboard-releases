"""Generate or update release-repo/version.json with SHA-256 for a new installer build."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path

REPO_SLUG = "IchwanNurDwiYoga/redashboard-releases"


def compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Update version.json for ReDashboard releases.")
    parser.add_argument("--version", required=True, help="Semantic version, e.g. 0.2.0")
    parser.add_argument("--installer", required=True, help="Path to built ReDashboard-Setup-X.Y.Z.exe")
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Changelog bullet item (can be passed multiple times)",
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[1] / "version.json"),
        help="Output path for version.json",
    )
    args = parser.parse_args()

    version = args.version.strip().lstrip("vV")
    installer_path = Path(args.installer)
    if not installer_path.is_file():
        raise SystemExit(f"Installer tidak ditemukan: {installer_path}")

    sha256 = compute_sha256(installer_path)
    tag = f"v{version}"
    asset_name = installer_path.name
    payload = {
        "version": version,
        "published_at": date.today().isoformat(),
        "release_url": f"https://github.com/{REPO_SLUG}/releases/tag/{tag}",
        "download_url": f"https://github.com/{REPO_SLUG}/releases/download/{tag}/{asset_name}",
        "sha256": sha256,
        "changelog": args.note or [f"Pembaruan ReDashboard {tag}"],
    }

    out_path = Path(args.output)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {out_path} -> {tag} (SHA-256: {sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
