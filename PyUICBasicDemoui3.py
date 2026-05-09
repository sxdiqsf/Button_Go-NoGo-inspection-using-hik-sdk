# -*- coding: utf-8 -*-
#
# PyUICBasicDemo.py — Redesigned UI  (v3)
# Industrial HMI aesthetic: gunmetal panels, filled color buttons,
# JetBrains Mono typography, 2-row right panel.
#
# KEY FIX: Every button gets setStyleSheet() called directly on the
# widget instance — inline styles always beat Qt class selectors and
# platform themes, so colors actually appear.
#
# Layout: right panel is 2 columns side-by-side in the top row:
#   LEFT  → INITIALIZATION
#   RIGHT → ACQUISITION
# PARAMETERS group is hidden (stubs kept so main script won't crash).

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen, QRadialGradient


# ── Color tokens ──────────────────────────────────────────────────────────────

BG_BASE      = "#0d0f11"
BG_PANEL     = "#13171c"
BG_CARD      = "#1a1f26"
BG_INPUT     = "#0d0f11"
BORDER_DIM   = "#2a313b"
BORDER_MID   = "#3a4455"
C_AMBER      = "#e8a020"
C_GREEN      = "#27ae60"
C_GREEN_LT   = "#2ecc71"
C_RED        = "#c0392b"
C_RED_LT     = "#e74c3c"
C_BLUE       = "#2980b9"
C_BLUE_LT    = "#4a9eff"
C_PURPLE     = "#8e44ad"
C_PURPLE_LT  = "#9b59b6"
TEXT_WHITE   = "#ffffff"
TEXT_BLACK   = "#0a0a0a"
TEXT_PRIMARY = "#dce8f0"
TEXT_MUTED   = "#7a8a9a"
TEXT_DIM     = "#3a4a5a"

FONT_MONO = "JetBrains Mono, Consolas, Courier New, monospace"


# ── Button style factory ──────────────────────────────────────────────────────
# Uses inline setStyleSheet per instance — guaranteed to override platform theme.

def _btn(bg, fg, hover, pressed):
    return f"""
        QPushButton {{
            background-color: {bg};
            color: {fg};
            border: 2px solid {bg};
            border-radius: 5px;
            padding: 8px 14px;
            font-family: {FONT_MONO};
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 1px;
            min-height: 36px;
        }}
        QPushButton:hover {{
            background-color: {hover};
            border-color: {hover};
            color: {fg};
        }}
        QPushButton:pressed {{
            background-color: {pressed};
            border-color: {pressed};
            color: {fg};
            padding-top: 10px;
            padding-bottom: 6px;
        }}
        QPushButton:disabled {{
            background-color: #1c2028;
            border-color: {BORDER_DIM};
            color: #3a4a5a;
        }}
    """

BTN_BLUE   = _btn(C_BLUE,   TEXT_WHITE, C_BLUE_LT,  "#1a5a8a")
BTN_GREEN  = _btn(C_GREEN,  TEXT_BLACK, C_GREEN_LT, "#1a6a3a")
BTN_RED    = _btn(C_RED,    TEXT_WHITE, C_RED_LT,   "#8a1f15")
BTN_AMBER  = _btn(C_AMBER,  TEXT_BLACK, "#ffbe45",  "#b07010")
BTN_PURPLE = _btn(C_PURPLE, TEXT_WHITE, C_PURPLE_LT,"#6c3483")
BTN_TEAL   = _btn("#16a085",TEXT_WHITE, "#1abc9c",  "#0e6655")


# ── Global stylesheet (non-button widgets) ────────────────────────────────────

GLOBAL_SS = f"""
QMainWindow, QWidget {{
    background-color: {BG_BASE};
    color: {TEXT_PRIMARY};
    font-family: {FONT_MONO};
    font-size: 13px;
}}

QGroupBox {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER_DIM};
    border-radius: 8px;
    margin-top: 28px;
    padding: 12px 8px 10px 8px;
    font-family: {FONT_MONO};
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 3px;
    color: {TEXT_MUTED};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 5px;
    padding: 2px 8px;
    background-color: {BG_CARD};
    color: {C_AMBER};
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: bold;
}}

QComboBox {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER_MID};
    border-radius: 5px;
    padding: 6px 10px;
    color: {TEXT_PRIMARY};
    font-family: {FONT_MONO};
    font-size: 13px;
    min-height: 34px;
}}
QComboBox::drop-down {{ border:none; width:28px; }}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {C_AMBER};
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

QLineEdit {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER_MID};
    border-radius: 4px;
    padding: 5px 8px;
    color: {C_AMBER};
    font-family: {FONT_MONO};
    font-size: 14px;
    selection-background-color: #2a3a50;
}}
QLineEdit:focus {{
    border-color: {C_AMBER};
    background-color: #0f1215;
}}

QLabel {{
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 12px;
    letter-spacing: 1px;
    background: transparent;
}}

QRadioButton {{
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 12px;
    spacing: 7px;
    letter-spacing: 1px;
}}
QRadioButton::indicator {{
    width: 14px; height: 14px;
    border-radius: 7px;
    border: 2px solid {BORDER_MID};
    background-color: {BG_BASE};
}}
QRadioButton::indicator:checked {{
    background-color: {C_AMBER};
    border-color: {C_AMBER};
}}
QRadioButton::indicator:hover {{ border-color: {C_AMBER}; }}
QRadioButton:checked {{ color: {C_AMBER}; }}

QStatusBar {{
    background-color: {BG_PANEL};
    border-top: 1px solid {BORDER_DIM};
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 11px;
    letter-spacing: 1px;
}}

QDockWidget {{
    background-color: {BG_PANEL};
    font-family: {FONT_MONO};
    font-size: 11px;
}}
QDockWidget::title {{
    background-color: {BG_CARD};
    padding: 8px 12px;
    border-bottom: 1px solid {BORDER_DIM};
    color: {C_AMBER};
    font-weight: bold;
    letter-spacing: 3px;
    text-align: left;
}}

QToolTip {{
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    border: 1px solid {C_AMBER};
    font-family: {FONT_MONO};
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 3px;
}}
QMessageBox {{ background-color: {BG_CARD}; }}
QMessageBox QLabel {{ color: {TEXT_PRIMARY}; font-size: 13px; }}

QScrollBar:vertical {{
    background: {BG_BASE}; width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_MID}; border-radius: 3px; min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
"""


# ── LED indicator ─────────────────────────────────────────────────────────────

class StatusLED(QtWidgets.QWidget):
    OFF   = "#252a30"
    GREEN = C_GREEN_LT
    AMBER = C_AMBER
    RED   = C_RED_LT

    def __init__(self, color=None, parent=None):
        super().__init__(parent)
        self._color = color or self.OFF
        self.setFixedSize(12, 12)

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(1, 1, -1, -1)
        grad = QRadialGradient(r.center().x() - 1, r.center().y() - 1, r.width() / 2)
        c = QColor(self._color)
        grad.setColorAt(0.0, c.lighter(170))
        grad.setColorAt(1.0, c.darker(140))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(c.darker(160), 1))
        p.drawEllipse(r)


# ── Camera viewport ───────────────────────────────────────────────────────────

class CameraViewport(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("widgetDisplay")
        self._streaming = False
        self.setMinimumSize(520, 420)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)

    def set_streaming(self, state: bool):
        self._streaming = state
        self.update()

    def paintEvent(self, event):
        if self._streaming:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        p.fillRect(self.rect(), QColor(BG_BASE))

        p.setPen(QPen(QColor(BORDER_DIM), 1, Qt.DotLine))
        step = 44
        for x in range(0, w, step):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, step):
            p.drawLine(0, y, w, y)

        cx, cy = w // 2, h // 2
        p.setPen(QPen(QColor(BORDER_MID), 1))
        p.drawLine(cx - 22, cy, cx + 22, cy)
        p.drawLine(cx, cy - 22, cx, cy + 22)
        p.drawRect(cx - 44, cy - 32, 88, 64)

        p.setPen(QPen(QColor(C_AMBER), 2))
        L = 22
        for (ox, oy), (dx, dy) in [
            ((12, 12),   ( 1,  1)),
            ((w-12, 12), (-1,  1)),
            ((12, h-12), ( 1, -1)),
            ((w-12, h-12), (-1, -1)),
        ]:
            p.drawLine(ox, oy, ox + dx * L, oy)
            p.drawLine(ox, oy, ox, oy + dy * L)

        p.setPen(QPen(QColor(TEXT_DIM)))
        p.setFont(QFont("JetBrains Mono, Consolas", 13))
        p.drawText(self.rect(), Qt.AlignCenter, "[ NO SIGNAL ]")


# ── Thin separator ────────────────────────────────────────────────────────────

class HSep(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setFixedHeight(1)
        self.setStyleSheet(f"background:{BORDER_DIM}; border:none; max-height:1px;")


# ── Main UI class ─────────────────────────────────────────────────────────────

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1340, 820)
        MainWindow.setMinimumSize(QSize(1100, 700))
        MainWindow.setStyleSheet(GLOBAL_SS)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # Root: camera (stretch) | right controls (fixed)
        root = QtWidgets.QHBoxLayout(self.centralWidget)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(14)

        # ── LEFT ─────────────────────────────────────────────────────────────
        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(10)

        dev_row = QtWidgets.QHBoxLayout()
        dev_row.setSpacing(8)
        dev_icon = QtWidgets.QLabel("⬡")
        dev_icon.setStyleSheet(f"color:{C_AMBER}; font-size:16px; background:transparent;")
        dev_icon.setFixedWidth(20)
        self.ComboDevices = QtWidgets.QComboBox(self.centralWidget)
        self.ComboDevices.setObjectName("ComboDevices")
        self.ComboDevices.setToolTip("Select camera device")
        self.ComboDevices.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        dev_row.addWidget(dev_icon)
        dev_row.addWidget(self.ComboDevices, 1)
        left_col.addLayout(dev_row)

        self.widgetDisplay = CameraViewport(self.centralWidget)
        self.widgetDisplay.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        left_col.addWidget(self.widgetDisplay, 1)

        # Status strip below camera
        strip = QtWidgets.QHBoxLayout()
        strip.setSpacing(10)

        def _chip(label_text):
            w = QtWidgets.QWidget()
            w.setStyleSheet(f"QWidget{{background:{BG_PANEL}; border:1px solid {BORDER_DIM}; border-radius:4px;}}")
            hl = QtWidgets.QHBoxLayout(w)
            hl.setContentsMargins(10, 4, 10, 4)
            hl.setSpacing(7)
            led = StatusLED(StatusLED.OFF, w)
            lbl = QtWidgets.QLabel(label_text, w)
            lbl.setStyleSheet(f"font-size:11px; letter-spacing:2px; color:{TEXT_DIM}; border:none; background:transparent;")
            hl.addWidget(led)
            hl.addWidget(lbl)
            return w, led

        self._chip_conn, self._led_conn = _chip("DEVICE")
        self._chip_grab, self._led_grab = _chip("STREAM")
        strip.addWidget(self._chip_conn)
        strip.addWidget(self._chip_grab)
        strip.addStretch()
        branding = QtWidgets.QLabel("HIK VISION  ·  MV SDK")
        branding.setStyleSheet(f"font-size:11px; color:{TEXT_DIM}; letter-spacing:2px; background:transparent;")
        strip.addWidget(branding)
        left_col.addLayout(strip)

        root.addLayout(left_col, 1)

        # ── RIGHT: 2 columns in top row ───────────────────────────────────────
        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(12)
        right_col.setContentsMargins(0, 0, 0, 0)

        # Wrap in a fixed-width container
        right_container = QtWidgets.QWidget(self.centralWidget)
        right_container.setFixedWidth(290)
        right_container.setLayout(right_col)

        top_row = QtWidgets.QVBoxLayout()
        top_row.setSpacing(12)

        # ── GROUP: INITIALIZATION ─────────────────────────────────────────────
        self.groupInit = QtWidgets.QGroupBox("Initialization", self.centralWidget)
        self.groupInit.setObjectName("groupInit")

        init_vbox = QtWidgets.QVBoxLayout(self.groupInit)
        init_vbox.setContentsMargins(12, 26, 12, 14)
        init_vbox.setSpacing(10)

        self.bnEnum = QtWidgets.QPushButton("⬡  FIND DEVICES", self.groupInit)
        self.bnEnum.setObjectName("bnEnum")
        self.bnEnum.setToolTip("Scan for connected cameras")
        self.bnEnum.setStyleSheet(BTN_BLUE)

        oc_row = QtWidgets.QHBoxLayout()
        oc_row.setSpacing(8)

        self.bnOpen = QtWidgets.QPushButton("▶  OPEN", self.groupInit)
        self.bnOpen.setObjectName("bnOpen")
        self.bnOpen.setToolTip("Open selected device")
        self.bnOpen.setStyleSheet(BTN_GREEN)

        self.bnClose = QtWidgets.QPushButton("■  CLOSE", self.groupInit)
        self.bnClose.setObjectName("bnClose")
        self.bnClose.setEnabled(False)
        self.bnClose.setToolTip("Close device")
        self.bnClose.setStyleSheet(BTN_RED)

        oc_row.addWidget(self.bnOpen)
        oc_row.addWidget(self.bnClose)
        init_vbox.addWidget(self.bnEnum)
        init_vbox.addLayout(oc_row)

        # ── GROUP: ACQUISITION ────────────────────────────────────────────────
        self.groupGrab = QtWidgets.QGroupBox("Acquisition", self.centralWidget)
        self.groupGrab.setObjectName("groupGrab")
        self.groupGrab.setEnabled(False)

        grab_vbox = QtWidgets.QVBoxLayout(self.groupGrab)
        grab_vbox.setContentsMargins(12, 26, 12, 14)
        grab_vbox.setSpacing(10)

        mode_row = QtWidgets.QHBoxLayout()
        mode_row.setSpacing(16)
        self.radioContinueMode = QtWidgets.QRadioButton("CONTINUOUS", self.groupGrab)
        self.radioContinueMode.setObjectName("radioContinueMode")
        self.radioTriggerMode  = QtWidgets.QRadioButton("TRIGGER", self.groupGrab)
        self.radioTriggerMode.setObjectName("radioTriggerMode")
        mode_row.addWidget(self.radioContinueMode)
        mode_row.addWidget(self.radioTriggerMode)
        grab_vbox.addLayout(mode_row)

        ss_row = QtWidgets.QHBoxLayout()
        ss_row.setSpacing(8)

        self.bnStart = QtWidgets.QPushButton("▶  START", self.groupGrab)
        self.bnStart.setObjectName("bnStart")
        self.bnStart.setEnabled(False)
        self.bnStart.setStyleSheet(BTN_GREEN)

        self.bnStop = QtWidgets.QPushButton("■  STOP", self.groupGrab)
        self.bnStop.setObjectName("bnStop")
        self.bnStop.setEnabled(False)
        self.bnStop.setStyleSheet(BTN_RED)

        ss_row.addWidget(self.bnStart)
        ss_row.addWidget(self.bnStop)
        grab_vbox.addLayout(ss_row)

        self.bnSoftwareTrigger = QtWidgets.QPushButton("◉  TRIGGER ONCE", self.groupGrab)
        self.bnSoftwareTrigger.setObjectName("bnSoftwareTrigger")
        self.bnSoftwareTrigger.setEnabled(False)
        self.bnSoftwareTrigger.setStyleSheet(BTN_AMBER)
        grab_vbox.addWidget(self.bnSoftwareTrigger)

        grab_vbox.addWidget(HSep(self.groupGrab))

        self.bnSaveImage = QtWidgets.QPushButton("⬇  SAVE FRAME", self.groupGrab)
        self.bnSaveImage.setObjectName("bnSaveImage")
        self.bnSaveImage.setEnabled(False)
        self.bnSaveImage.setStyleSheet(BTN_PURPLE)
        grab_vbox.addWidget(self.bnSaveImage)

        top_row.addWidget(self.groupInit)
        top_row.addWidget(self.groupGrab)
        right_col.addLayout(top_row)
        right_col.addStretch(1)

        root.addWidget(right_container)

        # ── PARAMETERS — hidden stubs (main script still works) ───────────────
        self.groupParam = QtWidgets.QGroupBox("Parameters", self.centralWidget)
        self.groupParam.setObjectName("groupParam")
        self.groupParam.setEnabled(False)
        self.groupParam.setVisible(False)

        _p = QtWidgets.QGridLayout(self.groupParam)

        def _lbl(t):
            l = QtWidgets.QLabel(t)
            l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return l

        self.label_4         = _lbl("EXPOSURE")
        self.edtExposureTime = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtExposureTime.setObjectName("edtExposureTime")

        self.label_5  = _lbl("GAIN")
        self.edtGain  = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtGain.setObjectName("edtGain")

        self.label_6      = _lbl("FRAME RATE")
        self.edtFrameRate = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtFrameRate.setObjectName("edtFrameRate")

        self.bnGetParam = QtWidgets.QPushButton("↓ GET", self.groupParam)
        self.bnGetParam.setObjectName("bnGetParam")
        self.bnGetParam.setStyleSheet(BTN_BLUE)

        self.bnSetParam = QtWidgets.QPushButton("↑ SET", self.groupParam)
        self.bnSetParam.setObjectName("bnSetParam")
        self.bnSetParam.setStyleSheet(BTN_AMBER)

        _p.addWidget(self.label_4,         0, 0)
        _p.addWidget(self.edtExposureTime, 0, 1)
        _p.addWidget(self.label_5,         1, 0)
        _p.addWidget(self.edtGain,         1, 1)
        _p.addWidget(self.label_6,         2, 0)
        _p.addWidget(self.edtFrameRate,    2, 1)
        _p.addWidget(self.bnGetParam,      3, 0)
        _p.addWidget(self.bnSetParam,      3, 1)

        # ── Status bar ────────────────────────────────────────────────────────
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.showMessage("  SYSTEM READY  ·  SELECT DEVICE AND CLICK FIND DEVICES")

        MainWindow.setCentralWidget(self.centralWidget)
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_led(self, device_open: bool, grabbing: bool):
        """Called from enable_controls() in BasicDemo_with_gonogo.py"""
        self._led_conn.set_color(StatusLED.GREEN if device_open else StatusLED.OFF)
        self._led_grab.set_color(StatusLED.AMBER if grabbing    else StatusLED.OFF)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HIK Camera  —  GO / NO-GO Inspector"))