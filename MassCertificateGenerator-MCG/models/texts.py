from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from .enums import Alignment, TextCategory
from .font import Font


class Texts(ABC):
    """Abstract base class for a text block placed on a certificate."""

    def __init__(
        self,
        category: TextCategory = TextCategory.BODY,
        text_body: str = "",
        is_bold: bool = False,
        is_italic: bool = False,
        is_underline: bool = False,
        color: tuple[int, int, int] = (0, 0, 0),
        font: list[Font] = None,
        text_size: float = 12.0,
        ending_constraints: str = "",
    ) -> None:
        self._category: TextCategory = category
        self._text_body: str = text_body
        self._is_bold: bool = is_bold
        self._is_italic: bool = is_italic
        self._is_underline: bool = is_underline
        self._color: Tuple[int, int, int] = color
        self._font: Optional[list[Font]] = font
        self._text_size: float = text_size
        self._ending_constraints: str = ending_constraints

    @property
    def category(self) -> TextCategory:
        return self._category

    @category.setter
    def category(self, value: TextCategory) -> None:
        self._category = value

    @property
    def text_body(self) -> str:
        return self._text_body

    @text_body.setter
    def text_body(self, value: str) -> None:
        self._text_body = value

    @property
    def is_bold(self) -> bool:
        return self._is_bold

    @is_bold.setter
    def is_bold(self, value: bool) -> None:
        self._is_bold = value

    @property
    def is_italic(self) -> bool:
        return self._is_italic

    @is_italic.setter
    def is_italic(self, value: bool) -> None:
        self._is_italic = value

    @property
    def is_underline(self) -> bool:
        return self._is_underline

    @is_underline.setter
    def is_underline(self, value: bool) -> None:
        self._is_underline = value

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self._color = value

    @property
    def font(self) -> Optional[list[Font]]:
        return self._font

    @font.setter
    def font(self, value: Optional[list[Font]]) -> None:
        self._font = value

    @property
    def text_size(self) -> float:
        return self._text_size

    @text_size.setter
    def text_size(self, value: float) -> None:
        self._text_size = value

    @property
    def ending_constraints(self) -> str:
        return self._ending_constraints

    @ending_constraints.setter
    def ending_constraints(self, value: str) -> None:
        self._ending_constraints = value

    @abstractmethod
    def resolve_text(self, row: dict) -> str:
        """Resolve the final display text for a given CSV data row."""
        pass

    def apply_style(self, valid_font_names: set[str] | None = None) -> str:
        """Return an inline CSS style string for this text block.

        If *valid_font_names* is provided, font-family is only emitted if the font
        is verified to be present and embeddable, preventing missing-font substitution errors.
        """
        r, g, b = self.color
        parts = [
            f"color: rgb({r},{g},{b})",
            f"font-size: {self.text_size}pt",
        ]
        if self.font and self.font[0].font_name:
            fname = self.font[0].font_name
            if valid_font_names is None or fname in valid_font_names:
                parts.append(f"font-family: '{fname}'")
        return "; ".join(parts)

    def validate(self) -> bool:
        """Return True if this text block is properly configured."""
        return self.text_size > 0


class VariableTexts(Texts):
    """Text block whose content is drawn from a CSV column at render time."""

    def __init__(self, csv_column_name: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self._csv_column_name: str = csv_column_name

    @property
    def csv_column_name(self) -> str:
        return self._csv_column_name

    @csv_column_name.setter
    def csv_column_name(self, value: str) -> None:
        self._csv_column_name = value

    def resolve_text(self, row: dict) -> str:
        """Return the value from row[csv_column_name]."""
        value = row.get(self.csv_column_name, "")
        return str(value)

    def validate(self) -> bool:
        """Return True if csv_column_name is set and base validation passes."""
        return bool(self.csv_column_name) and super().validate()

    def __repr__(self) -> str:
        return (
            f"VariableTexts(csv_column_name={self.csv_column_name!r}, "
            f"category={self.category})"
        )


class ConstantTexts(Texts):
    """Text block whose content is fixed and never changes across certificates."""

    def resolve_text(self, row: dict) -> str:
        """Return self.text_body unchanged (ignores row data)."""
        return self.text_body

    def __repr__(self) -> str:
        return (
            f"ConstantTexts(text_body={self.text_body!r}, category={self.category})"
        )
