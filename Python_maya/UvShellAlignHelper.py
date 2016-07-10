# -*- coding: utf-8 -*-

"""
sm_modellib
モデリング関連のライブラリ
"""# -*- coding: utf-8 -*-

#2016/3/31最終更新

import maya.cmds as cmds
import pymel.core as pm
import re

class smUvShellAlignHelper:
#===========================================
# 選択範囲内のバウンディングボックス座標を取得
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
		self.frameForm = cmds.frameLayout(label = " 1. 基準とする UVShell を選択して登録", bgc = (0.5, 0.3, 0.2), cll = False)
		self.setUVSBtn1 = cmds.button(label = "基準　UVShell を登録"  , command = self.registUVBndBox1, height = 30 )
		cmds.rowLayout( numberOfColumns = 1, adj = True)					

				




		cmds.setParent("..")			
		self.frameForm = cmds.frameLayout(label = " 2. 位置を揃えたい UVShell を選択して実行", bgc = (0.2, 0.3, 0.5), cll = False)
		self.distDcheckBox = cmds.radioButtonGrp('radioBtn', label = "", numberOfRadioButtons = 4 ,
							 sl = 1, cl4 = ['left','left','left','left'] , la4 = [ 'Left', 'Right', 'Bottom', 'Top'], adj = True)

		self.backupPathText = cmds.text("※ 2016/1/5 現在、複数UVを選択した状態での位置揃えには対応していません", font = "smallBoldLabelFont", align = 'left');
		self.setUVSBtn2 = cmds.button(label = "選択した　UVShell　を揃える" , command = self.registUVBndBox2, height = 30 )
		cmds.setParent("..")	
		
		cmds.separator(width = self.width, style = 'in')
		
		cmds.text("【問い合わせ先】 ： TAセクション.村岡", bgc = (0.2, 0.2, 0.2), align = 'left', width = self.width);

		cmds.setParent("..")	
		cmds.showWindow()


			

	# UVバウンディングボックス1 への登録
	def registUVBndBox1(self, *args):
		self.getUVcoordinate(1)     
		self.uvBndBox1 = self.getUVboundingBox(self.uvShell1)
		print self.uvBndBox1

		
	# UVバウンディングボックス2 への登録 と 移動の実行		
	def registUVBndBox2(self, *args):
		self.getUVcoordinate(0)        
		self.uvBndBox2 = self.getUVboundingBox(self.uvShell2)	
	
		print self.uvBndBox2	
		
		selected = cmds.radioButtonGrp('radioBtn', query = True, select = True)
		
		# ラジオボタンを参照して位置合わせを変更(ラジオボタンは 1 始まりなので注意!)	
		if selected == 1:	# 左合わせ
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 0)		
			
		elif selected == 2:	# 右合わせ
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 1)		
			
 		elif selected == 3:	# 下合わせ
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 2)		
			       
		elif selected == 4:	# 上合わせ
			self.uvAlign(self.uvBndBox1, self.uvBndBox2, 3)		
			
		else:
			print "ラジオボタン入力が不正です"
			pass  
	

					    		
	# 重複要素の削除メソッド　※list.set((a))では順番が保存されないため
	def getUniqueNumber(self, lis):
		r = []
		for a in lis:
			if not a in r:
				r.append(a)
		return r
		
	
#===========================================
# UV座標移動
#===========================================		    
	def uvAlign(self, uv1, uv2, num):
	    
		if num == 0: # 左合わせ
			cmds.polyEditUV (u = (uv1[0] - uv2[0]), v = 0)
			print num
		elif num == 1: # 右合わせ
			cmds.polyEditUV (u = (uv1[1] - uv2[1]), v = 0)   
			print num    	
		elif num == 2: # 下合わせ
			cmds.polyEditUV (u = 0, v = (uv1[2] - uv2[2]))      
		elif num == 3: # 上合わせ
			cmds.polyEditUV (u = 0, v = (uv1[3] - uv2[3]))  
		else:
			print "不正な値です"
			pass    
    
#===========================================
# UV座標取得
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

		# 選択から UVShell を取得して UVboundingBox リストに追加
		mel.eval('polySelectBorderShell 0');
		tmpVtx.extend(cmds.ls(sl = 1))

		# 文字列型に変換
		for vtx in tmpVtx:
			unicode(vtx)
			finalVtx = str(vtx)
			tmpVtxList.append(finalVtx)
			
		#print tmpVtxList
	
		# 取得した map名 から オブジェクト名 部分を取得　
		for vtx in tmpVtxList:
			uvName = str(tmpVtxList[i])
			uvNameSplitted = uvName.split(".")		
			objNames.append(uvNameSplitted[0])

			i += 1	
			
		# リストから重複要素を削除
		sortedUniqueObjNames = self.getUniqueNumber(objNames)

				
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
				
		# vtxRange リストから重複要素を削除
		sortedVtxRange = self.getUniqueNumber(tmpVtxRange)	
		# vtxRange リスト の要素数 ÷ 2 で後のループ数を取得しておく
		loop = len(mapRange)/2	
		
		# vtxUnique リストから重複要素を削除
		sortedVtxUnique = self.getUniqueNumber(tmpVtxUnique)

				
		# tmpVtxRange から 数字部分のみを抽出						
		mapRange = re.findall("\d+",str(sortedVtxRange))
		# tmpVtxUnique から 数字部分のみを抽出						
		mapUnique = re.findall("\d+",str(sortedVtxUnique))
		
		
		# tmpVtxRange の範囲の数値を count に取得
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

		
		# objName と mapNumbers から localUvShell を再定義 
		for map in mapNumbers:
			localUvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')
		# objName と mapUnique から localUvShell を再定義 		
		for map in mapUnique:
			localUvShell.append( str(sortedUniqueObjNames[0]) + '.map[' + str(map) + ']')			


	
		# Shell単位でuvを選択、 引数num で判断して self.uvShell 1 or 2 どちらかに値を格納

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
# 選択範囲内のバウンディングボックス座標を取得
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

	# 頂点のUV座標を取得するが頂点ごとのU座標・.V座標順のListで返ってくる
		vtxList = cmds.polyEditUV(query = True)
		#print vtxList
		
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

		print "【 UV MinMax情報 】"
		print 'Umin is : ' + str(ucoordsMin)
		print 'Umax is : ' + str(ucoordsMax)
		print 'Vmin is : ' + str(vcoordsMin)
		print 'Vmax is : ' + str(vcoordsMax)

		A[0:2] = [ucoordsMin, vcoordsMin]
		B[0:2] = [ucoordsMax, vcoordsMin]
		C[0:2] = [ucoordsMax, vcoordsMax]
		D[0:2] = [ucoordsMin, vcoordsMax]
		
		print "【　UV BoundingBox情報 】"
		print 'A : ' + str(A)
		print 'B : ' + str(B)
		print 'C : ' + str(C)
		print 'D : ' + str(D)
		
		minMax.append(ucoordsMin)
		minMax.append(ucoordsMax)
		minMax.append(vcoordsMin)
		minMax.append(vcoordsMax)				        

	# UVシェル選択
		mel.eval('polySelectBorderShell 0');
       
		return minMax

smUvShellAlignHelperWindow = smUvShellAlignHelper()
smUvShellAlignHelperWindow.create()
