# Author: Noirai

import hashlib

# read every texture in every shopnets in every node in your project
# find duplicated textures with MD5 calculation
# point to same texture to (theoretically prevent loading the same texture with different name into VRAM multiple times)
# Currently OCTANE ONLY

textureObjArray = {}
targetSubnetName = "targetGeo"
geo = hou.pwd().node("/obj/" + targetSubnetName)

for nodeCount, nodeNet in enumerate(list(geo.children())):
    
    #Find all shopnets in nodes
    if nodeNet.type() == hou.nodeType("Sop/shopnet"):
        
        #find all vopnet in shopnet
        for shopCount, shopNet in enumerate(list(nodeNet.children())):
            if shopNet.type() == hou.nodeType("Shop/octane_vopnet"):

                #find all texture in vopnet
                for textureNode in shopNet.children():

                    # Should check type instead of name here
                    if textureNode.name().startswith("NT_TEX_IMAGE"): 
                        print("Current Texture Node: ", textureNode.name())
                        texPath = textureNode.evalParm("A_FILENAME")
                        print("Current Texture Path: ", texPath)
                        texHash = hashlib.md5(open(texPath, 'rb').read()).hexdigest()
                        print("Current Texture MD5: ", texHash)
                        
                        if texHash not in textureObjArray:
                            textureObjArray[texHash] = texPath
                        else:
                            print("Found Used Texture: ", texHash)
                            textureNode.parm("A_FILENAME").set(textureObjArray[texHash])
