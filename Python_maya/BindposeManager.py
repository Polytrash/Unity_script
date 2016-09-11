# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import re


class BindposeManager(object):


    def __init__(self):

        self.window = 'BindposeManagerWindow'
        self.title = 'Bind Pose Manger'
        self.size = (300, 200)
        self.height = 200
        self.width = 300

        self.transformName = ''
        self.transforms = []
        self.allInfluences = []
        self.dagPoseNodes = []
        
        
    def create(self):

        if cmds.window('BindposeMangerWindow', exists = True):
            cmds.deleteUI('BindposeMangerWindow')

#===================================================================================
# GUIの定義
#===================================================================================

#-----------------------------------------------------------------------------------
# 1オブジェクトからバンドポーズ情報を取得
#-----------------------------------------------------------------------------------  


        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.frameFrm1 = cmds.frameLayout(label = u"シーンのバインドポーズを取得/追加", bgc = (0.5, 0.25, 0.3), cll = False)
        
        self.getBtn = cmds.button( l = u"取得", command = self.doGetDagPose, height = 30 )    
        self.textScllist = cmds.textScrollList('bpList', ams = True, dkc = self.removeAt, dcc = self.selectAt)
   
        cmds.setParent('..')  
        cmds.setParent('..') 

        self.frameFrm2 = cmds.frameLayout(label = u"未使用のバインドポーズを削除", bgc = (0.5, 0.25, 0.3), cll = False)
        self.getBtn = cmds.button( l = u"削除", command = self.doRemoveUnusedDagPose, height = 30 )    

        cmds.setParent('..')             
        cmds.showWindow()


#===================================================================================
# 汎用メソッドの定義
#===================================================================================
     
#-----------------------------------------------------------------------------------
# dagPose(バインドポーズ)取得
#----------------------------------------------------------------------------------- 

    def doGetDagPose(self, *args):
        
        selection = cmds.ls(type = 'transform')

        for a in selection:
            
            if self.typeCheck1(a) == False:
                self.transforms.append(a)

        print(self.transforms)

        for b in self.transforms:

            if self.typeCheck2(b) == False:
                
                cmds.select( b, r = True)
                print("selection is " + b)
                      
                try:
                    self.getDagPose()
                    print(u"Info: "+ b +" is valid")
                    break
                except Exception:
                    print(u"Info: "+ b +" is not valid")
            

#-----------------------------------------------------------------------------------
# dagPose(バインドポーズ)追加 ※用途が無いため不使用
#----------------------------------------------------------------------------------- 

    def doAddDagPose(self, *args):

            name = cmds.select
            self.addDagPose(name)


#-----------------------------------------------------------------------------------
# dagPose(バインドポーズ)削除
#-----------------------------------------------------------------------------------             
             
    def doRemoveUnusedDagPose(self, *args):

        # textScrollList を一度リセット
        cmds.textScrollList(self.textScllist, e = True, ra = True )     

        dagPose = pm.ls(type='dagPose')
        for a in dagPose:

            clstr = a.listConnections(type='skinCluster')

            if len(clstr) == 0:   
                pm.delete(a)
                print(self.dagPoseNodes)                            

        self.getDagPose()


#-----------------------------------------------------------------------------------
# dagPose(バインドポーズ)取得メソッド
#----------------------------------------------------------------------------------- 

    def getDagPose(self, *args):

        i = 0

        # weightedInfluence で 0 以外のウェイトを持つインフルエンスオブジェクト
        # (ジョイント/トランスフォーム)の文字列を取得
        try:

            self.allInfluences = cmds.skinCluster(q = True, weightedInfluence = True)
            # DAG内にあるノードのすべてのパスをリスト化して取得
            tmpDagPoseNodes = cmds.ls( type = 'dagPose')                       

        except Exception:
            #タイプチェック
            self.typeCheck(obj)
            print( u" Info: Current selecting object is not a deformer.")

        if(len(tmpDagPoseNodes) == 0):
            print( u" Info: dagPose has not exists in current object.")
            return 1

        else:
            # textScrollList を一度リセット
            cmds.textScrollList(self.textScllist, e = True, ra = True )
            for a in tmpDagPoseNodes :
                
                # self.dagPoseNodes 内に同名の文字列が無ければ追加
                if a in self.dagPoseNodes:

                    cmds.textScrollList(self.textScllist, e = True , append = a)
                                      
                else: 

                    self.dagPoseNodes.append(a)  
                    cmds.textScrollList(self.textScllist, e = True , append = a)

                i += 1


#-----------------------------------------------------------------------------------
# dagPose(バインドポーズ)追加メソッド ※用途が無いため不使用
#----------------------------------------------------------------------------------- 

    def addDagPose(self, obj, *args):
        
        # weightedInfluence で 0 以外のウェイトを持つインフルエンスオブジェクト
        # (ジョイント/トランスフォーム)の文字列を取得
        try:
            self.allInfluences = cmds.skinCluster(q = True, weightedInfluence = True)

        except Exception:
            # オブジェクトタイプをチェック
            self.typeCheck(obj)
            print( u" Info: Current selecting object is not a deformer. ")	

        if(len(relatives) == 0):
            print( u" Info:" + obj + " has not exists in current object.")
            return 1

        else:
            dagpose = cmds.dagPose(obj, bp = True, save = True)
            cmds.textScrollList(self.textScllist, e = True , append = dagpose)
            self.dagPoseNodes.append(dagpose)  


#===================================================================================
# textScrollListの選択から対象を選択	
#===================================================================================
    
    def selectAt(self, *args):
        i = 0

        selectItem = cmds.textScrollList(self.textScllist, q = True , si = True)
        
        cmds.select(selectItem)


#===================================================================================
# textScrollListから選択項目を削除	
#===================================================================================

    def removeAt(self, *args):

        i = 0

        delItem = cmds.textScrollList(self.textScllist, q = True , si = True)
        
        cmds.select(delItem)

        for a in delItem:

            if delItem[i] in self.dagPoseNodes:
                
                
                # textScrollList と self.dagPoseNodes から delItem を削除
                cmds.textScrollList(self.textScllist, e = True , removeItem = delItem[i])
                self.dagPoseNodes.remove(delItem[i])   
                print(self.dagPoseNodes)            
               
            i += 1
        
                                    
#want name of skin cluster on  selection

    def checkSkinCluster(self, *args):
        selection = cmds.ls(sl=True)
        item= selection[0]
        print mel.eval('findRelatedSkinCluster '+item)


#-----------------------------------------------------------------------------------
# オブジェクトタイプチェック	
#----------------------------------------------------------------------------------- 

    def typeCheck1(self, name, *args):

        # name がjointでないかチェック
        type = cmds.objectType(name, isType = u"joint")


        if type == True:

            print("Info: " + name + " is joint")
            return type
        else:
            type = False
            return type  



    def typeCheck2(self, name, *args):

        
        shapeInfo = cmds.objectType(name)

        # Cameraチェック
        if shapeInfo == 'camera':
            print("Info: " + name + " is a camera, therefore which could not add to the list.")
            type = True
            return type

        # Nurbsチェック
        elif shapeInfo == 'nurbsCurve':
            print("Info: " + name + " is a nurbsCurve, therefore which could not add to the list.")
            type = True
            return type

        # Locatorチェック
        elif shapeInfo == 'locator':
            print("Info: " + name + " is a locator, therefore which could not add to the list.")
            type = True
            return type
  
        # Mesh チェック
        elif shapeInfo == 'mesh':
            print("Info: " + name + " is a mesh, therefore which could not add to the list.")
            type = True
            return type        
                  
        else:
            type = False
            return type            


        
BPManager = BindposeManager()
BPManager.create()