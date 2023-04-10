# ecgannotate

## Description

Graphical User Interface for viewing and annotating Electrocardiogram (ECG) signals with arrhythmia labels. Built with Python, PyQt5 and pyqtgraph. Expects single-channel signals in .npy format as input. Outputs plotted ECG signal and user convenience when annotating ECG signals. 

## Unit Tests

Check the "tests/" folder for a markdown file with example GUI functionality.

## How to Run

Download latest .whl release from the "Releases" section of this repository.

Install the wheel file on your local machine. It is recommended to do pip install within a virtual environment such as conda.

- pip install ecgannotate-0.1.0-py3-none-any.whl

Clone this repository to your local drive, navigate to the top-level of the repository, and run

- python ecgannotate/gui.py

Expected Result: The GUI interface will show up on screen.

For example functionality, check the notebooks in the tutorial/ folder.
