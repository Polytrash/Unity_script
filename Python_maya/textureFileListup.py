import pymel.core as pm
import maya.cmds as cmds

i = 0
j = 0
k = 0
tex ={}

geo = pm.ls(sl=True)[0].getShape()
print geo
sg = geo.outputs(type='shadingEngine')
print sg


#↑と同じ結果を得る


list = cmds.ls( shapes=True )
print list
list.remove(u'frontShape')
list.remove(u'perspShape')
list.remove(u'sideShape')
list.remove(u'topShape')
print list






sg = list.outputs(type='shadingEngine')
print sg




for x in shape:


	print sg
	
	for a in sg:
		sgInfo = sg[i].connections(type='materialInfo')
		fileNode =sgInfo[0].connections(type='file')
		for b in fileNode:
			textureFile = pm.getAttr(fileNode[0].fileTextureName)		
			tex = str(''.join(textureFile))
			print tex
		i += 1
	
print b in tex:
	print tex[0]
