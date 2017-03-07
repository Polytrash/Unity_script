# -*- coding: utf-8 -*-

#2017/2/10最終更新

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import re

class ObjectScatter(object):
    
    def __init__(self):
        self.window = 'ObjectScatterWindow'
        self.title = 'Object Scatter'
        self.size = (175, 280)

        self.width = 280
        self.height = 175  
        
        self.count = 0
        
        self.trgtObjName = ''
        self.srcObjName = ''
        
        self.trgtShapeName = ''                          
        self.srcShapeName = '' 

                     
    def create(self, *args):
        if cmds.window('ObjectScatterWindow', exists = True):
            cmds.deleteUI('ObjectScatterWindow')
            
        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.frameFrm1 = cmds.frameLayout(label = u"ターゲット表面 に オブジェクト を ランダム に配置します", bgc = (0.1, 0.2, 0.5))
    
        cmds.text(u"■ ターゲット", bgc = (0.1, 0.5, 0.2), align = 'left', width = self.width)   
        cmds.rowColumnLayout(nc = 3, rowSpacing=(10,10))             
        cmds.text(label=u"選択してセット : ")       
        self.trgtFld = cmds.textField( 'trgtNameF',text = '', width = 150)         
        self.trgtSetBtn = cmds.button( l = u"セット", width = 60 , c = self.setTrgtName)  
        cmds.setParent('..')          
    
        cmds.text(u"■ 配置オブジェクト", bgc = (0.5, 0.1, 0.2), align = 'left', width = self.width)
        cmds.rowColumnLayout(nc = 3, rowSpacing=(10,10))        
        cmds.text(label=u"選択してセット : ")       
        self.srcFld = cmds.textField( 'srcNameF',text = '', width = 150)         
        self.srcSetBtn = cmds.button( l = u"セット", width = 60 , c = self.setSrcName)   
        cmds.setParent('..')        
        cmds.text(u"■ 設定", bgc = (0.1, 0.2, 0.5), align = 'left', width = self.width)          
        cmds.columnLayout( columnAttach=('right', 5), rowSpacing=10, columnWidth=290 )       
         
        cmds.intSliderGrp('countSliderG', field = True,l = u"配置数：", minValue = 0, maxValue = 1000, fieldMinValue = 1, fieldMaxValue = 1000 )           

        cmds.text(u"・ 係数", bgc = (0.2, 0.2, 0.2), align = 'left', width = self.width) 
        cmds.floatSliderGrp('radiusSliderG', field = True,l = u"距離：", value = 10, minValue = 0, maxValue = 100, fieldMinValue = 1, fieldMaxValue = 100 )                   
        cmds.floatSliderGrp('widthSliderG', field = True,l = u"幅：", value = 100, minValue = 0, maxValue = 1000, fieldMinValue = 1, fieldMaxValue = 1000 )           
        cmds.floatSliderGrp('heightSliderG', field = True,l = u"高さ：", value = 100,  minValue = 0, maxValue = 1000, fieldMinValue = 1, fieldMaxValue = 1000 )           
        cmds.floatSliderGrp('depthSliderG', field = True,l = u"奥行き：", value = 100,  minValue = 0, maxValue = 1000, fieldMinValue = 1, fieldMaxValue = 1000 )                           

        #cmds.text(u"・ ランダム", bgc = (0.2, 0.2, 0.2), align = 'left', width = self.width)
        #cmds.checkBox('randomChck', l = u"■ ランダム回転",  v = True)  

        cmds.setParent('..') 
                     
        self.renameBtn = cmds.button( l = u"配置", command = self.doPlacement )             
        self.renameBtn = cmds.button( l = u"リセット", command = self.resetPlacement )  
        cmds.showWindow()         
        
#-----------------------------------------------------------------------------------
# 汎用メソッド	
#-----------------------------------------------------------------------------------
    def removeDigit(self, target, *args):
        result = ''.join([i for i in target if not i.isdigit()])
        return result
 
    def listToStr(self, target, *args):
        target = ''.join(unicode(target))
        target = target.replace("[u'", "").replace("']", "").replace("/", "\\")
        return str(target)

#-----------------------------------------------------------------------------------
# 指定メソッド	
#-----------------------------------------------------------------------------------
    
    def setTrgtName(self, *args):    
        trgtShapeName = ''
        
        self.trgtObjName = cmds.ls(sl=True)
        trgtShapeName = cmds.listRelatives(shapes = True)
        
        trgtShapeName = self.listToStr(trgtShapeName)
        self.trgtObjName = self.listToStr(self.trgtObjName)
                          
        cmds.textField(self.trgtFld, e = True, text = str(trgtShapeName ))
        self.trgtShapeName = trgtShapeName
        print("Trgt Shape Set : " + trgtShapeName)

              
    def setSrcName(self, *args):        
        srtShapeName = ''
                   
        self.srcObjName = cmds.ls(sl=True)
        srcShapeName = cmds.listRelatives(shapes = True)
        
        srcShapeName = self.listToStr(srcShapeName)                  
        self.srcObjName = self.listToStr(self.srcObjName)
        
        cmds.textField(self.srcFld, e = True, text = str(srcShapeName ))
        self.srcShapeName = srcShapeName
        print("Source Shape Set : " + srcShapeName)            

#-----------------------------------------------------------------------------------
# 配置メソッド	
#-----------------------------------------------------------------------------------

        
    def setLocator(self, *args):
        locatorName = ''
        exist = False
        
        try:
            cmds.select('scatterLocator', r = True)
            exist = True
        except ValueError:
            exist = False                        
    
        if not exist:                            
                locatorName = self.listToStr(cmds.spaceLocator (p = (0,0,0)))
                cmds.select(locatorName, r = True)
                cmds.rename('scatterLocator') 
        else:
            cmds.select('scatterLocator', r = True)
            cmds.xform(a = True, t = (0,0,0))
            cmds.select(cl = True)                                            
  
    def doPlacement(self, *args):
        
        trgtObj = ''
        srcObj = ''  
        count = 0 
        
        radius = 10
        width = 1000
        height = 1000
        depth = 1000
        
        randVal = 1
                        
        self.setLocator()     
        
                
        trgtShape = cmds.textField('trgtNameF', query = True, text = True)
        srcShape = cmds.textField('srcNameF', query = True, text = True)
        count = cmds.intSliderGrp('countSliderG', query = True, value = True)
        width = cmds.floatSliderGrp('radiusSliderG', query = True, value = True)
        width = cmds.floatSliderGrp('widthSliderG', query = True, value = True)
        height = cmds.floatSliderGrp('heightSliderG', query = True, value = True)
        depth = cmds.floatSliderGrp('depthSliderG', query = True, value = True)  
        #randChck = cmds.checkBox('randomChck', q=True, value=True)    
        
        trgtName = re.sub('Shape', '', trgtShape)             
        
        cmds.select('scatterLocator', r = True)
        cmds.xform(a = True, t = (0,0,0))
        cmds.select(cl = True)
        
        cmds.select(trgtShape,r = True )
        cmds.select('scatterLocator', tgl = True)
        cmds.select(srcShape, tgl = True)
    
        print width

        mel.eval("objectScatter -c " + str(count) + " -n " + str(trgtName) + " -r " + str(radius) + " -w " + str(width) + " -h " + str(height) + " -d " + str(depth))     
        
#-----------------------------------------------------------------------------------
# リセットメソッド	
#-----------------------------------------------------------------------------------
        
    def resetPlacement(self, *args):
        self.selectScatterObjects()
        cmds.select('scatterLocator', tgl = True)
        cmds.delete()        
        
    def selectScatterObjects(self, *args):        
        uScatterObjsName = []
        sScatterObjsName = []
        
        uScatterObjsName = (cmds.ls(self.removeDigit(str(self.srcObjName)) + '*', tr = True))
        for a in uScatterObjsName:
            sScatterObjsName.append(self.listToStr(a))
        
        sScatterObjsName.remove(self.srcObjName)
        print sScatterObjsName
        
        cmds.select(cl = True)
        for b in sScatterObjsName:
            cmds.select(b, tgl = True)
            
        
objScatter = ObjectScatter()
objScatter.create()        