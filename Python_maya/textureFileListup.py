import pymel.core as pm
import maya.cmds as cmds

class simpleMeasureTool(object):
#selection = cmds.ls(sl=True)
#objPos = cmds.getAttr(".translateX") 
#print objPos
	def __init__(self):
		self.window = 'simpleMeasureToolWindow';
		self.title = 'Simple Measure Tool Window';
		
		self.size = (320, 150);
		self.width = 320;
		self.height = 50;
		
		self.meshCheckA = True
		self.meshCheckB = True
			
						
		vtxPosA = []
		vtxPosB = []
		objPosA = []
		objPosB = []
	
	def create(self):
		if cmds.window('simpleMeasureToolWindow', exists = True):
			cmds.deleteUI('simpleMeasureToolWindow' )

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
		self.frameForm = cmds.frameLayout(label = " ëŒè€ÇÃãóó£Çåvë™ÇµÇ‹Ç∑", bgc = (0.3, 0.4, 0.1), cll = False)
		
		cmds.columnLayout()
		self.posAField = cmds.floatFieldGrp('posAF', numberOfFields=3, label='PositionA', extraLabel='cm', value1 = 0, value2 = 0, value3 = 0 )
		self.posBField = cmds.floatFieldGrp('posBF', numberOfFields=3, label='PositionB', extraLabel='cm', value1 = 0, value2 = 0, value3 = 0 )
		cmds.setParent("..")		
		self.executeButton = cmds.button(label = "åvë™" , command = self.measurementPosition, height = 30 )

		
		cmds.text("Åyñ‚Ç¢çáÇÌÇπêÊÅz", bgc = (0.2, 0.2, 0.2), align = 'left')	

		cmds.setParent("..")	

		cmds.showWindow()

	

	def setVtxPosA(self, pos):
		vtxPosA = pos
	
	def setVtxPosB(self, pos):
		vtxPosB = pos

		
	def setObjPosA(self, pos):
		vtxPosA = pos
		
	def setObjPosB(self, pos):
		vtxPosB = pos	



	def setPositionA(self, *args):
		
		self.selectCheckerA()
		
		if self.meshCheck == True:
			getObjPos()
		else:			
			getVtxPos()
	
	def selectCheckerA(self, selection):
		if cmds.objectType(selection) == u'mesh':
			print "this is mesh"
			self.meshCheckA = True
		else:
			print "this is transform"
			self.meshCheckA = False
	
	
	
	def selectCheckerB(self, selection):
		if cmds.objectType(selection) == u'mesh':
			print "this is mesh"
			self.meshCheckB = True
		else:
			print "this is transform"
			self.meshCheckB = False
			
			

	def getVtxPos(self, *args):
		i = 0
		selection = cmds.ls(sl=True)
		vtxPos = cmds.pointPosition(selection)
		for a in vtxPos:
			vtxPosA.append(a)
			print vtxPosA
			i += 1

		self.posAField = cmds.floatFieldGrp(query = True, value1 = vtxPosA[0], value2 = vtxPosA[1], value3 = vtxPosA[2])	
	
		return vtxPosA



	def getObjPos(self, *args):
		pos = []
		selection = cmds.ls(sl=True)
		pos.append(cmds.getAttr(".translateX"))
		pos.append(cmds.getAttr(".translateY"))
		pos.append(cmds.getAttr(".translateZ"))
		print pos	
		return pos


	def measurementPosition(self,  PosA, PosB ):
		dx = posA[0] - posB[0]
		dy = posA[1] - posB[1]
		dz = posA[2] - posB[2]
		return math.sqrt( dx*dx + dy*dy + dz*dz )

testWindow = simpleMeasureTool()
testWindow.create()



	
import pymel.core as pm
import maya.cmds as cmds

allFilePath = {}
uniqueFilePath = []
finalFilePath = []


for transform in transforms:
	transforms = pm.ls(type="transform")
	shape = transform.getShape()
	shadingEngine = shape.outputs(type='shadingEngine')
	if not shadingEngine:
		pass	
	else:
		print transform
		print shadingEngine
		for materialInfo in shadingEngine:
			shadingEngineInfo = materialInfo.connections(type = 'materialInfo')
			
			for fileNode in shadingEngineInfo:
				fileNames = fileNode.connections(type = 'file')
				
				for files in fileNames:
					textureFiles = pm.getAttr(files.fileTextureName)
					print textureFiles
					allFilePath[i] = textureFiles
					i += 1
				

allFileList = allFilePath.values()

for x in allFileList:
    if x not in uniqueFilePath:
        uniqueFilePath.append(x)
        
print ""
print uniqueFilePath
print ""

for y in uniqueFilePath:
	output = y.replace("/", "\\")	
	print output
 
