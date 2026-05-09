# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
import threading

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QDockWidget
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor, QPalette, QFont

from CamOperation_class import CameraOperation
from MvCameraControl_class import *
from MvErrorDefine_const import *
from CameraParams_header import *# -*- coding: utf-8 -*-
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
from PyUICBasicDemo_continuous import Ui_MainWindow
import ctypes


# ─────────────────────────────────────────────
# GO / NO-GO Detection Functions (your methods)
# ─────────────────────────────────────────────

def find_button_crop(img):
    """
    Detects a circular button in the image using HoughCircles.
    Returns a masked crop of the button region, or None if not found.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=100,
        param1=100,
        param2=30,
        minRadius=40,
        maxRadius=300
    )

    if circles is None:
        return None

    circles = np.round(circles[0, :]).astype(int)
    x, y, r = circles[0]

    pad = 10
    x1 = max(x - r - pad, 0)
    y1 = max(y - r - pad, 0)
    x2 = min(x + r + pad, img.shape[1])
    y2 = min(y + r + pad, img.shape[0])

    crop = img[y1:y2, x1:x2]

    if crop.size == 0:
        return None

    cx = x - x1
    cy = y - y1

    mask = np.zeros(crop.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (cx, cy), r, 255, -1)

    masked_crop = cv2.bitwise_and(crop, crop, mask=mask)

    return masked_crop


def detect_go_nogo(crop):
    """
    Classifies a cropped button image as GO or NO-GO based on edge density.
    Returns: (result_str, score, edges_img, masked_edges_img)
    """
    crop = cv2.resize(crop, (300, 300))

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 150)

    h, w = edges.shape
    Y, X = np.ogrid[:h, :w]
    cx, cy = w // 2, h // 2
    r = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)

    mask = (r < 140).astype(np.uint8) * 255
    masked = cv2.bitwise_and(edges, edges, mask=mask)

    score = cv2.countNonZero(masked)
    result = "NO-GO" if score > 1050 else "GO"

    return result, score, edges, masked


# ─────────────────────────────────────────────
# Frame Processor: runs in a background thread
# ─────────────────────────────────────────────

class GoNoGoProcessor:
    """
    Continuously grabs the latest frame from the camera using GetImageBuffer,
    runs GO/NO-GO detection, and emits results via a callback.
    """

    def __init__(self, cam_operation_ref, result_callback):
        self.cam_op = cam_operation_ref
        self.callback = result_callback
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        stOutFrame = MV_FRAME_OUT()
        ctypes.memset(ctypes.byref(stOutFrame), 0, ctypes.sizeof(stOutFrame))

        while self._running:
            ret = self.cam_op.obj_cam.MV_CC_GetImageBuffer(stOutFrame, 1000)
            if ret != MV_OK:
                continue

            try:
                img = self._frame_to_bgr(stOutFrame)
                if img is not None:
                    crop = find_button_crop(img)
                    if crop is not None and crop.size > 0:
                        result, score, edges, masked = detect_go_nogo(crop)
                        self.callback(result, score, crop, masked)
                    else:
                        self.callback("NO BUTTON", 0, None, None)
            finally:
                self.cam_op.obj_cam.MV_CC_FreeImageBuffer(stOutFrame)

    def _frame_to_bgr(self, frame):
        """Convert MV_FRAME_OUT to a BGR numpy array."""
        try:
            pixel_fmt = frame.stFrameInfo.enPixelType
            w = frame.stFrameInfo.nWidth
            h = frame.stFrameInfo.nHeight
            buf_size = frame.stFrameInfo.nFrameLen

            raw = (ctypes.c_ubyte * buf_size)()
            ctypes.memmove(raw, frame.pBufAddr, buf_size)
            arr = np.frombuffer(raw, dtype=np.uint8)

            # Common pixel format handling
            if pixel_fmt == PixelType_Gvsp_Mono8:
                img = arr.reshape((h, w))
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif pixel_fmt in (PixelType_Gvsp_RGB8_Packed,):
                img = arr.reshape((h, w, 3))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            elif pixel_fmt in (PixelType_Gvsp_BayerRG8, PixelType_Gvsp_BayerGR8,
                               PixelType_Gvsp_BayerBG8, PixelType_Gvsp_BayerGB8):
                img = arr.reshape((h, w))
                bayer_map = {
                    PixelType_Gvsp_BayerRG8: cv2.COLOR_BayerRG2BGR,
                    PixelType_Gvsp_BayerGR8: cv2.COLOR_BayerGR2BGR,
                    PixelType_Gvsp_BayerBG8: cv2.COLOR_BayerBG2BGR,
                    PixelType_Gvsp_BayerGB8: cv2.COLOR_BayerGB2BGR,
                }
                img = cv2.cvtColor(img, bayer_map[pixel_fmt])
            else:
                # Fallback: try treating as mono
                img = arr.reshape((h, w)) if arr.size == h * w else None

            return img
        except Exception as e:
            print(f"[GoNoGoProcessor] Frame conversion error: {e}")
            return None


# ─────────────────────────────────────────────
# Helper utilities (unchanged from original)
# ─────────────────────────────────────────────

def TxtWrapBy(start_str, end, all):
    start = all.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = all.find(end, start)
        if end >= 0:
            return all[start:end].strip()


def ToHexStr(num):
    chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hexStr = ""
    if num < 0:
        num = num + 2 ** 32
    while num >= 16:
        digit = num % 16
        hexStr = chaDic.get(digit, str(digit)) + hexStr
        num //= 16
    hexStr = chaDic.get(num, str(num)) + hexStr
    return hexStr


def decoding_char(ctypes_char_array):
    byte_str = memoryview(ctypes_char_array).tobytes()
    null_index = byte_str.find(b'\x00')
    if null_index != -1:
        byte_str = byte_str[:null_index]
    for encoding in ['gbk', 'utf-8', 'latin-1']:
        try:
            return byte_str.decode(encoding)
        except UnicodeDecodeError:
            continue
    return byte_str.decode('latin-1', errors='replace')


# ─────────────────────────────────────────────
# Result Overlay Widget
# ─────────────────────────────────────────────

class GoNoGoOverlay(QWidget):
    """
    A floating overlay panel that shows the live GO/NO-GO result,
    edge score, and a small preview of the detected crop + masked edges.
    Attach it next to the camera display widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(320)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # ── Result badge ──
        self.lbl_result = QLabel("WAITING")
        self.lbl_result.setAlignment(Qt.AlignCenter)
        self.lbl_result.setFixedHeight(64)
        font = QFont("Courier New", 22, QFont.Bold)
        self.lbl_result.setFont(font)
        self.lbl_result.setStyleSheet("""
            QLabel {
                background: #2a2a2a;
                color: #aaaaaa;
                border-radius: 8px;
                letter-spacing: 3px;
            }
        """)
        layout.addWidget(self.lbl_result)

        # ── Score ──
        self.lbl_score = QLabel("Edge Score: —")
        self.lbl_score.setAlignment(Qt.AlignCenter)
        self.lbl_score.setFont(QFont("Courier New", 11))
        self.lbl_score.setStyleSheet("color: #cccccc;")
        layout.addWidget(self.lbl_score)

        # ── Crop preview row ──
        preview_row = QHBoxLayout()

        self.lbl_crop_title = QLabel("Button Crop")
        self.lbl_crop_title.setAlignment(Qt.AlignCenter)
        self.lbl_crop_title.setFont(QFont("Courier New", 9))
        self.lbl_crop_title.setStyleSheet("color: #888;")

        self.lbl_edges_title = QLabel("Masked Edges")
        self.lbl_edges_title.setAlignment(Qt.AlignCenter)
        self.lbl_edges_title.setFont(QFont("Courier New", 9))
        self.lbl_edges_title.setStyleSheet("color: #888;")

        col1 = QVBoxLayout()
        col1.addWidget(self.lbl_crop_title)
        self.lbl_crop = QLabel()
        self.lbl_crop.setFixedSize(140, 140)
        self.lbl_crop.setAlignment(Qt.AlignCenter)
        self.lbl_crop.setStyleSheet("background: #1a1a1a; border-radius: 4px;")
        col1.addWidget(self.lbl_crop)

        col2 = QVBoxLayout()
        col2.addWidget(self.lbl_edges_title)
        self.lbl_edges = QLabel()
        self.lbl_edges.setFixedSize(140, 140)
        self.lbl_edges.setAlignment(Qt.AlignCenter)
        self.lbl_edges.setStyleSheet("background: #1a1a1a; border-radius: 4px;")
        col2.addWidget(self.lbl_edges)

        preview_row.addLayout(col1)
        preview_row.addLayout(col2)
        layout.addLayout(preview_row)

        # ── Threshold note ──
        self.lbl_threshold = QLabel("Threshold: score > 1200 → NO-GO")
        self.lbl_threshold.setAlignment(Qt.AlignCenter)
        self.lbl_threshold.setFont(QFont("Courier New", 9))
        self.lbl_threshold.setStyleSheet("color: #555;")
        layout.addWidget(self.lbl_threshold)

        layout.addStretch()

    def update_result(self, result, score, crop_img, masked_img):
        """Call this from the main thread via QTimer/signal to update UI."""

        if result == "GO":
            color = "#00cc66"
            bg = "#0a2e1a"
        elif result == "NO-GO":
            color = "#ff3333"
            bg = "#2e0a0a"
        else:
            color = "#aaaaaa"
            bg = "#2a2a2a"

        self.lbl_result.setText(result)
        self.lbl_result.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {color};
                border-radius: 8px;
                letter-spacing: 3px;
                border: 2px solid {color};
            }}
        """)

        self.lbl_score.setText(f"Edge Score: {score}")

        if crop_img is not None:
            self._set_label_image(self.lbl_crop, crop_img)
        else:
            self.lbl_crop.clear()
            self.lbl_crop.setText("No button\ndetected")
            self.lbl_crop.setStyleSheet("background: #1a1a1a; color: #555; border-radius: 4px;")

        if masked_img is not None:
            masked_bgr = cv2.cvtColor(masked_img, cv2.COLOR_GRAY2BGR)
            self._set_label_image(self.lbl_edges, masked_bgr)
        else:
            self.lbl_edges.clear()

    def _set_label_image(self, label, bgr_img):
        """Convert a BGR numpy array to QPixmap and display in a QLabel."""
        rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg).scaled(
            label.width(), label.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        label.setPixmap(pix)


# ─────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────

if __name__ == "__main__":

    MvCamera.MV_CC_Initialize()

    global deviceList
    deviceList = MV_CC_DEVICE_INFO_LIST()
    global cam
    cam = MvCamera()
    global nSelCamIndex
    nSelCamIndex = 0
    global obj_cam_operation
    obj_cam_operation = 0
    global isOpen
    isOpen = False
    global isGrabbing
    isGrabbing = False
    global isCalibMode
    isCalibMode = True

    # GO/NOGO processor instance (created on start_grabbing)
    global gonogo_processor
    gonogo_processor = None

    # ── Latest result cache (written by bg thread, read by QTimer on main thread) ──
    _latest_result = {"result": None, "score": 0, "crop": None, "masked": None}
    _result_lock = threading.Lock()

    def _on_gonogo_result(result, score, crop, masked):
        """Called from background thread — just cache, don't touch Qt here."""
        with _result_lock:
            _latest_result["result"] = result
            _latest_result["score"] = score
            _latest_result["crop"] = crop.copy() if crop is not None else None
            _latest_result["masked"] = masked.copy() if masked is not None else None

    # QTimer polls the cache and pushes to UI safely on the main thread
    ui_refresh_timer = QTimer()

    def _refresh_ui():
        with _result_lock:
            r = _latest_result["result"]
            s = _latest_result["score"]
            c = _latest_result["crop"]
            m = _latest_result["masked"]
        if r is not None:
            overlay_widget.update_result(r, s, c, m)

    ui_refresh_timer.timeout.connect(_refresh_ui)

    # ── Camera UI callbacks (all unchanged, except start/stop_grabbing) ──

    def enum_devices():
        global deviceList, obj_cam_operation

        deviceList = MV_CC_DEVICE_INFO_LIST()
        n_layer_type = (MV_GIGE_DEVICE | MV_USB_DEVICE | MV_GENTL_CAMERALINK_DEVICE
                        | MV_GENTL_CXP_DEVICE | MV_GENTL_XOF_DEVICE)
        ret = MvCamera.MV_CC_EnumDevices(n_layer_type, deviceList)
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "Enum devices fail! ret = :" + ToHexStr(ret), QMessageBox.Ok)
            return ret

        if deviceList.nDeviceNum == 0:
            QMessageBox.warning(mainWindow, "Info", "Find no device", QMessageBox.Ok)
            return ret

        print("Find %d devices!" % deviceList.nDeviceNum)
        devList = []

        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType in (MV_GIGE_DEVICE, MV_GENTL_GIGE_DEVICE):
                info = mvcc_dev_info.SpecialInfo.stGigEInfo
                name = decoding_char(info.chUserDefinedName)
                model = decoding_char(info.chModelName)
                ip = info.nCurrentIp
                nip = ((ip >> 24) & 0xff, (ip >> 16) & 0xff, (ip >> 8) & 0xff, ip & 0xff)
                devList.append(f"[{i}]GigE: {name} {model}({'.'.join(map(str,nip))})")
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                info = mvcc_dev_info.SpecialInfo.stUsb3VInfo
                name = decoding_char(info.chUserDefinedName)
                model = decoding_char(info.chModelName)
                sn = "".join(chr(c) for c in info.chSerialNumber if c != 0)
                devList.append(f"[{i}]USB: {name} {model}({sn})")
            elif mvcc_dev_info.nTLayerType == MV_GENTL_CAMERALINK_DEVICE:
                info = mvcc_dev_info.SpecialInfo.stCMLInfo
                name = decoding_char(info.chUserDefinedName)
                model = decoding_char(info.chModelName)
                sn = "".join(chr(c) for c in info.chSerialNumber if c != 0)
                devList.append(f"[{i}]CML: {name} {model}({sn})")
            elif mvcc_dev_info.nTLayerType == MV_GENTL_CXP_DEVICE:
                info = mvcc_dev_info.SpecialInfo.stCXPInfo
                name = decoding_char(info.chUserDefinedName)
                model = decoding_char(info.chModelName)
                sn = "".join(chr(c) for c in info.chSerialNumber if c != 0)
                devList.append(f"[{i}]CXP: {name} {model}({sn})")
            elif mvcc_dev_info.nTLayerType == MV_GENTL_XOF_DEVICE:
                info = mvcc_dev_info.SpecialInfo.stXoFInfo
                name = decoding_char(info.chUserDefinedName)
                model = decoding_char(info.chModelName)
                sn = "".join(chr(c) for c in info.chSerialNumber if c != 0)
                devList.append(f"[{i}]XoF: {name} {model}({sn})")

        ui.ComboDevices.clear()
        ui.ComboDevices.addItems(devList)
        ui.ComboDevices.setCurrentIndex(0)

    def open_device():
        global deviceList, nSelCamIndex, obj_cam_operation, isOpen
        if isOpen:
            QMessageBox.warning(mainWindow, "Error", 'Camera is Running!', QMessageBox.Ok)
            return MV_E_CALLORDER

        nSelCamIndex = ui.ComboDevices.currentIndex()
        if nSelCamIndex < 0:
            QMessageBox.warning(mainWindow, "Error", 'Please select a camera!', QMessageBox.Ok)
            return MV_E_CALLORDER

        obj_cam_operation = CameraOperation(cam, deviceList, nSelCamIndex)
        ret = obj_cam_operation.Open_device()
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "Open device failed ret:" + ToHexStr(ret), QMessageBox.Ok)
            isOpen = False
        else:
            set_continue_mode()
            get_param()
            isOpen = True
            enable_controls()

    def start_grabbing():
        """
        Starts the camera stream AND launches the GO/NO-GO processor thread.
        The processor reads frames independently; results are pushed to the
        overlay widget every 100 ms via ui_refresh_timer.
        """
        global obj_cam_operation, isGrabbing, gonogo_processor

        ret = obj_cam_operation.Start_grabbing(ui.widgetDisplay.winId())
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "Start grabbing failed ret:" + ToHexStr(ret), QMessageBox.Ok)
            return

        isGrabbing = True
        enable_controls()

        # Start GO/NO-GO background processor
        gonogo_processor = GoNoGoProcessor(obj_cam_operation, _on_gonogo_result)
        gonogo_processor.start()

        # Refresh UI every 100 ms (10 fps display update for overlay)
        ui_refresh_timer.start(100)

        overlay_widget.update_result("DETECTING...", 0, None, None)
        print("[GO/NOGO] Processor started.")

    def stop_grabbing():
        global obj_cam_operation, isGrabbing, gonogo_processor

        # Stop GO/NO-GO processor first
        if gonogo_processor is not None:
            gonogo_processor.stop()
        ui_refresh_timer.stop()
        overlay_widget.update_result("WAITING", 0, None, None)

        ret = obj_cam_operation.Stop_grabbing()
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "Stop grabbing failed ret:" + ToHexStr(ret), QMessageBox.Ok)
        else:
            isGrabbing = False
            enable_controls()
        print("[GO/NOGO] Processor stopped.")

    def close_device():
        global isOpen, isGrabbing, obj_cam_operation, gonogo_processor

        if gonogo_processor is not None:
            gonogo_processor.stop()
        ui_refresh_timer.stop()

        if isOpen:
            obj_cam_operation.Close_device()
            isOpen = False

        isGrabbing = False
        enable_controls()

    def set_continue_mode():
        ret = obj_cam_operation.Set_trigger_mode(False)
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "Set continue mode failed ret:" + ToHexStr(ret), QMessageBox.Ok)
        else:
            ui.radioContinueMode.setChecked(True)
            ui.radioTriggerMode.setChecked(False)
            ui.bnSoftwareTrigger.setEnabled(False)

    def set_software_trigger_mode():
        ret = obj_cam_operation.Set_trigger_mode(True)
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "Set trigger mode failed ret:" + ToHexStr(ret), QMessageBox.Ok)
        else:
            ui.radioContinueMode.setChecked(False)
            ui.radioTriggerMode.setChecked(True)
            ui.bnSoftwareTrigger.setEnabled(isGrabbing)

    def trigger_once():
        ret = obj_cam_operation.Trigger_once()
        if ret != 0:
            QMessageBox.warning(mainWindow, "Error", "TriggerSoftware failed ret:" + ToHexStr(ret), QMessageBox.Ok)

    def save_bmp():
        ret = obj_cam_operation.Save_Bmp()
        if ret != MV_OK:
            QMessageBox.warning(mainWindow, "Error", "Save BMP failed ret:" + ToHexStr(ret), QMessageBox.Ok)
        else:
            print("Save image success")

    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def get_param():
        ret = obj_cam_operation.Get_parameter()
        if ret != MV_OK:
            QMessageBox.warning(mainWindow, "Error", "Get param failed ret:" + ToHexStr(ret), QMessageBox.Ok)
        else:
            ui.edtExposureTime.setText("{0:.2f}".format(obj_cam_operation.exposure_time))
            ui.edtGain.setText("{0:.2f}".format(obj_cam_operation.gain))
            ui.edtFrameRate.setText("{0:.2f}".format(obj_cam_operation.frame_rate))

    def set_param():
        frame_rate = ui.edtFrameRate.text()
        exposure = ui.edtExposureTime.text()
        gain = ui.edtGain.text()
        if not (is_float(frame_rate) and is_float(exposure) and is_float(gain)):
            QMessageBox.warning(mainWindow, "Error", "Set param failed ret:" + ToHexStr(MV_E_PARAMETER), QMessageBox.Ok)
            return MV_E_PARAMETER
        ret = obj_cam_operation.Set_parameter(frame_rate, exposure, gain)
        if ret != MV_OK:
            QMessageBox.warning(mainWindow, "Error", "Set param failed ret:" + ToHexStr(ret), QMessageBox.Ok)
        return MV_OK

    def enable_controls():
        global isGrabbing, isOpen
        ui.groupGrab.setEnabled(isOpen)
        ui.groupParam.setEnabled(isOpen)
        ui.bnOpen.setEnabled(not isOpen)
        ui.bnClose.setEnabled(isOpen)
        ui.bnStart.setEnabled(isOpen and not isGrabbing)
        ui.bnStop.setEnabled(isOpen and isGrabbing)
        ui.bnSoftwareTrigger.setEnabled(isGrabbing and ui.radioTriggerMode.isChecked())
        ui.bnSaveImage.setEnabled(isOpen and isGrabbing)

    # ── Build the window ──
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    app.setPalette(dark_palette)

    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)

    # ── Add GO/NO-GO panel as a dock widget — central widget untouched ──
    overlay_widget = GoNoGoOverlay()
    overlay_widget.setStyleSheet("background: #1e1e1e;")

    dock = QDockWidget("GO / NO-GO Inspector", mainWindow)
    dock.setWidget(overlay_widget)
    dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
    dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
    mainWindow.addDockWidget(Qt.RightDockWidgetArea, dock)

    # ── Connect signals ──
    ui.bnEnum.clicked.connect(enum_devices)
    ui.bnOpen.clicked.connect(open_device)
    ui.bnClose.clicked.connect(close_device)
    ui.bnStart.clicked.connect(start_grabbing)
    ui.bnStop.clicked.connect(stop_grabbing)
    ui.bnSoftwareTrigger.clicked.connect(trigger_once)
    ui.radioTriggerMode.clicked.connect(set_software_trigger_mode)
    ui.radioContinueMode.clicked.connect(set_continue_mode)
    ui.bnGetParam.clicked.connect(get_param)
    ui.bnSetParam.clicked.connect(set_param)
    ui.bnSaveImage.clicked.connect(save_bmp)

    mainWindow.setWindowTitle("HIK Camera — GO / NO-GO Inspector")
    mainWindow.show()

    app.exec_()

    close_device()
    MvCamera.MV_CC_Finalize()
    sys.exit()