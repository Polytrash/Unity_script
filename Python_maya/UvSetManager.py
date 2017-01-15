# -*- coding: utf-8 -*-

#2017/1/15最終更新

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import re

class UVSetManager(object):
    
    def __init__(self):
        self.window = 'UVSetManagerWindow'
        self.title = 'UV Set Manager'
        self.size = (250, 350)

        self.width = 250
        self.height = 350  
                          
        self.transforms = [] 
        self.selectItem = ''
        self.uvs = []
        self.uvName = ''
        self.copyUvName = ''     
        self.getAllGeom    
                     
    def create(self, *args):
        if cmds.window('UVSetManagerWindow', exists = True):
            cmds.deleteUI('UVSetManagerWindow')
            
        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.frameFrm1 = cmds.frameLayout(label = u"UV Set　を編集します", bgc = (0.1, 0.2, 0.3))

        self.meshBtn = cmds.button( l = u"メッシュ取得", command = self.getAllGeom, height = 30 )     
        cmds.text(u"■ Mesh", bgc = (0.1, 0.2, 0.2), align = 'left', width = self.width)        
        self.objScllist = cmds.textScrollList('objL', ams = True, sc = self.getAllUVSets)
        
        cmds.separator (h = 10, w = self.width, style = 'in')    
             
        cmds.text(u"■ UV : [ダブルクリック : UVEditor起動]\n            [Delete / BackSpace : UVSet削除]", bgc = (0.2, 0.1, 0.2), align = 'left', width = self.width)

        self.uvScllist = cmds.textScrollList('uvL', ams = True, sc = self.getUVName, dkc = self.deleteUVSet, dcc = self.openTextureWindow)           
        c = cmds.columnLayout(adjustableColumn=True)



                     
        self.renameBtn = cmds.button( l = u"選択 UVSet をコピーして新規作成", command = self.doGetCopyUVName )      
        cmds.formLayout(nch = True)             
        cmds.rowColumnLayout(nc = 3)
        cmds.text(label='UVSet 名 : ')       
        self.uvNameFld = cmds.textField( 'uvNameF', )         
        self.renameBtn = cmds.button( l = u"リネーム", command = self.uvNameChange )  
        cmds.setParent('..')     
        cmds.setParent('..')              
 
        cmds.setParent('..')               
        cmds.setParent('..')                 
        cmds.setParent('..')  
  
        cmds.showWindow()  

        
                
#===================================================================================
# 汎用メソッドの定義
#===================================================================================        
#-----------------------------------------------------------------------------------
# list 比較	
#----------------------------------------------------------------------------------- 
    
    def diffList(self, list1, list2, *args):
        c = set(list1).union(set(list2))
        d = set(list1).intersection(set(list2))
        return list(c - d) 
        
#-----------------------------------------------------------------------------------
# list から string 変換	
#-----------------------------------------------------------------------------------         
    def listToStr(self, target, *args):
        print(target)

        target = ''.join(unicode(target))
        target = target.replace("[u'", "").replace("']", "").replace("/", "\\")
        return str(target)
        
    def refreshUVScrlList(self, *args):
        self.initGUI     
        print('refreshUVScrlist')           
                    
    def initGUI(self, *args):
        cmds.textScrollList(self.objScllist, e=True, ra=True)
        cmds.textScrollList(self.uvScllist, e=True, ra=True)            
        self.getAllGeom        
        self.getAllUVSets
        print('initialize GUI')                   
         
#-----------------------------------------------------------------------------------
# mesh の list を取得	
#-----------------------------------------------------------------------------------                        
    def getAllGeom(self, *args):
        trns = []
        matched = []            
        geometry = cmds.ls(typ = "mesh")

        # self.transforms が empty の場合はすべて取得        
        if not self.transforms: 
            print "empty"
            self.transforms = cmds.listRelatives(geometry, p=True, path=True)
            cmds.textScrollList(self.objScllist, e = True , append = self.transforms)
        else:
            trns = cmds.listRelatives(geometry, p=True, path=True)
            matched = self.diffList(trns, self.transforms)              
            cmds.textScrollList(self.objScllist, e = True , append = matched)
            
        print('getAllGeom')
        
#-----------------------------------------------------------------------------------
# uv の list を取得	
#-----------------------------------------------------------------------------------
    def getAllUVSets(self, *args):
        cmds.textScrollList(self.uvScllist, e = True, ra = True)   
                 
        self.selectItem = cmds.textScrollList(self.objScllist, q = True , si = True) 
        print('self.selectItem : ' + str(self.selectItem))
             
        cmds.select(self.selectItem, replace = True)       
        for a in self.selectItem:    
            self.uvs = cmds.polyUVSet (a, query = True , allUVSets = True)
            cmds.textScrollList(self.uvScllist, e = True , append = self.uvs)         
               
#-----------------------------------------------------------------------------------
# UVSet 名を取得
#-----------------------------------------------------------------------------------
    def getUVName(self, *args):
        self.uvName = ''
        self.uvName = cmds.textScrollList(self.uvScllist, q = True , si = True)
        self.uvName = self.listToStr(self.uvName)   
        cmds.polyUVSet(currentUVSet = True, uvSet = str(self.uvName))
        print('self.uv : ' + str(self.uvName))
        
#-----------------------------------------------------------------------------------
# UVSet 名を変更
#-----------------------------------------------------------------------------------
    def uvNameChange(self, *args):                        
    
        textList = []
        newUVName = cmds.textField('uvNameF', query =True, text = True)  
        print('newUV : ' + str(newUVName))  
        
        cmds.polyUVSet(rename=True, newUVSet = str(newUVName) , uvSet= str(self.uvName ))

        # 以下のGUIUpdate部分はメソッドとして分けて実行すると動作しない模様
        textList = cmds.textScrollList(self.objScllist, q = True, ai = True);
               
        cmds.textScrollList(self.objScllist, e = True, ra = True)   
        cmds.textScrollList(self.uvScllist, e = True, ra = True)             
        
        for v in textList:
            cmds.textScrollList(self.objScllist, e = True,  append = v)
               
        cmds.textScrollList(self.objScllist, e = True, si = self.selectItem) 
                   
        for a in self.selectItem:    
            self.uvs = cmds.polyUVSet (a, query = True , allUVSets = True)
            cmds.textScrollList(self.uvScllist, e = True , append = self.uvs)                           

        print('initialize GUI')  
        
#-----------------------------------------------------------------------------------
# UVSet を削除
#-----------------------------------------------------------------------------------        
    def deleteUVSet(self, *args):
        i = 0

        delItem = cmds.textScrollList(self.uvScllist, q = True , si = True)
        
        for a in delItem:
            cmds.polyUVSet( delete = True , uvSet= str(a ))
            cmds.textScrollList(self.uvScllist, e = True , removeItem = a)
            i += 1    
                        
#-----------------------------------------------------------------------------------
# UVSet を新規作成
#-----------------------------------------------------------------------------------           
    def createUVSet(self, *args):
        cmds.polyUVSet( create = True )
        
        # 以下のGUIUpdate部分はメソッドとして分けて実行すると動作しない模様
        textList = cmds.textScrollList(self.objScllist, q = True, ai = True);
               
        cmds.textScrollList(self.objScllist, e = True, ra = True)   
        cmds.textScrollList(self.uvScllist, e = True, ra = True)             
        
        for v in textList:
            cmds.textScrollList(self.objScllist, e = True,  append = v)
               
        cmds.textScrollList(self.objScllist, e = True, si = self.selectItem) 
                   
        for a in self.selectItem:    
            self.uvs = cmds.polyUVSet (a, query = True , allUVSets = True)
            cmds.textScrollList(self.uvScllist, e = True , append = self.uvs)                           

        print('initialize GUI')         

#-----------------------------------------------------------------------------------
# UVSet (名前)をコピーして新規作成
#-----------------------------------------------------------------------------------           

    def doGetCopyUVName(self, *args):
        self.copyUvName = cmds.textScrollList(self.objScllist, e = True, si = self.selectItem)
        cmds.polyUVSet( copy=True, uvSet = 'uvSet' )
        
        # 以下のGUIUpdate部分はメソッドとして分けて実行すると動作しない模様
        textList = cmds.textScrollList(self.objScllist, q = True, ai = True);
               
        cmds.textScrollList(self.objScllist, e = True, ra = True)   
        cmds.textScrollList(self.uvScllist, e = True, ra = True)             
        
        for v in textList:
            cmds.textScrollList(self.objScllist, e = True,  append = v)
               
        cmds.textScrollList(self.objScllist, e = True, si = self.selectItem) 
                   
        for a in self.selectItem:    
            self.uvs = cmds.polyUVSet (a, query = True , allUVSets = True)
            cmds.textScrollList(self.uvScllist, e = True , append = self.uvs)                           

        print('initialize GUI')      
                                        
#-----------------------------------------------------------------------------------
# UVEditor(TextureViewWindow) を起動
#-----------------------------------------------------------------------------------
    def openTextureWindow(self, *args):
        mel.eval('TextureViewWindow')

               
uvSetManager = UVSetManager()
uvSetManager.create()