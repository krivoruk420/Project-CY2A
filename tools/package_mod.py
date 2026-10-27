#!/usr/bin/env python3
"""Package the vehicle game files into a BeamNG-style ZIP archive."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile


VEHICLE_NAME = "hirochi_cuirassier"
ARCHIVE_NAME = f"{VEHICLE_NAME}.zip"


class PackagingError(Exception):
    """Raised when the game tree cannot be packaged as a vehicle mod."""


def collect_vehicle_files(vehicle_dir: Path) -> list[Path]:
    if not vehicle_dir.is_dir():
        raise PackagingError(
            f"Vehicle game directory was not found: {vehicle_dir}. "
            "Add the vehicle files under game/vehicles/hirochi_cuirassier/ first."
        )

    files = sorted(
        path
        for path in vehicle_dir.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    )
    if not files:
        raise PackagingError(
            f"No vehicle files found in {vehicle_dir}; refusing to create an empty mod ZIP."
        )
    return files


def package_mod(project_root: Path, output_dir: Path) -> Path:
    vehicle_dir = project_root / "game" / "vehicles" / VEHICLE_NAME
    files = collect_vehicle_files(vehicle_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / ARCHIVE_NAME

    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for file_path in files:
            relative = file_path.relative_to(vehicle_dir).as_posix()
            archive.write(file_path, f"vehicles/{VEHICLE_NAME}/{relative}")
    return archive_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root (defaults to the parent of tools/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (defaults to <project-root>/dist)",
    )
    args = parser.parse_args(argv)
    output_dir = args.output_dir or args.project_root / "dist"

    try:
        archive = package_mod(args.project_root, output_dir)
    except (PackagingError, OSError) as exc:
        print(f"Packaging failed: {exc}", file=sys.stderr)
        return 1

    print(f"Created mod archive: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
