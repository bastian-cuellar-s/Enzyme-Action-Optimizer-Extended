"""Cross-platform build helper: create sdist+wheel and zip artifacts.

Usage:
    python scripts/build_release.py

This script is intended to work on Windows/macOS/Linux using the same Python
interpreter. It mirrors the behavior of scripts/build_release.ps1 and
scripts/build_release.sh.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd, **kwargs):
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd, **kwargs)


def main():
    project_root = Path(__file__).resolve().parent.parent
    dist_dir = project_root / "dist"

    # Ensure build package is available
    run([sys.executable, "-m", "pip", "install", "--upgrade", "build"])

    # Run build
    run([sys.executable, "-m", "build", "--sdist", "--wheel"], cwd=str(project_root))

    if dist_dir.exists():
        zip_path = dist_dir / "release_artifacts.zip"
        # Remove existing zip if present
        if zip_path.exists():
            zip_path.unlink()
        # Create zip containing only the files in dist/
        shutil.make_archive(
            str(zip_path.with_suffix("")), "zip", root_dir=str(dist_dir)
        )
        print(f"Created {zip_path}")
    else:
        print("No dist folder created.")


if __name__ == "__main__":
    main()
