from __future__ import annotations

import pymupdf as mupdf

from .enums import Alignment, PageOrientation, PaperSize
from .font import Font
from .texts import Texts


class Certificate:
    """Represents a single certificate layout with its content and styling."""

    PAPER_SIZE_MAP = {
        PaperSize.A4: "A4",
        PaperSize.LETTER: "letter",
    }

    def __init__(
        self,
        paper_size: PaperSize = PaperSize.A4,
        page_orientation: PageOrientation = PageOrientation.LANDSCAPE,
        top_left_x: float = 0.0,
        top_left_y: float = 0.0,
        bottom_right_x: float = 0.0,
        bottom_right_y: float = 0.0,
        list_fonts: list[Font] | None = None,
        text_body: list[Texts] | None = None,
        alignment: Alignment = Alignment.CENTER,
    ) -> None:
        self._paper_size: PaperSize = paper_size
        self._page_orientation: PageOrientation = page_orientation
        self._top_left_coordinate_x: float = top_left_x
        self._top_left_coordinate_y: float = top_left_y
        self._bottom_right_coordinate_x: float = bottom_right_x
        self._bottom_right_coordinate_y: float = bottom_right_y
        self._list_fonts: list[Font] = list_fonts if list_fonts is not None else []
        self._text_body: list[Texts] = text_body if text_body is not None else []
        self._alignment: Alignment = alignment
        self._debug_mode: bool = False

    @property
    def paper_size(self) -> PaperSize:
        return self._paper_size

    @paper_size.setter
    def paper_size(self, value: PaperSize) -> None:
        self._paper_size = value

    @property
    def page_orientation(self) -> PageOrientation:
        return self._page_orientation

    @page_orientation.setter
    def page_orientation(self, value: PageOrientation) -> None:
        self._page_orientation = value

    @property
    def top_left_coordinate_x(self) -> float:
        return self._top_left_coordinate_x

    @top_left_coordinate_x.setter
    def top_left_coordinate_x(self, value: float) -> None:
        self._top_left_coordinate_x = value

    @property
    def top_left_coordinate_y(self) -> float:
        return self._top_left_coordinate_y

    @top_left_coordinate_y.setter
    def top_left_coordinate_y(self, value: float) -> None:
        self._top_left_coordinate_y = value

    @property
    def bottom_right_coordinate_x(self) -> float:
        return self._bottom_right_coordinate_x

    @bottom_right_coordinate_x.setter
    def bottom_right_coordinate_x(self, value: float) -> None:
        self._bottom_right_coordinate_x = value

    @property
    def bottom_right_coordinate_y(self) -> float:
        return self._bottom_right_coordinate_y

    @bottom_right_coordinate_y.setter
    def bottom_right_coordinate_y(self, value: float) -> None:
        self._bottom_right_coordinate_y = value

    @property
    def list_fonts(self) -> list[Font]:
        return self._list_fonts

    @list_fonts.setter
    def list_fonts(self, value: list[Font]) -> None:
        self._list_fonts = value

    @property
    def text_body(self) -> list[Texts]:
        return self._text_body

    @text_body.setter
    def text_body(self, value: list[Texts]) -> None:
        self._text_body = value

    @property
    def alignment(self) -> Alignment:
        return self._alignment

    @alignment.setter
    def alignment(self, value: Alignment) -> None:
        self._alignment = value

    @property
    def debug_mode(self) -> bool:
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value: bool) -> None:
        self._debug_mode = value

    def add_font(self, font: Font) -> None:
        """Add a Font to the certificate's font list."""
        self.list_fonts.append(font)

    def add_text_block(self, text: Texts) -> None:
        """Add a Texts block to the certificate's text body."""
        self.text_body.append(text)

    def remove_text_block(self, text: Texts) -> None:
        """Remove a Texts block from the certificate's text body."""
        self.text_body.remove(text)

    def _build_css(self) -> str:
        """Build a combined CSS string from all registered fonts."""
        parts = []
        for font in self.list_fonts:
            if font.is_valid():
                parts.append(font.to_css())
        align = self.alignment.name.lower()
        parts.append(f'* {{ text-align: {align}; }}')
        return "\n".join(parts)

    def _build_html(self, row: dict) -> str:
        """Build the HTML body by resolving every text block against *row*.

        Text blocks are concatenated inline by default.
        When a block has ending_constraints (Line Break checked), the
        current line is closed into a ``<div>`` and a new line begins.
        ``text-align`` is taken from the Certificate's alignment.
        """
        valid_font_names = {f.font_name for f in self.list_fonts if f.is_valid()}
        lines: list[list] = [[]]  # list of lines, each line is a list of (span_html, text_block)
        for text_block in self.text_body:
            resolved = text_block.resolve_text(row)
            inner = resolved

            if text_block.is_bold:
                inner = f"<b>{inner}</b>"
            if text_block.is_italic:
                inner = f"<i>{inner}</i>"
            if text_block.is_underline:
                inner = f"<u>{inner}</u>"

            style = text_block.apply_style(valid_font_names=valid_font_names)
            span = f'<span style="{style}">{inner}</span>'
            lines[-1].append((span, text_block))

            if text_block.ending_constraints:
                lines.append([])

        # Remove trailing empty line
        if lines and not lines[-1]:
            lines.pop()

        parts = []
        align = self.alignment.name.lower()
        for line in lines:
            if not line:
                continue
            spans = " ".join(s for s, _ in line)
            parts.append(f'<div style="text-align: {align}; margin: 0">{spans}</div>')
        return "\n".join(parts)

    def _get_text_rect(self) -> mupdf.Rect:
        """Return the text container rectangle from the stored coordinates."""
        return mupdf.Rect(
            self.top_left_coordinate_x,
            self.top_left_coordinate_y,
            self.bottom_right_coordinate_x,
            self.bottom_right_coordinate_y,
        )

    def render(self, row: dict, page: mupdf.Page, draw_debug: bool = False) -> None:
        """Render this certificate's text blocks onto *page* for a single CSV data row.

        The *draw_debug* flag controls whether the visual blue bounding box is drawn.
        It defaults to False so that exported output files never contain debugging
        rectangles even if debuggingMode_checkBox is enabled in the UI.

        Implements 3-tier progressive fallback to guarantee crash-free rendering:
        1. Custom fonts with CSS @font-face.
        2. Safe-font HTML without custom font-family (prevents missing font substitute errors).
        3. Native low-level textbox text insertion (Base-14 PDF fonts).
        """
        text_rect = self._get_text_rect()
        if text_rect.is_empty or text_rect.width <= 1 or text_rect.height <= 1:
            return

        css = self._build_css()
        html = self._build_html(row)

        # Tier 1: Render with full custom fonts and CSS
        try:
            page.insert_htmlbox(text_rect, html, css=css)
        except Exception:
            # Tier 2: Strip custom font families and render with standard CSS fallback
            try:
                import re
                safe_html = re.sub(r"font-family\s*:\s*[^;\"'>]+;?", "", html)
                align = self.alignment.name.lower()
                safe_css = f"* {{ text-align: {align}; }}"
                page.insert_htmlbox(text_rect, safe_html, css=safe_css)
            except Exception:
                # Tier 3: Low-level native text insertion (immune to font engine substitute errors)
                try:
                    lines = []
                    current_line = []
                    for block in self.text_body:
                        txt = block.resolve_text(row)
                        if txt:
                            current_line.append(txt)
                        if block.ending_constraints:
                            lines.append(" ".join(current_line))
                            current_line = []
                    if current_line:
                        lines.append(" ".join(current_line))
                    fallback_text = "\n".join(lines)

                    align_code = mupdf.TEXT_ALIGN_CENTER
                    if self.alignment == Alignment.LEFT:
                        align_code = mupdf.TEXT_ALIGN_LEFT
                    elif self.alignment == Alignment.RIGHT:
                        align_code = mupdf.TEXT_ALIGN_RIGHT
                    elif self.alignment == Alignment.JUSTIFY:
                        align_code = mupdf.TEXT_ALIGN_JUSTIFIED

                    page.insert_textbox(text_rect, fallback_text, fontsize=14, align=align_code)
                except Exception as e3:
                    print(f"Fallback rendering encountered error: {e3}")

        # Visual debug rectangle is only rendered when explicitly requested (e.g. preview)
        if draw_debug and self.debug_mode:
            shape = page.new_shape()
            shape.draw_rect(text_rect)
            shape.finish(width=1.0, color=mupdf.pdfcolor["blue"])
            shape.commit()

    def __repr__(self) -> str:
        return (
            f"Certificate(paper_size={self.paper_size}, "
            f"orientation={self.page_orientation}, "
            f"text_blocks={len(self.text_body)})"
        )
