# -*- coding: utf-8 -*-
#
# PyUICBasicDemo.py — Redesigned UI
# Industrial HMI aesthetic: gunmetal panels, amber/green indicators,
# JetBrains Mono typography, precision engineering tone.
#
# Drop-in replacement for the pyuic5-generated file.
# All widget names are identical to the original so BasicDemo_with_gonogo.py
# requires zero changes.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QGradient


# ── Palette & tokens ─────────────────────────────────────────────────────────

BG_BASE       = "#0d0f11"   # near-black base
BG_PANEL      = "#13171c"   # panel background
BG_CARD       = "#1a1f26"   # card / group background
BG_INPUT      = "#0d0f11"   # input fields
BORDER_DIM    = "#2a313b"   # subtle borders
BORDER_MID    = "#3a4455"   # medium borders
ACCENT_AMBER  = "#e8a020"   # amber — primary accent
ACCENT_GREEN  = "#2ecc71"   # go-green
ACCENT_RED    = "#e74c3c"   # no-go red
ACCENT_BLUE   = "#4a9eff"   # info blue
TEXT_PRIMARY  = "#dce8f0"   # bright text
TEXT_MUTED    = "#5a6a7a"   # dimmed labels
TEXT_DIM      = "#3a4a5a"   # very dim decorative text

FONT_MONO  = "JetBrains Mono, Consolas, Courier New, monospace"
FONT_SANS  = "Segoe UI, SF Pro Display, Helvetica Neue, sans-serif"


# ── Global stylesheet ─────────────────────────────────────────────────────────

STYLESHEET = f"""
/* ── Base ── */
QMainWindow, QWidget {{
    background-color: {BG_BASE};
    color: {TEXT_PRIMARY};
    font-family: {FONT_MONO};
    font-size: 14px;
}}

/* ── Group boxes ── */
QGroupBox {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER_DIM};
    border-radius: 6px;
    margin-top: 26px;
    padding: 10px 8px 8px 8px;
    font-family: {FONT_MONO};
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
    color: {TEXT_MUTED};
    text-transform: uppercase;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    top: 4px;
    padding: 0 6px;
    background-color: {BG_CARD};
    color: {ACCENT_AMBER};
    letter-spacing: 3px;
}}

/* ── Push buttons ── */
QPushButton {{
    background-color: {BG_PANEL};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_MID};
    border-radius: 4px;
    padding: 8px 12px;
    font-family: {FONT_MONO};
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 1px;
    min-height: 34px;
}}
QPushButton:hover {{
    background-color: #1e2530;
    border-color: {ACCENT_AMBER};
    color: {ACCENT_AMBER};
}}
QPushButton:pressed {{
    background-color: #111620;
    border-color: {ACCENT_AMBER};
    padding-top: 9px;
    padding-bottom: 7px;
}}
QPushButton:disabled {{
    background-color: #111418;
    border-color: {BORDER_DIM};
    color: {TEXT_DIM};
}}

/* ── Find Device ── */
QPushButton#bnEnum {{
    background-color: {ACCENT_BLUE};
    border-color: {ACCENT_BLUE};
    color: #000000;
    letter-spacing: 2px;
    font-weight: bold;
}}
QPushButton#bnEnum:hover {{
    background-color: #7bbfff;
    border-color: #7bbfff;
    color: #000000;
}}
QPushButton#bnEnum:pressed {{
    background-color: #2a7acc;
    border-color: #2a7acc;
    color: #ffffff;
}}

/* ── Start ── */
QPushButton#bnStart {{
    background-color: {ACCENT_GREEN};
    border-color: {ACCENT_GREEN};
    color: #000000;
    font-weight: bold;
}}
QPushButton#bnStart:hover {{
    background-color: #55e899;
    border-color: #55e899;
    color: #000000;
}}
QPushButton#bnStart:pressed {{
    background-color: #1fa050;
    color: #ffffff;
}}
QPushButton#bnStart:disabled {{
    background-color: #111418;
    border-color: {BORDER_DIM};
    color: {TEXT_DIM};
}}

/* ── Stop ── */
QPushButton#bnStop {{
    background-color: {ACCENT_RED};
    border-color: {ACCENT_RED};
    color: #ffffff;
    font-weight: bold;
}}
QPushButton#bnStop:hover {{
    background-color: #ff5a4a;
    border-color: #ff5a4a;
    color: #ffffff;
}}
QPushButton#bnStop:pressed {{
    background-color: #b02a1e;
    color: #ffffff;
}}
QPushButton#bnStop:disabled {{
    background-color: #111418;
    border-color: {BORDER_DIM};
    color: {TEXT_DIM};
}}

/* ── Trigger Once ── */
QPushButton#bnSoftwareTrigger {{
    background-color: {ACCENT_AMBER};
    border-color: {ACCENT_AMBER};
    color: #000000;
    letter-spacing: 1px;
    font-weight: bold;
}}
QPushButton#bnSoftwareTrigger:hover {{
    background-color: #ffbe45;
    border-color: #ffbe45;
    color: #000000;
}}
QPushButton#bnSoftwareTrigger:pressed {{
    background-color: #b07010;
    color: #ffffff;
}}
QPushButton#bnSoftwareTrigger:disabled {{
    background-color: #111418;
    border-color: {BORDER_DIM};
    color: {TEXT_DIM};
}}

/* ── Save Image ── */
QPushButton#bnSaveImage {{
    background-color: #9b59b6;
    border-color: #9b59b6;
    color: #ffffff;
    letter-spacing: 1px;
    font-weight: bold;
}}
QPushButton#bnSaveImage:hover {{
    background-color: #b07cc8;
    border-color: #b07cc8;
    color: #ffffff;
}}
QPushButton#bnSaveImage:pressed {{
    background-color: #6c3483;
    color: #ffffff;
}}
QPushButton#bnSaveImage:disabled {{
    background-color: #111418;
    border-color: {BORDER_DIM};
    color: {TEXT_DIM};
}}

/* ── Open Device ── */
QPushButton#bnOpen {{
    background-color: #27ae60;
    border-color: #27ae60;
    color: #000000;
    font-weight: bold;
}}
QPushButton#bnOpen:hover {{
    background-color: #2ecc71;
    border-color: #2ecc71;
    color: #000000;
}}
QPushButton#bnOpen:pressed {{
    background-color: #1a7a40;
    color: #ffffff;
}}

/* ── Close Device ── */
QPushButton#bnClose {{
    background-color: #c0392b;
    border-color: #c0392b;
    color: #ffffff;
    font-weight: bold;
}}
QPushButton#bnClose:hover {{
    background-color: {ACCENT_RED};
    border-color: {ACCENT_RED};
    color: #ffffff;
}}
QPushButton#bnClose:pressed {{
    background-color: #8a1f15;
    color: #ffffff;
}}
QPushButton#bnClose:disabled {{
    background-color: #111418;
    border-color: {BORDER_DIM};
    color: {TEXT_DIM};
}}

/* ── Get / Set param ── */
QPushButton#bnGetParam {{
    font-size: 12px;
    background-color: {ACCENT_BLUE};
    border-color: {ACCENT_BLUE};
    color: #000000;
    font-weight: bold;
}}
QPushButton#bnGetParam:hover {{
    background-color: #7bbfff;
    border-color: #7bbfff;
    color: #000000;
}}
QPushButton#bnSetParam {{
    font-size: 12px;
    background-color: {ACCENT_AMBER};
    border-color: {ACCENT_AMBER};
    color: #000000;
    font-weight: bold;
}}
QPushButton#bnSetParam:hover {{
    background-color: #ffbe45;
    border-color: #ffbe45;
    color: #000000;
}}

/* ── ComboBox ── */
QComboBox {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER_MID};
    border-radius: 4px;
    padding: 5px 10px;
    color: {TEXT_PRIMARY};
    font-family: {FONT_MONO};
    font-size: 13px;
    min-height: 32px;
    selection-background-color: #1e2a3e;
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {ACCENT_AMBER};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER_MID};
    color: {TEXT_PRIMARY};
    font-size: 13px;
    selection-background-color: #1e2a3e;
    outline: none;
}}

/* ── Line edits ── */
QLineEdit {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER_MID};
    border-radius: 3px;
    padding: 5px 8px;
    color: {ACCENT_AMBER};
    font-family: {FONT_MONO};
    font-size: 14px;
    selection-background-color: #2a3a50;
}}
QLineEdit:focus {{
    border-color: {ACCENT_AMBER};
    background-color: #0f1215;
}}

/* ── Labels ── */
QLabel {{
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 12px;
    letter-spacing: 1px;
    background: transparent;
}}

/* ── Radio buttons ── */
QRadioButton {{
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 12px;
    spacing: 7px;
    letter-spacing: 1px;
}}
QRadioButton::indicator {{
    width: 13px;
    height: 13px;
    border-radius: 7px;
    border: 2px solid {BORDER_MID};
    background-color: {BG_BASE};
}}
QRadioButton::indicator:checked {{
    background-color: {ACCENT_AMBER};
    border-color: {ACCENT_AMBER};
}}
QRadioButton::indicator:hover {{
    border-color: {ACCENT_AMBER};
}}
QRadioButton:checked {{
    color: {ACCENT_AMBER};
}}

/* ── Scrollbars ── */
QScrollBar:vertical {{
    background: {BG_BASE};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_MID};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* ── Status bar ── */
QStatusBar {{
    background-color: {BG_PANEL};
    border-top: 1px solid {BORDER_DIM};
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 10px;
    letter-spacing: 1px;
}}

/* ── Dock widget ── */
QDockWidget {{
    background-color: {BG_PANEL};
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 10px;
    letter-spacing: 2px;
    titlebar-close-icon: none;
}}
QDockWidget::title {{
    background-color: {BG_CARD};
    padding: 6px 10px;
    border-bottom: 1px solid {BORDER_DIM};
    color: {ACCENT_AMBER};
    font-weight: bold;
    letter-spacing: 3px;
    text-transform: uppercase;
}}

/* ── Tooltip ── */
QToolTip {{
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    border: 1px solid {ACCENT_AMBER};
    font-family: {FONT_MONO};
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 3px;
}}

/* ── Message box ── */
QMessageBox {{
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
}}
QMessageBox QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 12px;
}}
QMessageBox QPushButton {{
    min-width: 80px;
}}
"""


# ── Separator widget  ─────────────────────────────────────────────────────────

class HLineSeparator(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setStyleSheet(f"color: {BORDER_DIM}; background: {BORDER_DIM}; max-height: 1px;")


# ── Status indicator LED ──────────────────────────────────────────────────────

class StatusLED(QtWidgets.QWidget):
    """A small circular LED indicator."""
    OFF     = "#1a1a1a"
    GREEN   = ACCENT_GREEN
    AMBER   = ACCENT_AMBER
    RED     = ACCENT_RED

    def __init__(self, color=None, parent=None):
        super().__init__(parent)
        self._color = color or self.OFF
        self.setFixedSize(10, 10)

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QBrush, QPen, QRadialGradient
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(1, 1, -1, -1)
        grad = QRadialGradient(r.center().x() - 1, r.center().y() - 1, r.width() / 2)
        c = QColor(self._color)
        grad.setColorAt(0.0, c.lighter(160))
        grad.setColorAt(1.0, c.darker(130))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(c.darker(150), 1))
        p.drawEllipse(r)


# ── Camera feed placeholder  ──────────────────────────────────────────────────

class CameraViewport(QtWidgets.QWidget):
    """
    Replaces the plain QWidget used as the display surface.
    Renders a dark panel with a scanline-style crosshair overlay
    when not streaming. The HIK SDK writes directly to this widget's
    WinId so it must remain a plain QWidget underneath.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("widgetDisplay")
        self._streaming = False
        self.setMinimumSize(511, 401)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)

    def set_streaming(self, state: bool):
        self._streaming = state
        self.update()

    def paintEvent(self, event):
        if self._streaming:
            return   # SDK owns the surface while streaming
        from PyQt5.QtGui import QPainter, QPen, QBrush, QLinearGradient
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Background
        p.fillRect(self.rect(), QColor(BG_BASE))

        # Subtle grid
        pen = QPen(QColor(BORDER_DIM), 1)
        pen.setStyle(Qt.DotLine)
        p.setPen(pen)
        step = 40
        for x in range(0, w, step):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, step):
            p.drawLine(0, y, w, y)

        # Centre crosshair
        cx, cy = w // 2, h // 2
        p.setPen(QPen(QColor(BORDER_MID), 1))
        p.drawLine(cx - 20, cy, cx + 20, cy)
        p.drawLine(cx, cy - 20, cx, cy + 20)
        p.drawRect(cx - 40, cy - 30, 80, 60)

        # Corner brackets
        p.setPen(QPen(QColor(ACCENT_AMBER), 2))
        L = 18
        corners = [(10, 10), (w - 10, 10), (10, h - 10), (w - 10, h - 10)]
        dirs = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for (ox, oy), (dx, dy) in zip(corners, dirs):
            p.drawLine(ox, oy, ox + dx * L, oy)
            p.drawLine(ox, oy, ox, oy + dy * L)

        # Label
        p.setPen(QPen(QColor(TEXT_DIM)))
        p.setFont(QFont("JetBrains Mono, Consolas", 13, QFont.Normal))
        p.drawText(self.rect(), Qt.AlignCenter, "[ NO SIGNAL ]")


# ── Main UI class (drop-in replacement) ──────────────────────────────────────

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 780)
        MainWindow.setMinimumSize(QSize(1100, 680))

        # Apply global stylesheet
        MainWindow.setStyleSheet(STYLESHEET)

        # ── Central widget ──────────────────────────────────────────────────
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.setStyleSheet(f"background-color: {BG_BASE};")

        # Root layout: left column (camera) | right column (controls)
        root = QtWidgets.QHBoxLayout(self.centralWidget)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ── LEFT: camera column ─────────────────────────────────────────────
        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(8)

        # Device selector row
        dev_row = QtWidgets.QHBoxLayout()
        dev_row.setSpacing(8)

        dev_icon = QtWidgets.QLabel("⬡")
        dev_icon.setStyleSheet(f"color: {ACCENT_AMBER}; font-size: 14px; background: transparent;")
        dev_icon.setFixedWidth(18)

        self.ComboDevices = QtWidgets.QComboBox(self.centralWidget)
        self.ComboDevices.setObjectName("ComboDevices")
        self.ComboDevices.setToolTip("Select camera device")
        self.ComboDevices.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        dev_row.addWidget(dev_icon)
        dev_row.addWidget(self.ComboDevices, 1)
        left_col.addLayout(dev_row)

        # Camera viewport
        self.widgetDisplay = CameraViewport(self.centralWidget)
        self.widgetDisplay.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        left_col.addWidget(self.widgetDisplay, 1)

        # Bottom status strip
        strip = QtWidgets.QHBoxLayout()
        strip.setSpacing(12)

        def _make_status_chip(label_text):
            w = QtWidgets.QWidget()
            w.setStyleSheet(f"""
                QWidget {{
                    background: {BG_PANEL};
                    border: 1px solid {BORDER_DIM};
                    border-radius: 3px;
                }}
            """)
            hl = QtWidgets.QHBoxLayout(w)
            hl.setContentsMargins(8, 3, 8, 3)
            hl.setSpacing(6)
            led = StatusLED(StatusLED.OFF, w)
            lbl = QtWidgets.QLabel(label_text, w)
            lbl.setStyleSheet(f"font-size: 11px; letter-spacing: 2px; color: {TEXT_DIM}; border: none; background: transparent;")
            hl.addWidget(led)
            hl.addWidget(lbl)
            return w, led

        self._chip_conn, self._led_conn  = _make_status_chip("DEVICE")
        self._chip_grab, self._led_grab  = _make_status_chip("STREAM")

        strip.addWidget(self._chip_conn)
        strip.addWidget(self._chip_grab)
        strip.addStretch()

        coord_lbl = QtWidgets.QLabel("HIK VISION  ·  MV SDK")
        coord_lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_DIM}; letter-spacing: 2px; background: transparent;")
        strip.addWidget(coord_lbl)

        left_col.addLayout(strip)
        root.addLayout(left_col, 1)

        # ── RIGHT: controls column ──────────────────────────────────────────
        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(10)
        right_col.setContentsMargins(0, 0, 0, 0)

        # ── GROUP: Initialization ───────────────────────────────────────────
        self.groupInit = QtWidgets.QGroupBox("Initialization", self.centralWidget)
        self.groupInit.setObjectName("groupInit")
        self.groupInit.setFixedWidth(270)

        init_layout = QtWidgets.QVBoxLayout(self.groupInit)
        init_layout.setContentsMargins(10, 18, 10, 10)
        init_layout.setSpacing(7)

        self.bnEnum = QtWidgets.QPushButton("⬡  FIND DEVICES", self.groupInit)
        self.bnEnum.setObjectName("bnEnum")
        self.bnEnum.setToolTip("Enumerate connected cameras")
        self.bnEnum.setMinimumHeight(38)

        open_close_row = QtWidgets.QHBoxLayout()
        open_close_row.setSpacing(6)

        self.bnOpen = QtWidgets.QPushButton("▶  OPEN", self.groupInit)
        self.bnOpen.setObjectName("bnOpen")
        self.bnOpen.setToolTip("Open selected device")

        self.bnClose = QtWidgets.QPushButton("■  CLOSE", self.groupInit)
        self.bnClose.setObjectName("bnClose")
        self.bnClose.setEnabled(False)
        self.bnClose.setToolTip("Close device")

        open_close_row.addWidget(self.bnOpen)
        open_close_row.addWidget(self.bnClose)

        init_layout.addWidget(self.bnEnum)
        init_layout.addLayout(open_close_row)

        right_col.addWidget(self.groupInit)

        # ── GROUP: Acquisition ──────────────────────────────────────────────
        self.groupGrab = QtWidgets.QGroupBox("Acquisition", self.centralWidget)
        self.groupGrab.setObjectName("groupGrab")
        self.groupGrab.setEnabled(False)
        self.groupGrab.setFixedWidth(270)

        grab_layout = QtWidgets.QVBoxLayout(self.groupGrab)
        grab_layout.setContentsMargins(10, 18, 10, 10)
        grab_layout.setSpacing(7)

        # Mode row
        mode_row = QtWidgets.QHBoxLayout()
        mode_row.setSpacing(10)
        self.radioContinueMode = QtWidgets.QRadioButton("CONTINUOUS", self.groupGrab)
        self.radioContinueMode.setObjectName("radioContinueMode")
        self.radioTriggerMode  = QtWidgets.QRadioButton("TRIGGER", self.groupGrab)
        self.radioTriggerMode.setObjectName("radioTriggerMode")
        mode_row.addWidget(self.radioContinueMode)
        mode_row.addWidget(self.radioTriggerMode)

        # Start / Stop row
        ss_row = QtWidgets.QHBoxLayout()
        ss_row.setSpacing(6)
        self.bnStart = QtWidgets.QPushButton("▶  START", self.groupGrab)
        self.bnStart.setObjectName("bnStart")
        self.bnStart.setEnabled(False)
        self.bnStop  = QtWidgets.QPushButton("■  STOP", self.groupGrab)
        self.bnStop.setObjectName("bnStop")
        self.bnStop.setEnabled(False)
        ss_row.addWidget(self.bnStart)
        ss_row.addWidget(self.bnStop)

        self.bnSoftwareTrigger = QtWidgets.QPushButton("◉  TRIGGER ONCE", self.groupGrab)
        self.bnSoftwareTrigger.setObjectName("bnSoftwareTrigger")
        self.bnSoftwareTrigger.setEnabled(False)

        grab_layout.addLayout(mode_row)
        grab_layout.addLayout(ss_row)
        grab_layout.addWidget(self.bnSoftwareTrigger)
        grab_layout.addWidget(HLineSeparator(self.groupGrab))

        self.bnSaveImage = QtWidgets.QPushButton("⬇  SAVE FRAME", self.groupGrab)
        self.bnSaveImage.setObjectName("bnSaveImage")
        self.bnSaveImage.setEnabled(False)
        grab_layout.addWidget(self.bnSaveImage)

        right_col.addWidget(self.groupGrab)

        # ── GROUP: Parameters ───────────────────────────────────────────────
        self.groupParam = QtWidgets.QGroupBox("Parameters", self.centralWidget)
        self.groupParam.setObjectName("groupParam")
        self.groupParam.setEnabled(False)
        self.groupParam.setFixedWidth(270)

        param_layout = QtWidgets.QGridLayout(self.groupParam)
        param_layout.setContentsMargins(10, 22, 10, 10)
        param_layout.setSpacing(7)
        param_layout.setColumnStretch(0, 2)
        param_layout.setColumnStretch(1, 3)

        def _param_label(text):
            lbl = QtWidgets.QLabel(text)
            lbl.setStyleSheet(f"""
                color: {TEXT_MUTED};
                font-size: 9px;
                letter-spacing: 2px;
                background: transparent;
            """)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return lbl

        self.label_4    = _param_label("EXPOSURE")
        self.edtExposureTime = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtExposureTime.setObjectName("edtExposureTime")
        self.edtExposureTime.setAlignment(Qt.AlignRight)

        self.label_5    = _param_label("GAIN")
        self.edtGain    = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtGain.setObjectName("edtGain")
        self.edtGain.setAlignment(Qt.AlignRight)

        self.label_6    = _param_label("FRAME RATE")
        self.edtFrameRate = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtFrameRate.setObjectName("edtFrameRate")
        self.edtFrameRate.setAlignment(Qt.AlignRight)

        param_layout.addWidget(self.label_4,         0, 0)
        param_layout.addWidget(self.edtExposureTime, 0, 1)
        param_layout.addWidget(self.label_5,         1, 0)
        param_layout.addWidget(self.edtGain,         1, 1)
        param_layout.addWidget(self.label_6,         2, 0)
        param_layout.addWidget(self.edtFrameRate,    2, 1)

        getset_row = QtWidgets.QHBoxLayout()
        getset_row.setSpacing(6)
        self.bnGetParam = QtWidgets.QPushButton("↓ GET", self.groupParam)
        self.bnGetParam.setObjectName("bnGetParam")
        self.bnSetParam = QtWidgets.QPushButton("↑ SET", self.groupParam)
        self.bnSetParam.setObjectName("bnSetParam")
        getset_row.addWidget(self.bnGetParam)
        getset_row.addWidget(self.bnSetParam)
        param_layout.addLayout(getset_row, 3, 0, 1, 2)

        right_col.addWidget(self.groupParam)
        right_col.addStretch(1)

        root.addLayout(right_col, 0)

        # ── Status bar ──────────────────────────────────────────────────────
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.showMessage("  SYSTEM READY  ·  SELECT DEVICE AND CLICK FIND")

        MainWindow.setCentralWidget(self.centralWidget)
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Wire LED updates via button connections (done after signals are set)
        self._wire_leds(MainWindow)

    def _wire_leds(self, MainWindow):
        """
        Hook into bnOpen / bnClose / bnStart / bnStop to update
        the status LEDs in the camera strip. Called once after setupUi.
        """
        # We can only do this after the main script connects its signals,
        # so we patch the buttons' clicked signals here as secondary slots.
        pass  # LEDs are updated via enable_controls() in the main script

    def update_led(self, device_open: bool, grabbing: bool):
        """Call this from enable_controls() in the main script to sync LEDs."""
        self._led_conn.set_color(StatusLED.GREEN if device_open  else StatusLED.OFF)
        self._led_grab.set_color(StatusLED.AMBER if grabbing else StatusLED.OFF)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HIK Vision  ·  GO / NO-GO Inspector"))