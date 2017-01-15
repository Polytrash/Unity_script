# -*- coding: utf-8 -*-

#2017/1/15最終更新

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import re

class CharaChecker(object):
    
    def __init__(self):
        self.window = 'CharaCheckerWindow'
        self.title = 'Character Checker'
        self.size = (500, 350)

        self.width = 500
        self.height = 350  
                          
        self.transforms = [] 
        self.selectItem = ''
        self.uvs = []
        self.uvName = ''

                     
    def create(self, *args):
        if cmds.window('CharaCheckerWindow', exists = True):
            cmds.deleteUI('CharaCheckerWindow')
            
        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.nameFrm = cmds.frameLayout(label = u"キャラクターチェック項目", bgc = (0.15, 0.15, 0.15))        
        self.nameFrm = cmds.frameLayout(label = u"■ 命名規則", bgc = (0.3, 0.5, 0.1), cll = True)
        self.nameChckBox1 = cmds.checkBox(l = u"1. 名前に不要な文字が含まれていないか", bgc = (0.2, 0.2, 0.2), v = True)    
        cmds.setParent('..')  
          
        self.modelFrm = cmds.frameLayout(label = u"■ モデル", bgc = (0.2, 0.2, 0.4), cll = True)
        self.modelChckBox1 = cmds.checkBox(l = u"1. ポリゴン数は ～8000 tri 以下か", bgc = (0.4, 0.0, 0.0), v = True)           
        self.modelChckBox2 = cmds.checkBox(l = u"2. UVSet は 1つだけになっているか", bgc = (0.2, 0.2, 0.2), v = True)    
        self.modelChckBox3 = cmds.checkBox(l = u"3. UVSet 名が map1 になっているか", bgc = (0.4, 0.0, 0.0), v = True)           
        cmds.setParent('..')        
            
        self.jntFrm = cmds.frameLayout(label = u"■ ジョイント", bgc = (0.5, 0.3, 0.1), cll = True)      
        self.jntChckBox1 = cmds.checkBox(l = u"1. root以下のノードが全てユニーク名になっているか", bgc = (0.2, 0.2, 0.2), v = True)    
        self.jntChckBox2 = cmds.checkBox(l = u"2. _l 対して同じ数の _r が存在しているか", bgc = (0.2, 0.2, 0.2), v = True)
        self.jntChckBox3 = cmds.checkBox(l = u"3. Joint Orient が全て 0 になっているか", bgc = (0.2, 0.2, 0.2), v = True)   
        self.jntChckBox4 = cmds.checkBox(l = u"4. 移動値・回転値にリミットが指定されていないか", bgc = (0.2, 0.2, 0.2), v = True)
        self.jntChckBox5 = cmds.checkBox(l = u"5. mant , tail , hair 関連の ジョイント はX軸が子方向に向いているか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.setParent('..')       
             
        self.renameBtn = cmds.button( l = u"チェック実行" )   
        
        cmds.separator (h = 10, w = self.width, style = 'in') 
                
        cmds.text(u"チェック結果", bgc = (0.1, 0.1, 0.1), align = 'left', width = self.width)     
        cmds.scrollField(it = '■ モデル-1 : ポリゴン数が 10000 tri です\n■ モデル-3 : UVSet 名が uvSet です\n', bgc = (0.4, 0.1, 0.1 ))                                            

        cmds.setParent('..')              
        cmds.setParent('..')                 
        cmds.setParent('..')  
  
        cmds.showWindow()  

        
#-----------------------------------------------------------------------------------
# 命名規則	
#----------------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------------
# モデル	
#----------------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------------
# ジョイント	
#-----------------------------------------------------------------------------------  

               
charaChecker = CharaChecker()
charaChecker.create()