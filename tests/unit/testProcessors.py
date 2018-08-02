# -*- coding: utf-8 -*-
import unittest
from pathlib import Path
import timeview

from timeview.dsp import tracking, processing

# see also: http://johnnado.com/pyqt-qtest-example/

EXAMPLE_DIR = Path(timeview.__file__).parents[1] / "example"


class TestProcessors(unittest.TestCase):
    def setUp(self):
        wav_name = EXAMPLE_DIR / "speech-mwm.wav"
        self.wav = tracking.Track.read(wav_name)
        par_name = EXAMPLE_DIR / "speech-mwm.lab"
        self.par = tracking.Track.read(par_name)

    def test_PeakTracker(self):
        processor = processing.PeakTracker()
        processor.set_data({"wave": self.wav})
        processor.process()

    def test_F0Analyzer(self):
        processor = processing.F0Analyzer()
        # step 1: set data (because parameter defaults may depend on data properties)
        processor.set_data({"wave": self.wav})
        processor.process()
