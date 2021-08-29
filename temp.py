from pymxs import runtime as rt

#maxscript  to  pymxs
# polyop.getFaceSelection $

rt.polyop.getgetFaceSelection

# $.EditablePoly.ConvertSelection #Face #Edge

rt.Editable_Poly.ConvertSelection(rt.name('#Face'),rt.name('#Edge'),requireAll=False)

# $.EditablePoly.makeSmoothEdges 1



# $.EditablePoly.ConvertSelectionToBorder #Face #Edge


# $.EditablePoly.makeHardEdges 1



a = LayerManager.newLayer()
a.current = true
a.name = "high"
a.addnodes $
a.setname "high"
