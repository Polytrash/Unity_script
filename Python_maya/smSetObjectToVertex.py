import re
import os
import sys
import math
import maya.cmds as cmds
import pymel.core as pm


class smSetObjToVerts(object):
	
# �W���C���g���i�[�p���X�g
	def __init__(self):
		self.window = 'smSetObjToVertsWindow';
		self.title = 'Set Objects for Verts Window';
		self.size = (320, 150);
		self.width = 320;
		self.height = 50;
		
		# �I�u�W�F�N�g��
		self.objNameA = ''
		self.objNameB = ''
		self.objDplcNameList = []
		
		# �I�u�W�F�N�g��񃊃X�g / �t�F�[�X���X�g / �t�F�[�X�����X�g / �t�F�[�X�@�����X�g
		self.rawList = []
		self.faceList = []
		self.faceNum = []
		self.faceCount = 0
		self.faceNrmlList = []

		# ���_���X�g / ���_�� /  ���_�ԍ����X�g / ���_�ʒu / ���_�@�� 
		self.vrtsList = []
		self.vrtsCount = 0
		self.vrtsNum = []
		self.vrtsPos = []

				
		# �O���[�o���J�E���^�[
		self.counter = 0

		# XYZ�U�蕪���p���_���W���X�g
		self.vrtsPosListX = []
		self.vrtsPosListY = []
		self.vrtsPosListZ = []

		# XYZ�U�蕪���p���_�@�����X�g
		self.vrtsNorList = []



	def create(self):
		if cmds.window('smSetObjToVertsWindow', exists = True):
			cmds.deleteUI('smSetObjToVertsWindow' );

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);	
		self.frameForm = cmds.frameLayout(label = u" 1. �z�u��̃I�u�W�F�N�g��I�����Ă��������B", bgc = (0.3, 0.4, 0.1), cll = False);
		self.executeButton = cmds.button(label = u"�I��" , command = self.getFaceList, height = 30 );
		self.columForm = cmds.columnLayout();	
		cmds.setParent("..")
		self.frameForm = cmds.frameLayout(label = u" 2. �z�u����I�u�W�F�N�g��I�����Ă��������B", bgc = (0.3, 0.4, 0.1), cll = False);
		self.offsetF = cmds.floatFieldGrp('offsetF', numberOfFields=3, v1 = 0, v2 = 0, v3 = 0, label = u'�I�t�Z�b�g�l', adj = True)
		self.columForm = cmds.columnLayout();	
		cmds.setParent("..")

		self.executeButton = cmds.button(label = u"�z�u" , command = self.setObjectsToVerts, height = 30 );
		
		cmds.text("�y�₢���킹��z", bgc = (0.2, 0.2, 0.2), align = 'left')
		cmds.setParent("..")	

		cmds.showWindow()		
	
		
#===================================
#	���C�����\�b�h	(+�z�u����擾)
#===================================
		
	def getFaceList(self, *args):

		self.clearList()
		# �z�u��I�u�W�F�N�g�����擾
		self.getObjName("A")
		
		self.rawList = cmds.polyInfo( fv=True )
		print(self.rawList)
		self.getVrtsInfo()

		
#===================================
#	���X�g�N���A���\�b�h	(+�z�u����擾)
#===================================
	
	def clearList(self, *args):
		
		del self.objDplcNameList[:]
		
		# �I�u�W�F�N�g��񃊃X�g / �t�F�[�X���X�g / �t�F�[�X�@�����X�g
		del self.rawList[:]
		del self.faceList[:]
		del self.faceNrmlList[:]
		
		del self.vrtsPosListX[:]
		del self.vrtsPosListY[:]
		del self.vrtsPosListZ[:]

		del self.vrtsNorList[:]


#===================================
#	�I�u�W�F�N�g���Q�b�^�[	
#===================================

	def getObjName(self, AB, *args):
		
		if AB == "A" :
			self.objNameA = str(cmds.ls(sl = True, type = 'transform')).split("'")[1]	
			# ���_���擾
			self.vrtsCount = cmds.polyEvaluate(v = True)
		elif AB == "B" :
			self.objNameB = str(cmds.ls(sl = True, type = 'transform')).split("'")[1]
		else :
			print "error"
			
#===================================
#	�I�u�W�F�N�g���Z�b�^�[	
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
#	���_���擾���\�b�h	
#===================================

	def getVrtsInfo(self, *args):
		
		i = 0
		
		# �t�F�[�X�̏d�S�����߂��Ȃ����߁A�����͌��ݖ��g�p
		for num in self.rawList :
			self.faceList.append(str(self.objNameA + '.f[' + str(re.findall("\d+",str(num))).split("'")[1] + ']'))
			self.faceNrmlList = re.findall("\d+\.\d+",str(cmds.polyInfo(fn = True)))

		cmds.select(cl = True)
		
		# ���̂܂ܒ��_�����擾
		self.getVtxNum()
		

#===================================
#	���_���W�擾���\�b�h	
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
#	���_���WXYZ�U�蕪�����\�b�h	
#===================================
		
	def setVrtsPos(self, vtxPosX, vtxPosY, vtxPosZ, *args):
								
			self.vrtsPosListX.append(vtxPosX)

			self.vrtsPosListY.append(vtxPosY)	

			self.vrtsPosListZ.append(vtxPosZ)


			
#===================================
#	�I�u�W�F�N�g�z�u���\�b�h	
#===================================

	def setObjectsToVerts(self, *args):
		
		# �z�u�I�u�W�F�N�g�����擾
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