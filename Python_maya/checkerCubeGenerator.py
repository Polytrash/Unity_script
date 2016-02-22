import os
import sys
import maya.cmds as cmds
import pymel.core as pm

class checkCubeGenerator(object):
	
# ジョイント名格納用リスト
	def __init__(self):
		self.window = 'checkCubeGenerateWindow';
		self.title = 'Check Cube Generate Window';
		self.size = (320, 150);
		self.width = 320;
		self.height = 50;
		
		self.cubeNumX = 1;
		self.cubeNumZ = 1;

# GUIメソッドの宣言
	
	def create(self):
		if cmds.window('checkCubeGenerateWindow', exists = True):
			cmds.deleteUI('checkCubeGenerateWindow' );

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		self.divIntF = cmds.intFieldGrp('divIntF', numberOfFields=3, v1 = 1, v2 = 1, v3 = 1, label = u'分割数', adj = True)
		self.numIntF = cmds.intFieldGrp('numIntF', numberOfFields=2, v1 = 1, v2 = 1, label = u'オブジェクト数',  adj = True)		
		self.frameForm = cmds.frameLayout(label = " Checker 用 Cube を作成します。", bgc = (0.3, 0.4, 0.1), cll = False);
		self.columForm = cmds.columnLayout();	
		cmds.setParent("..")
		self.executeButton = cmds.button(label = "実行" , command = self.createCube, height = 30 );

		
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left');	
		cmds.setParent("..")	

		cmds.showWindow();

# ジョイントオリエントメソッドの実行

	def createCube(self, *args):
		
		i = 0
		j = 0
		k = 1
		posX = 0
		
		cubeStock = []
		dupCubeStock = []
		
		self.cubeNumX = self.numX_input()
		self.cubeNumZ = self.numZ_input()
				
		while i < self.cubeNumX :	
		
			cmds.polyCube( w = 10, h = 10, d = 10, sx = self.divX_input(), sy = self.divY_input(), sz = self.divZ_input(), ax = (0, 1, 0), cuv = 4, ch = 1)

			cmds.move(15 * i, 0, 0)
			
			self.cubeName = str(cmds.pickWalk(d = "up"))
			self.splittedCubeName = self.cubeName.split("'")[1]
			self.cubeFinalName = unicode(self.splittedCubeName)
			print("cubeFinalName : " + self.cubeFinalName)
			cubeStock.append(self.cubeFinalName)
			
			i += 1
			
		while j < self.cubeNumZ :			
			posX = cmds.getAttr(str(cubeStock[j]) + ".translateX")
			cmds.select(cubeStock[j], r = True)
			dup = cmds.duplicate(cubeStock[j])
			cmds.move(posX, 0, 15 * k)	
			j += 1
			k += 1


	def divX_input(self):	
		self.divXval = cmds.intFieldGrp("divIntF", query = True, v1 = True);	
		return self.divXval; 	

	def divY_input(self):	
		self.divYval = cmds.intFieldGrp("divIntF", query = True, v2 = True);	
		return self.divYval; 	
		
	def divZ_input(self):	
		self.divZval = cmds.intFieldGrp("divIntF", query = True, v3 = True);	
		return self.divZval;
		
	def numX_input(self):	
		self.numXval = cmds.intFieldGrp("numIntF", query = True, v1 = True);	
		return self.numXval;
		
	def numZ_input(self):	
		self.numZval = cmds.intFieldGrp("numIntF", query = True, v2 = True);	
		return self.numZval;					
		 					
ccgWindow = checkCubeGenerator()
ccgWindow.create()