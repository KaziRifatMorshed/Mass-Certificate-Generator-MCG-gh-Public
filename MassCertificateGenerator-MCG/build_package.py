#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-platform build and packaging script for Mass Certificate Generator.

Supports Nuitka (default, high performance & minimal footprint) and PyInstaller.
Avoids heavy assets/frameworks (LLVM, PyArrow, SciPy, Jupyter, etc.).
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime


def get_git_commit_hash() -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=3,
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


def ensure_icons(repo_dir: str):
    ico_path = os.path.join(repo_dir, "extra", "MCG_logo.ico")
    png_path = os.path.join(repo_dir, "extra", "MCG_logo.png")
    if not os.path.exists(ico_path) and os.path.exists(png_path):
        try:
            from PIL import Image
            img = Image.open(png_path)
            sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save(ico_path, sizes=sizes)
            print("[*] Generated extra/MCG_logo.ico from PNG")
        except Exception as e:
            print(f"[!] Warning: Could not generate .ico file: {e}")


def build_with_nuitka(repo_dir: str) -> tuple[int, str]:
    print("[*] Building with Nuitka (C-compiled standalone)...")
    import pymupdf
    pymupdf_dir = os.path.dirname(pymupdf.__file__)
    cpu_count = min(os.cpu_count() or 4, 4)

    nuitka_cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--static-libpython=no",
        "--enable-plugin=pyside6",
        "--noinclude-qt-translations",
        "--include-data-dir=extra=extra",
        f"--include-data-dir={pymupdf_dir}=pymupdf",
        "--nofollow-import-to=pymupdf,llvmlite,numba,pyarrow,scipy,matplotlib,IPython,jupyter,notebook,bokeh,panel,lief,sqlalchemy,sphinx,tornado,pytest,sklearn,skimage,torch,dask",
        f"--jobs={cpu_count}",
        "--low-memory",
        "--no-deployment-flag=excluded-module-usage",
        "--output-dir=dist",
        "--output-filename=MassCertificateGenerator",
        "main.py",
    ]
    res = subprocess.run(nuitka_cmd)
    if res.returncode != 0:
        return res.returncode, ""

    exe_suffix = ".exe" if sys.platform == "win32" else ""
    # Nuitka standalone creates dist/main.dist/ or dist/MassCertificateGenerator.dist/
    candidates = [
        os.path.join(repo_dir, "dist", "main.dist", f"main{exe_suffix}"),
        os.path.join(repo_dir, "dist", "main.dist", f"MassCertificateGenerator{exe_suffix}"),
        os.path.join(repo_dir, "dist", "MassCertificateGenerator.dist", f"MassCertificateGenerator{exe_suffix}"),
        os.path.join(repo_dir, "dist", f"MassCertificateGenerator{exe_suffix}"),
    ]
    binary_path = next((c for c in candidates if os.path.isfile(c)), "")
    return 0, binary_path


def build_with_pyinstaller(repo_dir: str) -> tuple[int, str]:
    print("[*] Building with PyInstaller (stripped heavy assets)...")
    spec_path = os.path.join(repo_dir, "MassCertificateGenerator.spec")
    print(f"[*] Executing PyInstaller with: {spec_path}")
    pyinstaller_cmd = [sys.executable, "-m", "PyInstaller", spec_path, "--noconfirm", "--clean"]
    res = subprocess.run(pyinstaller_cmd)
    if res.returncode != 0:
        return res.returncode, ""

    exe_suffix = ".exe" if sys.platform == "win32" else ""
    binary_path = os.path.join(repo_dir, "dist", f"MassCertificateGenerator{exe_suffix}")
    return 0, binary_path


def package_linux(repo_dir: str, binary_path: str, png_path: str):
    import tarfile
    import version

    pkg_name = f"MassCertificateGenerator-{version.APP_VERSION_STR}-linux-x86_64"
    pkg_dir = os.path.join(repo_dir, "dist", pkg_name)
    os.makedirs(pkg_dir, exist_ok=True)

    target_bin = os.path.join(pkg_dir, "MassCertificateGenerator")

    # If Nuitka standalone directory, copy all runtime dependencies into package folder
    bin_parent = os.path.dirname(binary_path)
    if os.path.isdir(bin_parent) and os.path.basename(bin_parent).endswith(".dist"):
        for item in os.listdir(bin_parent):
            s = os.path.join(bin_parent, item)
            d = os.path.join(pkg_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        # Ensure executable name matches MassCertificateGenerator
        produced_bin = os.path.join(pkg_dir, os.path.basename(binary_path))
        if produced_bin != target_bin and os.path.isfile(produced_bin):
            shutil.move(produced_bin, target_bin)
    else:
        shutil.copy2(binary_path, target_bin)

    os.chmod(target_bin, 0o755)

    if os.path.exists(png_path):
        shutil.copy2(png_path, os.path.join(pkg_dir, "MCG_logo.png"))

    desktop_content = """[Desktop Entry]
Type=Application
Name=Mass Certificate Generator
GenericName=Certificate Generator
Comment=Generate bulk certificates with custom fonts, layouts, and CSV/Excel data
Exec=MassCertificateGenerator %F
Icon=mass-certificate-generator
Terminal=false
Categories=Office;Publishing;Graphics;Utility;
Keywords=certificate;pdf;generator;bulk;batch;
StartupNotify=true
"""
    desktop_path = os.path.join(pkg_dir, "MassCertificateGenerator.desktop")
    with open(desktop_path, "w", encoding="utf-8") as f:
        f.write(desktop_content)

    install_script = """#!/usr/bin/env bash
set -e

INSTALL_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
APP_DIR="${HOME}/.local/share/MassCertificateGenerator/app"

mkdir -p "$INSTALL_DIR" "$DESKTOP_DIR" "$ICON_DIR" "$APP_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Mass Certificate Generator..."

# Copy all application files to APP_DIR
cp -r "$SCRIPT_DIR"/* "$APP_DIR/"
chmod +x "$APP_DIR/MassCertificateGenerator"

# Create symlink in INSTALL_DIR
ln -sf "$APP_DIR/MassCertificateGenerator" "$INSTALL_DIR/MassCertificateGenerator"

if [ -f "$SCRIPT_DIR/MCG_logo.png" ]; then
    cp "$SCRIPT_DIR/MCG_logo.png" "$ICON_DIR/mass-certificate-generator.png"
fi

sed -e "s|^Exec=.*|Exec=$INSTALL_DIR/MassCertificateGenerator %F|" \\
    -e "s|^Icon=.*|Icon=$ICON_DIR/mass-certificate-generator.png|" \\
    "$SCRIPT_DIR/MassCertificateGenerator.desktop" > "$DESKTOP_DIR/MassCertificateGenerator.desktop"
chmod +x "$DESKTOP_DIR/MassCertificateGenerator.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo "Mass Certificate Generator successfully installed to $INSTALL_DIR!"
echo "You can launch it from your desktop application menu or run 'MassCertificateGenerator' in terminal."
"""
    install_path = os.path.join(pkg_dir, "install.sh")
    with open(install_path, "w", encoding="utf-8") as f:
        f.write(install_script)
    os.chmod(install_path, 0o755)

    uninstall_script = """#!/usr/bin/env bash
INSTALL_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
APP_DIR="${HOME}/.local/share/MassCertificateGenerator/app"

echo "Uninstalling Mass Certificate Generator..."
rm -f "$INSTALL_DIR/MassCertificateGenerator"
rm -rf "$APP_DIR"
rm -f "$DESKTOP_DIR/MassCertificateGenerator.desktop"
rm -f "$ICON_DIR/mass-certificate-generator.png"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo "Uninstallation complete."
"""
    uninstall_path = os.path.join(pkg_dir, "uninstall.sh")
    with open(uninstall_path, "w", encoding="utf-8") as f:
        f.write(uninstall_script)
    os.chmod(uninstall_path, 0o755)

    archive_path = os.path.join(repo_dir, "dist", f"{pkg_name}.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(pkg_dir, arcname=pkg_name)
    print(f"[SUCCESS] Linux distribution package: {archive_path}")


def main() -> int:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)

    parser = argparse.ArgumentParser(
        description="Build and package Mass Certificate Generator.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "builder_pos",
        nargs="?",
        choices=["nuitka", "pyinstaller"],
        default=None,
        help="Optional positional builder name: 'nuitka' or 'pyinstaller'.",
    )
    parser.add_argument(
        "--builder", "-b",
        choices=["nuitka", "pyinstaller"],
        default="nuitka",
        help="Build tool to use (default: nuitka).",
    )
    args = parser.parse_args()
    builder = args.builder_pos if args.builder_pos else args.builder

    print("=" * 60)
    print("  Mass Certificate Generator - Cross-Platform Build Script")
    print("=" * 60)
    print(f"[*] Selected Builder: {builder.upper()}")

    # 1. Extract Git Commit Hash
    git_hash = get_git_commit_hash()
    print(f"[*] Git Commit Hash : {git_hash}")
    os.environ["MCG_GIT_HASH"] = git_hash

    # 2. Extract Build Timestamp
    build_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"[*] Build Timestamp : {build_time}")
    os.environ["MCG_BUILD_DATE_TIME"] = build_time

    # 3. Generate Windows Icon (.ico) if missing
    ensure_icons(repo_dir)
    png_path = os.path.join(repo_dir, "extra", "MCG_logo.png")

    # 4. Execute Selected Builder
    if builder == "nuitka":
        code, dist_binary = build_with_nuitka(repo_dir)
    else:
        code, dist_binary = build_with_pyinstaller(repo_dir)

    if code != 0 or not dist_binary:
        print(f"[!] Build failed with exit code {code}")
        return code or 1

    print(f"[SUCCESS] Binary created: {dist_binary}")

    # 5. On Windows, check for Inno Setup compiler (ISCC)
    if sys.platform == "win32":
        iscc_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
            shutil.which("ISCC.exe"),
        ]
        iscc_exe = next((p for p in iscc_paths if p and os.path.isfile(p)), None)
        if iscc_exe:
            iss_script = os.path.join(repo_dir, "winInstallationInnoScript.iss")
            print(f"[*] Compiling Inno Setup installer using: {iscc_exe}")
            res_iss = subprocess.run([iscc_exe, iss_script])
            if res_iss.returncode == 0:
                print("[SUCCESS] Windows installer generated in dist/installer/")
            else:
                print("[!] Warning: Inno Setup compilation exited with error.")
        else:
            print("[*] Inno Setup 6 (ISCC.exe) not found. Skipping installer creation.")

    # 6. On Linux, generate .desktop file, installer scripts, and .tar.gz bundle
    elif sys.platform.startswith("linux"):
        package_linux(repo_dir, dist_binary, png_path)

    print("=" * 60)
    print("  Build completed successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
