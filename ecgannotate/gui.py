"""
ECGannotate GUI main function
"""

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets

app = pg.mkQApp("Plotting Example")
win = QtWidgets.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)
win.setWindowTitle('pyqtgraph example: docks')

#win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
#win.resize(1000,600)
#win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


## Create docks, place them into the window one at a time.
## Note that size arguments are only a suggestion; docks will still have to
## fill the entire dock area and obey the limits of their internal widgets.
d1 = Dock("Dock1", size=(1000, 100))
d2 = Dock("Dock2", size=(200,400))
d3 = Dock("Dock3 (tabbed) - Plot", size=(800,400))
d4 = Dock("Dock4 (tabbed) - Plot", size=(800,400))

area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
area.addDock(d2, 'bottom', d1)## place d2 at bottom edge of d1
area.addDock(d3, 'left', d2)     ## place d3 at left edge of d2
area.addDock(d4, 'left', d2)  ## place d4 at left edge of d2

## Test ability to move docks programatically after they have been placed
area.moveDock(d3, 'above', d4)   ## move to stack


## add widgets into docks

w1 = pg.LayoutWidget()
label = QtWidgets.QLabel(""" -- DockArea Example -- """)
saveBtn = QtWidgets.QPushButton('Save dock state')
restoreBtn = QtWidgets.QPushButton('Restore dock state')
restoreBtn.setEnabled(False)
w1.addWidget(label, row=0, col=0)
w1.addWidget(saveBtn, row=1, col=0)
w1.addWidget(restoreBtn, row=2, col=0)
d1.addWidget(w1)

w2 = ConsoleWidget()
d2.addWidget(w2)

x2 = np.linspace(-100, 100, 1000)
data2 = np.sin(x2) / x2
w3 = pg.PlotWidget(title="Region Selection")
p8 = w3.plot(data2, pen=(255,255,255,200))
lr = pg.LinearRegionItem([400,700])
lr.setZValue(-10)
w3.addItem(lr)
d3.addWidget(w3)
#p8 = win.addPlot(title="Region Selection")
#p8.plot(data2, pen=(255,255,255,200))
#lr = pg.LinearRegionItem([400,700])
#lr.setZValue(-10)
#p8.addItem(lr)

w4 = pg.PlotWidget(title="Zoom on selected region")
w4.plot(data2)
def updatePlot():
    w4.setXRange(*lr.getRegion(), padding=0)
def updateRegion():
    lr.setRegion(w4.getViewBox().viewRange()[0])
lr.sigRegionChanged.connect(updatePlot)
w4.sigXRangeChanged.connect(updateRegion)
updatePlot()
d4.addWidget(w4)

#p9 = win.addPlot(title="Zoom on selected region")
#p9.plot(data2)
#def updatePlot():
#    p9.setXRange(*lr.getRegion(), padding=0)
#def updateRegion():
#    lr.setRegion(p9.getViewBox().viewRange()[0])
#lr.sigRegionChanged.connect(updatePlot)
#p9.sigXRangeChanged.connect(updateRegion)
#updatePlot()

win.show()

if __name__ == '__main__':
    pg.exec()
