import hashlib
import os
import struct
import tempfile


def sanitize_font_for_embedding(font_path: str) -> str:
    """Check if font has restricted embedding permissions (never-embed / fsType != 0).

    If restricted, creates a cached copy with embedding restrictions fully cleared (fsType = 0)
    and valid table checksums, so PyMuPDF/MuPDF can embed it cleanly without triggering
    'substitute font creation is not implemented yet'. Handles TTF, OTF, and TTC collections.
    Returns the path to be used for rendering (either original or sanitized file).
    """
    if not font_path or not os.path.isfile(font_path):
        return font_path

    try:
        with open(font_path, "rb") as f:
            data = bytearray(f.read())
        if len(data) < 12:
            return font_path

        modified = False

        # Support TrueType Collections (.ttc)
        if data[:4] == b"ttcf":
            if len(data) >= 12:
                num_fonts = struct.unpack_from(">I", data, 8)[0]
                for font_idx in range(num_fonts):
                    if len(data) < 12 + (font_idx + 1) * 4:
                        break
                    font_offset = struct.unpack_from(">I", data, 12 + font_idx * 4)[0]
                    if len(data) < font_offset + 12:
                        continue
                    num_tables = struct.unpack_from(">H", data, font_offset + 4)[0]
                    for i in range(num_tables):
                        entry_offset = font_offset + 12 + i * 16
                        if len(data) < entry_offset + 16:
                            break
                        tag, checksum, offset, length = struct.unpack_from(">4sIII", data, entry_offset)
                        if tag == b"OS/2":
                            if len(data) >= offset + 10:
                                fstype = struct.unpack_from(">H", data, offset + 8)[0]
                                if fstype != 0:
                                    struct.pack_into(">H", data, offset + 8, 0)
                                    modified = True
                                    # Recalculate OS/2 table checksum
                                    tbl = bytes(data[offset:offset + length])
                                    rem = len(tbl) % 4
                                    if rem:
                                        tbl += b"\x00" * (4 - rem)
                                    new_cs = sum(struct.unpack(f">{len(tbl) // 4}I", tbl)) & 0xFFFFFFFF
                                    struct.pack_into(">I", data, entry_offset + 4, new_cs)
        else:
            # Standard TrueType (.ttf) or OpenType (.otf)
            num_tables = struct.unpack_from(">H", data, 4)[0]
            if len(data) >= 12 + num_tables * 16:
                for i in range(num_tables):
                    entry_offset = 12 + i * 16
                    tag, checksum, offset, length = struct.unpack_from(">4sIII", data, entry_offset)
                    if tag == b"OS/2":
                        if len(data) >= offset + 10:
                            fstype = struct.unpack_from(">H", data, offset + 8)[0]
                            if fstype != 0:
                                struct.pack_into(">H", data, offset + 8, 0)
                                modified = True
                                # Recalculate OS/2 table checksum
                                tbl = bytes(data[offset:offset + length])
                                rem = len(tbl) % 4
                                if rem:
                                    tbl += b"\x00" * (4 - rem)
                                new_cs = sum(struct.unpack(f">{len(tbl) // 4}I", tbl)) & 0xFFFFFFFF
                                struct.pack_into(">I", data, entry_offset + 4, new_cs)
                        break

        if not modified:
            return font_path

        try:
            from PySide6.QtCore import QStandardPaths, QDir
            base_cache = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.CacheLocation)
            if base_cache:
                cache_dir = os.path.join(QDir.toNativeSeparators(base_cache), "mcg_fonts")
            else:
                cache_dir = os.path.join(tempfile.gettempdir(), "mcg_sanitized_fonts")
        except Exception:
            cache_dir = os.path.join(tempfile.gettempdir(), "mcg_sanitized_fonts")

        os.makedirs(cache_dir, exist_ok=True)
        path_hash = hashlib.md5(font_path.encode("utf-8", errors="replace")).hexdigest()[:8]
        fname = f"{path_hash}_{os.path.basename(font_path)}"
        out_path = os.path.join(cache_dir, fname)

        # Avoid re-writing if identical file already exists (prevents Windows file lock errors)
        if os.path.isfile(out_path) and os.path.getsize(out_path) == len(data):
            return out_path

        try:
            with open(out_path, "wb") as f:
                f.write(data)
            return out_path
        except (OSError, PermissionError):
            # If primary cache file is locked by a running process on Windows, use a unique temp file
            alt_path = os.path.join(tempfile.gettempdir(), f"mcg_font_{os.getpid()}_{fname}")
            try:
                with open(alt_path, "wb") as f:
                    f.write(data)
                return alt_path
            except Exception:
                return font_path
    except Exception:
        return font_path


class Font:
    """Represents a font used inside a certificate text block."""

    def __init__(self, font_name: str = "", font_location: str = "") -> None:
        self._font_name: str = font_name
        self._font_location: str = font_location
        self._cached_render_location: str | None = None

    @property
    def font_name(self) -> str:
        return self._font_name

    @font_name.setter
    def font_name(self, value: str) -> None:
        self._font_name = value

    @property
    def font_location(self) -> str:
        return self._font_location

    @font_location.setter
    def font_location(self, value: str) -> None:
        if self._font_location != value:
            self._font_location = value
            self._cached_render_location = None

    def get_render_location(self) -> str:
        """Return the font file location suitable for embedding during render."""
        if self._cached_render_location is None:
            self._cached_render_location = sanitize_font_for_embedding(self._font_location)
        return self._cached_render_location

    def load(self) -> None:
        """Load the font from font_location."""
        if not self.is_valid():
            raise FileNotFoundError(f"Font file not found: {self._font_location}")

    def is_valid(self) -> bool:
        """Return True if the font file exists and is readable."""
        return bool(self._font_location) and os.path.isfile(self._font_location)

    def to_css(self) -> str:
        """Return a CSS @font-face declaration for this font."""
        # Use forward slashes for CSS compatibility on Windows
        loc = self.get_render_location().replace("\\", "/")
        return (
            f"@font-face {{\n"
            f'    font-family: "{self._font_name}";\n'
            f'    src: url("{loc}");\n'
            f"}}"
        )

    def __repr__(self) -> str:
        return f"Font(font_name={self._font_name!r}, font_location={self._font_location!r})"

