import pymel.core as pm
import maya.cmds as cmds
import math

class simpleMeasureTool(object):
#selection = cmds.ls(sl=True)
#objPos = cmds.getAttr(".translateX") 
#print objPos
	def __init__(self):
		self.window = 'simpleMeasureToolWindow';
		self.title = 'Simple Measure Tool Window';
		
		self.size = (360, 420);
		self.width = 360;
		self.height = 420;
		
		self.buttonApressed = False	
		self.buttonBpressed = False	
					
		self.meshCheckA = True
		self.meshCheckB = True
		
		self.genDistD = False
		
		self.posA = []
		self.posB = []
			
						

	
	def create(self):
		if cmds.window('simpleMeasureToolWindow', exists = True):
			cmds.deleteUI('simpleMeasureToolWindow')

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
		self.frameForm = cmds.frameLayout(label = " A - B　間の距離を計測します ", bgc = (0.3, 0.4, 0.1), cll = True)
		self.distDcheckBox = cmds.checkBox('chckD', label = "計測位置にメジャーツールを作成します", edit = False, value = False, onCommand = self.setGendistDT)

		
		cmds.columnLayout()
		cmds.setParent("..")	
		cmds.rowColumnLayout()	
		cmds.setParent("..")	
		self.frameForm = cmds.frameLayout(label = " A地点", bgc = (0.2, 0.3, 0.2), cll = False)		
		self.posFieldA = cmds.floatFieldGrp('posFA', numberOfFields=3, label = u'A点', pre = 3, adj = True)
		self.setButtonA = cmds.button(label = "セットA" , command = self.setPositionA, height = 30 )
		self.frameForm = cmds.frameLayout(label = " B地点", bgc = (0.2, 0.3, 0.2), cll = False)		
		self.posFieldB = cmds.floatFieldGrp('posFB', numberOfFields=3, label = u'B点', pre = 3, adj = True)
		self.setButtonB = cmds.button(label = "セットB" , command = self.setPositionB, height = 30 )
				

		
		cmds.separator(width = self.width, style = 'in')
		self.distField = cmds.floatFieldGrp('distF',numberOfFields=1, label = u'A - B 間の距離',extraLabel='cm', pre = 3, adj = True)		
		self.executeButton = cmds.button(label = "計測" , command = self.measurementPosition, height = 30 )

		
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left')	

		cmds.setParent("..")	
		cmds.showWindow()


	def setGendistDT(self, *args):
		self.genDistD = True


	def setGendistDF(self, *args):
		self.genDistD = False

	def setNameA(self, name):
		self.posFieldA = cmds.floatFieldGrp('posFA', edit = True, label = name)	

	def setNameB(self, name):
		self.posFieldA = cmds.floatFieldGrp('posFB', edit = True, label = name)		
		
		
	def setPosFA(self, pos):
		self.posFieldA = cmds.floatFieldGrp('posFA', edit = True, value1 = pos[0], value2 = pos[1], value3 = pos[2])	
		self.posA = pos
	
	def setPosFB(self, pos):
		self.posFieldB = cmds.floatFieldGrp('posFB', edit = True, value1 = pos[0], value2 = pos[1], value3 = pos[2])	
		self.posB = pos


	def generateDistanceDimension(self, posA, posB):	
		cmds.distanceDimension(sp = (self.posA[0], self.posA[1], self.posA[2]), ep = (self.posB[0], self.posB[1], self.posB[2]))


	def getUnicode(self, selection):
		uniSelection = unicode(selection)
		output = uniSelection.split("'")[1]	
		print output
		return output



	def setPositionA(self, *args):
		
		self.buttonApressed = True
		selection = cmds.ls(sl=True)
		print(selection)
		selectionName =	self.getUnicode(selection)
		print(selectionName)
		self.setNameA(selectionName)

		
		self.selectCheckerA(selectionName)
		if self.meshCheckA == True:
			self.getObjPos(selectionName)
		else:			
			self.getVtxPos(selectionName)			
		self.buttonApressed = False	

	
	
	def setPositionB(self, *args):
		
		self.buttonBpressed = True
		selection = cmds.ls(sl=True)
		selectionName =	self.getUnicode(selection)
		print(selectionName)		
		self.setNameB(selectionName)

		
		self.selectCheckerB(selectionName)	
		if self.meshCheckB == True:
			self.getObjPos(selectionName)
		else:			
			self.getVtxPos(selectionName)	
		self.buttonBpressed = False			
				
				
				
	def selectCheckerA(self, selection):
		if cmds.objectType(selection) == u'mesh':
			print "this is mesh"
			self.meshCheckA = False
		else:
			print "this is transform"
			self.meshCheckA = True

	
	
	def selectCheckerB(self, selection):
		if cmds.objectType(selection) == u'mesh':
			print "this is mesh"
			self.meshCheckB = False
		else:
			print "this is transform"
			self.meshCheckB = True
		
			
	def getVtxPos(self, selection):
		i = 0
		pos = []
		print "getVtxPos"
		print selection
		vtxPos = cmds.pointPosition(selection)
		for a in vtxPos:
			pos.append(a)
			print pos
			i += 1
		
		if 	self.buttonApressed == True	:
			self.setPosFA(pos)
		else:
			self.setPosFB(pos)
		return pos



	def getObjPos(self, selection):
		pos = []
		print "getObjPos"
		pos.append(cmds.getAttr(selection + u'.translateX'))
		pos.append(cmds.getAttr(selection + u'.translateY'))
		pos.append(cmds.getAttr(selection + u'.translateZ'))
		print pos		
		if 	self.buttonApressed == True	:
			self.setPosFA(pos)
		else:
			self.setPosFB(pos)	
		return pos



	def measurementPosition(self, *args):
		dx = self.posA[0] - self.posB[0]
		dy = self.posA[1] - self.posB[1]
		dz = self.posA[2] - self.posB[2]
		distance = math.sqrt( dx*dx + dy*dy + dz*dz )
		print distance
		self.distField = cmds.floatFieldGrp('distF', edit = True, value1 = distance)
		if self.genDistD == True:
			self.generateDistanceDimension(self.posA, self.posB)
			self.genDistD == False
		
simpleMesurToolWindow = simpleMeasureTool()
simpleMesurToolWindow.create()



	
