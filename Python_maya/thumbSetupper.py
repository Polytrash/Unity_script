import os
import sys
import maya.cmds as cmds
import pymel.core as pm

# ジョイント名格納用リスト

childNames = [];
rootJointName = "";

# 選択したジョイントの親の名を取得(最後の親子付けを戻す処理に必要ため)
jointName = cmds.ls(sl = True)
rootJointName = cmds.pickWalk(d = "up")
cmds.select(clear = True)

# 再度ジョイントを選択
cmds.select(jointName)
cmds.parent(world = True)


# 子ジョイントの数を取得
childCount = cmds.listRelatives( ad=True, type='joint', fullPath=False)
num = len(childCount)


strJointName = str(jointName)
splitedJointName = strJointName.split("'")[1]
jointFinalName = unicode(splitedJointName)

# ジョイント名をchildNamesリストに追加
childNames.append(jointFinalName)

jntOrientValX = cmds.getAttr(jointFinalName + u".jointOrientX")
jntOrientValY = cmds.getAttr(jointFinalName + u".jointOrientY")
jntOrientValZ = cmds.getAttr(jointFinalName + u".jointOrientZ")

print (u"[" + jointFinalName + u".jointOrient" + u"]")
print (u"X : " + unicode(jntOrientValX))
print (u"Y : " + unicode(jntOrientValY))
print (u"Z : " + unicode(jntOrientValZ))


for a in childCount:
	childJointName = cmds.pickWalk(d = "down")

	cmds.parent(world = True)
	
	strJointName = str(childJointName)
	splitedChildJointName = strJointName.split("'")[1]
	childJointFinalName = unicode(splitedChildJointName)

	# ジョイント名をchildNamesリストに追加	
	childNames.append(childJointFinalName)
	
	cmds.setAttr(childJointFinalName + u".jointOrientX", jntOrientValX)
	cmds.setAttr(childJointFinalName + u".jointOrientY", jntOrientValY)
	cmds.setAttr(childJointFinalName + u".jointOrientZ", jntOrientValZ)

i = -1
j = -2

for a in childNames:
	try:
		cmds.select(childNames[i])
		cmds.select(childNames[j], add = True)
		cmds.Parent(performParent = False)
		i -= 1
		j -= 1

	except:
		pass	
	
	cmds.select(clear = True)

cmds.select(childNames[0])
cmds.select(rootJointName, add = True)
cmds.Parent(performParent = False)





















