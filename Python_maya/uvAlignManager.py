# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import re

class uvAlignManager(object):
#---------------------------------------
# �I��͈͓��̃o�E���f�B���O�{�b�N�X���W���擾
#---------------------------------------

	def __init__(self):

		self.window = 'uvShellAlignWindow';
		self.title = 'UVShell Align Window';
		self.size = (320, 150)
		self.height = 150
		self.width = 320

		self.uvShell1 = []
		self.uvShell2 = []
		self.uvShell3 = []
	
	def create(self):
		if cmds.window('uvShellAlignWindow', exists = True):
			cmds.deleteUI('uvShellAlignWindow')

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
		self.frameForm = cmds.frameLayout(label = " UVShell ��o�^���܂� ", bgc = (0.3, 0.4, 0.1), cll = True)
		self.setUVSBtn1 = cmds.button(label = "UV1��o�^"  , command = self.getUVboundBox, height = 30 )
		self.setUVSBtn2 = cmds.button(label = "UV2��o�^" , height = 30 )
				
		cmds.columnLayout()
		cmds.setParent("..")	
		self.frameForm = cmds.frameLayout(label = " UVShell", bgc = (0.2, 0.3, 0.2), cll = False)		
		self.uvSetField = cmds.floatFieldGrp('uvsF', numberOfFields=2, label = u'UV���W', pre = 2, adj = True)
		
		self.distDcheckBox = cmds.radioButtonGrp('radioBtn', label = "", numberOfRadioButtons = 4 ,
							 sl = 1, cl4 = ['left','left','left','left'] , la4 = [ 'Right', 'Left', 'Top', 'Bottom'], adj = True)
		self.setButtonA = cmds.button(label = "���s" , height = 30 )		
		
		cmds.separator(width = self.width, style = 'in')
		
		cmds.text("�y�₢���킹��z", bgc = (0.2, 0.2, 0.2), align = 'left')	

		cmds.setParent("..")	
		cmds.showWindow()
		
	
	# �I������ UVborder ���擾

	def getUVboundBox(self, *args):
		
		i = 0
		j = 0
		
		objName = []
		mapList = []
		mapNumbers = ""
		tmpVerts = []
		tmpVertsUnique = []

		tmpList = []	
		uvShell = []
		
		cmds.SelectUVBorder;
		mel.eval('polySelectBorderShell 1')
		tmpVerts = cmds.ls (sl = 1)
		#print tmpVerts

		# �I������ UVShell ���擾���� UVborder���X�g�ɒǉ�
		mel.eval('polySelectBorderShell 0');
		tmpVerts.extend(cmds.ls(sl = 1))

		# ������^�ɕϊ�
		for tmp in tmpVerts:
			unicode(tmp)
			finalTmp = str(tmp)
			tmpList.append(finalTmp)
	
		#print tmpList

		# ���X�g����d���v�f���폜
		tmpVertsUnique = list(set(tmpList))

		# UVShell
		#print tmpVertsUnique


		# �I������ UVvertex �ɕϊ�
		tmpVerts = cmds.ls (sl = 1)
		uvs = cmds.polyListComponentConversion (tmpVerts, tuv = True )
		#print uvs

		for uv in uvs:
			uvName = str(uvs[i])
			uvNameSplitted = uvName.split(".")
			objName.append(uvNameSplitted[0])
			mapList.append(uvNameSplitted[1])
			i += 1

		i = 0

		# re.findall �Ő����������擾
		mapNumbers = re.findall("\d+",str(mapList))

		# objName �� mapNumbers ���� uvShell ���Ē�` 
		for map in mapNumbers:
			uvShell.append( str(objName[0]) + '.map[' + str(mapNumbers[j]) + ']')
			j += 1
	
			#print uvShell
		
		j = 0
	
		# Shell�P�ʂ�uv��I��
		for uv in uvShell:
			cmds.select(uv, add = True)
			self.uvShell1.append( uv )
			print self.uvShell1

		# boundingBox�̍��W���擾
		#self.boundingBox(uvShell)



#---------------------------------------
# �I��͈͓��̃o�E���f�B���O�{�b�N�X���W���擾
#---------------------------------------

	def boundingBox(self, uvShell):

		cmds.ConvertSelectionToUVs;
		mel.eval('PolySelectConvert 4')

		i = 0
		j = 1

		vtxUcoords = []
		vtxVcoords = []

		ucoordsMin = 0
		ucoordsMax = 0
		vcoordsMin = 0
		vcoordsMax = 0

		A = []
		B = []
		C = []
		D = []

	# ���_��UV���W���擾���邪���_���Ƃ�U���W�E.V���W����List�ŕԂ��Ă���
		vtxList = cmds.polyEditUV(query = True)
		print vtxList
		
	# U���W������List�����
		for a in vtxList:
			if i >= len(vtxList):
				break
			vtxUcoords.append(vtxList[i])
			i += 2
	
	# V���W������List�����
		for a in vtxList:
			if j >= len(vtxList):
				break
			vtxVcoords.append(vtxList[j])
			j += 2
	
		vtxUcoords.sort()
		vtxVcoords.sort()

		ucoordsMin = vtxUcoords[0]
		ucoordsMax = vtxUcoords[-1]

		vcoordsMin = vtxVcoords[0]
		vcoordsMax = vtxVcoords[-1]

		A[0:2] = [ucoordsMin, vcoordsMin]
		B[0:2] = [ucoordsMax, vcoordsMin]
		C[0:2] = [ucoordsMax, vcoordsMax]
		D[0:2] = [ucoordsMin, vcoordsMax]

	# UV�V�F���I��
		mel.eval('polySelectBorderShell 0');

	#cmds.polyEditUV( u = ucoordsMax, v = vcoordsMax )

		print vtxUcoords
		print vtxVcoords

		print 'Umin is : ' + str(ucoordsMin)
		print 'Umax is : ' + str(ucoordsMax)
		print 'Vmin is : ' + str(vcoordsMin)
		print 'Vmax is : ' + str(vcoordsMax)

		print 'A : ' + str(A)
		print 'B : ' + str(B)
		print 'C : ' + str(C)
		print 'D : ' + str(D)


	def alignTop(C, vtxList):
		a = 1;
	
	
	

uvAlignWindow = uvAlignManager()
uvAlignWindow.create()
	
	



