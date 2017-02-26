# -*- coding: utf-8 -*-

#2017/2/10�ŏI�X�V

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
        self.frameFrm1 = cmds.frameLayout(label = u"�^�[�Q�b�g�\�� �� �I�u�W�F�N�g �� �����_�� �ɔz�u���܂�", bgc = (0.1, 0.2, 0.5))
    
        cmds.text(u"�� �^�[�Q�b�g", bgc = (0.1, 0.5, 0.2), align = 'left', width = self.width)   
        cmds.rowColumnLayout(nc = 3, rowSpacing=(10,10))             
        cmds.text(label=u"�I�����ăZ�b�g : ")       
        self.trgtFld = cmds.textField( 'trgtNameF',text = '', width = 150)         
        self.trgtSetBtn = cmds.button( l = u"�Z�b�g", width = 60 , c = self.setTrgtName)  
        cmds.setParent('..')          
    
        cmds.text(u"�� �I�u�W�F�N�g", bgc = (0.5, 0.1, 0.2), align = 'left', width = self.width)
        cmds.rowColumnLayout(nc = 3, rowSpacing=(10,10))        
        cmds.text(label=u"�I�����ăZ�b�g : ")       
        self.srcFld = cmds.textField( 'srcNameF',text = '', width = 150)         
        self.srcSetBtn = cmds.button( l = u"�Z�b�g", width = 60 , c = self.setSrcName)   
        cmds.setParent('..')          
        cmds.columnLayout( columnAttach=('right', 5), rowSpacing=10, columnWidth=290 )
        cmds.intSliderGrp('countSliderG', field = True,l = u"�z�u���F", minValue = 0, maxValue = 1000, fieldMinValue = 1, fieldMaxValue = 1000 )           
        cmds.setParent('..') 
                     
        self.renameBtn = cmds.button( l = u"�z�u", command = self.doPlacement )             
        self.renameBtn = cmds.button( l = u"���Z�b�g", command = self.resetPlacement )  
        cmds.showWindow()         
        
#-----------------------------------------------------------------------------------
# �ėp���\�b�h	
#-----------------------------------------------------------------------------------
    def removeDigit(self, target, *args):
        result = ''.join([i for i in target if not i.isdigit()])
        return result
 
    def listToStr(self, target, *args):
        target = ''.join(unicode(target))
        target = target.replace("[u'", "").replace("']", "").replace("/", "\\")
        return str(target)

#-----------------------------------------------------------------------------------
# �w�胁�\�b�h	
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
# �z�u���\�b�h	
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
        
        self.setLocator()     
        
        trgtObj = cmds.textField('trgtNameF', query = True, text = True)
        srcObj = cmds.textField('srcNameF', query = True, text = True)
        count = cmds.intSliderGrp('countSliderG', query = True, value = True)
        
        cmds.select('scatterLocator', r = True)
        cmds.xform(a = True, t = (0,0,0))
        cmds.select(cl = True)
        
        cmds.select(trgtObj,r = True )
        cmds.select('scatterLocator', tgl = True)
        cmds.select(srcObj, tgl = True)
        

        mel.eval("closestPointOnNurbsSurface -c " + str(count))     
        
#-----------------------------------------------------------------------------------
# ���Z�b�g���\�b�h	
#-----------------------------------------------------------------------------------
        
    def resetPlacement(self, *args):
        self.selectScatterObjects()
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