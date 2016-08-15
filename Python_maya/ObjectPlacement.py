# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
import string as st
import re
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, XML
import xml.etree.ElementTree as et

import xml.dom as minidom


class objectPlacement(object):


    def __init__(self):

        self.window = 'objectTransformExporterWindow'
        self.title = 'Object Transform Exporter'
        self.size = (300, 300)
        self.height = 300
        self.width = 300
        
        self.dirPath = ""
        self.filePath = ""
        self.searchInput =''
      
        # 書き出し用
        self.exportObjNameList = []
        self.transform = []

        # 読み込み用
        self.importObjCount = 0
        self.importObjNameList = []
        self.objPosition = []
        self.objRotation = []
        self.objScale = []

    def create(self):

        if cmds.window('objectTransformExporterWindow', exists = True):
            cmds.deleteUI('objectTransformExporterWindow')

#===================================================================================
# GUIの定義
#===================================================================================

#-----------------------------------------------------------------------------------
# 1.トランスフォームを書き出すオブジェクトを選択
#-----------------------------------------------------------------------------------  


        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.frameFrm1 = cmds.frameLayout(label = u"1.トランスフォームを書き出すオブジェクトを選択", bgc = (0.5, 0.25, 0.3), cll = True)

        self.srchBtn = cmds.button( l = u"リストに追加", command = self.nameSearch, height = 30 )
        
        self.textScllist = cmds.textScrollList('objL', ams = True, dkc = self.removeAt)


        cmds.checkBox(l = u"リスト内オブジェクトの Rotate Order を Unity仕様(ZXY) に変更", onCommand = self.rotateOrderZXY, offCommand = self.rotateOrderXYZ, rs = True)

        cmds.separator (h = 10, w = self.width, style = 'in') 


        cmds.setParent('..')     

#-----------------------------------------------------------------------------------
# 2.XMLファイルを書き出す
#-----------------------------------------------------------------------------------  
                      
        self.frameFrm2 = cmds.frameLayout(label = u"2.XMLファイルを書き出す", bgc = (0.5, 0.25, 0.3), cll = True)

        self.rowForm1 =	cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)])
        self.exportPathText = cmds.text(u"パスの指定", font = 'smallBoldLabelFont', align = 'left')


        try:
            self.pathText1 = cmds.textField(self.chosenPath, editable =False);
        except:
            self.pathText1 = cmds.textField(text = self.exportPath, editable =False)  

        self.chosenButton1 = cmds.button(label = u"参照" , command = self.chosenPath)
        

        cmds.setParent('..')    

        self.exportFileNameText = cmds.text(u"ファイル名", font = 'smallBoldLabelFont', align = 'left')          
        self.fileNameFld = cmds.textField('fileNameF1')

        self.exportXmlBtn = cmds.button(l = u"書き出し",command = self.getTransform, height = 30)


#-----------------------------------------------------------------------------------
# 3.XMLファイルを読み込む
#-----------------------------------------------------------------------------------

        self.frameFrm3 = cmds.frameLayout(label = u"3.XMLファイルを読み込む", bgc = (0.5, 0.25, 0.3), cll = True)

        self.rowForm2 =	cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)])
        self.importPathText = cmds.text(u"ファイルの指定", font = 'smallBoldLabelFont', align = 'left')


        try:
            self.pathText2 = cmds.textField(self.chosenPath, editable =False);
        except:
            self.pathText2 = cmds.textField(text = self.exportPath, editable =False)  

        self.chosenButton2 = cmds.button(label = u"参照" , command = self.chosenFile)


        cmds.setParent('..')

        self.importXmlBtn = cmds.button(l = u"読み込み/更新",command = self.setTransform, height = 30)

        
        cmds.setParent('..')


        cmds.showWindow()

#===================================================================================
# 汎用メソッドの定義
#===================================================================================
     
#-----------------------------------------------------------------------------------
# XMLエラーチェック	
#----------------------------------------------------------------------------------- 

    def errorCheck(self, key, val, *args):

        if not val:
            print ("XMLファイルに" + str(key) + " の " + str(val) + " 値が入っていません")

        elif val == '':
            print ("XMLファイルに" + str(key) + " の " + str(val) + " 値が入っていません")
        else:
            return val  

#-----------------------------------------------------------------------------------
# オブジェクトタイプチェック	
#----------------------------------------------------------------------------------- 

    def typeCheck(self, name, *args):

        # name がjointでないかチェック
        type = cmds.objectType(name, isType = u"joint")



        if type == True:

            print("Info: " + name + " is joint, therefore which could not add to the list.")
            return type
        else:

            # name のシェイプを取得してさらにチェック
            shape = cmds.listRelatives(name, s = True, path = True)
            shapeInfo = cmds.objectType(shape)

            
        if shapeInfo == 'camera':
            print("Info: " + name + " is camera, therefore which could not add to the list.")
            type = True
            return type

        elif shapeInfo == 'nurbsCurve':
            print("Info: " + name + " is nurbsCurve, therefore which could not add to the list.")
            type = True
            return type

        else:
            type = False
            return type

#===================================================================================
# Rotate Order を XYZ に変更
#===================================================================================

    def rotateOrderXYZ(self, *args):
        
        for a in self.exportObjNameList:

            name = str(a)

            cmds.setAttr(name + ".rotateOrder", 0)


#===================================================================================
# Rotate Order を ZXY に変更
#===================================================================================

    def rotateOrderZXY(self, *args):
        
        for a in self.exportObjNameList:

            name = str(a)

            cmds.setAttr(name + ".rotateOrder", 2)


    
#===================================================================================
# 書き出しフォルダ参照メソッドの定義
#===================================================================================

    def chosenPath(self, *args):
        try:
            dialogText = cmds.fileDialog2(fm=3, ds=2, cap= 'Open', okc = u"選択")
            uniToStr = str(dialogText)
            dirPath = uniToStr.split("'")[1]
        except Exception:
            print(u" Info: Export Folder Reference Error: Tool <Object Transform Exporter> 142")			
        else:					
            fPath = cmds.textField(self.pathText1, edit=True, text=unicode(dirPath))
            self.dirPath = dirPath
            print('current userPath -> ' + self.dirPath)	
 

#===================================================================================
# 読み込みファイル参照メソッドの定義
#===================================================================================

    def chosenFile(self, *args):
        try:
            dialogText = cmds.fileDialog2(fm=4, ds=2, cap= 'Open', okc = u"選択")
            uniToStr=str(dialogText)
            filePath = uniToStr.split("'")[1]
        except Exception:
            print(u" Info: Import File Reference Error: Tool <Object Transform Exporter> 159")			
        else:					
            fPath = cmds.textField(self.pathText2, edit=True, text=unicode(filePath))
            self.filePath = filePath
            print('current userFile -> ' + self.filePath)            
            
                                  	
#===================================================================================
# ユーザー入力メソッドの定義	
#===================================================================================

    def nameSearch(self, *args):

        i = 0
        selection = []

        if(cmds.ls(selection = True)):


            selection = cmds.ls(selection = True, tr = True)
            exist = cmp(self.exportObjNameList, selection)
            print(selection)
            print(self.exportObjNameList)

            for a in selection:

                if selection[i] in self.exportObjNameList:
        
                    print("Info: "+ selection[i] + "is exist in the list already.") 
                
                else:

                    type = self.typeCheck(selection[i])

                    if type == False:

                        self.exportObjNameList.append(selection[i])
                        cmds.textScrollList(self.textScllist, e = True , append = selection[i])

                    else:

                        print("")
                i += 1


        #print(self.exportObjNameList)


    def removeAt(self, *args):

        i = 0

        delItem = cmds.textScrollList(self.textScllist, q = True , si = True)
        
        for a in delItem:

            if delItem[i] in self.exportObjNameList:

                self.exportObjNameList.remove(delItem[i])
                cmds.textScrollList(self.textScllist, e = True , removeItem = delItem[i])
            i += 1


#===================================================================================
# ゲットトランスフォーム(書き出しに使用)	
#=================================================================================== 

    def getTransform(self, *args):


        # 書き出し先パスの取得

        dirPath = self.dirPath
        
        sourceWorkspaceName = dirPath.replace("/", "\\\\") + "\\\\"
        
        fileName = cmds.textField('fileNameF1', query =True, text = True)
        
        exportXml = sourceWorkspaceName + fileName + ".xml"

        print exportXml



        # XML 書き出し

        root = Element('UserData')

        root.set('version', '1.0')
        root.append(Comment('Generated at :'))
        

        tree = et.ElementTree(root)

        # オブジェクト名からトランスフォーム取得

        i = 0

        for a in self.exportObjNameList:

            print self.exportObjNameList[i]        

            cmds.select(self.exportObjNameList[i], replace = True)

            pos = cmds.xform(q = True, ws = True, t = True)
            rot = cmds.xform(q = True, ws = True, ro = True)
            scl = cmds.xform(q = True, ws = True, s = True)

            print(pos)
            print(rot)
            print(scl)

            try:
                self.exportData(root, pos, rot, scl,  self.exportObjNameList[i])
            except Exception:
                print(u" Info: Data Export Error: Tool <Object Transform Exporter> 266")	

            i += 1
        

        uExportXml = unicode(exportXml)

        tree.write( uExportXml, xml_declaration=True, encoding='utf-8', method="xml")
               
        print tostring(root)


#===================================================================================
# トランスフォーム書き出し
#=================================================================================== 

    def exportData(self, root, pos, rot, scl, name, *args):
        
        nameXpos = name + 'xPos'
        nameYpos = name + 'yPos'
        nameZpos = name + 'zPos'

        nameXrot = name + 'xRot'
        nameYrot = name + 'yRot'
        nameZrot = name + 'zRot'

        nameXscl = name + 'xScl'
        nameYscl = name + 'xScl'
        nameZscl = name + 'zScl'


        # オブジェクト名
        object = SubElement(root, 'object', id = name)
        position = SubElement(object, 'position')
        rotation = SubElement(object, 'rotation')
        scale = SubElement(object, 'scale')

        # 移動値        
        for p in object.iter('position'):

            p.set('X', str(pos[0]))
            p.set('Y', str(pos[1]))
            p.set('Z', str(pos[2]))

        # 回転値
        for r in object.iter('rotation'):

            r.set('X', str(rot[0]))
            r.set('Y', str(rot[1]))
            r.set('Z', str(rot[2]))
            
        # スケール値
        for s in object.iter('scale'):

            s.set('X', str(scl[0]))
            s.set('Y', str(scl[1]))
            s.set('Z', str(scl[2]))
                    

#===================================================================================
# セットトランスフォーム(読み込みに使用)
#===================================================================================    

    def setTransform(self, *args):

        filePath = self.filePath
        sourceFileName = filePath.replace("/", "\\")
        print sourceFileName

        # XMLオブジェクト作成
        tree = et.parse(sourceFileName)
        root = tree.getroot()

        # XMLの情報をグローバルリストにそれぞれ格納
        for object in root.iter('object'):
            self.importObjNameList.append(object.attrib)

                           
            for position in object.iter('position'):
                self.objPosition.append(position.attrib)


            for rotation in object.iter('rotation'):
                self.objRotation.append(rotation.attrib)


            for scale in object.iter('scale'):
                self.objScale.append(scale.attrib)


        # 読み込み情報の確認用プリント
        print "Imported Data List:"
        print ( self.importObjNameList)
        print ( self.objPosition)
        print ( self.objRotation)
        print ( self.objScale)

   
        #トランスフォーム実行
        self.transformObject()
        
#===================================================================================
# オブジェクト複製	
#===================================================================================   

    def duplicateObject(self, objName, *args):

        targetName = self.checkDigit(str(objName))
        print(str(targetName))
        # ベースオブジェクトを選択
        cmds.select(str(targetName), r = True)
        
        # 複製しXMLと合致しなかった名前にリネーム
        cmds.duplicate(n = objName, rr = True)

#===================================================================================
#  文字列に含まれる数字を削除
#=================================================================================== 

    def checkDigit(self, objName, *args):

        numbers = '';
        
        for c in objName:

            if re.match('^[0-9]{1,}$', c):
                numbers += c;

        replacedName = str(objName).replace(str(numbers), '')

        return replacedName


   
#===================================================================================
# トランスフォーム実行	
#===================================================================================    

    def transformObject(self, *args):
        
        positionList = {}
        rotationList = {}
        scaleList = {}
        i = 0      

        cmds.select(cl = True)

        for n in self.importObjNameList:

            n = str(n['id'])
                       
          
            # グローバルリストの各値をローカル辞書に格納                     
            positionList = self.objPosition[i]
            rotationList = self.objRotation[i]
            scaleList = self.objScale[i]
            
            # 位置(キーでオブジェクトを検索)
            xPos = positionList["X"]
            yPos = positionList["Y"]
            zPos = positionList["Z"]

            # 回転(キーでオブジェクトを検索)
            xRot = rotationList["X"]
            yRot = rotationList["Y"]
            zRot = rotationList["Z"]

            # スケール(キーでオブジェクトを検索)
            xScl = scaleList["X"]
            yScl = scaleList["Y"]
            zScl = scaleList["Z"]

            # トランスフォーム情報プリント
            print "-----------------------------------------------------------------------"
            print ("Name : " + n)
            print ("Position: ")
            print ("X : " + xPos + " Y : " + yPos + " Z : " + zPos)
            print ("Rotation: ")
            print ("X : " + xRot + " Y : " + yRot + " Z : " + zRot)
            print ("Scale: ")
            print ("X : " + xScl + " Y : " + yScl + " Z : " + zScl)
            print "-----------------------------------------------------------------------"

            # トランスフォーム実行

            existsOrNot = cmds.objExists(str(n))


            if (existsOrNot == True):

                cmds.select(str(n), r = True)

                # Rotate Order を ZXY に変更
                cmds.setAttr(str(n) + ".rotateOrder", 2)

                cmds.xform(a = True, ws = True, ro = [float(xRot), float(yRot), float(zRot)], s = [float(xScl), float(yScl), float(zScl)], t = [float(xPos), float(yPos), float(zPos)])
            
            else :

                print(u" Info: Value is Empty, therefore Transition to duplicate phase...")

                try :
                    # XMLと合致しなかったのオブジェクトをベースオブジェクトから複製
                    self.duplicateObject(str(n))

                    cmds.select(str(n), r = True)

                    # Rotate Order を ZXY に変更
                    cmds.setAttr(str(n) + ".rotateOrder", 2)

                    cmds.xform(a = True, ws = True, ro = [float(xRot), float(yRot), float(zRot)], s = [float(xScl), float(yScl), float(zScl)], t = [float(xPos), float(yPos), float(zPos)])


                except:
                    print(u" Info: duplicate Error: Tool <Object Transform Exporter> 402")

            # ローカル辞書をクリア
            positionList.clear()
            rotationList.clear()
            scaleList.clear()

            i +=1

        # 次の読み込みに備えてグローバルリストの値をクリア
        del self.importObjNameList[:]
        del self.objPosition[:]
        del self.objRotation[:]
        del self.objScale [:] 
        
          
                 

objectPlacer = objectPlacement()

objectPlacer.create()