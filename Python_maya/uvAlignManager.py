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
		
	# �d���v�f�̍폜���\�b�h�@��list.set((a))�ł͏��Ԃ��ۑ�����Ȃ�����
	def getUniqueNumber(self, lis):
		r = []
		for a in lis:
			if not a in r:
				r.append(a)
		return r
				
		
	def getUVboundBox(self, *args):
		
		i = 0
		j = 0		
		k = 0
		l = 1
		m = 0
	
		objNames = []
		mapList = []
			
		tmpVtx = []
		tmpVtxList = []

		tmpVtxRange = []
		tmpVtxUnique = []

		mapNumbers = []		
		
		uvShell = []				
		self.uvShell1 = []

		sortedUniqueObjNames = []
		sortedVtxRange = []
		sortedVtxUnique = []
		
		mapUnique = []
		mapRange = []
				
		cmds.SelectUVBorder;
		mel.eval('polySelectBorderShell 1')
		tmpVtx = cmds.ls (sl = 1)
		#print tmpVerts

		# �I������ UVShell ���擾���� UVboundingBox ���X�g�ɒǉ�
		mel.eval('polySelectBorderShell 0');
		tmpVtx.extend(cmds.ls(sl = 1))

		# ������^�ɕϊ�
		for vtx in tmpVtx:
			unicode(vtx)
			finalVtx = str(vtx)
			tmpVtxList.append(finalVtx)
			
		print tmpVtxList
	
		# �擾���� map�� ���� �I�u�W�F�N�g�� �������擾�@
		for vtx in tmpVtxList:
			uvName = str(tmpVtxList[i])
			uvNameSplitted = uvName.split(".")		
			objNames.append(uvNameSplitted[0])

			i += 1	
			
		# ���X�g����d���v�f���폜
		sortedUniqueObjNames = self.getUniqueNumber(objNames)
		print "sortedUniqueObjNames:"
		print sortedUniqueObjNames
				
		# �擾�����I�u�W�F�N�g�� sortedUniqueObjNames �� tmpVtxList ���ƍ�
		for vtxName in tmpVtxList:
			vtxNameSplitted = vtxName.split(".")

			# vtxName �� objUniqueNames[j] �����v������ map ������ tmpVtxRange �Ɋi�[
			for vtxElement in sortedUniqueObjNames:
				if ":" in vtxNameSplitted[1] and vtxElement == vtxNameSplitted[0]:			
					tmpVtxRange.append(vtxNameSplitted[1])			

			# ���v���Ȃ���� �P�̂�vtx�Ȃ̂ŁAtmpVtxUnique �Ɋi�[
				if not ":" in vtxNameSplitted[1] and vtxElement == vtxNameSplitted[0]:	
					tmpVtxUnique.append(vtxNameSplitted[1])			

			j += 1
				
		# ���X�g����d���v�f���폜
		sortedVtxRange = self.getUniqueNumber(tmpVtxRange)
		print "sortedVtxRange:"
		print sortedVtxRange
				
		# ���X�g����d���v�f���폜
		sortedVtxUnique = self.getUniqueNumber(tmpVtxUnique)
		print "sortedVtxUnique:"
		print sortedVtxUnique
				
		# tmpVtxRange ���� ���������݂̂𒊏o						
		mapRange = re.findall("\d+",str(sortedVtxRange))
		print "mapRange:"
		print mapRange
		print "mapRange len:"
		loop = len(mapRange)/2
		print loop

		# tmpVtxUnique ���� ���������݂̂𒊏o						
		mapUnique = re.findall("\d+",str(sortedVtxUnique))
		print "mapUnique:"
		print mapUnique
		
		
		# tmpVtxRange �͈̔͂̐��l�� count �Ɏ擾
		count = 0
		w = 0
		while w < loop: 
			#print "mapRange[k] is:" 
			#print mapRange[k]
			#print "mapRange[l] is:" 
			#print mapRange[l]
			for var in range(int(mapRange[k]), int(mapRange[l])):
				count = var				
				mapNumbers.append(count)
				mapNumbers.append(count+1)
				#print "mapNumbers:"
				#print mapNumbers

				k += 2
				l += 2
				var += 1

			w += 1

		
		
		# objName �� mapNumbers ���� uvShell ���Ē�` 
		for map in mapNumbers:
			uvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')
		
		for map in mapUnique:
			uvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')			


	
		# Shell�P�ʂ�uv��I��

		for uv in uvShell:
			cmds.select(uv, add = True)
			self.uvShell1.append( uv )
		print self.uvShell1

		# boundingBox�̍��W���擾
		self.boundingBox(uvShell)
		
		
		tmpVtxList = []
		sortedUniqueObjNames = []
		sortedVtxRange = []
		sortedVtxUnique = []
		mapUnique = []
		mapNumbers = []
		mapRange = []


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
	
	



