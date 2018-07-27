# -*- coding: utf-8 -*-
import pytest  # noqa: F401
from timeview.gui.viewer import Viewer
from timeview.gui import rendering
from PyQt5.QtCore import Qt
import pyqtgraph as pg


def testViewer(timeview_qtbot):
    """Check to make sure the viewer is actually visible

    Arguments:
        viewer {Viewer} -- QMainWindow of this application
        qtbot {PyTest Fixture} -- Fixture for Interacting with QtWidgets
    """
    viewer = timeview_qtbot.timeview_app.viewer
    viewer.show()
    assert viewer.isVisible()
    viewer.close()


def testMakeSpectrogram(viewerWithExample: Viewer, timeview_qtbot):
    view = viewerWithExample.selectedView
    renderComboBox = viewerWithExample.selectedDisplayPanel.view_table.cellWidget(0, 2)
    plotObject = viewerWithExample.selectedDisplayPanel.pw

    # Watch for the app.worker.finished signal, then start the worker.
    with timeview_qtbot.waitSignal(plotObject.finished, timeout=20000, raising=False):
        # blocker.connect(plotObject.error)  # Can add other signals to blocker
        timeview_qtbot.mouseClick(renderComboBox, Qt.LeftButton)
        timeview_qtbot.keyClick(renderComboBox, Qt.Key_Down)
        timeview_qtbot.keyClick(renderComboBox, Qt.Key_Enter)
        plotObject.deleteLater()
        # Test will block at this point until either the "finished" or the
        # "failed" signal is emitted. If 10 seconds passed without a signal,
        # SignalTimeoutError will be raised.
    assert view.renderer.item.isVisible()
    assert isinstance(view.renderer.item, pg.ImageItem)


def testMakeWaveform(viewerWithExample: Viewer, timeview_qtbot):
    view = viewerWithExample.selectedView

    def check_view():
        assert isinstance(view.renderer, rendering.Waveform)

    timeview_qtbot.waitUntil(check_view)
