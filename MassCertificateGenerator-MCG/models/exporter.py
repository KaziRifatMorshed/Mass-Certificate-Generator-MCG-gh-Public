from __future__ import annotations
import os
from abc import ABC, abstractmethod

import pymupdf as mupdf

from .certificate import Certificate
from .enums import OutputFormat, OutputType
from .importer import Importer
from .singleton import SingletonMeta


# ── Abstraction (Dependency-Inversion) ────────────────────────────────────────

class IExporter(ABC):
    """Interface for all exporter implementations."""

    @abstractmethod
    def export(self, certificate: Certificate) -> None:
        """Export the rendered certificates to the output folder."""
        pass

    @abstractmethod
    def set_output_folder(self, path: str) -> None:
        """Set the destination folder for exported files."""
        pass


# ── Concrete Singleton implementation ─────────────────────────────────────────

class Exporter(IExporter, metaclass=SingletonMeta):
    """
    Singleton exporter.
    Writes generated certificate files to a configured output folder.
    """

    def __init__(self) -> None:
        self._output_folder_path: str = ""
        self._output_file_name: str = "output"
        self._output_format: OutputFormat = OutputFormat.PDF
        self._output_type: OutputType = OutputType.INDIVIDUAL_FILE
        self._name_column: str = "Name"

    @property
    def output_folder_path(self) -> str:
        return self._output_folder_path

    @output_folder_path.setter
    def output_folder_path(self, value: str) -> None:
        self._output_folder_path = value

    @property
    def output_file_name(self) -> str:
        return self._output_file_name

    @output_file_name.setter
    def output_file_name(self, value: str) -> None:
        self._output_file_name = value

    @property
    def output_format(self) -> OutputFormat:
        return self._output_format

    @output_format.setter
    def output_format(self, value: OutputFormat) -> None:
        self._output_format = value

    @property
    def output_type(self) -> OutputType:
        return self._output_type

    @output_type.setter
    def output_type(self, value: OutputType) -> None:
        self._output_type = value

    @property
    def name_column(self) -> str:
        return self._name_column

    @name_column.setter
    def name_column(self, value: str) -> None:
        self._name_column = value

    def set_output_folder(self, path: str) -> None:
        """Validate and store the output folder path, creating it if needed."""
        os.makedirs(path, exist_ok=True)
        self.output_folder_path = path

    def export(self, certificate: Certificate) -> None:
        """Dispatch to _export_individual or _export_single based on output_type.

        Guarantees that preview debug elements (such as the blue text bounding box)
        are never rendered into exported files, regardless of whether the preview
        debugging checkbox is enabled.
        """
        orig_debug = certificate.debug_mode
        certificate.debug_mode = False
        try:
            if self.output_type == OutputType.INDIVIDUAL_FILE:
                self._export_individual(certificate)
            else:
                self._export_single(certificate)
        finally:
            certificate.debug_mode = orig_debug

    def _export_individual(self, certificate: Certificate) -> None:
        """Write one file per certificate into output_folder_path."""
        importer = Importer()
        if importer.template_doc is None or importer.csv_data is None:
            raise RuntimeError("Template or CSV data not loaded.")

        for _, row in importer.csv_data.iterrows():
            output_doc = mupdf.Document()
            output_doc.insert_pdf(importer.template_doc, from_page=0, to_page=0)
            page = output_doc[-1]
            certificate.render(row.to_dict(), page, draw_debug=False)
            name = row.get(self.name_column, f"cert_{_}")
            ext = self.output_format.name.lower()
            out_path = os.path.join(self.output_folder_path, f"{name}.{ext}")

            if self.output_format == OutputFormat.PDF:
                try:
                    output_doc.save(out_path)
                except Exception:
                    output_doc.save(out_path, garbage=3, deflate=True)
            else:
                pix = page.get_pixmap(dpi=300)
                pix.save(out_path)

            output_doc.close()

    def _export_single(self, certificate: Certificate) -> None:
        """Export all certificate pages into a single file."""
        importer = Importer()
        if importer.template_doc is None or importer.csv_data is None:
            raise RuntimeError("Template or CSV data not loaded.")

        if self.output_format != OutputFormat.PDF:
            # Single file image output (multi-page) is not supported easily.
            # We'll just export individual images instead.
            self._export_individual(certificate)
            return

        output_doc = mupdf.Document()
        for _, row in importer.csv_data.iterrows():
            output_doc.insert_pdf(importer.template_doc, from_page=0, to_page=0)
            page = output_doc[-1]
            certificate.render(row.to_dict(), page, draw_debug=False)

        ext = self.output_format.name.lower()
        out_path = os.path.join(
            self.output_folder_path,
            f"{self.output_file_name}.{ext}",
        )
        try:
            output_doc.save(out_path)
        except Exception:
            output_doc.save(out_path, garbage=3, deflate=True)
        output_doc.close()

    def __repr__(self) -> str:
        return (
            f"Exporter(output_folder_path={self.output_folder_path!r}, "
            f"output_type={self.output_type})"
        )
