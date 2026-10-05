# This Python file uses the following encoding: utf-8
import json
import os
import sys

from PySide6.QtCore import Qt, QUrl, QStandardPaths, QDir, QTimer, QEvent
from PySide6.QtGui import QIcon, QCloseEvent, QColor, QDesktopServices
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                               QGroupBox, QFormLayout, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget,
                               QSpinBox, QCheckBox, QComboBox, QPlainTextEdit,
                               QHBoxLayout, QGridLayout, QFrame, QSizePolicy,
                               QColorDialog, QDialog)

import version
from models import (Importer, Exporter, Certificate, Font, OutputFormat, OutputType,
                    Alignment, VariableTexts, ConstantTexts, Texts)
from ui_mainWindow import Ui_MainWindow


def get_app_data_dir() -> str:
    """Return a standard writable directory for app data (settings, session state, etc.).

    Uses QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation).
    On Windows: C:/Users/<User>/AppData/Local/MassCertificateGenerator
    On Linux: ~/.local/share/MassCertificateGenerator
    On macOS: ~/Library/Application Support/MassCertificateGenerator
    Falls back to application directory if standard path is empty.
    Ensures the directory is created.
    """
    from PySide6.QtCore import QCoreApplication
    if not QCoreApplication.applicationName():
        QCoreApplication.setApplicationName(version.APP_NAME)

    path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
    if not path:
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        else:
            path = os.path.dirname(os.path.abspath(__file__))

    path = QDir.toNativeSeparators(path)
    os.makedirs(path, exist_ok=True)
    return path


def get_state_file_path() -> str:
    """Return path to mcg_session_state.json in standard data directory, migrating legacy files if present."""
    data_dir = get_app_data_dir()
    state_file = os.path.join(data_dir, "mcg_session_state.json")

    # Seamless migration: if state file does not exist, check for legacy files
    if not os.path.exists(state_file):
        legacy_candidates = [
            os.path.join(data_dir, "session_state.json"),
            os.path.join(
                os.path.dirname(sys.executable)
                if getattr(sys, 'frozen', False)
                else os.path.dirname(os.path.abspath(__file__)),
                "mcg_session_state.json",
            ),
            os.path.join(
                os.path.dirname(sys.executable)
                if getattr(sys, 'frozen', False)
                else os.path.dirname(os.path.abspath(__file__)),
                "session_state.json",
            ),
        ]
        for candidate in legacy_candidates:
            if os.path.isfile(candidate):
                try:
                    import shutil
                    shutil.copy2(candidate, state_file)
                    break
                except OSError:
                    pass
    return state_file


_STATE_FILE = get_state_file_path()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pipeline_tabWidget.setCurrentIndex(0)

        # Dynamic window title and executable icon
        self.setWindowTitle(f"{version.APP_DISPLAY_NAME} - {version.APP_VERSION_STR} ({version.GIT_HASH_STR})")
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._setup_coordinate_controls()

        self.ui.nextTab_pushButton.clicked.connect(self.next_tab)
        self.ui.prevTab_pushButton.clicked.connect(self.prev_tab)
        self.ui.selectTemplate_pushButton.clicked.connect(self.select_template)
        self.ui.help_pushButton.clicked.connect(self.open_help)

        self.importer = Importer()
        self.exporter = Exporter()
        self.certificate = Certificate()
        self.pdf_doc = QPdfDocument(self)
        self.fonts: list[Font] = []
        self._font_group_boxes: list[dict] = []
        self.text_entries: list[dict] = []

        # Hide the template font_groupBox from Designer — we create them dynamically
        self.ui.font_groupBox.hide()

        # Wrap font tab content in a scroll area
        self._font_scroll_container = QWidget()
        self._font_scroll_layout = QVBoxLayout(self._font_scroll_container)
        self._font_scroll_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self._font_scroll_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Replace the font tab's layout contents
        while self.ui.verticalLayout_4.count():
            self.ui.verticalLayout_4.takeAt(0)
        self.ui.verticalLayout_4.addWidget(self.ui.addNewFont_newGrpBox_pushButton)
        self.ui.verticalLayout_4.addWidget(scroll_area)

        # Font tab connections
        self.ui.addNewFont_newGrpBox_pushButton.clicked.connect(self._add_font_group_box)

        # ── Text Body tab setup ───────────────────────────────────────────────
        self._setup_text_body_tab()

        # Import Data tab connections
        self.ui.selectImortFile_pushButton.clicked.connect(self.select_import_file)

        # Export tab connections
        self.ui.selectExportLocation_pushButton.clicked.connect(self.select_export_location)
        self.ui.EXPORT_pushButton.clicked.connect(self.do_export)
        self.ui.outputFormat_comboBox.currentIndexChanged.connect(self._on_output_format_changed)

        # Global alignment connection
        self.ui.currentTextAlignment_comboBox.currentTextChanged.connect(self._on_alignment_changed)

        # State saving debounce timer
        self._loading_state: bool = False
        self._state_save_timer = QTimer(self)
        self._state_save_timer.setSingleShot(True)
        self._state_save_timer.setInterval(500)
        self._state_save_timer.timeout.connect(self._save_state)

        # Tab navigation & change auto-save
        self.ui.pipeline_tabWidget.currentChanged.connect(self._on_tab_changed)

        # Additional combo connections for auto-saving session state
        self.ui.singleFile_multipleFiile_comboBox.currentIndexChanged.connect(lambda _: self._schedule_state_save())
        self.ui.oututFiileNameField_comboBox.currentTextChanged.connect(lambda _: self._schedule_state_save())
        self.ui.importFileFotmat_comboBox.currentIndexChanged.connect(lambda _: self._schedule_state_save())

        # Restore previous session
        self._load_state()

    def _schedule_state_save(self):
        """Schedule a debounced write of session state to disk."""
        if not getattr(self, "_loading_state", False):
            self._state_save_timer.start(500)

    def _on_tab_changed(self, index: int):
        if getattr(self, "_loading_state", False):
            return
        self._auto_save_all()
        self._save_state()

    def _auto_save_all(self):
        """Auto-save all active font and text entries."""
        for font_entry in list(self._font_group_boxes):
            self._save_font_for(font_entry)
        for text_entry in list(self.text_entries):
            self._save_text_entry(text_entry)
        self._sync_certificate_texts()
        self._update_preview()

    def _sync_certificate_texts(self):
        """Synchronize self.certificate.text_body to match self.text_entries in exact order."""
        self.certificate.text_body.clear()
        for entry in self.text_entries:
            if entry.get("text_obj") is not None:
                self.certificate.add_text_block(entry["text_obj"])

    def _on_coordinate_changed(self):
        self._update_preview()
        self._schedule_state_save()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange and not self.isActiveWindow():
            self._save_state()
        super().changeEvent(event)

    def _on_output_format_changed(self, index: int):
        text = self.ui.outputFormat_comboBox.currentText()
        if text == "PDF":
            self.exporter.output_format = OutputFormat.PDF
        elif text == "PNG":
            self.exporter.output_format = OutputFormat.PNG
        elif text == "JPEG":
            self.exporter.output_format = OutputFormat.JPEG
        self._schedule_state_save()

    def _on_alignment_changed(self, text: str):
        self.certificate.alignment = self._alignment_from_text(text)
        self._update_preview()
        self._schedule_state_save()

    def next_tab(self):
        tab = self.ui.pipeline_tabWidget
        tab.setCurrentIndex(min(tab.currentIndex() + 1, tab.count() - 1))

    def prev_tab(self):
        tab = self.ui.pipeline_tabWidget
        tab.setCurrentIndex(max(tab.currentIndex() - 1, 0))

    def open_help(self):
        """Open the About & Help dialog displaying version, build info, and resources."""
        self.show_about_dialog()

    def show_about_dialog(self):
        """Display comprehensive About and Help dialog with version, git hash, build time, and links."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"About - {version.APP_DISPLAY_NAME}")
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)

        # Header with Logo and Title
        header_layout = QHBoxLayout()
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.png")
        if os.path.exists(icon_path):
            logo_label = QLabel()
            pixmap = QIcon(icon_path).pixmap(56, 56)
            logo_label.setPixmap(pixmap)
            header_layout.addWidget(logo_label)

        title_info = QLabel(
            f"<h2 style='margin:0;'>{version.APP_DISPLAY_NAME}</h2>"
            f"<b style='color:#27bf73;'>Version {version.APP_VERSION_STR}</b> &nbsp;|&nbsp; "
            f"Commit: <code>{version.GIT_HASH_STR}</code><br>"
            f"<small style='color:gray;'>Build Timestamp: {version.BUILD_DATE_TIME}</small>"
        )
        title_info.setTextFormat(Qt.TextFormat.RichText)
        header_layout.addWidget(title_info)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Environment details
        sys_info = version.get_system_info()
        data_dir = get_app_data_dir()
        details_text = (
            f"<b>Python:</b> {sys_info.get('python_version', 'N/A')}<br>"
            f"<b>Qt / PySide6:</b> {sys_info.get('qt_version', 'N/A')} / {sys_info.get('pyside6_version', 'N/A')}<br>"
            f"<b>PyMuPDF:</b> {sys_info.get('pymupdf_version', 'N/A')}<br>"
            f"<b>Platform:</b> {sys_info.get('platform', sys.platform)}<br>"
            f"<b>Data Directory:</b> <code style='font-size:11px;'>{data_dir}</code>"
        )
        details_label = QLabel(details_text)
        details_label.setTextFormat(Qt.TextFormat.RichText)
        details_label.setWordWrap(True)
        details_label.setStyleSheet("padding: 8px; background-color: rgba(128, 128, 128, 0.1); border-radius: 4px;")
        layout.addWidget(details_label)

        # Links and Actions
        btn_layout = QHBoxLayout()
        tutorial_btn = QPushButton("Video Tutorials")
        tutorial_btn.setToolTip("Open YouTube tutorial playlist")
        tutorial_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(version.APP_YOUTUBE)))
        btn_layout.addWidget(tutorial_btn)

        website_btn = QPushButton("Website")
        website_btn.setToolTip("Open project website")
        website_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(version.APP_WEBSITE)))
        btn_layout.addWidget(website_btn)

        data_dir_btn = QPushButton("Open Data Folder")
        data_dir_btn.setToolTip("Open local AppData/configuration directory in file manager")
        data_dir_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(data_dir)))
        btn_layout.addWidget(data_dir_btn)

        btn_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)
        dialog.exec()

    def _setup_coordinate_controls(self):
        pairs = [
            (self.ui.topLeft_x_spinBox, self.ui.left_top_x_horizontalSlider),
            (self.ui.topLeft_y_spinBox, self.ui.left_top_y_verticalSlider),
            (self.ui.bottomRight_x_spinBox, self.ui.bottom_right_x_horizontalSlider),
            (self.ui.bottomRight_y_spinBox, self.ui.botto_right_y_verticalSlider),
        ]
        for spinbox, slider in pairs:
            spinbox.setRange(0, 100)
            slider.setRange(0, 100)
            spinbox.valueChanged.connect(slider.setValue)
            slider.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(self._on_coordinate_changed)

        # Debug mode checkbox (preview only)
        self.ui.debuggingMode_checkBox.setToolTip(
            "Show bounding box in preview only (never included in exported output files)"
        )
        self.ui.debuggingMode_checkBox.toggled.connect(self._on_debug_toggled)

    def _on_debug_toggled(self, checked: bool):
        self.certificate.debug_mode = checked
        self._update_preview()
        self._schedule_state_save()

    def _sync_certificate_coordinates(self):
        """Convert percentage-based spinbox values to actual page coordinates."""
        if self.importer.template_doc is None:
            return
        page = self.importer.template_doc[0]
        w, h = page.rect.width, page.rect.height
        self.certificate.top_left_coordinate_x = self.ui.topLeft_x_spinBox.value() / 100.0 * w
        self.certificate.top_left_coordinate_y = self.ui.topLeft_y_spinBox.value() / 100.0 * h
        self.certificate.bottom_right_coordinate_x = (100 - self.ui.bottomRight_x_spinBox.value()) / 100.0 * w
        self.certificate.bottom_right_coordinate_y = (100 - self.ui.bottomRight_y_spinBox.value()) / 100.0 * h
        self.certificate.alignment = self._alignment_from_text(self.ui.currentTextAlignment_comboBox.currentText())

    def _update_preview(self):
        """Render a sample certificate and display it in the thumbnail viewer."""
        if self.importer.template_doc is None:
            return
        self._sync_certificate_coordinates()
        self.certificate.list_fonts = self.fonts

        import pymupdf as mupdf
        import tempfile, os, time

        # Build a sample row from CSV data or use placeholder
        if self.importer.csv_data is not None and len(self.importer.csv_data) > 0:
            sample_row = self.importer.csv_data.iloc[0].to_dict()
        else:
            sample_row = {col: col for col in self.importer.csv_column_names} if self.importer.csv_column_names else {}

        try:
            # Create a temporary document from the template's first page
            preview_doc = mupdf.Document()
            preview_doc.insert_pdf(self.importer.template_doc, from_page=0, to_page=0)
            page = preview_doc[-1]
            self.certificate.render(sample_row, page, draw_debug=True)

            # Save to a unique temp file to avoid 'Permission Denied' on Windows
            # Windows locks the file when QPdfDocument loads it.
            tmp_dir = tempfile.gettempdir()
            ts = int(time.time() * 1000)
            tmp_path = os.path.join(tmp_dir, f"mcg_preview_{os.getpid()}_{ts}.pdf")
            
            preview_doc.save(tmp_path, garbage=1)
            preview_doc.close()

            # Load into QPdfDocument for display
            self.pdf_doc.load(tmp_path)
            self.ui.pdfThumbViwerWidget.setDocument(self.pdf_doc)
            self.ui.pdfThumbViwerWidget.setPageMode(QPdfView.PageMode.SinglePage)
            self.ui.pdfThumbViwerWidget.setZoomMode(QPdfView.ZoomMode.FitInView)

            # Cleanup older preview files of this process to keep temp dir clean
            for f in os.listdir(tmp_dir):
                if f.startswith(f"mcg_preview_{os.getpid()}") and f != os.path.basename(tmp_path):
                    try:
                        os.remove(os.path.join(tmp_dir, f))
                    except (OSError, PermissionError):
                        pass # Still locked by viewer, will clean up next time
        except Exception as e:
            print(f"Preview update failed: {e}")

    def select_template(self):
        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF Template", initial_dir, "PDF Files (*.pdf)"
        )
        if file_path:
            file_path = QDir.toNativeSeparators(file_path)
            self.ui.templateFilePath_label.setText(file_path)
            self.importer.load_pdf_template(file_path)
            # Enable debug checkbox now that we have a template
            self.ui.debuggingMode_checkBox.setEnabled(True)
            self.ui.label_3.setEnabled(True)
            self._update_preview()
            self._save_state()

    # ── Font tab ──────────────────────────────────────────────────────────────

    def _add_font_group_box(self):
        group_box = QGroupBox("New Font")
        form = QFormLayout(group_box)

        name_label = QLabel("Font Name:")
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Enter font name")
        form.setWidget(0, QFormLayout.ItemRole.LabelRole, name_label)
        form.setWidget(0, QFormLayout.ItemRole.FieldRole, name_edit)

        loc_label_title = QLabel("Font Location:")
        loc_label = QLabel("Not Selected")
        loc_label.setWordWrap(True)
        form.setWidget(1, QFormLayout.ItemRole.LabelRole, loc_label_title)
        form.setWidget(1, QFormLayout.ItemRole.FieldRole, loc_label)

        select_btn = QPushButton("Select Font File")
        form.setWidget(2, QFormLayout.ItemRole.FieldRole, select_btn)

        delete_btn = QPushButton("Delete Font")
        delete_btn.setEnabled(True)
        form.setWidget(3, QFormLayout.ItemRole.LabelRole, delete_btn)

        entry = {
            "group_box": group_box,
            "name_edit": name_edit,
            "loc_label": loc_label,
            "delete_btn": delete_btn,
            "font_location": "",
            "font": None,
            "saved": False,
        }
        self._font_group_boxes.append(entry)

        select_btn.clicked.connect(lambda: self._select_font_for(entry))
        delete_btn.clicked.connect(lambda: self._delete_font_for(entry))
        name_edit.textChanged.connect(lambda _: self._save_font_for(entry))

        # Insert before the stretch at the end
        layout = self._font_scroll_layout
        layout.insertWidget(layout.count() - 1, group_box)

    def _select_font_for(self, entry: dict):
        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.FontsLocation)
        if not initial_dir or not os.path.exists(initial_dir):
            initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Font File", initial_dir,
            "Font Files (*.ttf *.otf *.woff *.woff2)"
        )
        if file_path:
            file_path = QDir.toNativeSeparators(file_path)
            entry["font_location"] = file_path
            entry["loc_label"].setText(file_path)
            if not entry["name_edit"].text().strip():
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                entry["name_edit"].setText(base_name)
            self._save_font_for(entry, show_status=True)

    def _save_font_for(self, entry: dict, show_status: bool = False):
        name = entry["name_edit"].text().strip()
        location = entry["font_location"]
        if not name or not location:
            return
        if not os.path.isfile(location):
            return

        old_name: str | None = None
        if entry["font"] is None:
            font = Font(font_name=name, font_location=location)
            entry["font"] = font
            self.fonts.append(font)
        else:
            # Capture the previous name so _refresh_font_combos can remap
            # any text-entry combo that was displaying the old name.
            old_name = entry["font"].font_name
            entry["font"].font_name = name
            entry["font"].font_location = location

        entry["saved"] = True
        entry["group_box"].setTitle(f"Font: {name}")
        self._refresh_font_combos(old_name=old_name, new_name=name)
        if show_status:
            self.statusBar().showMessage(f"Font '{name}' saved.", 3000)
        if not getattr(self, "_loading_state", False):
            self._update_preview()
            self._schedule_state_save()


    def _delete_font_for(self, entry: dict):
        if entry["font"] in self.fonts:
            self.fonts.remove(entry["font"])
        group_box = entry["group_box"]
        self._font_scroll_layout.removeWidget(group_box)
        group_box.deleteLater()
        if entry in self._font_group_boxes:
            self._font_group_boxes.remove(entry)
        self._refresh_font_combos()
        self.statusBar().showMessage("Font deleted.", 3000)
        if not getattr(self, "_loading_state", False):
            self._update_preview()
            self._schedule_state_save()

    def _refresh_font_combos(self, old_name: str | None = None, new_name: str | None = None):
        """Update font combo boxes in all text entries without losing selected value.

        Parameters
        ----------
        old_name:
            Previous font name when a font was *renamed* (None otherwise).
        new_name:
            Replacement font name when a font was *renamed* (None otherwise).

        Behaviour
        ---------
        * Deduplicates the font name list so the combo never shows the same
          name twice (guards against two font entries sharing a name).
        * When a font is renamed, any combo that was showing *old_name* is
          automatically updated to *new_name*, so the user's selection is
          preserved without any manual action.
        * When the effective selection changes (font deleted, or selection
          snapped to a different item), ``_save_text_entry`` is called so
          the underlying ``text_obj`` stays in sync with the visible combo.
        """
        # Deduplicate while preserving insertion order.
        font_names = list(dict.fromkeys(f.font_name for f in self.fonts))
        for entry in self.text_entries:
            combo = entry["selectFontForCurrentText_comboBox"]
            previous_text = combo.currentText()

            # If this combo was showing a font that was just renamed, follow it.
            target_text = previous_text
            if old_name is not None and previous_text == old_name and new_name is not None:
                target_text = new_name

            combo.blockSignals(True)
            combo.clear()
            combo.addItems(font_names)
            idx = combo.findText(target_text)
            if idx >= 0:
                combo.setCurrentIndex(idx)
            combo.blockSignals(False)

            # If the effective selection changed (e.g. renamed font, or deleted
            # font caused a fall-back to index 0), sync the model so text_obj
            # is not left referencing a stale/deleted Font object.
            if combo.currentText() != previous_text and not getattr(self, "_loading_state", False):
                self._save_text_entry(entry)


    # ── Text Body tab ─────────────────────────────────────────────────────────

    def _setup_text_body_tab(self):
        """Set up the Text Body tab with a scroll area, mirroring the Font tab pattern."""
        # Hide the designer template groupBox — we create them dynamically
        self.ui.TEXT_groupBox.hide()

        self._text_scroll_container = QWidget()
        self._text_scroll_layout = QVBoxLayout(self._text_scroll_container)
        self._text_scroll_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self._text_scroll_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Replace the text body tab's layout contents
        while self.ui.verticalLayout_6.count():
            self.ui.verticalLayout_6.takeAt(0)
        self.ui.verticalLayout_6.addWidget(self.ui.addNewText_pushButton)
        self.ui.verticalLayout_6.addWidget(scroll_area)

        self.ui.addNewText_pushButton.clicked.connect(self._add_text_group_box)

    def _get_csv_columns(self) -> list[str]:
        """Return imported CSV column names, or empty list if none loaded."""
        if self.importer.csv_data is not None:
            return self.importer.get_column_names()
        return []

    def _refresh_variable_columns(self):
        """Update selectVariables combo boxes in all text entries."""
        columns = self._get_csv_columns()
        for entry in self.text_entries:
            combo = entry["selectVariables_comboBox"]
            current = combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(columns)
            idx = combo.findText(current)
            if idx >= 0:
                combo.setCurrentIndex(idx)
            combo.blockSignals(False)
            self._save_text_entry(entry)

    def _add_text_group_box(self):
        idx = len(self.text_entries) + 1
        group_box = QGroupBox(f"Text: {idx}")
        group_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        grid = QGridLayout(group_box)

        # ── Row 0, cols 0-8: variable_or_constant + selectVariables (HBoxLayout) ─
        h_layout = QHBoxLayout()
        h_layout.setStretch(1, 1)

        var_const_combo = QComboBox()
        var_const_combo.addItems(["Variable", "Constant"])
        h_layout.addWidget(var_const_combo)

        select_var_combo = QComboBox()
        select_var_combo.addItems(self._get_csv_columns())
        h_layout.addWidget(select_var_combo)

        grid.addLayout(h_layout, 0, 0, 1, 10)

        # ── Row 0-1, col 9: vertical separator line ──────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        grid.addWidget(line, 0, 10, 4, 1)

        # ── Row 0-1, col 9: sendUp button ───────────────────────────────────
        send_up_btn = QPushButton()
        send_up_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        size_policy_min = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        send_up_btn.setSizePolicy(size_policy_min)
        grid.addWidget(send_up_btn, 0, 11, 2, 1)

        # ── Rows 1-2, cols 0-8: constantText_plainTextEdit ───────────────────
        constant_text = QPlainTextEdit()
        constant_text.setPlaceholderText("Write Text Here")
        constant_text.setMinimumHeight(50)
        constant_text.setMaximumHeight(70)
        grid.addWidget(constant_text, 1, 0, 2, 10)

        # ── Row 2-3, col 10: sendDown button ─────────────────────────────────
        send_down_btn = QPushButton()
        send_down_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        send_down_btn.setSizePolicy(size_policy_min)
        grid.addWidget(send_down_btn, 2, 11, 2, 1)

        # ── Row 3: Size | spinbox | sep | Bold | Italic | Underline | sep | Line Break
        size_policy_fixed = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_size = QLabel("Size:")
        label_size.setSizePolicy(size_policy_fixed)
        grid.addWidget(label_size, 3, 0, 1, 1)

        text_size_spin = QSpinBox()
        text_size_spin.setRange(1, 999)
        text_size_spin.setValue(12)
        grid.addWidget(text_size_spin, 3, 1, 1, 1)

        line_3 = QFrame()
        line_3.setFrameShape(QFrame.Shape.VLine)
        line_3.setFrameShadow(QFrame.Shadow.Sunken)
        grid.addWidget(line_3, 3, 2, 1, 1)

        is_bold_cb = QCheckBox("Bold")
        grid.addWidget(is_bold_cb, 3, 3, 1, 1)

        is_italic_cb = QCheckBox("Italic")
        grid.addWidget(is_italic_cb, 3, 4, 1, 1)

        is_underline_cb = QCheckBox("Underline")
        grid.addWidget(is_underline_cb, 3, 5, 1, 1)

        is_newline_cb = QCheckBox("Line Break")
        grid.addWidget(is_newline_cb, 3, 6, 1, 4)

        # ── Row 4: Font | font combo | Color | Delete ────────────────────────
        label_font = QLabel("Font:")
        label_font.setSizePolicy(size_policy_fixed)
        grid.addWidget(label_font, 4, 0, 1, 1)

        font_combo = QComboBox()
        font_combo.addItems([f.font_name for f in self.fonts])
        grid.addWidget(font_combo, 4, 1, 1, 4)

        color_btn = QPushButton("Color")
        grid.addWidget(color_btn, 4, 5, 1, 2)

        delete_btn = QPushButton("Delete")
        delete_btn.setEnabled(True)
        grid.addWidget(delete_btn, 4, 7, 1, 3)

        # Toggle visibility based on Variable/Constant choice
        def _on_type_changed(text):
            is_variable = text == "Variable"
            select_var_combo.setVisible(is_variable)
            constant_text.setVisible(not is_variable)

        var_const_combo.currentTextChanged.connect(_on_type_changed)
        # Default state: Variable selected → hide constantText, show selectVariables
        constant_text.setVisible(False)

        entry = {
            "group_box": group_box,
            "variable_or_constant_comboBox": var_const_combo,
            "selectVariables_comboBox": select_var_combo,
            "constantText_plainTextEdit": constant_text,
            "textSize_spinBox": text_size_spin,
            "isBold_checkBox": is_bold_cb,
            "isItalic_checkBox": is_italic_cb,
            "isUndrline_checkBox": is_underline_cb,
            "isNewlineAtEnd_checkBox": is_newline_cb,
            "selectFontForCurrentText_comboBox": font_combo,
            "color_btn": color_btn,
            "delete_btn": delete_btn,
            "text_obj": None,
            "saved": False,
            "current_color": QColor(0, 0, 0),
        }
        self.text_entries.append(entry)

        color_btn.clicked.connect(lambda: self._select_color_for(entry))
        send_up_btn.clicked.connect(lambda: self._move_text_entry(entry, -1))
        send_down_btn.clicked.connect(lambda: self._move_text_entry(entry, 1))
        delete_btn.clicked.connect(lambda: self._delete_text_entry(entry))

        # Event-driven auto-saving for all inputs
        var_const_combo.currentTextChanged.connect(lambda _: self._save_text_entry(entry))
        select_var_combo.currentTextChanged.connect(lambda _: self._save_text_entry(entry))
        constant_text.textChanged.connect(lambda: self._save_text_entry(entry))
        text_size_spin.valueChanged.connect(lambda _: self._save_text_entry(entry))
        is_bold_cb.toggled.connect(lambda _: self._save_text_entry(entry))
        is_italic_cb.toggled.connect(lambda _: self._save_text_entry(entry))
        is_underline_cb.toggled.connect(lambda _: self._save_text_entry(entry))
        is_newline_cb.toggled.connect(lambda _: self._save_text_entry(entry))
        font_combo.currentTextChanged.connect(lambda _: self._save_text_entry(entry))

        # Insert before the stretch at the end
        layout = self._text_scroll_layout
        layout.insertWidget(layout.count() - 1, group_box)

        if not getattr(self, "_loading_state", False):
            self._save_text_entry(entry)

    def _select_color_for(self, entry: dict):
        color = QColorDialog.getColor(entry["current_color"], self, "Select Text Color")
        if color.isValid():
            entry["current_color"] = color
            entry["color_btn"].setStyleSheet(f"background-color: {color.name()}")
            self._save_text_entry(entry)

    def _alignment_from_text(self, text: str) -> Alignment:
        mapping = {
            "LEFT": Alignment.LEFT,
            "CENTER": Alignment.CENTER,
            "RIGHT": Alignment.RIGHT,
            "JUSTIFY": Alignment.JUSTIFY,
        }
        return mapping.get(text, Alignment.CENTER)

    def _save_text_entry(self, entry: dict, show_status: bool = False):
        is_variable = entry["variable_or_constant_comboBox"].currentText() == "Variable"
        size = entry["textSize_spinBox"].value()
        bold = entry["isBold_checkBox"].isChecked()
        italic = entry["isItalic_checkBox"].isChecked()
        underline = entry["isUndrline_checkBox"].isChecked()
        newline = entry["isNewlineAtEnd_checkBox"].isChecked()
        ending = "<br/>" if newline else ""

        # Resolve selected font
        selected_font_name = entry["selectFontForCurrentText_comboBox"].currentText()
        selected_font = None
        for f in self.fonts:
            if f.font_name == selected_font_name:
                selected_font = [f]
                break

        color = entry["current_color"]
        color_tuple = (color.red(), color.green(), color.blue())

        kwargs = dict(
            text_size=float(size),
            is_bold=bold,
            is_italic=italic,
            is_underline=underline,
            font=selected_font,
            ending_constraints=ending,
            color=color_tuple,
        )

        if is_variable:
            col = entry["selectVariables_comboBox"].currentText()
            if not col:
                entry["text_obj"] = None
                self._sync_certificate_texts()
                return
            text_obj = VariableTexts(csv_column_name=col, **kwargs)
        else:
            body = entry["constantText_plainTextEdit"].toPlainText()
            text_obj = ConstantTexts(text_body=body, **kwargs)

        entry["text_obj"] = text_obj
        entry["saved"] = True
        entry["delete_btn"].setEnabled(True)
        idx = self.text_entries.index(entry) + 1
        entry["group_box"].setTitle(f"Text: {idx}")

        self._sync_certificate_texts()

        if show_status:
            self.statusBar().showMessage("Text block saved.", 3000)

        if not getattr(self, "_loading_state", False):
            self._update_preview()
            self._schedule_state_save()

    def _delete_text_entry(self, entry: dict):
        group_box = entry["group_box"]
        self._text_scroll_layout.removeWidget(group_box)
        group_box.deleteLater()
        if entry in self.text_entries:
            self.text_entries.remove(entry)
        self._renumber_text_entries()
        self._sync_certificate_texts()
        self.statusBar().showMessage("Text block deleted.", 3000)
        if not getattr(self, "_loading_state", False):
            self._update_preview()
            self._schedule_state_save()

    def _move_text_entry(self, entry: dict, direction: int):
        """Move a text entry up (-1) or down (+1) in the list."""
        idx = self.text_entries.index(entry)
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(self.text_entries):
            return

        # Swap in the data list
        self.text_entries[idx], self.text_entries[new_idx] = (
            self.text_entries[new_idx], self.text_entries[idx]
        )

        # Re-insert widgets in correct visual order.
        # After removeWidget, only the stretch spacer remains at index 0.
        # insertWidget(i, ...) places each box before the stretch → [box0, box1, …, stretch].
        # Using (i+1) would insert AFTER the stretch → stretch ends up at the top (visual bug).
        for e in self.text_entries:
            self._text_scroll_layout.removeWidget(e["group_box"])
        for i, e in enumerate(self.text_entries):
            self._text_scroll_layout.insertWidget(i, e["group_box"])

        self._renumber_text_entries()
        self._sync_certificate_texts()
        if not getattr(self, "_loading_state", False):
            self._update_preview()
            self._schedule_state_save()

    def _renumber_text_entries(self):
        """Update group box titles to reflect current ordering."""
        for i, entry in enumerate(self.text_entries):
            entry["group_box"].setTitle(f"Text: {i + 1}")

    # ── Import Data tab ───────────────────────────────────────────────────────

    def select_import_file(self):
        fmt = self.ui.importFileFotmat_comboBox.currentText()
        if "Excel" in fmt:
            filter_str = "Excel Files (*.xlsx *.xls)"
        else:
            filter_str = "CSV Files (*.csv)"

        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Data File", initial_dir, filter_str
        )
        if file_path:
            file_path = QDir.toNativeSeparators(file_path)
            self.ui.imoportFilePath_label.setText(file_path)
            self.importer.load_csv(file_path)
            columns = self.importer.get_column_names()
            self.ui.importFiile_columHeaders_label.setText(", ".join(columns))
            self.ui.imortData_groupBox.setTitle(
                f"Import data from file ({self.importer.data_count} rows)"
            )
            self.statusBar().showMessage(
                f"Loaded {self.importer.data_count} rows with {self.importer.csv_column_count} columns.", 3000
            )
            # Refresh variable column choices in existing text entries
            self._refresh_variable_columns()
            # Populate export name-column combo
            self.ui.oututFiileNameField_comboBox.clear()
            self.ui.oututFiileNameField_comboBox.addItems(columns)
            self._update_preview()
            self._save_state()

    # ── Export tab ──────────────────────────────────────────────────────────────

    def select_export_location(self):
        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        folder = QFileDialog.getExistingDirectory(
            self, "Select Export Folder", initial_dir
        )
        if folder:
            folder = QDir.toNativeSeparators(folder)
            self.ui.exportFolderLocaion_label.setText(folder)
            self.exporter.set_output_folder(folder)
            self.statusBar().showMessage(f"Export folder set to: {folder}", 3000)
            self._save_state()

    def do_export(self):
        if not self.exporter.output_folder_path:
            self.statusBar().showMessage("Please select an export folder first.", 3000)
            return
        if self.importer.csv_data is None or self.importer.template_doc is None:
            self.statusBar().showMessage(
                "Please load a PDF template and import data first.", 3000)
            return

        self._auto_save_all()
        self._sync_certificate_coordinates()
        self._save_state()

        combo_text = self.ui.singleFile_multipleFiile_comboBox.currentText()
        if "Single" in combo_text:
            self.exporter.output_type = OutputType.SINGLE_FILE
        else:
            self.exporter.output_type = OutputType.INDIVIDUAL_FILE

        # Use the name-column combo for individual file naming
        name_col = self.ui.oututFiileNameField_comboBox.currentText()
        if name_col:
            self.exporter.name_column = name_col

        self.certificate.list_fonts = self.fonts

        try:
            self.exporter.export(self.certificate)
            self.statusBar().showMessage("Export completed successfully!", 5000)
        except Exception as e:
            self.statusBar().showMessage(f"Export failed: {e}", 5000)

    # ── State persistence ─────────────────────────────────────────────────────

    def _save_state(self) -> None:
        """Serialize all UI and model state to mcg_session_state.json with descriptive comments."""
        state = {
            "_header": "Mass Certificate Generator (MCG) - Session State Configuration",
            "_description": (
                "This file automatically preserves your current session state across application runs. "
                "It records the loaded PDF template, coordinates, alignment, custom fonts, text layers, "
                "CSV/Excel data bindings, and export configurations."
            ),
            "_notes": (
                "Auto-generated by MCG. You do not need to modify this file manually. "
                "If settings become invalid or you want to start fresh, simply delete this file."
            ),
            "app_version": version.APP_VERSION_STR,
            "template_path": self.ui.templateFilePath_label.text(),
            "coordinates": {
                "_info": "Bounding box percentages (0-100) for the certificate text region",
                "top_left_x": self.ui.topLeft_x_spinBox.value(),
                "top_left_y": self.ui.topLeft_y_spinBox.value(),
                "bottom_right_x": self.ui.bottomRight_x_spinBox.value(),
                "bottom_right_y": self.ui.bottomRight_y_spinBox.value(),
            },
            "alignment": self.ui.currentTextAlignment_comboBox.currentText(),
            "debug_mode": self.ui.debuggingMode_checkBox.isChecked(),
            "fonts": [
                {"name": e["name_edit"].text(), "location": e["font_location"]}
                for e in self._font_group_boxes if e["saved"]
            ],
            "text_entries": [],
            "import": {
                "_info": "Source data file (CSV or Excel) and format selection",
                "file_path": self.ui.imoportFilePath_label.text(),
                "format_index": self.ui.importFileFotmat_comboBox.currentIndex(),
            },
            "export": {
                "_info": "Export output folder, file format, and naming column",
                "folder": self.ui.exportFolderLocaion_label.text(),
                "type_index": self.ui.singleFile_multipleFiile_comboBox.currentIndex(),
                "name_column": self.ui.oututFiileNameField_comboBox.currentText(),
                "format_index": self.ui.outputFormat_comboBox.currentIndex(),
            },
            "current_tab": self.ui.pipeline_tabWidget.currentIndex(),
        }

        for entry in self.text_entries:
            te = {
                "type": entry["variable_or_constant_comboBox"].currentText(),
                "variable_column": entry["selectVariables_comboBox"].currentText(),
                "constant_text": entry["constantText_plainTextEdit"].toPlainText(),
                "text_size": entry["textSize_spinBox"].value(),
                "bold": entry["isBold_checkBox"].isChecked(),
                "italic": entry["isItalic_checkBox"].isChecked(),
                "underline": entry["isUndrline_checkBox"].isChecked(),
                "newline": entry["isNewlineAtEnd_checkBox"].isChecked(),
                "font": entry["selectFontForCurrentText_comboBox"].currentText(),
                "color": entry["current_color"].name(),
                "saved": entry["saved"],
            }
            state["text_entries"].append(te)

        try:
            state_file = get_state_file_path()
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except OSError:
            pass

    def _load_state(self) -> None:
        """Restore UI and model state from a previously saved JSON file."""
        state_file = get_state_file_path()
        if not os.path.isfile(state_file):
            return
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
        except (OSError, json.JSONDecodeError):
            return

        # ── Template ──────────────────────────────────────────────────────
        template_path = state.get("template_path", "")
        if template_path and os.path.isfile(template_path):
            self.ui.templateFilePath_label.setText(template_path)
            self.importer.load_pdf_template(template_path)
            self.ui.debuggingMode_checkBox.setEnabled(True)
            self.ui.label_3.setEnabled(True)

        # ── Import data ───────────────────────────────────────────────────
        imp = state.get("import", {})
        self.ui.importFileFotmat_comboBox.setCurrentIndex(imp.get("format_index", 0))
        imp_path = imp.get("file_path", "")
        if imp_path and os.path.isfile(imp_path):
            self.ui.imoportFilePath_label.setText(imp_path)
            try:
                self.importer.load_csv(imp_path)
                columns = self.importer.get_column_names()
                self.ui.importFiile_columHeaders_label.setText(", ".join(columns))
                self.ui.imortData_groupBox.setTitle(
                    f"Import data from file ({self.importer.data_count} rows)")
                self.ui.oututFiileNameField_comboBox.clear()
                self.ui.oututFiileNameField_comboBox.addItems(columns)
            except Exception:
                pass

        # ── Fonts ─────────────────────────────────────────────────────────
        # Disable preview updates during bulk loading
        original_update = self._update_preview
        self._update_preview = lambda: None 
        self._loading_state = True

        try:
            for font_data in state.get("fonts", []):
                name = font_data.get("name", "")
                location = font_data.get("location", "")
                if not name or not location:
                    continue
                self._add_font_group_box()
                entry = self._font_group_boxes[-1]
                entry["name_edit"].setText(name)
                entry["font_location"] = location
                entry["loc_label"].setText(location)
                self._save_font_for(entry)

            # ── Text entries ──────────────────────────────────────────────────
            for te in state.get("text_entries", []):
                self._add_text_group_box()
                entry = self.text_entries[-1]
                entry["variable_or_constant_comboBox"].setCurrentText(te.get("type", "Variable"))
                entry["selectVariables_comboBox"].setCurrentText(te.get("variable_column", ""))
                entry["constantText_plainTextEdit"].setPlainText(te.get("constant_text", ""))
                entry["textSize_spinBox"].setValue(te.get("text_size", 12))
                entry["isBold_checkBox"].setChecked(te.get("bold", False))
                entry["isItalic_checkBox"].setChecked(te.get("italic", False))
                entry["isUndrline_checkBox"].setChecked(te.get("underline", False))
                entry["isNewlineAtEnd_checkBox"].setChecked(te.get("newline", False))
                entry["selectFontForCurrentText_comboBox"].setCurrentText(te.get("font", ""))
                
                color_str = te.get("color", "#000000")
                entry["current_color"] = QColor(color_str)
                entry["color_btn"].setStyleSheet(f"background-color: {color_str}")

                self._save_text_entry(entry)

            # ── Coordinates ───────────────────────────────────────────────────
            coords = state.get("coordinates", {})
            self.ui.topLeft_x_spinBox.setValue(coords.get("top_left_x", 0))
            self.ui.topLeft_y_spinBox.setValue(coords.get("top_left_y", 0))
            self.ui.bottomRight_x_spinBox.setValue(coords.get("bottom_right_x", 0))
            self.ui.bottomRight_y_spinBox.setValue(coords.get("bottom_right_y", 0))

            # ── Alignment ─────────────────────────────────────────────────────
            align_text = state.get("alignment", "CENTER")
            self.ui.currentTextAlignment_comboBox.setCurrentText(align_text)
            self.certificate.alignment = self._alignment_from_text(align_text)

            # ── Debug mode ────────────────────────────────────────────────────
            self.ui.debuggingMode_checkBox.setChecked(state.get("debug_mode", False))

            # ── Export settings ───────────────────────────────────────────────
            exp = state.get("export", {})
            exp_folder = exp.get("folder", "")
            if exp_folder and exp_folder != "Not Selected":
                self.ui.exportFolderLocaion_label.setText(exp_folder)
                if os.path.isdir(exp_folder):
                    self.exporter.set_output_folder(exp_folder)
            self.ui.singleFile_multipleFiile_comboBox.setCurrentIndex(exp.get("type_index", 0))
            name_col = exp.get("name_column", "")
            if name_col:
                idx = self.ui.oututFiileNameField_comboBox.findText(name_col)
                if idx >= 0:
                    self.ui.oututFiileNameField_comboBox.setCurrentIndex(idx)
            
            self.ui.outputFormat_comboBox.setCurrentIndex(exp.get("format_index", 0))

            # ── Restore tab ──────────────────────────────────────────────────
            self.ui.pipeline_tabWidget.setCurrentIndex(state.get("current_tab", 0))
        finally:
            self._loading_state = False
            self._sync_certificate_texts()
            # Re-enable and call once
            self._update_preview = original_update

        # ── Refresh preview ───────────────────────────────────────────────
        try:
            self._update_preview()
        except Exception as e:
            print(f"Failed to restore preview: {e}")

    def closeEvent(self, event: QCloseEvent) -> None:
        self._save_state()
        super().closeEvent(event)


if __name__ == "__main__":
    version.setup_windows_console()
    app = QApplication(sys.argv)
    app.setApplicationName(version.APP_NAME)
    app.setApplicationDisplayName(version.APP_DISPLAY_NAME)
    app.setOrganizationName(version.ORGANIZATION_NAME)
    app.setOrganizationDomain(version.ORGANIZATION_DOMAIN)
    app.setApplicationVersion(version.APP_VERSION_STR)

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
