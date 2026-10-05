from enum import Enum, auto


class OutputFormat(Enum):
    PDF = auto()
    PNG = auto()
    JPEG = auto()


class OutputType(Enum):
    INDIVIDUAL_FILE = auto()
    SINGLE_FILE = auto()


class PageOrientation(Enum):
    PORTRAIT = auto()
    LANDSCAPE = auto()


class PaperSize(Enum):
    A4 = auto()
    LETTER = auto()


class Alignment(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    JUSTIFY = auto()


class TextCategory(Enum):
    HEADER = auto()
    BODY = auto()
    FOOTER = auto()
    LABEL = auto()


# ── Utility functions ─────────────────────────────────────────────────────────

def position_to_ordinal(position: int) -> str:
    """Convert an integer position to its ordinal string (1→'1st', 2→'2nd', …)."""
    if position == 1:
        return "1st"
    elif position == 2:
        return "2nd"
    elif position == 3:
        return "3rd"
    else:
        return f"{position}th"


def positional_to_str(position: int, runnersup_limit: int) -> str:
    """Convert a competition position to a human-readable label."""
    if position == 1:
        return "Champion"
    elif (runnersup_limit + 1) >= position:
        return f"{position_to_ordinal(position - 1)} Runners-up"
    else:
        return f"{position}th"
