from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qtmax
from pymxs import runtime as rt
import os

def make_editpoly():
    rt.convertToPoly(rt.selection)
    return

def make_material():
    a = rt.selection
    m = rt.standardMaterial()
    for x in a :
        x.material = m
    return 

def clear_material():
    for obj in rt.selection:
        obj.material = rt.undefined

def open_uv():
    a = rt.selection
    uv = rt.Unwrap_UVW()
    for x in a :
        rt.addModifier(x,uv)
    uv.edit()

def fbx_setting():
    rt.OpenFbxSetting()   

class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('启虹游戏工具盒')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def select_path(self):
        directory = os.path.dirname(self.path_line.text())
        if not os.path.exists(directory):
            directory = ''       
        output_path = QtWidgets.QFileDialog.getExistingDirectory(dir=directory)
        output_path =  output_path +"\\"
        self.path_line.setText(output_path)

    def export_fbx(self):
        path = self.path_line.text()
        name = self.name_line.text()
        rt.exportFile(path+name,rt.name('noPrompt'),selectedOnly=True,using=rt.FBXEXP)

    def export_obj(self):
        path = self.path_line.text()
        name = self.name_line.text()
        rt.exportFile(path+name,rt.name('noPrompt'),selectedOnly=True,using=rt.ObjExp)

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()
        
        label = QtWidgets.QLabel("多边形")
        main_layout.addWidget(label)

        editpoly_btn = QtWidgets.QPushButton("塌陷并转换为Editpoly")
        editpoly_btn.clicked.connect(make_editpoly)
        main_layout.addWidget(editpoly_btn)
        #
        label_m = QtWidgets.QLabel("材质")
        main_layout.addWidget(label_m)

        material_btn = QtWidgets.QPushButton("快速赋予材质")
        material_btn.clicked.connect(make_material)
        main_layout.addWidget(material_btn)

        materialclear_btn = QtWidgets.QPushButton("清除选择物体材质")
        materialclear_btn.clicked.connect(clear_material)
        main_layout.addWidget(materialclear_btn)
        #
        label2 = QtWidgets.QLabel("修改器")
        main_layout.addWidget(label2)

        uv_btn = QtWidgets.QPushButton("UV")
        uv_btn.clicked.connect(open_uv)
        main_layout.addWidget(uv_btn)
        #
        label3 = QtWidgets.QLabel("导出")
        main_layout.addWidget(label3)

        self.fbxsetting_btn = QtWidgets.QPushButton("FBX输出设置........")
        self.fbxsetting_btn.clicked.connect(fbx_setting)
        main_layout.addWidget(self.fbxsetting_btn)
        #
        self.main_layout2 = QtWidgets.QHBoxLayout()
        self.selectpath_btn = QtWidgets.QPushButton("选择路径........")
        self.selectpath_btn.clicked.connect(self.select_path)
        self.main_layout2.addWidget(self.selectpath_btn)
        #
        self.path_line = QtWidgets.QLineEdit()
        self.main_layout2.addWidget(self.path_line)
        self.name_line = QtWidgets.QLineEdit()
        self.main_layout2.addWidget(self.name_line)
        #
        self.main_layout2.setStretch(0,1)
        self.main_layout2.setStretch(1,3)
        self.main_layout2.setStretch(2,1)
        main_layout.addLayout(self.main_layout2)

        export_btn = QtWidgets.QPushButton("导出FBX")
        export_btn.clicked.connect(self.export_fbx)
        main_layout.addWidget(export_btn)
        export_btn2 = QtWidgets.QPushButton("导出OBJ")
        export_btn2.clicked.connect(self.export_obj)
        main_layout.addWidget(export_btn2)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(350, 200)

def main():
    
    main_window = qtmax.GetQMaxMainWindow()
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()

if __name__ == '__main__':
    main()