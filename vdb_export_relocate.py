# Export geo components after VDB'd in Houdini
# Retopo / Sculpt / Do whatever you want with any other apps (ZB Decimating Master, Maya etc.)
# Import back with a match size node to relocate

# Specify targetNode name
targetVDBNodeName = "targetVDBNode"
targetMergeNodeName = "object_merge1"

# Specify VDB Parameters
vdbSmoothIteration = 2
vdbSmoothOperation = "meancurvature" #gaussian medianvalue meancurvature meanvalue laplacianflow
vdbVoxelSize = 0.05
vdbVoxelAdaptivity = 0.00001

# Models ready to retopo goes in 
ropOutputPath = "/model_for_retopo/" + targetVDBNodeName + "/"

# Models after retopo goes in (match size node)
modelOutputPath = "/model/" + targetVDBNodeName + "/"

geo = hou.pwd().node("../" + targetVDBNodeName)

# loop through all the nodes and 
for childCount, childNet in enumerate(list(geo.children())):

    if childNet.name() == targetMergeNodeName:
        groups = [g.name() for g in childNet.geometry().primGroups()]

        for i, name in enumerate(groups):
            print("Found Component: ", childNet.name())

            splitNode = geo.createNode("split")
            splitNode.parm("group").set(name)
            splitNode.setInput(0, childNet, 0)
           
            vdbFromPolygonsNode = geo.createNode("vdbfrompolygons")
            vdbFromPolygonsNode.parm("voxelsize").set(vdbVoxelSize)
            vdbFromPolygonsNode.setInput(0, splitNode, 0)
            
            vdbSmoothNode = geo.createNode("vdbsmoothsdf")
            vdbSmoothNode.parm("operation").set(vdbSmoothOperation)
            vdbSmoothNode.parm("iterations").set(vdbSmoothIteration)
            vdbSmoothNode.setInput(0, vdbFromPolygonsNode, 0)

            convertVDBNode = geo.createNode("convertvdb")
            convertVDBNode.setInput(0, vdbSmoothNode, 0)
            convertVDBNode.parm("conversion").set("poly")
            convertVDBNode.parm("adaptivity").set(vdbVoxelAdaptivity)
 
            ropNode = geo.createNode("rop_fbx")
            ropNode.parm("sopoutput").set(ropOutputPath + name + ".fbx")
            ropNode.setInput(0, convertVDBNode, 0)

            fileNode = geo.createNode("file")
            fileNode.parm("file").set(modelOutputPath + name + ".fbx")

            matchSizeNode = geo.createNode("matchsize")
            matchSizeNode.setInput(1, fileNode, 0)
            matchSizeNode.setInput(0, childNet, 0)