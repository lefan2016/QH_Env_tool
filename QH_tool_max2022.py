from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qtmax
from pymxs import runtime as rt
import os
import pymxs

def make_editpoly():
    rt.convertToPoly(rt.selection)
    return

def make_material():
    with pymxs.undo(True):
        a = rt.selection
        m = rt.ai_Standard_Surface()
        for x in a :
            x.material = m
    return 

def clear_material():
    with pymxs.undo(True):
        for obj in rt.selection:
            obj.material = rt.undefined

def open_uv():
    a = rt.selection
    uv = rt.Unwrap_UVW()
    for x in a :
        rt.addModifier(x,uv)

    rt.setCommandPanelTaskMode(rt.name('create'))
    rt.setCommandPanelTaskMode(rt.name('modify'))
    uv.edit()



def fbx_setting():
    rt.OpenFbxSetting()   

class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('启虹游戏_场景工具盒')
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

    def import_fast(self):
        rt.execute('max file import')
        
    def cencter_select(self):
        with pymxs.undo(True):
            rt.CenterPivot(rt.selection)

    def world_select(self):
        with pymxs.undo(True):
            s = rt.selection
            for x in s:
                rt.setProperty(x,"pos.x", 0.0)
                rt.setProperty(x,"pos.y", 0.0)
                rt.setProperty(x,"pos.z", 0.0)

    def bake(self):
        
        rt.execute('actionMan.executeAction 1858480148 "23214332"')

    def smmothing(self):
        with pymxs.undo(True):       
            rt.execute('$.EditablePoly.ConvertSelection #Face #Edge')
            rt.execute('$.EditablePoly.makeSmoothEdges 1')
            rt.execute('$.EditablePoly.ConvertSelectionToBorder #Face #Edge')
            rt.execute('$.EditablePoly.makeHardEdges 1')

        #pymxs metond
        # getDollarSel = getattr(rt, '%getDollarSel')
        # rt.polyop.getFaceSelection(getDollarSel())
        # getDollarSel().makeSmoothEdges(1)
        # getDollarSel().convertSelectionToBorder(rt.name('Face'),rt.name('Edge'))
        # getDollarSel().makeHardEdges(1)

    def smmothing_makeplane(self):
        with pymxs.undo(True):       
            rt.execute('$.EditablePoly.ConvertSelection #Face #Edge')
            rt.execute('$.EditablePoly.makeSmoothEdges 1')
            rt.execute('$.EditablePoly.ConvertSelectionToBorder #Face #Edge')
            rt.execute('$.EditablePoly.makeHardEdges 1')
            rt.execute('$.EditablePoly.makePlanar #Face')


    def remove(self):
        with pymxs.undo(True):
            rt.execute('$.EditablePoly.Remove ()')

    def layer_high(self):
        with pymxs.undo(True):
            rt.execute('a = LayerManager.newLayer()')
            rt.execute('a.current = true')         
            rt.execute('a.addnodes $')
            rt.execute('a.setname "high"')

    def layer_low(self):
        with pymxs.undo(True):
            rt.execute('a = LayerManager.newLayer()')
            rt.execute('a.current = true')        
            rt.execute('a.addnodes $')
            rt.execute('a.setname "low"')

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()
        
        label = QtWidgets.QLabel("Mesh-多边形")
        main_layout.addWidget(label)

        editpoly_btn = QtWidgets.QPushButton("塌陷并转换为poly")
        editpoly_btn.clicked.connect(make_editpoly)
        main_layout.addWidget(editpoly_btn)

        remove_btn = QtWidgets.QPushButton("移除边/点")
        remove_btn.clicked.connect(self.remove)
        main_layout.addWidget(remove_btn)

        Tr_label = QtWidgets.QLabel("Pivot-变化")
        main_layout.addWidget(Tr_label)

        bt_cenceterObj = QtWidgets.QPushButton("枢轴到物体中心")
        bt_cenceterObj.clicked.connect(self.cencter_select)
        main_layout.addWidget(bt_cenceterObj)

        bt_world = QtWidgets.QPushButton("枢轴到[0,0,0]")
        bt_world.clicked.connect(self.world_select)
        main_layout.addWidget(bt_world)

        smoothing_lb = QtWidgets.QLabel("Smoothing-光滑组")
        main_layout.addWidget(smoothing_lb)


        smoothing_btn = QtWidgets.QPushButton("光滑组")
        smoothing_btn.clicked.connect(self.smmothing)
        main_layout.addWidget(smoothing_btn)

        smoothing_plane_btn = QtWidgets.QPushButton("打平面+光滑组")
        smoothing_plane_btn.clicked.connect(self.smmothing_makeplane)
        main_layout.addWidget(smoothing_plane_btn)

        #
        label_m = QtWidgets.QLabel("Material-材质")
        main_layout.addWidget(label_m)

        material_btn = QtWidgets.QPushButton("单一材质")
        material_btn.clicked.connect(make_material)
        main_layout.addWidget(material_btn)

        materialclear_btn = QtWidgets.QPushButton("清除选择物体材质")
        materialclear_btn.clicked.connect(clear_material)
        main_layout.addWidget(materialclear_btn)
        #
        label2 = QtWidgets.QLabel("Modifter-修改器")
        main_layout.addWidget(label2)

        uv_btn = QtWidgets.QPushButton("UV")
        uv_btn.clicked.connect(open_uv)
        main_layout.addWidget(uv_btn)

        label_bake = QtWidgets.QLabel("Bake-烘培")
        main_layout.addWidget(label_bake)

        bt_bake = QtWidgets.QPushButton('烘培')
        bt_bake.clicked.connect(self.bake)
        main_layout.addWidget(bt_bake)
        #
        label3 = QtWidgets.QLabel("Export-导出")
        main_layout.addWidget(label3)

        self.fbxsetting_btn = QtWidgets.QPushButton("FBX输出设置........")
        self.fbxsetting_btn.clicked.connect(fbx_setting)
        main_layout.addWidget(self.fbxsetting_btn)
        #
        self.main_layout2 = QtWidgets.QHBoxLayout()
        self.selectpath_btn = QtWidgets.QPushButton("选择路径........")
        self.selectpath_btn.clicked.connect(self.select_path)
        main_layout.addWidget(self.selectpath_btn)
        #
        self.path_line = QtWidgets.QLineEdit()
        self.main_layout2.addWidget(self.path_line)
        self.name_line = QtWidgets.QLineEdit()
        self.main_layout2.addWidget(self.name_line)
        #
        self.main_layout2.setStretch(0,3)
        self.main_layout2.setStretch(1,1)
        
        main_layout.addLayout(self.main_layout2)

        export_btn = QtWidgets.QPushButton("导出FBX")
        export_btn.clicked.connect(self.export_fbx)
        main_layout.addWidget(export_btn)
        export_btn2 = QtWidgets.QPushButton("导出OBJ")
        export_btn2.clicked.connect(self.export_obj)
        main_layout.addWidget(export_btn2)

        label_import = QtWidgets.QLabel("Import-导入")
        main_layout.addWidget(label_import)

        bt_import = QtWidgets.QPushButton('导入')
        bt_import.clicked.connect(self.import_fast)
        main_layout.addWidget(bt_import)


        label_layer = QtWidgets.QLabel("Layer-图层")
        main_layout.addWidget(label_layer)

        bt_high = QtWidgets.QPushButton('high')
        bt_high.clicked.connect(self.layer_high)
        main_layout.addWidget(bt_high)


        bt_low = QtWidgets.QPushButton('low')
        bt_low.clicked.connect(self.layer_low)
        main_layout.addWidget(bt_low)



        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(300, 600)

def main():
    
    main_window = qtmax.GetQMaxMainWindow()
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()

if __name__ == '__main__':
    main()