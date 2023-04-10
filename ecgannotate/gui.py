"""
ECGannotate GUI main function
"""

import numpy as np
import csv

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets

import ecg
import sortMergeAnnotations


class UI(QtWidgets.QWidget):
    '''Main GUI Class'''

    def __init__(self):
        '''Initialize GUI window and parameters'''
        super(UI, self).__init__()
        self.win = QtWidgets.QMainWindow()
        
        self.sr = 500 # default MIT-BIH sampling rate
        self.win_size = 10*self.sr  # 10 second default view
        self.idx = 0  # left-most plot time index
        self.cur_win = 0
        
        # placeholder data
        self.ecg = np.linspace(-1, 1, self.win_size)
        self.len = len(self.ecg)
        self.peaks = np.array([])
        self.max_win = 0
        # example table
        # [{'win': 1, 'start': 23, 'end': 48, 'type': 'AF'}]
        self.table = []
        
        self.setupUI(self.win)
        self.win.show()

    def setupUI(self, win):
        '''Create initial dock components'''
        area = DockArea()
        win.setCentralWidget(area)
        win.resize(1000,500)
        win.setWindowTitle('UI')

        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        d1 = Dock("File IO", size=(1000, 100))
        d2 = Dock("Plot Controls", size=(200,400))
        d3 = Dock("ECG Plot", size=(800,400))
        d4 = Dock("Annotations Table", size=(800,400))

        area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
        area.addDock(d2, 'bottom', d1)## place d2 at bottom edge of d1
        area.addDock(d3, 'left', d2)     ## place d3 at left edge of d2
        area.addDock(d4, 'left', d2)  ## place d4 at left edge of d2

        ## Test ability to move docks programatically after they have been placed
        area.moveDock(d3, 'above', d4)   ## move to stack


        ## add widgets into docks

        self.w1 = pg.LayoutWidget()
        label = QtWidgets.QLabel(""" -- Load ECG / Save Annotations -- 
        Warning: Loading new data will clear preexisting annotations. """)
        loadBtn = QtWidgets.QPushButton('Load file')
        loadBtn.clicked.connect(self.loadClicked)
        
        saveBtn = QtWidgets.QPushButton('Save annotations')
        saveBtn.clicked.connect(self.saveClicked)
        
        self.w1.addWidget(label, row=0, col=0)
        self.w1.addWidget(loadBtn, row=1, col=0)
        self.w1.addWidget(saveBtn, row=2, col=0)
        d1.addWidget(self.w1)

        # plot controls and display
        self.w2 = pg.LayoutWidget()
        nextBtn = QtWidgets.QPushButton('Next window')
        nextBtn.clicked.connect(self.nextClicked)
        prevBtn = QtWidgets.QPushButton('Previous window')
        prevBtn.clicked.connect(self.prevClicked)
        self.winNum = QtWidgets.QLabel('Current window: 0 out of 0')
        self.hrNum = QtWidgets.QLabel('Current window heart rate: 0')
        self.pkNum = QtWidgets.QLabel('Number of R peaks detected: 0')
        
        self.boxLabel = QtWidgets.QLabel('Go to window: ')
        self.winBox = QtWidgets.QSpinBox()
        self.winBox.setRange(0, 0)
        self.winBox.setSingleStep(1)
        self.winBox.setValue(0)
        self.winBox.valueChanged.connect(self.winBoxChanged)
        
        self.w2.addWidget(nextBtn, row=0, col=0)
        self.w2.addWidget(prevBtn, row=1, col=0)
        self.w2.addWidget(self.winNum, row=2, col=0)
        self.w2.addWidget(self.boxLabel, row=3, col=0)
        self.w2.addWidget(self.winBox, row=4, col=0)
        self.w2.addWidget(self.pkNum, row=5, col=0)
        self.w2.addWidget(self.hrNum, row=6, col=0)
        
        d2.addWidget(self.w2)
        

        # w3 (ecg plot)
        self.w3 = pg.PlotWidget(title="ECG Viewer")
        self.w3_plot = self.w3.plot(self.ecg, pen=(255,255,255,200))
        self.w3_scatter = pg.ScatterPlotItem(x=[], y=[], symbol='o', brush='r')
        self.w3.addItem(self.w3_scatter)
        
        self.w3.setMenuEnabled(False)
        d3.addWidget(self.w3)
        
        # right click menu for plot
        self.w3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.w3.customContextMenuRequested.connect(self.plotRightMenu)
        
        self.action = QtGui.QAction(self)
        self.action.setObjectName('af')
        self.action.setText('AF')

        self.action1 = QtGui.QAction(self)
        self.action1.setObjectName('vt')
        self.action1.setText('VT')
        
        self.action2 = QtGui.QAction(self)
        self.action2.setObjectName('noise')
        self.action2.setText('Noise')  

        self.customMenu = QtWidgets.QMenu('Menu', self.w3)       
        self.customMenu.addAction(self.action)
        self.customMenu.addAction(self.action1)
        self.customMenu.addAction(self.action2)

        self.action.triggered.connect(self.afClicked)
        self.action1.triggered.connect(self.vtClicked)
        self.action2.triggered.connect(self.noiseClicked)
        
        # w4 (annotation table)
        self.w4 = pg.TableWidget(editable=True)
        d4.addWidget(self.w4)
        
        self.updatePlot()
        self.updateTable()
    
    
    def loadClicked(self):
        '''ECG Load file button clicked'''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.w1,
            "QFileDialog", 
            "example_data",
            "Numpy Files (*.npy)", 
            options=options)
        # check for null or empty file
        if fileName:
            raw = np.load(fileName)
            if not np.isnan(raw).any():
                self.ecg = raw.flatten()
                self.len = len(self.ecg)
                self.peaks = np.array(ecg.findPeaks(self.sr, self.ecg))
                self.max_win = self.len // self.win_size
                self.winBox.setRange(0, self.max_win-1)
            # clear preexisting annotations when loading new data
            self.table = []
            self.updatePlot()
            self.updateTable()
    
    def saveClicked(self, event):
        if len(self.table) != 0:
            # sort and merge annotations
            new_table = sortMergeAnnotations.sortMergeAnnotations(self.table)
            # Show a file dialog to choose where to save the CSV file
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self.w1,
                            "Save CSV File", "",
                            "CSV Files (*.csv)",
                            options=options)
            if filename:
                # Save the dictionary to the chosen CSV file
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = new_table[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in new_table:
                        writer.writerow(row)
    
    def nextClicked(self, event):
        # plot next window
        new_idx = self.idx + self.win_size
        # check for out of bounds
        if new_idx+self.win_size <= self.len:
            self.idx = new_idx
        self.updatePlot()
    
    def prevClicked(self, event):
        # plot next window
        new_idx = self.idx - self.win_size
        # check for out of bounds
        if new_idx >= 0:
            self.idx = new_idx
        self.updatePlot()
    
    def winBoxChanged(self, value):
        self.idx = value * self.win_size
        self.updatePlot()
    
    def plotRightMenu(self, event):
        self.customMenu.popup(QtGui.QCursor.pos())
    
    def afClicked(self, event):
        '''Atrial fibrillation label for this time section'''
        self.table.append({'win': self.cur_win,
                           'start': self.idx, 
                           'end': self.idx+self.win_size, 
                           'type': 'AF'})
        self.updateTable()
    
    def vtClicked(self, event):
        '''Ventricular Tachycardia label for this time section'''
        self.table.append({'win': self.cur_win,
                           'start': self.idx, 
                           'end': self.idx+self.win_size, 
                           'type': 'VT'})
        self.updateTable()
    
    def noiseClicked(self, event):
        '''Noise label for this time section'''
        self.table.append({'win': self.cur_win,
                           'start': self.idx, 
                           'end': self.idx+self.win_size, 
                           'type': 'Noise'})
        self.updateTable()
    
    def updatePlot(self):
        '''Refresh plots and heart rate statistics'''
        w_start = self.idx
        w_end = self.idx+self.win_size
        new_data = self.ecg[w_start:w_end]
        self.cur_win = self.idx // self.win_size
        
        if self.peaks.size != 0:
            self.cur_peaks = self.peaks[(self.peaks >= w_start) & (self.peaks <= w_end)]
            new_hr = ecg.calculateHR(len(self.cur_peaks), self.sr, self.win_size)
            # update statistics display
            self.winNum.setText('Current window: ' + str(self.cur_win) + ' out of ' + str(self.max_win-1))
            self.pkNum.setText('Number of R peaks detected: ' + str(len(self.cur_peaks)))
            self.hrNum.setText('Current window heart rate: ' + str(new_hr))
            if self.cur_peaks.size != 0:
                plot_peaks = self.cur_peaks - self.idx
                self.w3_scatter.setData(x=plot_peaks, y=new_data[plot_peaks])
        
        self.w3_plot.setData(new_data)
    
    def updateTable(self):
        '''Refresh annotation table'''
        self.w4.setData(self.table)



def runGUI():
    pg.setConfigOptions(antialias=True)
    app = pg.mkQApp("Plotting Example")
    ui = UI()
    pg.exec()



if __name__ == '__main__':
    pg.setConfigOptions(antialias=True)
    app = pg.mkQApp("Plotting Example")
    
    ui = UI()
    
    pg.exec()
