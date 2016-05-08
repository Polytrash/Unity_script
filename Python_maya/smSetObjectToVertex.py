import re
import os
import sys
import math
import maya.cmds as cmds
import pymel.core as pm


class smSetObjToVerts(object):
	
# ジョイント名格納用リスト
	def __init__(self):
		self.window = 'smSetObjToVertsWindow';
		self.title = 'Set Objects for Verts Window';
		self.size = (320, 150);
		self.width = 320;
		self.height = 50;
		
		# オブジェクト名
		self.objNameA = ''
		self.objNameB = ''
		self.objDplcNameList = []
		
		# オブジェクト情報リスト / フェースリスト / フェース数リスト / フェース法線リスト
		self.rawList = []
		self.faceList = []
		self.faceNum = []
		self.faceCount = 0
		self.faceNrmlList = []

		# 頂点リスト / 頂点数 /  頂点番号リスト / 頂点位置 / 頂点法線 
		self.vrtsList = []
		self.vrtsCount = 0
		self.vrtsNum = []
		self.vrtsPos = []

				
		# グローバルカウンター
		self.counter = 0

		# XYZ振り分け用頂点座標リスト
		self.vrtsPosListX = []
		self.vrtsPosListY = []
		self.vrtsPosListZ = []

		# XYZ振り分け用頂点法線リスト
		self.vrtsNorList = []



	def create(self):
		if cmds.window('smSetObjToVertsWindow', exists = True):
			cmds.deleteUI('smSetObjToVertsWindow' );

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);	
		self.frameForm = cmds.frameLayout(label = u" 1. 配置先のオブジェクトを選択してください。", bgc = (0.3, 0.4, 0.1), cll = False);
		self.executeButton = cmds.button(label = u"選択" , command = self.getFaceList, height = 30 );
		self.columForm = cmds.columnLayout();	
		cmds.setParent("..")
		self.frameForm = cmds.frameLayout(label = u" 2. 配置するオブジェクトを選択してください。", bgc = (0.3, 0.4, 0.1), cll = False);
		self.offsetF = cmds.floatFieldGrp('offsetF', numberOfFields=3, v1 = 0, v2 = 0, v3 = 0, label = u'オフセット値', adj = True)
		self.columForm = cmds.columnLayout();	
		cmds.setParent("..")

		self.executeButton = cmds.button(label = u"配置" , command = self.setObjectsToVerts, height = 30 );
		
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left')
		cmds.setParent("..")	

		cmds.showWindow()		
	
		
#===================================
#	メインメソッド	(+配置先情報取得)
#===================================
		
	def getFaceList(self, *args):

		self.clearList()
		# 配置先オブジェクト名を取得
		self.getObjName("A")
		
		self.rawList = cmds.polyInfo( fv=True )
		print(self.rawList)
		self.getVrtsInfo()

		
#===================================
#	リストクリアメソッド	(+配置先情報取得)
#===================================
	
	def clearList(self, *args):
		
		del self.objDplcNameList[:]
		
		# オブジェクト情報リスト / フェースリスト / フェース法線リスト
		del self.rawList[:]
		del self.faceList[:]
		del self.faceNrmlList[:]
		
		del self.vrtsPosListX[:]
		del self.vrtsPosListY[:]
		del self.vrtsPosListZ[:]

		del self.vrtsNorList[:]


#===================================
#	オブジェクト名ゲッター	
#===================================

	def getObjName(self, AB, *args):
		
		if AB == "A" :
			self.objNameA = str(cmds.ls(sl = True, type = 'transform')).split("'")[1]	
			# 頂点数取得
			self.vrtsCount = cmds.polyEvaluate(v = True)
		elif AB == "B" :
			self.objNameB = str(cmds.ls(sl = True, type = 'transform')).split("'")[1]
		else :
			print "error"
			
#===================================
#	オブジェクト名セッター	
#===================================

	def setObjName(self, AB, *args):
		
		objName
		
		if AB == "A" :
			objName = self.objNameA 
		elif AB == "B" :
			objName = self.objNameB 
		else :
			print "error"
						
		return objName

#===================================
#	頂点情報取得メソッド	
#===================================

	def getVrtsInfo(self, *args):
		
		i = 0
		
		# フェースの重心が求められないため、ここは現在未使用
		for num in self.rawList :
			self.faceList.append(str(self.objNameA + '.f[' + str(re.findall("\d+",str(num))).split("'")[1] + ']'))
			self.faceNrmlList = re.findall("\d+\.\d+",str(cmds.polyInfo(fn = True)))

		cmds.select(cl = True)
		
		# そのまま頂点情報を取得
		self.getVtxNum()
		

#===================================
#	頂点座標取得メソッド	
#===================================

	def getVtxNum(self, *args):
		
		i = 0
		j = 0
		
		while i < self.vrtsCount:
	
			cmds.select(self.objNameA + '.f[' + str(i) + ']')			
			self.vrtsList.append(re.findall("\d+",str(cmds.polyInfo(fv = True))))
			self.vrtsPos = cmds.xform(self.objNameA + '.vtx[' + str(i) + ']', q=True, ws=True, t=True)
			self.setVrtsPos(self.vrtsPos[0], self.vrtsPos[1], self.vrtsPos[2])
			
			print("vrtsPos[" + str(i) + "]")
			print(self.vrtsPos)	

			i += 1	

		cmds.select(cl = True)
										
				
#===================================
#	頂点座標XYZ振り分けメソッド	
#===================================
		
	def setVrtsPos(self, vtxPosX, vtxPosY, vtxPosZ, *args):
								
			self.vrtsPosListX.append(vtxPosX)

			self.vrtsPosListY.append(vtxPosY)	

			self.vrtsPosListZ.append(vtxPosZ)


			
#===================================
#	オブジェクト配置メソッド	
#===================================

	def setObjectsToVerts(self, *args):
		
		# 配置オブジェクト名を取得
		self.getObjName("B")
		
		offsetX = cmds.floatFieldGrp("offsetF", query = True, v1 = True);
		offsetY = cmds.floatFieldGrp("offsetF", query = True, v2 = True);
		offsetZ = cmds.floatFieldGrp("offsetF", query = True, v3 = True);
		
		counterA = 0
		counterB = 0

		cmds.xform(self.objNameB, piv = (offsetX, offsetY, offsetZ), r = True)		
		
		while counterA < len(self.vrtsPosListX):
	
			cmds.select(self.objNameB, r = True)	
			self.objDplcNameList.append(cmds.duplicate(rr = True))
			cmds.move (self.vrtsPosListX[counterA], self.vrtsPosListY[counterA], self.vrtsPosListZ[counterA])
				
			cmds.select(self.objNameA, r = True)
			cmds.select(self.objDplcNameList[counterA], add = True)	

			cmds.geometryConstraint(w = 1.0);
			cmds.normalConstraint (weight = 1, aimVector = (0.0, 1.0, 0.0), upVector = (0.0, 1.0, 0.0), worldUpType = "scene");
			counterA += 1
		cmds.select(cl = True)
		
		for a in self.objDplcNameList:
			cmds.select(self.objDplcNameList[counterB], add = True)
			counterB += 1
			print ("counterB")
			print (counterB)
		cmds.group()

smSetObjToVertsWindow = smSetObjToVerts()
smSetObjToVertsWindow.create()