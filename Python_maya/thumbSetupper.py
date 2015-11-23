import os
import sys
import maya.cmds as cmds
import pymel.core as pm

# ジョイント名格納用リスト

childNames = [];
jointName = "";

# 選択したジョイントの親の名を取得(最後の親子付けを戻す処理に必要ため)
jointName = cmds.ls(sl = True)
cmds.parent(world = True)
cmds.select(clear = True)

# 再度ジョイントを選択
cmds.select(jointName)
cmds.makeIdentity(apply = True, t = False, r = True, s =  False, n = False, pn = False, jointOrient = True)
cmds.select(clear = True)

# 子ジョイントの数を取得

cmds.select(jointName)
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
	cmds.select(childJointName)
	cmds.parent(world = True)
	
	strChildJointName = str(childJointName)
	splitedChildJointName = strChildJointName.split("'")[1]
	childJointFinalName = unicode(splitedChildJointName)

	# ジョイント名をchildNamesリストに追加	
	childNames.append(childJointFinalName)

	cmds.setAttr(childJointFinalName + u".jointOrientX", 0)
	cmds.setAttr(childJointFinalName + u".jointOrientY", 0)
	cmds.setAttr(childJointFinalName + u".jointOrientZ", 0)
	
cNum = 0;

for a in childNames:
	
	cmds.select(childNames[cNum])
	cmds.setAttr(childNames[cNum] + u".jointOrientY", -45)
	cmds.select(clear = True)
	cNum += 1;
	
cmds.setAttr(jointFinalName + u".jointOrientX", 0)
cmds.setAttr(jointFinalName + u".jointOrientY", 0)
cmds.setAttr(jointFinalName + u".jointOrientZ", 0)
	
cmds.setAttr(jointFinalName + u".rotateX", 0)
cmds.setAttr(jointFinalName + u".rotateY", -45)
cmds.setAttr(jointFinalName + u".rotateZ", 0)	

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
	

print(rootJointName)
cmds.select(jointName)
cmds.select(jointName)
