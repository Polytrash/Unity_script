# -*- coding: utf-8 -*-

"""
sm_modellib
���f�����O�֘A�̃��C�u����
"""# -*- coding: utf-8 -*-

#2016/3/31�ŏI�X�V

import maya.cmds as cmds
import pymel.core as pm
import re

class smUvShellAlignHelper:
#===========================================
# �I��͈͓��̃o�E���f�B���O�{�b�N�X���W���擾
#===========================================

	def __init__(self):

		self.window = 'uvShellAlignWindow';
		self.title = 'UVShell Align Window';
		self.size = (400, 150)
		self.height = 150
		self.width = 400

		self.uvShell1 = []
		self.uvShell2 = []	
		
		self.uvBndBox1 = []
		self.uvBndBox2 = []

						
	def create(self):
		if cmds.window('uvShellAlignWindow', exists = True):
			cmds.deleteUI('uvShellAlignWindow')

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
		self.frameForm = cmds.frameLayout(label = " 1. ��Ƃ��� UVShell ��I�����ēo�^", bgc = (0.5, 0.3, 0.2), cll = False)
		self.setUVSBtn1 = cmds.button(label = "��@UVShell ��o�^"  , command = self.registUVBndBox1, height = 30 )
		cmds.rowLayout( numberOfColumns = 1, adj = True)					

				




		cmds.setParent("..")			
		self.frameForm = cmds.frameLayout(label = " 2. �ʒu�𑵂����� UVShell ��I�����Ď��s", bgc = (0.2, 0.3, 0.5), cll = False)
		self.distDcheckBox = cmds.radioButtonGrp('radioBtn', label = "", numberOfRadioButtons = 4 ,
							 sl = 1, cl4 = ['left','left','left','left'] , la4 = [ 'Left', 'Right', 'Bottom', 'Top'], adj = True)

		self.backupPathText = cmds.text("�� 2016/1/5 ���݁A����UV��I��������Ԃł̈ʒu�����ɂ͑Ή����Ă��܂���", font = "smallBoldLabelFont", align = 'left');
		self.setUVSBtn2 = cmds.button(label = "�I�������@UVShell�@�𑵂���" , command = self.registUVBndBox2, height = 30 )
		cmds.setParent("..")	
		
		cmds.separator(width = self.width, style = 'in')
		
		cmds.text("�y�₢���킹��z �F TA�Z�N�V����.����", bgc = (0.2, 0.2, 0.2), align = 'left', width = self.width);

		cmds.setParent("..")	
		cmds.showWindow()


			

	# UV�o�E���f�B���O�{�b�N�X1 �ւ̓o�^
	def registUVBndBox1(self, *args):
		self.getUVcoordinate(1)     
		self.uvBndBox1 = self.getUVboundingBox(self.uvShell1)
		print self.uvBndBox1

		
	# UV�o�E���f�B���O�{�b�N�X2 �ւ̓o�^ �� �ړ��̎��s		
	def registUVBndBox2(self, *args):
		self.getUVcoordinate(0)        
		self.uvBndBox2 = self.getUVboundingBox(self.uvShell2)	
	
		print self.uvBndBox2	
		
		selected = cmds.radioButtonGrp('radioBtn', query = True, select = True)
		
		# ���W�I�{�^�����Q�Ƃ��Ĉʒu���킹��ύX(���W�I�{�^���� 1 �n�܂�Ȃ̂Œ���!)	
		if selected == 1:	# �����킹
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 0)		
			
		elif selected == 2:	# �E���킹
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 1)		
			
 		elif selected == 3:	# �����킹
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 2)		
			       
		elif selected == 4:	# �㍇�킹
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 3)		
			
		else:
			print "���W�I�{�^�����͂��s���ł�"
			pass  
	

					    		
	# �d���v�f�̍폜���\�b�h�@��list.set((a))�ł͏��Ԃ��ۑ�����Ȃ�����
	def getUniqueNumber(self, lis):
		r = []
		for a in lis:
			if not a in r:
				r.append(a)
		return r
		
	
#===========================================
# UV���W�ړ�
#===========================================		    
	def uvAlign(self, uv1, uv2, num):
	    
		if num == 0: # �����킹
			cmds.polyEditUV (u = (uv1[0] - uv2[0]), v = 0)
			print num
		elif num == 1: # �E���킹
			cmds.polyEditUV (u = (uv1[1] - uv2[1]), v = 0)   
			print num    	
		elif num == 2: # �����킹
			cmds.polyEditUV (u = 0, v = (uv1[2] - uv2[2]))      
		elif num == 3: # �㍇�킹
			cmds.polyEditUV (u = 0, v = (uv1[3] - uv2[3]))  
		else:
			print "�s���Ȓl�ł�"
			pass    
    
#===========================================
# UV���W�擾
#===========================================				

	def getUVcoordinate(self, num):
		
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
		
		localUvShell = []				
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
			
		#print tmpVtxList
	
		# �擾���� map�� ���� �I�u�W�F�N�g�� �������擾�@
		for vtx in tmpVtxList:
			uvName = str(tmpVtxList[i])
			uvNameSplitted = uvName.split(".")		
			objNames.append(uvNameSplitted[0])

			i += 1	
			
		# ���X�g����d���v�f���폜
		sortedUniqueObjNames = self.getUniqueNumber(objNames)

				
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
				
		# vtxRange ���X�g����d���v�f���폜
		sortedVtxRange = self.getUniqueNumber(tmpVtxRange)	
		# vtxRange ���X�g �̗v�f�� �� 2 �Ō�̃��[�v�����擾���Ă���
		loop = len(mapRange)/2	
		
		# vtxUnique ���X�g����d���v�f���폜
		sortedVtxUnique = self.getUniqueNumber(tmpVtxUnique)

				
		# tmpVtxRange ���� ���������݂̂𒊏o						
		mapRange = re.findall("\d+",str(sortedVtxRange))
		# tmpVtxUnique ���� ���������݂̂𒊏o						
		mapUnique = re.findall("\d+",str(sortedVtxUnique))
		
		
		# tmpVtxRange �͈̔͂̐��l�� count �Ɏ擾
		count = 0
		a = 0
		b = 1
		for x in range(0, loop):
			for y in range(int(mapRange[a]), int(mapRange[b])+1):
				count = y		    
				mapNumbers.append(count)
				count += 1

			a += 2
			b += 2

		
		# objName �� mapNumbers ���� localUvShell ���Ē�` 
		for map in mapNumbers:
			localUvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')
		# objName �� mapUnique ���� localUvShell ���Ē�` 		
		for map in mapUnique:
			localUvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')			


	
		# Shell�P�ʂ�uv��I���A ����num �Ŕ��f���� self.uvShell 1 or 2 �ǂ��炩�ɒl���i�[

		for uv in localUvShell:
			cmds.select(uv, add = True)
			
			if num == 1:			
				self.uvShell1.append( uv )
				#print self.uvShell1
			else:
				self.uvShell2.append( uv )			    			    			
				#print self.uvShell2

	
		tmpVtxList = []
		sortedUniqueObjNames = []
		sortedVtxRange = []
		sortedVtxUnique = []
		mapUnique = []
		mapNumbers = []
		mapRange = []


#===========================================
# �I��͈͓��̃o�E���f�B���O�{�b�N�X���W���擾
#===========================================

	def getUVboundingBox(self, uvShell):

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
		
		minMax = []

	# ���_��UV���W���擾���邪���_���Ƃ�U���W�E.V���W����List�ŕԂ��Ă���
		vtxList = cmds.polyEditUV(query = True)
		#print vtxList
		
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

		print "�y UV MinMax��� �z"
		print 'Umin is : ' + str(ucoordsMin)
		print 'Umax is : ' + str(ucoordsMax)
		print 'Vmin is : ' + str(vcoordsMin)
		print 'Vmax is : ' + str(vcoordsMax)

		A[0:2] = [ucoordsMin, vcoordsMin]
		B[0:2] = [ucoordsMax, vcoordsMin]
		C[0:2] = [ucoordsMax, vcoordsMax]
		D[0:2] = [ucoordsMin, vcoordsMax]
		
		print "�y�@UV BoundingBox��� �z"
		print 'A : ' + str(A)
		print 'B : ' + str(B)
		print 'C : ' + str(C)
		print 'D : ' + str(D)
		
		minMax.append(ucoordsMin)
		minMax.append(ucoordsMax)
		minMax.append(vcoordsMin)
		minMax.append(vcoordsMax)				        

	# UV�V�F���I��
		mel.eval('polySelectBorderShell 0');
       
		return minMax

smUvShellAlignHelperWindow = smUvShellAlignHelper()
smUvShellAlignHelperWindow.create()
