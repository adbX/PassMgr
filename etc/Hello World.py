import sys
from PySide.QtCore import *
from PySide.QtGui import *

app = QApplication(sys.argv)
label = QLabel("<font color=red size=40>Hello World</font>")
label.show()
app.exec_()
