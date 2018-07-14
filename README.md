# TimeView

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Travis Status](https://travis-ci.org/j9ac9k/timeview.svg?branch=master)](https://travis-co.org/j9ac9k/timeview)
[![AppVeyor Status](https://ci.appveyor.com/api/projects/status/github/j9ac9k/timeview?branch=master&svg=true)](https://ci.appveyor.com/api/projects/status/github/j9ac9k/timeview)

TimeView is a cross-platform desktop application for viewing and editing Waveforms, Time-Value data, and Segmentation data. These data can easily be analyzed or manipulated using a library of built-in processors; for example, a linear filter can operate on a waveform, or an activity detector can create a segmentation from a waveform. Processors can be easily customized or created created from scratch.

This is a very early preview, and is not suitable for general usage yet.

![screenshot](docs/source/TimeView.png)

## Features

* *Cross-platform*, verified to run on macOS, Linux, and Windows
* Flexible arrangement of any number of *panels*, which contain any number of superimposed *views* (e.g. waveforms, spectrograms, feature trajectories, segmentations)
* Views can easily be *moved* between panels
* Views can be *linked* so that modifications in one panel are reflected in other panels
* *Customizable Rendering* of views (e.g. frame_size for spectrogram)
* *On-the-fly Spectrogram* rendering automatically adjusts frame-rate and FFT-size to calculate information for each available pixel without interpolation
* *Editable segmentation* (insertion, deletion, modification of boundaries; modification of labels)
* Basic *processing plug-ins* are provided (e.g. activity detection, F0-analysis)
* Processing plug-ins are easily *customizable* or *extendable* using python
* API allows accessing processing plugins for *batch file processing* or *pre-configuring the GUI* (examples are provided)
* *EDF-file-format* support
* A *dataset-manager* allows grouping of files into datasets, for quick access to often-used files
* *Command Line Interface* support, for easy chaining with other tools

An introductory video is available

[![thumbnail_large](https://i.vimeocdn.com/video/670176079_640.jpg)](https://vimeo.com/245480108 "TimeView Demo")

## Installation

### Pip

To install TimeView via `pip` one needs a python 3.6 environment setup in advance

```bash
pip install timeview
```

To execute run

```bash
timeview
```

### Pipenv

TimeView supports installation via `pipenv`

```bash
pipenv install timeview
```

To execute run

```bash
pipenv run timeview
```

## Contributing

TimeView welcomes contributors.  Currently the primary use case for TimeView is audio files of speech, however there is no reason we any other signal data cannot be used here.  This is the authors first major project that is public facing and deployable via pip, so there are lots of opportunities to help us make TimeView better.

Some immediate goals of the project include

* Expanding the test suite (right now it verifies the application starts and that's about it)
* Incorporate `mkl-fft` library for faster spectrogram generation
* Create documentation and provide a consistent API so other developers can integrate their own *processors* or *renderers*
* Create new *renderers*, allowing for modification of pitch curves
* Incorporate audio playback
* Make better use of multithreading
* Incorporate type hinting, such that we can use [mypy](http://mypy-lang.org/)
* Make application launch through the GUI of all major operating systems

To contribute, follow the following steps

1. Fork the repo!
2. Create a feature branch (`git checkout -b feature/fooBar`)
3. Commit changes (`git commit -am 'added feature fooBar!`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a Pull Request!

## Testing

To setup a development environment for TimeView, set up an empty python environment

```bash
git clone https://github.com/{username}/timeview.git timeview

# installing dependencies to run and execute tests
pip install -e "timeview[test]"
```

After installing the test dependencies, you can run the tests.

```bash
python timeview/setup.py test
```

## Support

* Report issues to the [GitHub issue tracker](https://github.com/pyqtgraph/pyqtgraph/issues)

## Authors

* Dr. Alex Kain - Professor at Oregon Health and Science University - Originally envisioned this project, had lots of existing code to make it happen
* Ogi Moore - Student at Oregon Health and Science University - Hired at BioSpeech to take this project from an idea into something usable

## Acknowledgments

* BioSpeech for funding the initial work and allowing to open source
* Dr. Alex Kain for giving a student trying to make a career transition to a software role an opportunity
* Library maintainers of PyQtGraph, SciPy, NumPy, and other dependencies if it was not for their effort this project would never have existed
