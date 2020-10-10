# Author: Noirai

# AUTO SPLIT, UV UNWRAP, UV LAYOUT with UDIM starting from 1001, CREATE OC UNIVERSAL MATERIAL

# If you already have a geo with different components in groups
# Set up an Object Merge or filecache and import your geo
# Specify geo and merge node name below
targetSubnetName = "targetGeo" 
targetMergeNodeName = "object_merge1"

# Output FBX File Name: cube.fbx
# Substance Painter preset: $mesh_$textureSet_channel
# Substance texture output path: D:/textures/cube/
# -> meshName "cube"
# -> texturePath "D:/textures/cube/"
meshName = "mesh_name"
texturePath = "texture_path" 

geo = hou.pwd().node("../" + targetSub  netName)
texturePath += (meshName + "_")
shopNetNode = geo.createNode("shopnet")

# Default displacement and material IOR
displacement = 0.001
IOR = 1

for childCount, childNet in enumerate(list(geo.children())):
    if childNet.name() == targetMergeNodeName:

        groups = [g.name() for g in childNet.geometry().primGroups()]
        #print(childNet.geometry().primGroups())
        for i, name in enumerate(groups):
            splitNode = geo.createNode("split")
            splitNode.parm("group").set(name)
            splitNode.setInput(0, childNet, 0)

            uvUnwrapNode = geo.createNode("uvunwrap")
            uvUnwrapNode.setInput(0, splitNode, 0)
            
            udim = 1001 + i
            uvLayoutNode = geo.createNode("uvlayout::3.0")
            uvLayoutNode.parm("targettype").set("udim")
            uvLayoutNode.parm("usedefaultudimtarget").set(1)
            uvLayoutNode.parm("defaultudimtarget").set(udim)
            uvLayoutNode.setInput(0, uvUnwrapNode, 0)
           
            uvTransformNode = geo.createNode("uvtransform::2.0")
            uvTransformNode.setInput(0, uvLayoutNode, 0)
            uvTransformNode.parm('px').setExpression("lvar('CEX')", language=hou.exprLanguage.Python)
            uvTransformNode.parm('py').setExpression("lvar('CEY')", language=hou.exprLanguage.Python)
            uvTransformNode.parm("pz").setExpression("lvar('CEZ')", language=hou.exprLanguage.Python)
            
            uvTransformNode.parm("sx").set(0.95)
            uvTransformNode.parm("sy").set(0.95)
            uvTransformNode.parm("sz").set(0.95)
            
            fileCacheNode = geo.createNode("filecache")
            fileCacheNode.parm("file").set("$HIP/geo/" + name +"_UVED.bgeo.sc")
            fileCacheNode.setInput(0, uvTransformNode, 0)
            
            materialNode = geo.createNode("material")
            materialNode.setInput(0, fileCacheNode, 0)
            
            # Create OC Material in Shopnet
            udim = str(udim)
            ocMaterialNode = shopNetNode.createNode("octane_vopnet")
            ocMaterialNode.setName(name)
            ocMaterialNodePath = ocMaterialNode.path()

            #base color srgb, set brightness to 1
            baseColorNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            baseColorNode.parm("A_FILENAME").set(texturePath + name + "_BaseColor.exr")
            baseColorNode.parm("gamma").set(1)

            #other color linear, keep brightness number
            specularNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            specularNode.parm("A_FILENAME").set(texturePath + name + "_Specular.exr")

            roughnessNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            roughnessNode.parm("A_FILENAME").set(texturePath + name + "_Roughness.exr")

            normalNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            normalNode.parm("A_FILENAME").set(texturePath + name + "_Normal.exr")

            heightNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            heightNode.parm("A_FILENAME").set(texturePath + name + "_Height.exr")

            metallicNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            metallicNode.parm("A_FILENAME").set(texturePath + name + "_Metallic.exr")

            #opacityNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            #opacityNode.parm("A_FILENAME").set(texturePath + udim + "_Opacity.exr")
            
            #emissiveNode = ocMaterialNode.createNode("octane::NT_TEX_IMAGE")
            #emissiveNode.parm("A_FILENAME").set(texturePath + udim + "_Emissive.exr")

            vertexDisplacementNode = ocMaterialNode.createNode("octane::NT_VERTEX_DISPLACEMENT")
            vertexDisplacementNode.setInput(0, heightNode, 0)
            vertexDisplacementNode.parm("amount").set(displacement)

            glossyMaterialNode = ocMaterialNode.createNode("octane::NT_MAT_UNIVERSAL")

            #SET MATERIAL IOR
            glossyMaterialNode.parm("index4").set(IOR)

            glossyMaterialNode.setInput(2, baseColorNode, 0) #diffuse
            glossyMaterialNode.setInput(3, metallicNode, 0) #diffuse
            glossyMaterialNode.setInput(4, specularNode, 0) #specular
            glossyMaterialNode.setInput(6, roughnessNode, 0) #roughness 
            glossyMaterialNode.setInput(32, normalNode, 0) #normal
            glossyMaterialNode.setInput(33, vertexDisplacementNode, 0) #displacement   

            OCMaterialNode = hou.node(ocMaterialNodePath + "/octane_material1")
            OCMaterialNode.setInput(0, glossyMaterialNode, 0)

            materialNode.parm("shop_materialpath1").set(ocMaterialNodePath)
            

