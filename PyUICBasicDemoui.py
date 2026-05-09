# -*- coding: utf-8 -*-
#
# PyUICBasicDemo.py — Redesigned UI  (v4)
# Single right column: INITIALIZATION → ACQUISITION → GO / NO-GO INSPECTOR
# GoNoGoOverlay is defined here and exposed as ui.overlay_widget.
# BasicDemo_with_gonogo.py calls ui.overlay_widget.update_result() directly
# instead of using a QDockWidget.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen, QRadialGradient, QImage, QPixmap


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


# ── Button style factory (inline — beats platform theme) ──────────────────────

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

BTN_BLUE   = _btn(C_BLUE,   TEXT_WHITE, C_BLUE_LT,   "#1a5a8a")
BTN_GREEN  = _btn(C_GREEN,  TEXT_BLACK, C_GREEN_LT,  "#1a6a3a")
BTN_RED    = _btn(C_RED,    TEXT_WHITE, C_RED_LT,    "#8a1f15")
BTN_AMBER  = _btn(C_AMBER,  TEXT_BLACK, "#ffbe45",   "#b07010")
BTN_PURPLE = _btn(C_PURPLE, TEXT_WHITE, C_PURPLE_LT, "#6c3483")


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
    left: 12px; top: 5px;
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
QComboBox::drop-down {{ border: none; width: 28px; }}
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
QLineEdit:focus {{ border-color: {C_AMBER}; background-color: #0f1215; }}
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
QRadioButton::indicator:checked {{ background-color: {C_AMBER}; border-color: {C_AMBER}; }}
QRadioButton::indicator:hover  {{ border-color: {C_AMBER}; }}
QRadioButton:checked           {{ color: {C_AMBER}; }}
QStatusBar {{
    background-color: {BG_PANEL};
    border-top: 1px solid {BORDER_DIM};
    color: {TEXT_MUTED};
    font-family: {FONT_MONO};
    font-size: 11px;
    letter-spacing: 1px;
}}
QScrollBar:vertical {{
    background: {BG_BASE}; width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_MID}; border-radius: 3px; min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
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
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

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
        for x in range(0, w, 44):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 44):
            p.drawLine(0, y, w, y)
        cx, cy = w // 2, h // 2
        p.setPen(QPen(QColor(BORDER_MID), 1))
        p.drawLine(cx - 22, cy, cx + 22, cy)
        p.drawLine(cx, cy - 22, cx, cy + 22)
        p.drawRect(cx - 44, cy - 32, 88, 64)
        p.setPen(QPen(QColor(C_AMBER), 2))
        L = 22
        for (ox, oy), (dx, dy) in [
            ((12, 12),     ( 1,  1)),
            ((w-12, 12),   (-1,  1)),
            ((12, h-12),   ( 1, -1)),
            ((w-12, h-12), (-1, -1)),
        ]:
            p.drawLine(ox, oy, ox + dx * L, oy)
            p.drawLine(ox, oy, ox, oy + dy * L)
        p.setPen(QPen(QColor(TEXT_DIM)))
        p.setFont(QFont("JetBrains Mono, Consolas", 13))
        p.drawText(self.rect(), Qt.AlignCenter, "[ NO SIGNAL ]")


class HSep(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setFixedHeight(1)
        self.setStyleSheet(f"background:{BORDER_DIM}; border:none; max-height:1px;")


# ── GO / NO-GO Overlay (embedded in right column) ────────────────────────────

class GoNoGoOverlay(QtWidgets.QGroupBox):
    """
    Third section in the right column.
    Displays live GO/NO-GO result, edge score, crop and masked-edge previews.
    Styled as a QGroupBox to match the other two groups visually.
    """

    def __init__(self, parent=None):
        super().__init__("Go / No-Go Inspector", parent)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 26, 12, 14)
        layout.setSpacing(10)

        # ── Result badge ──────────────────────────────────────────────────
        self.lbl_result = QtWidgets.QLabel("WAITING")
        self.lbl_result.setAlignment(Qt.AlignCenter)
        self.lbl_result.setFixedHeight(56)
        self.lbl_result.setFont(QFont(FONT_MONO, 18, QFont.Bold))
        self._set_badge("WAITING")
        layout.addWidget(self.lbl_result)

        # ── Score ─────────────────────────────────────────────────────────
        self.lbl_score = QtWidgets.QLabel("Edge Score: —")
        self.lbl_score.setAlignment(Qt.AlignCenter)
        self.lbl_score.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px; background:transparent;")
        layout.addWidget(self.lbl_score)

        layout.addWidget(HSep(self))

        # ── Preview row: crop | masked edges ─────────────────────────────
        preview_row = QtWidgets.QHBoxLayout()
        preview_row.setSpacing(8)

        def _preview_col(title):
            col = QtWidgets.QVBoxLayout()
            col.setSpacing(4)
            t = QtWidgets.QLabel(title)
            t.setAlignment(Qt.AlignCenter)
            t.setStyleSheet(f"font-size:10px; letter-spacing:2px; color:{TEXT_DIM}; background:transparent;")
            img = QtWidgets.QLabel()
            img.setFixedSize(118, 118)
            img.setAlignment(Qt.AlignCenter)
            img.setStyleSheet(f"background:{BG_BASE}; border:1px solid {BORDER_DIM}; border-radius:4px;")
            col.addWidget(t)
            col.addWidget(img)
            return col, img

        col1, self.lbl_crop  = _preview_col("BUTTON CROP")
        col2, self.lbl_edges = _preview_col("MASKED EDGES")
        preview_row.addLayout(col1)
        preview_row.addLayout(col2)
        layout.addLayout(preview_row)

        # ── Threshold note ────────────────────────────────────────────────
        self.lbl_threshold = QtWidgets.QLabel("Threshold  score > 1200 → NO-GO")
        self.lbl_threshold.setAlignment(Qt.AlignCenter)
        self.lbl_threshold.setStyleSheet(f"font-size:10px; color:{TEXT_DIM}; background:transparent;")
        layout.addWidget(self.lbl_threshold)

    # ── Public API ────────────────────────────────────────────────────────

    def update_result(self, result, score, crop_img, masked_img):
        import cv2, numpy as np
        self._set_badge(result)
        self.lbl_score.setText(f"Edge Score:  {score}")

        if crop_img is not None:
            self._to_qlabel(self.lbl_crop, crop_img)
        else:
            self.lbl_crop.clear()
            self.lbl_crop.setText("—")

        if masked_img is not None:
            bgr = cv2.cvtColor(masked_img, cv2.COLOR_GRAY2BGR)
            self._to_qlabel(self.lbl_edges, bgr)
        else:
            self.lbl_edges.clear()

    # ── Internal helpers ──────────────────────────────────────────────────

    def _set_badge(self, result):
        if result == "GO":
            bg, fg, border = "#0a2e1a", "#2ecc71", "#2ecc71"
        elif result == "NO-GO":
            bg, fg, border = "#2e0a0a", "#e74c3c", "#e74c3c"
        else:
            bg, fg, border = "#1a1a1a", "#5a6a7a", BORDER_MID
        self.lbl_result.setText(result)
        self.lbl_result.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {fg};
                border: 2px solid {border};
                border-radius: 6px;
                font-family: {FONT_MONO};
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 4px;
            }}
        """)

    def _to_qlabel(self, label, bgr_img):
        import cv2
        rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg).scaled(
            label.width(), label.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        label.setPixmap(pix)


# ── Main UI class ─────────────────────────────────────────────────────────────

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1340, 820)
        MainWindow.setMinimumSize(QSize(1100, 700))
        MainWindow.setStyleSheet(GLOBAL_SS)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        root = QtWidgets.QHBoxLayout(self.centralWidget)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(14)

        # ── LEFT: camera ──────────────────────────────────────────────────────
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

        # Status strip
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

        # ── RIGHT: single scrollable column ───────────────────────────────────
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(300)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {BG_BASE};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background: {BG_BASE};
            }}
        """)

        scroll_inner = QtWidgets.QWidget()
        scroll_inner.setStyleSheet(f"background:{BG_BASE};")
        right_col = QtWidgets.QVBoxLayout(scroll_inner)
        right_col.setContentsMargins(0, 0, 6, 0)   # 6px right margin for scrollbar clearance
        right_col.setSpacing(12)

        # ── GROUP: INITIALIZATION ─────────────────────────────────────────────
        self.groupInit = QtWidgets.QGroupBox("Initialization", scroll_inner)
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

        right_col.addWidget(self.groupInit)

        # ── GROUP: ACQUISITION ────────────────────────────────────────────────
        self.groupGrab = QtWidgets.QGroupBox("Acquisition", scroll_inner)
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

        right_col.addWidget(self.groupGrab)

        # ── GROUP: GO / NO-GO INSPECTOR ───────────────────────────────────────
        self.overlay_widget = GoNoGoOverlay(scroll_inner)
        right_col.addWidget(self.overlay_widget)

        right_col.addStretch(1)
        scroll.setWidget(scroll_inner)
        root.addWidget(scroll)

        # ── PARAMETERS — hidden stubs (main script still calls get/set param) ──
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
        self.label_5         = _lbl("GAIN")
        self.edtGain         = QtWidgets.QLineEdit("0", self.groupParam)
        self.edtGain.setObjectName("edtGain")
        self.label_6         = _lbl("FRAME RATE")
        self.edtFrameRate    = QtWidgets.QLineEdit("0", self.groupParam)
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
        self._led_conn.set_color(StatusLED.GREEN if device_open else StatusLED.OFF)
        self._led_grab.set_color(StatusLED.AMBER if grabbing    else StatusLED.OFF)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HIK Camera  —  GO / NO-GO Inspector"))