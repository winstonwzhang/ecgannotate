"""
ECGannotate GUI main function
"""

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets


class UI(QtWidgets.QWidget):

    def __init__(self):
        super(UI, self).__init__()
        self.win = QtWidgets.QMainWindow()
        
        self.sr = 500 # default MIT-BIH sampling rate
        self.win_size = 10*self.sr  # 10 second default view
        self.idx = 0  # left-most plot time index
        
        # placeholder data
        self.ecg = np.linspace(-1, 1, self.win_size*2)
        # example table
        # [{'start': 23, 'end': 48, 'type': 'AF'}]
        self.table = []
        
        self.setupUI(self.win)
        self.win.show()

    def setupUI(self, win):
        area = DockArea()
        win.setCentralWidget(area)
        win.resize(1000,500)
        win.setWindowTitle('UI')

        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        d1 = Dock("File IO", size=(1000, 100))
        d2 = Dock("Dock2", size=(200,400))
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
        #restoreBtn.setEnabled(False)
        
        self.w1.addWidget(label, row=0, col=0)
        self.w1.addWidget(loadBtn, row=1, col=0)
        self.w1.addWidget(saveBtn, row=2, col=0)
        d1.addWidget(self.w1)

        w2 = ConsoleWidget()
        d2.addWidget(w2)

        # w3 (ecg plot)
        self.w3 = pg.PlotWidget(title="ECG Viewer")
        self.w3_plot = self.w3.plot(self.ecg, pen=(255,255,255,200))
        self.w3.setMenuEnabled(False)
        d3.addWidget(self.w3)
        
        # right click menu for plot
        self.w3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.w3.customContextMenuRequested.connect(self.plotRightMenu)
        
        self.action = QtGui.QAction(self)
        self.action.setObjectName('af')        
        self.action.setText ('AF')

        self.action1 = QtGui.QAction(self)
        self.action1.setObjectName('vt')
        self.action1.setText ('VT')  

        self.customMenu = QtWidgets.QMenu('Menu', self.w3)       
        self.customMenu.addAction(self.action)
        self.customMenu.addAction(self.action1)     

        self.action.triggered.connect(self.afClicked)
        self.action1.triggered.connect(self.vtClicked)
        
        
        # w4 (annotation table)
        self.w4 = pg.TableWidget(editable=True)
        d4.addWidget(self.w4)
        self.updateUI()
    
    def loadClicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.w1,
            "QFileDialog", 
            "example_data",
            "Numpy Files (*.npy)", 
            options=options)
        if fileName:
            raw = np.load(fileName)
            self.ecg = raw.flatten()
            # clear preexisting annotations when loading new data
            self.table = []
            self.updateUI()
    
    def plotRightMenu(self, event):
        self.customMenu.popup (QtGui.QCursor.pos())
    
    def afClicked(self, event):
        self.table.append({'start': self.idx, 
                           'end': self.idx+self.win_size, 
                           'type': 'AF'})
        self.updateUI()
    
    def vtClicked(self, event):
        self.table.append({'start': self.idx, 
                           'end': self.idx+self.win_size, 
                           'type': 'VT'})
        self.updateUI()
    
    def updateUI(self):
        self.w3_plot.setData(self.ecg[self.idx:self.idx+self.win_size])
        self.w4.setData(self.table)




if __name__ == '__main__':
    pg.setConfigOptions(antialias=True)
    app = pg.mkQApp("Plotting Example")
    
    ui = UI()
    
    pg.exec()
