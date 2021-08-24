from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qtmax

from pymxs import runtime as rt

def make_editpoly():
    rt.convertToPoly(rt.selection)

    return


def make_material():
    a = rt.selection
    m = rt.standardMaterial()
    for x in a :
        x.material = m

    return    

class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('启虹游戏')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("多边形")
        main_layout.addWidget(label)

        editpoly_btn = QtWidgets.QPushButton("塌陷转换为多边形")
        editpoly_btn.clicked.connect(make_editpoly)
        main_layout.addWidget(editpoly_btn)

        material_btn = QtWidgets.QPushButton("快速赋予材质")
        material_btn.clicked.connect(make_material)
        main_layout.addWidget(material_btn)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(250, 100)

def main():
    
    main_window = qtmax.GetQMaxMainWindow()
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()

if __name__ == '__main__':
    main()