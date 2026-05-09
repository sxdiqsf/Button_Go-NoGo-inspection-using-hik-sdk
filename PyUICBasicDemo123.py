# -*- coding: utf-8 -*-
# Rewritten — proper layouts, polished styling, 75/25 camera/controls split.
# Drop-in replacement for the pyuic5-generated file. All objectNames unchanged.

from PyQt5 import QtCore, QtGui, QtWidgets


# ── Shared style constants ────────────────────────────────────────────────────
_FONT_LABEL   = QtGui.QFont("Segoe UI", 9)
_FONT_BTN     = QtGui.QFont("Segoe UI", 9,  QtGui.QFont.Medium)
_FONT_GROUP   = QtGui.QFont("Segoe UI", 9,  QtGui.QFont.Bold)
_FONT_COMBO   = QtGui.QFont("Segoe UI", 9)
_FONT_RADIO   = QtGui.QFont("Segoe UI", 9)

# Button palette
_BTN_FIND     = "background:#2979ff; color:#fff; border-radius:5px; padding:5px 8px;"
_BTN_OPEN     = "background:#00c853; color:#fff; border-radius:5px; padding:5px 8px;"
_BTN_CLOSE    = "background:#d50000; color:#fff; border-radius:5px; padding:5px 8px;"
_BTN_START    = "background:#00897b; color:#fff; border-radius:5px; padding:5px 8px;"
_BTN_STOP     = "background:#e65100; color:#fff; border-radius:5px; padding:5px 8px;"
_BTN_TRIGGER  = "background:#6200ea; color:#fff; border-radius:5px; padding:5px 8px;"
_BTN_SAVE     = "background:#37474f; color:#fff; border-radius:5px; padding:5px 8px;"

_BTN_DISABLED = """
    QPushButton:disabled {
        background: #3a3a3a;
        color: #666;
        border-radius: 5px;
        padding: 5px 8px;
    }
"""

_GROUP_STYLE  = """
    QGroupBox {
        color: #bbbbbb;
        border: 1px solid #444;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 6px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 6px;
        color: #eeeeee;
    }
"""

_COMBO_STYLE  = """
    QComboBox {
        background: #2a2a2a;
        color: #e0e0e0;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 3px 6px;
    }
    QComboBox QAbstractItemView {
        background: #2a2a2a;
        color: #e0e0e0;
        selection-background-color: #2979ff;
    }
"""

_RADIO_STYLE  = """
    QRadioButton { color: #cccccc; }
    QRadioButton::indicator { width:14px; height:14px; }
"""


def _make_btn(text, obj_name, style, enabled=True):
    """Helper: create a styled QPushButton."""
    btn = QtWidgets.QPushButton(text)
    btn.setObjectName(obj_name)
    btn.setFont(_FONT_BTN)
    btn.setMinimumHeight(30)
    btn.setEnabled(enabled)
    btn.setStyleSheet(style + _BTN_DISABLED)
    return btn


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 660)
        MainWindow.setMinimumSize(800, 500)

        # ── Central widget ────────────────────────────────────────────────────
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        root_h = QtWidgets.QHBoxLayout(self.centralWidget)
        root_h.setContentsMargins(10, 10, 10, 10)
        root_h.setSpacing(10)

        # ══════════════════════════════════════════════════════════════════════
        # LEFT — camera display (75 %)
        # ══════════════════════════════════════════════════════════════════════
        left_v = QtWidgets.QVBoxLayout()
        left_v.setSpacing(6)

        self.ComboDevices = QtWidgets.QComboBox()
        self.ComboDevices.setObjectName("ComboDevices")
        self.ComboDevices.setFont(_FONT_COMBO)
        self.ComboDevices.setStyleSheet(_COMBO_STYLE)
        self.ComboDevices.setMinimumHeight(28)
        self.ComboDevices.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        left_v.addWidget(self.ComboDevices)

        self.widgetDisplay = QtWidgets.QWidget()
        self.widgetDisplay.setObjectName("widgetDisplay")
        self.widgetDisplay.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widgetDisplay.setMinimumSize(400, 300)
        self.widgetDisplay.setStyleSheet(
            "background:#000; border:1px solid #333; border-radius:4px;")
        left_v.addWidget(self.widgetDisplay)

        root_h.addLayout(left_v, stretch=3)   # 3 out of 4 → 75 %

        # ══════════════════════════════════════════════════════════════════════
        # RIGHT — controls + GO/NO-GO inspector (25 %)
        # ══════════════════════════════════════════════════════════════════════
        right_v = QtWidgets.QVBoxLayout()
        right_v.setSpacing(10)
        right_v.setContentsMargins(0, 0, 0, 0)

        # ── Group: Initialization ─────────────────────────────────────────────
        self.groupInit = QtWidgets.QGroupBox("INITIALIZATION")
        self.groupInit.setObjectName("groupInit")
        self.groupInit.setFont(_FONT_GROUP)
        self.groupInit.setStyleSheet(_GROUP_STYLE)
        init_grid = QtWidgets.QGridLayout(self.groupInit)
        init_grid.setSpacing(6)
        init_grid.setContentsMargins(8, 14, 8, 8)

        self.bnEnum = _make_btn("🔍  Find Device", "bnEnum", _BTN_FIND)
        init_grid.addWidget(self.bnEnum, 0, 0, 1, 2)

        self.bnOpen = _make_btn("▶  Open Device", "bnOpen", _BTN_OPEN)
        init_grid.addWidget(self.bnOpen, 1, 0)

        self.bnClose = _make_btn("✕  Close Device", "bnClose", _BTN_CLOSE, enabled=False)
        init_grid.addWidget(self.bnClose, 1, 1)

        right_v.addWidget(self.groupInit)

        # ── Group: Acquisition ────────────────────────────────────────────────
        self.groupGrab = QtWidgets.QGroupBox("ACQUISITION")
        self.groupGrab.setObjectName("groupGrab")
        self.groupGrab.setFont(_FONT_GROUP)
        self.groupGrab.setStyleSheet(_GROUP_STYLE)
        self.groupGrab.setEnabled(False)
        grab_grid = QtWidgets.QGridLayout(self.groupGrab)
        grab_grid.setSpacing(6)
        grab_grid.setContentsMargins(8, 14, 8, 8)

        self.radioContinueMode = QtWidgets.QRadioButton("Continuous")
        self.radioContinueMode.setObjectName("radioContinueMode")
        self.radioContinueMode.setFont(_FONT_RADIO)
        self.radioContinueMode.setStyleSheet(_RADIO_STYLE)
        grab_grid.addWidget(self.radioContinueMode, 0, 0)

        self.radioTriggerMode = QtWidgets.QRadioButton("Trigger")
        self.radioTriggerMode.setObjectName("radioTriggerMode")
        self.radioTriggerMode.setFont(_FONT_RADIO)
        self.radioTriggerMode.setStyleSheet(_RADIO_STYLE)
        grab_grid.addWidget(self.radioTriggerMode, 0, 1)

        self.bnStart = _make_btn("▶  Start", "bnStart", _BTN_START, enabled=False)
        grab_grid.addWidget(self.bnStart, 1, 0)

        self.bnStop = _make_btn("■  Stop", "bnStop", _BTN_STOP, enabled=False)
        grab_grid.addWidget(self.bnStop, 1, 1)

        self.bnSoftwareTrigger = _make_btn(
            "⚡  Trigger Once", "bnSoftwareTrigger", _BTN_TRIGGER, enabled=False)
        grab_grid.addWidget(self.bnSoftwareTrigger, 2, 0, 1, 2)

        self.bnSaveImage = _make_btn(
            "💾  Save Image", "bnSaveImage", _BTN_SAVE, enabled=False)
        grab_grid.addWidget(self.bnSaveImage, 3, 0, 1, 2)

        right_v.addWidget(self.groupGrab)

        # ── GO/NO-GO overlay slot ─────────────────────────────────────────────
        # GoNoGoOverlay is inserted here by the main script via gonogoSlotLayout
        self.gonogoSlot = QtWidgets.QWidget()
        self.gonogoSlot.setObjectName("gonogoSlot")
        self.gonogoSlot.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.gonogoSlotLayout = QtWidgets.QVBoxLayout(self.gonogoSlot)
        self.gonogoSlotLayout.setContentsMargins(0, 0, 0, 0)
        right_v.addWidget(self.gonogoSlot, stretch=1)

        # Wrap right panel — stretch=1 gives it 25 % (1 out of 4 total)
        right_container = QtWidgets.QWidget()
        right_container.setLayout(right_v)
        right_container.setMinimumWidth(220)

        root_h.addWidget(right_container, stretch=1)   # 1 out of 4 → 25 %

        MainWindow.setCentralWidget(self.centralWidget)

        # ── Status bar ────────────────────────────────────────────────────────
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.setFont(QtGui.QFont("Segoe UI", 8))
        self.statusBar.setStyleSheet("color:#aaa;")
        MainWindow.setStatusBar(self.statusBar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass