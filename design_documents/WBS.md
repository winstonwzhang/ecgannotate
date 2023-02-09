
# ECGannotate Work Breakdown Structure (WBS)

---

# Activity 1: First Basic Output

The first basic output of the GUI is to display a pre-processed ECG signal in the GUI window. The following components of the GUI will read in raw data from the MIT-BIH dataset, preprocess the signal data in Python, and display the data to the user.

## Task 1.1 What is the input data format?

A .csv file that contains raw ECG signals. Signals will be taken from lead II.

## Task 1.2 How should the input data be read into Python?

Using the "pandas" module, the .csv file will be read into a dataframe object. The time series ECG signal will then be manipulated using the dataframe format.

## Task 1.3 How will the raw ECG signal be pre-processed in the GUI?

Raw ECG signals are often noisy and have baseline wander which makes displaying the signals confusing for physicians. A butterworth bandpass filter will be used to remove frequencies above 40 Hz and below 0.5 Hz to remove high and low frequency noise. A median filter will be used to remove baseline wander. 

## Task 1.4 What other statistics will be calculated for display in the GUI?

QRS complexes will be found in the preprocessed ECG signals using the widely-used Pan-Tompkins algorithm. Heart rate statistics are calculated based on R peak locations. The statistics are then displayed at the side of the preprocessed signal plot in the GUI.

---

# Activity 2: Create GUI Framework

A suitable Python GUI library must be used to create the user interface of the program. The GUI must include callback functions and visual displays for loading, viewing, analyzing, and annotating input ECG data.

## Task 2.1 Choose Python GUI Library

For a scientific application GUI like this project, the PyQt wrapper library is the best choice for develping graph plotting and annotation functions.

## Task 2.2 Install and Test GUI Libraries and Dependencies

All dependencies for developing a PyQt GUI that can read in .csv files will be installed into a conda environment. The dependencies will be tested for compatibility and ease of installation when using setup.py.

## Task 2.3 Develop Simple Data Loader

To test the GUI framework, a simple GUI will be developed first that will load a selected .csv file into the program memory. A loading button will allow a user to load data by selecting a file from the file list box.

---

# Activity 3: Develop ECG Viewer

The GUI is split into the loading tab, the data viewer tab, and the annotation saver tab. In this activity the data viewer tab is developed.

## Task 3.1 Implement Preprocessing and Statistic Calculation

Raw ECG signals loaded during the loading tab are preprocessed and have statistics calculated as detailed in Activity 1. The results are stored in program memory.

## Task 3.2 Design Viewer Components

Using PyQt, position the main signal viewing plot in a central location in the data viewing tab. Buttons and a timeline component will allow users to view different time sections of the input ECG signal. Number displays will show important heart rate statistics to the side of the main signal plot.

---

# Activity 4: ECG Annotation and Saving

User annotations of viewed ECG signals will be stored within program memory. A separate tab will allow users to save any marked time sections of the signal as a .csv file to hard drive.

## Task 4.1 Develop Annotation Callback

To allow users to add annotations to any time section of the currently viewed ECG signal, a click and drag callback function is added to the signal plot to allow users to drag and select time sections that can then be annotated as various arrhythmias.

## Task 4.2 Annotation Display

Already created annotations will be displayed along with the ECG signal viewer. A full list of annotations and their time sample positions is displayed in the annotation tab within a table component. Annotations can be deleted or edited using the table component.

## Task 4.3 Annotation Saver

Finished annotations can be saved using a button that will create a file browser in the user hard drive.