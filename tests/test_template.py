import pytest  # noqa: F401
from timeview.gui import TimeView

pytest_plugins = "pytestqt.plugin"


def test_init(qtbot):
    timeview_app = TimeView()
    timeview_app.viewer.show()

    qtbot.addWidget(timeview_app.viewer)
    assert len(timeview_app.viewer.model.panels) == 1
