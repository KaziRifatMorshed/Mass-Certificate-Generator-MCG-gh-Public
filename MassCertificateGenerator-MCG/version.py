# -*- coding: utf-8 -*-
"""Version and build metadata for Mass Certificate Generator.

Provides dynamic extraction of git commit hash, build timestamp,
application metadata, Windows console attachment, and cross-platform information.
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from typing import Any

APP_NAME = "MassCertificateGenerator"
APP_DISPLAY_NAME = "Mass Certificate Generator"
ORGANIZATION_NAME = "MCG"
ORGANIZATION_DOMAIN = "kazirifatmorshed.github.io"
APP_VERSION = "1.1.0"
APP_VERSION_STR = f"v{APP_VERSION}"

APP_WEBSITE = "https://kazirifatmorshed.github.io/projects/MassCertificateGenerator.html"
APP_YOUTUBE = "https://youtube.com/playlist?list=PLTkxHCc7JjF0QC4yZf5OXDyFlfzSJvK1v&si=LOEa-Ta0xYcyaq3B"
APP_GITHUB = "https://github.com/KaziRifatMorshed/Mass-Certificate-Generator-MCG-gh-Public"
APP_GITLAB = "https://gitlab.com/KaziRifatMorshed/mass-certificate-generator"

# Fallback git hash if git is unavailable or running from a packaged release
_FALLBACK_GIT_HASH = "21b6942"


def get_git_hash() -> str:
    """Return the short git commit hash (HEAD), or a fallback if git is unavailable."""
    # Check for build-time injected environment variable first
    env_hash = os.environ.get("MCG_GIT_HASH")
    if env_hash:
        return env_hash

    try:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        )
        commit = res.stdout.strip()
        if commit:
            return commit
    except Exception:
        pass
    return _FALLBACK_GIT_HASH


def get_build_timestamp() -> str:
    """Return the build date and time formatted as YYYY-MM-DD_HH-mm-ss."""
    # Check for build-time injected environment variable first
    env_ts = os.environ.get("MCG_BUILD_DATE_TIME")
    if env_ts:
        return env_ts

    # If running in a frozen bundle, use executable timestamp as build time
    if getattr(sys, "frozen", False):
        try:
            mtime = os.path.getmtime(sys.executable)
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d_%H-%M-%S")
        except Exception:
            pass

    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


GIT_HASH_STR: str = get_git_hash()
BUILD_DATE_TIME: str = get_build_timestamp()


def get_full_version_string() -> str:
    """Return full version string including version, commit hash, and build timestamp."""
    return f"{APP_DISPLAY_NAME} {APP_VERSION_STR} (commit: {GIT_HASH_STR}, built: {BUILD_DATE_TIME})"


def get_system_info() -> dict[str, Any]:
    """Return a dictionary of system and runtime dependencies information."""
    import platform

    info: dict[str, Any] = {
        "app_name": APP_NAME,
        "app_display_name": APP_DISPLAY_NAME,
        "app_version": APP_VERSION,
        "app_version_str": APP_VERSION_STR,
        "git_hash": GIT_HASH_STR,
        "build_date_time": BUILD_DATE_TIME,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "os_name": sys.platform,
        "is_frozen": getattr(sys, "frozen", False),
    }

    try:
        import PySide6
        from PySide6.QtCore import qVersion
        info["pyside6_version"] = PySide6.__version__
        info["qt_version"] = qVersion()
    except Exception:
        pass

    try:
        import pymupdf
        info["pymupdf_version"] = pymupdf.__version__
    except Exception:
        pass

    try:
        import pandas
        info["pandas_version"] = pandas.__version__
    except Exception:
        pass

    return info


def setup_windows_console() -> bool:
    """Attach to the parent console on Windows if launched from CMD or PowerShell.

    Standard Qt GUI applications on Windows (compiled with console=False)
    do not write output to the console when launched from Command Prompt or PowerShell.
    This attaches to the parent process console and redirects stdout and stderr to CONOUT$.
    Returns True if attached, False otherwise.
    """
    if sys.platform != "win32":
        return False

    try:
        import ctypes
        from ctypes import wintypes

        # ATTACH_PARENT_PROCESS is (DWORD)-1
        ATTACH_PARENT_PROCESS = wintypes.DWORD(-1)
        kernel32 = ctypes.windll.kernel32
        if kernel32.AttachConsole(ATTACH_PARENT_PROCESS):
            # Reopen stdout and stderr to the console output device
            sys.stdout = open("CONOUT$", "w", encoding="utf-8", buffering=1)
            sys.stderr = open("CONOUT$", "w", encoding="utf-8", buffering=1)
            print(f"\n[{APP_DISPLAY_NAME}] CLI output attached ({APP_VERSION_STR} - {GIT_HASH_STR}).\n")
            return True
    except Exception:
        pass
    return False
