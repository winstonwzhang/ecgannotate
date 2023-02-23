
# Software Requirements Specification (SRS)
	For: ECGannotate
	By: Winston Zhang
	Version: 0.1.0

- 1.	Introduction
  - 1.1	Purpose
    - 1.1.1	A Graphical User Interface for reading and annotating electrocardiogram (ECG) signals
- 2.	Overall Description
  - 2.1	 Function
    - 2.1.1	Signal plot
      - 2.1.1.1	Read ECG signals from hard drive
      - 2.1.1.2	Preprocess signals
      - 2.1.1.3 Plot signals in GUI viewer
    - 2.1.2	Analyze signals
      - 2.1.2.1	Calculate QRS complex locations in signal
      - 2.1.2.2 Calculate heart rate statistics
      - 2.1.2.3 Display statistics in GUI
    - 2.1.3 Annotation table
      - 2.1.3.1 Annotation interaction using mouse and keyboard shortcuts
      - 2.1.3.2 Table displays all past annotations
      - 2.1.3.3 Annotations can be edited or deleted from table interface
      - 2.1.3.4 Annotations can be saved to hard drive
  - 2.2 Unit Tests
    - 2.2.1 GUI tests
      - 2.2.1.1 Manual test for successfully loading .npy file from drive
      - 2.2.1.2 Manual test for plotting of ECG signal
      - 2.2.1.3 Manual test for adding annotations by mouse right click
      - 2.2.1.4 Manual test for display of past added annotations in table interface
    - 2.2.2 Functionality tests
      - 2.2.2.1 Test for input file edge cases
      - 2.2.2.2 Test for successful preprocessing/normalization of ECG signal
      - 2.2.2.3 Test for successful calculation of QRS locations
      - 2.2.2.4 Test for successful heart rate calculation
- 3.	Requirements
  - 3.1	Language
    - 3.1.1	Python
  - 3.2	Input
    - 3.2.1	.npy file (converted from MIT-BIH arrhythmia database)
    - 3.2.2	Manual user annotations
  - 3.3	Interface
    - 3.3.1	Data loader module
    - 3.3.2	ECG signal viewer
    - 3.3.3	Annotation table with editing functions
    - 3.3.4	Mouse and keyboard annotation input
    - 3.3.5	Signal timeline browser
  - 3.4	Output
    - 3.4.1	ECG signal plots
    - 3.4.2	User annotations specific to ECG signal
