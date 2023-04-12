# ecgannotate

## Description

Graphical User Interface for viewing and annotating Electrocardiogram (ECG) signals with arrhythmia labels. Built with Python, PyQt5 and pyqtgraph. Expects single-channel signals in .npy format as input. Outputs plotted ECG signal and user convenience when annotating ECG signals. 

## Unit Tests

Check the "tests/" folder for a markdown file with example GUI functionality.

## How to Run

Download latest .whl release from the "Releases" section of this repository.

Install the wheel file on your local machine. It is recommended to do pip install within a virtual environment such as conda.

- pip install ecgannotate-0.2.0-py3-none-any.whl

Clone this repository to your local machine using

- git clone git@github.com:winstonwzhang/ecgannotate.git

and navigate to the root directory.

Run the GUI program in your command line:

- ecgannotate

Expected Result: The GUI interface will show up on screen.

For example functionality, check the notebooks in the tutorial/ folder.
