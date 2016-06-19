# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as et

import xml.dom as minidom


class objectPlacement(object):


    def __init__(self):

        self.window = 'objectTransformExporterWindow'
        self.title = 'Object Transform Exporter'
        self.size = (300, 300)
        self.height = 300
        self.width = 300
        
        self.dirPath = u"D:\\Unity\\Projects\\Photoreal_SEGA\\Assets"
        self.searchInput =''
      

        self.objNameList = []
        self.transform = []


    def create(self):

        if cmds.window('objectTransformExporterWindow', exists = True):
            cmds.deleteUI('objectTransformExporterWindow')

        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.frameFrm1 = cmds.frameLayout(label = u"1.トランスフォームを書き出すオブジェクトを選択", bgc = (0.5, 0.25, 0.3), cll = True)

        self.srchBtn = cmds.button( l = u"リストに追加", command = self.nameSearch, height = 30 )
        
        self.textScllist = cmds.textScrollList('objL', ams = True, dkc = self.removeAt)
        cmds.separator (h = 10, w = self.width, style = 'in') 


        cmds.setParent('..')       
                
        self.frameFrm2 = cmds.frameLayout(label = u"2.XMLファイルで書き出し", bgc = (0.5, 0.25, 0.3), cll = True)

        self.rowForm =	cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)])
        self.exportPathText = cmds.text(u"パスの指定", font = 'smallBoldLabelFont', align = 'left')


        try:
            self.pathText = cmds.textField(self.chosenPath, editable =False);
        except:
            self.pathText = cmds.textField(text = self.exportPath, editable =False)  

        self.chosenButton = cmds.button(label = u"参照" , command = self.chosenPath)
        

        cmds.setParent('..')    

        self.exportFileNameText = cmds.text(u"ファイル名", font = 'smallBoldLabelFont', align = 'left')          
        self.fileNameFld = cmds.textField('fileNameF')

        self.getPosBtn = cmds.button(l = u"書き出し",command = self.getTransform, height = 30)


        cmds.setParent('..')

        cmds.showWindow()

#===================================================================================
# 汎用メソッドの定義
#===================================================================================

    
#===================================================================================
# フォルダ参照メソッドの定義
#===================================================================================

    def chosenPath(self, *args):
        try:
            dialogText = cmds.fileDialog2(fm=3, ds=2, cap= 'Open', okc = u"選択")
            uniToStr=str(dialogText)
            filePath = uniToStr.split("'")[1]
        except Exception:
            print(u" Info: Folder Reference Error: Tool <Object Transform Exporter>")			
        else:					
            fPath = cmds.textField(self.pathText, edit=True, text=unicode(filePath))
            global	userPath 
            userPath = filePath
            print('current userPath -> ' + userPath)	
            	
#===================================================================================
# ユーザー入力メソッドの定義	
#===================================================================================


    def nameSearch(self, *args):

        i = 0
        selection = []

        if(cmds.ls(selection = True)):


            selection = cmds.ls(selection = True, tr = True)
            exist = cmp(self.objNameList, selection)
            print(selection)
            print(self.objNameList)

            for a in selection:

                if selection[i] in self.objNameList:
        
                    print("Already exist in the list.") 
                
                else:

                    self.objNameList.append(selection[i])
                    cmds.textScrollList(self.textScllist, e = True , append = selection[i])
                i += 1


        #print(self.objNameList)


    def removeAt(self, *args):

        i = 0

        delItem = cmds.textScrollList(self.textScllist, q = True , si = True)
        
        for a in delItem:

            if delItem[i] in self.objNameList:

                self.objNameList.remove(delItem[i])
                cmds.textScrollList(self.textScllist, e = True , removeItem = delItem[i])
            i += 1

#===================================================================================
# トランスフォーム取得		
#=================================================================================== 


    def getTransform(self, *args):

        i = 0

        # XML 書き出し

        UserData = Element('UserData')


        for a in self.objNameList:

            print self.objNameList[i]        

            cmds.select(self.objNameList[i], replace = True)

            pos = cmds.xform(q = True, ws = True, t = True)
            rot = cmds.xform(q = True, ws = True, ro = True)
            scl = cmds.xform(q = True, ws = True, s = True)

            print(pos)
            print(rot)
            print(scl)

            self.exportData(UserData, pos, rot, scl,  self.objNameList[i])

            i += 1

        tree = et.ElementTree(UserData)
        
        sourceWorkspaceName = self.exportPathText.replace("/", "\\")
        tree.write( u"D:\\Unity\\Projects\\Photoreal_SEGA\\Assets\\PlacementData.xml", xml_declaration=True, encoding='utf-8', method="xml")
        
        print tostring(UserData)



#===================================================================================
# トランスフォーム書き出し	
#===================================================================================        
    

    def exportData( self, UserData, pos, rot, scl, name,  *args):

        nameXpos = name + 'xPos';
        nameYpos = name + 'yPos';
        nameZpos = name + 'zPos';

        nameXrot = name + 'xRot';
        nameYrot = name + 'yRot';
        nameZrot = name + 'zRot';
                
        nameXscl = name + 'xScl';
        nameYscl = name + 'yScl';
        nameZscl = name + 'zScl';

        iUser = SubElement(UserData, '_iUser')

        # オブジェクト名
        
        objname = SubElement(iUser, 'name')

        # 移動値

        xPos = SubElement(iUser, nameXpos)
        xPos.text = str(pos[0] * -1)

        yPos = SubElement(iUser, nameYpos)
        yPos.text = str(pos[1])

        zPos = SubElement(iUser, nameZpos)
        zPos.text = str(pos[2])

        # 回転値

        xRot = SubElement(iUser, nameXrot)
        xRot.text = str(rot[0])
        
        yRot = SubElement(iUser, nameYrot)
        yRot.text = str(rot[1])

        zRot = SubElement(iUser, nameZrot)
        zRot.text = str(rot[2])

        # スケール値

        xScl = SubElement(iUser, nameXscl)
        xScl.text = str(scl[0])

        yScl = SubElement(iUser, nameYscl)
        yScl.text = str(scl[1])

        zScl = SubElement(iUser, nameZscl)
        zScl.text = str(scl[2])
               


        objname.text = str(name)

   




objectPlacer = objectPlacement()

objectPlacer.create()