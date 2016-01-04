# -*- coding: utf-8 -*-


import maya.cmds as cmds
import pymel.core as pm
import re

class uvAlignManager(object):
#---------------------------------------
# 選択範囲内のバウンディングボックス座標を取得
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
		self.frameForm = cmds.frameLayout(label = " UVShell を登録します ", bgc = (0.3, 0.4, 0.1), cll = True)
		self.setUVSBtn1 = cmds.button(label = "UV1を登録"  , command = self.getUVboundBox, height = 30 )
		self.setUVSBtn2 = cmds.button(label = "UV2を登録" , height = 30 )
				
		cmds.columnLayout()
		cmds.setParent("..")	
		self.frameForm = cmds.frameLayout(label = " UVShell", bgc = (0.2, 0.3, 0.2), cll = False)		
		self.uvSetField = cmds.floatFieldGrp('uvsF', numberOfFields=2, label = u'UV座標', pre = 2, adj = True)
		
		self.distDcheckBox = cmds.radioButtonGrp('radioBtn', label = "", numberOfRadioButtons = 4 ,
							 sl = 1, cl4 = ['left','left','left','left'] , la4 = [ 'Right', 'Left', 'Top', 'Bottom'], adj = True)
		self.setButtonA = cmds.button(label = "実行" , height = 30 )		
		
		cmds.separator(width = self.width, style = 'in')
		
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left')	

		cmds.setParent("..")	
		cmds.showWindow()
		
	# 重複要素の削除メソッド　※list.set((a))では順番が保存されないため
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

		# 選択から UVShell を取得して UVboundingBox リストに追加
		mel.eval('polySelectBorderShell 0');
		tmpVtx.extend(cmds.ls(sl = 1))

		# 文字列型に変換
		for vtx in tmpVtx:
			unicode(vtx)
			finalVtx = str(vtx)
			tmpVtxList.append(finalVtx)
			
		print tmpVtxList
	
		# 取得した map名 から オブジェクト名 部分を取得　
		for vtx in tmpVtxList:
			uvName = str(tmpVtxList[i])
			uvNameSplitted = uvName.split(".")		
			objNames.append(uvNameSplitted[0])

			i += 1	
			
		# リストから重複要素を削除
		sortedUniqueObjNames = self.getUniqueNumber(objNames)
		print "sortedUniqueObjNames:"
		print sortedUniqueObjNames
				
		# 取得したオブジェクト名 sortedUniqueObjNames と tmpVtxList を照合
		for vtxName in tmpVtxList:
			vtxNameSplitted = vtxName.split(".")

			# vtxName と objUniqueNames[j] が合致したら map 部分を tmpVtxRange に格納
			for vtxElement in sortedUniqueObjNames:
				if ":" in vtxNameSplitted[1] and vtxElement == vtxNameSplitted[0]:			
					tmpVtxRange.append(vtxNameSplitted[1])			

			# 合致しなければ 単体のvtxなので、tmpVtxUnique に格納
				if not ":" in vtxNameSplitted[1] and vtxElement == vtxNameSplitted[0]:	
					tmpVtxUnique.append(vtxNameSplitted[1])			

			j += 1
				
		# リストから重複要素を削除
		sortedVtxRange = self.getUniqueNumber(tmpVtxRange)
		print "sortedVtxRange:"
		print sortedVtxRange
				
		# リストから重複要素を削除
		sortedVtxUnique = self.getUniqueNumber(tmpVtxUnique)
		print "sortedVtxUnique:"
		print sortedVtxUnique
				
		# tmpVtxRange から 数字部分のみを抽出						
		mapRange = re.findall("\d+",str(sortedVtxRange))
		print "mapRange:"
		print mapRange
		print "mapRange len:"
		loop = len(mapRange)/2
		print loop

		# tmpVtxUnique から 数字部分のみを抽出						
		mapUnique = re.findall("\d+",str(sortedVtxUnique))
		print "mapUnique:"
		print mapUnique
		
		
		# tmpVtxRange の範囲の数値を count に取得
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

		
		
		# objName と mapNumbers から uvShell を再定義 
		for map in mapNumbers:
			uvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')
		
		for map in mapUnique:
			uvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')			


	
		# Shell単位でuvを選択

		for uv in uvShell:
			cmds.select(uv, add = True)
			self.uvShell1.append( uv )
		print self.uvShell1

		# boundingBoxの座標を取得
		self.boundingBox(uvShell)
		
		
		tmpVtxList = []
		sortedUniqueObjNames = []
		sortedVtxRange = []
		sortedVtxUnique = []
		mapUnique = []
		mapNumbers = []
		mapRange = []


#---------------------------------------
# 選択範囲内のバウンディングボックス座標を取得
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

	# 頂点のUV座標を取得するが頂点ごとのU座標・.V座標順のListで返ってくる
		vtxList = cmds.polyEditUV(query = True)
		print vtxList
		
	# U座標だけのListを作る
		for a in vtxList:
			if i >= len(vtxList):
				break
			vtxUcoords.append(vtxList[i])
			i += 2
	
	# V座標だけのListを作る
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

	# UVシェル選択
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
	
	



