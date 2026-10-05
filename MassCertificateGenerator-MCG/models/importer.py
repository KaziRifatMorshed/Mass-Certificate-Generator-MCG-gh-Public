from __future__ import annotations
import os
from abc import ABC, abstractmethod

import pandas as pd
import pymupdf as mupdf

from .singleton import SingletonMeta


# ── Abstraction (Dependency-Inversion) ────────────────────────────────────────

class IImporter(ABC):
    """Interface for all importer implementations."""

    @abstractmethod
    def load_pdf_template(self, path: str) -> None:
        """Load a PDF template from the given file path."""
        pass

    @abstractmethod
    def load_csv(self, path: str) -> None:
        """Load a CSV data file from the given file path."""
        pass

    @abstractmethod
    def get_column_names(self) -> list[str]:
        """Return the list of column names from the loaded CSV."""
        pass

    @abstractmethod
    def get_column_count(self) -> int:
        """Return the number of columns in the loaded CSV."""
        pass


# ── Concrete Singleton implementation ─────────────────────────────────────────

class Importer(IImporter, metaclass=SingletonMeta):
    """
    Singleton importer.
    Loads the PDF template and CSV data file used to generate certificates.
    """

    def __init__(self) -> None:
        self._pdf_template_location: str = "./input/template/input_template.pdf"
        self._template_doc: mupdf.Document | None = None
        self._csv_data: pd.DataFrame | None = None
        self._csv_column_names: list[str] = []
        self._data_count: int = 0

    @property
    def pdf_template_location(self) -> str:
        return self._pdf_template_location

    @pdf_template_location.setter
    def pdf_template_location(self, value: str) -> None:
        self._pdf_template_location = value

    @property
    def template_doc(self) -> mupdf.Document | None:
        return self._template_doc

    @template_doc.setter
    def template_doc(self, value: mupdf.Document | None) -> None:
        self._template_doc = value

    @property
    def csv_data(self) -> pd.DataFrame | None:
        return self._csv_data

    @csv_data.setter
    def csv_data(self, value: pd.DataFrame | None) -> None:
        self._csv_data = value

    @property
    def csv_column_count(self) -> int:
        return len(self._csv_column_names)

    @property
    def csv_column_names(self) -> list[str]:
        return self._csv_column_names

    @csv_column_names.setter
    def csv_column_names(self, value: list[str]) -> None:
        self._csv_column_names = value

    @property
    def data_count(self) -> int:
        return self._data_count

    @data_count.setter
    def data_count(self, value: int) -> None:
        self._data_count = value

    def load_pdf_template(self, path: str) -> None:
        """Store the PDF template path and validate it exists."""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"PDF template not found: {path}")
        self.pdf_template_location = path
        self.template_doc = mupdf.open(path)

    def load_csv(self, path: str) -> None:
        """Parse the CSV to populate column_count, column_names, and data."""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"CSV file not found: {path}")
        self.csv_data = pd.read_csv(path, quotechar='"')
        self.csv_column_names = list(self.csv_data.columns)
        self.data_count = len(self.csv_data)

    def get_column_names(self) -> list[str]:
        """Return csv_column_names."""
        return self.csv_column_names

    def get_column_count(self) -> int:
        """Return csv_column_count."""
        return self.csv_column_count

    def clear(self) -> None:
        """Reset all loaded data."""
        self.pdf_template_location = ""
        if self.template_doc:
            self.template_doc.close()
        self.template_doc = None
        self.csv_data = None
        self.csv_column_count = 0
        self.csv_column_names = []
        self.data_count = 0

    def __repr__(self) -> str:
        return (
            f"Importer(pdf_template_location={self.pdf_template_location!r}, "
            f"csv_columns={self.csv_column_names})"
        )
