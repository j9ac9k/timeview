# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import setup
from typing import Dict

# Package meta-data.
NAME = "timeview"
DESCRIPTION = "A GUI application to view and analyze time series signal data"
URL = "https://github.com/j9ac9k/timeview"
AUTHOR = "Ognyan Moore"
AUTHOR_EMAIL = "ognyan.moore@gmail.com"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = None

REQUIRED = [
    "numpy",
    "scipy",
    "sqlalchemy",
    "numba",
    "pyqt5",
    "qtpy",
    "pyqtgraph",
    "qtawesome",
    "pyedflib",
    "cython",
]

TESTS_REQUIRE = ["pytest", "pytest-qt", "pytest-runner"]

DEV_REQUIRE = ["black", "pre-config", "flake8-mypy", "flake8-bugbear"]


# here = os.path.abspath(os.path.dirname(__file__))
here = Path.resolve(Path(__file__).parent)

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open((here / "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about: Dict[str, str] = {}
if not VERSION:
    with open(here / NAME / "__version__.py") as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


setup(
    # meta-data
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords="timeview gui pyqt signal spectrogram",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Utilities",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    # app contents
    packages=["timeview", "timeview.dsp", "timeview.gui", "timeview.manager"],
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "timeview-gui = timeview.__main__:main",
            "timeview = timeview.__main__:main",
        ]
    },
    install_requires=REQUIRED,
    tests_require=TESTS_REQUIRE,
    extras_require={"dev": DEV_REQUIRE, "test": TESTS_REQUIRE},
    python_requires=REQUIRES_PYTHON,
    setup_requires=["pytest-runner"],
)
