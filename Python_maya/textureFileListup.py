import pymel.core as pm
import maya.cmds as cmds

i = 0
j = 0
k = 0

geo = pm.ls(sl=True)[0].getShape()

sg = geo.outputs(type='shadingEngine')
print sg

for a in sg:
	sgInfo = sg[i].connections(type='materialInfo')
	print 'sg:', sgInfo
	i += 1
	
for b in sgInfo:
	fileNode =sgInfo[j].connections(type='file')
	print 'sgInfo:', sgInfo
	j += 1

for c in fileNode:
	textureFile = pm.getAttr(fileNode[k].fileTextureName)
	print 'textureFile:', str(textureFile)
	k += 1

result = cmds.distanceDimension( sp=(0, 2, 2), ep=(1, 5, 6) )
print result