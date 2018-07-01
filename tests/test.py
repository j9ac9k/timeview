import unittest
from pathlib import Path

from timeview.dsp import tracking, processing

# see also: http://johnnado.com/pyqt-qtest-example/

class TestProcessors(unittest.TestCase):
    def setUp(self):
        wav_name = Path(__file__).parents[1] / 'example/speech-mwm.wav'
        self.wav = tracking.Track.read(wav_name)
        par_name = Path(__file__).parents[1] / 'example/speech-mwm.lab'
        self.par = tracking.Track.read(par_name)

    def test_PeakTracker(self):
        processor = processing.PeakTracker()
        processor.set_data({'wave': self.wav})
        processor.process()

    def test_F0Analyzer(self):
        processor = processing.F0Analyzer()
        # step 1: set data (because parameter defaults may depend on data properties)
        processor.set_data({'wave': self.wav})
        processor.process()


