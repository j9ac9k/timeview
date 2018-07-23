#!/usr/bin/env python3

"""
Example of using the TimeView python API to process files without the GUI

Activate the conda timeview environment before running this
"""

from pathlib import Path
from timeview.dsp import processing
from timeview.dsp.tracking import Track

wav_name = Path(__file__).with_name("speech-mwm.wav")
wav = Track.read(wav_name)
par_name = Path(__file__).with_name("speech-mwm.lab")
par = Track.read(par_name)

processor = processing.Filter()
processor.set_data({"wave": wav})
results, = processor.process()

print(results)
