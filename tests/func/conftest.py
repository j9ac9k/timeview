# -*- coding: utf-8 -*-
import pytest  # noqa: F401
import timeview
from timeview.gui import TimeView
from timeview.gui.viewer import Viewer
from pathlib import Path
from typing import Generator

pytest_plugins = "pytest-qt"
EXAMPLE_DIR = Path(timeview.__file__).parents[1] / "example"


@pytest.fixture
def speech_wav_path():
    return EXAMPLE_DIR / "speech-mwm.wav"


@pytest.fixture
def speech_lab_path():
    return EXAMPLE_DIR / "speech-mwm.lab"


@pytest.fixture
def cough_edf_path():
    return EXAMPLE_DIR / "cough.edf"


# @pytest.fixture(scope="function")
# def viewer(app, timeview_qtbot) -> Viewer:
#     viewer = app.viewer
#     viewer.show()
#     qtbot.addWidget(viewer)
#     return viewer


@pytest.fixture(scope="function")
def viewerWithExample(timeview_qtbot) -> Generator[Viewer, None, None]:
    viewer = timeview_qtbot.timeview_app.viewer
    viewer.guiAddView(file_names=[EXAMPLE_DIR / "speech-mwm.wav"])
    viewer.show()
    yield viewer
    viewer.guiDelView()
    viewer.close()


@pytest.yield_fixture(scope="session")
def app():
    timeview = TimeView()
    # qt_app = timeview.qtapp
    yield timeview
    timeview.qtapp.processEvents()
    timeview.qtapp.quit()


@pytest.yield_fixture
def timeview_qtbot(app, qtbot):
    qtbot.timeview_app = app
    yield qtbot
