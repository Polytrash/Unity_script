# -*- coding: utf-8 -*-

#2017/1/15最終更新

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import re
import string
import math
from collections import Counter

class CharaChecker(object):
    
    def __init__(self):
        self.window = 'CharaCheckerWindow'
        self.title = 'Character Checker'
        self.size = (600, 350)

        self.width = 600
        self.height = 350  

        self.okc =(0.1, 0.6, 0.2)
        self.ngc =(0.6, 0.1, 0.1)
        self.ggc =(0.2, 0.1, 0.1)
                        
        # チェック対象
        self.objs = []    
        self.transforms = []
        self.joints = []
        self.uvs = []
                
        # 選択対象        
        self.selectItem = ''
        self.uvName = ''


                     
    def create(self, *args):
        if cmds.window('CharaCheckerWindow', exists = True):
            cmds.deleteUI('CharaCheckerWindow')
            
        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.nameFrm = cmds.frameLayout(label = u"キャラクターチェック項目", bgc = (0.15, 0.15, 0.15))        
        self.nameFrm = cmds.frameLayout(label = u"■ 命名規則", bgc = (0.1, 0.2, 0.4), cll = True)
        cmds.checkBox('nameChckBox1', l = u"1. 名前 に 不要 な 文字 が 含まれていないか", bgc = (0.2, 0.2, 0.2), v = True)    
        cmds.checkBox('nameChckBox2', l = u"2. root 以下の ノード が 全て ユニーク名 になっているか", bgc = (0.2, 0.2, 0.2), v = True)    
        cmds.setParent('..')  
          
        self.modelFrm = cmds.frameLayout(label = u"■ モデル", bgc = (0.4, 0.1, 0.4), cll = True)
        cmds.checkBox('modelChckBox1', l = u"1. ポリゴン数は ～8000 tris 以下か", bgc = (0.2, 0.2, 0.2), v = True)           
        cmds.checkBox('modelChckBox2', l = u"2. UVSet は 1 つだけで、UVSet 名は map1 になっているか", bgc = (0.2, 0.2, 0.2), v = True)          
        cmds.setParent('..')        
            
        self.jntFrm = cmds.frameLayout(label = u"■ ジョイント", bgc = (0.4, 0.4, 0.0), cll = True)      
        cmds.checkBox('jointChckBox1', l = u"1. _l  に対して同数の _r  が存在しているか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.checkBox('jointChckBox2', l = u"2. Joint Orient が全て 0 になっているか", bgc = (0.2, 0.2, 0.2), v = True)   
        cmds.checkBox('jointChckBox3', l = u"3. 移動値・回転値 に リミット が指定されていないか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.checkBox('jointChckBox4', l = u"4. mant , tail , hair 関連の ジョイント は X軸 が 子方向 に 向いているか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.setParent('..')       
             
        self.renameBtn = cmds.button( l = u"チェック実行" ,command = self.doCheck )   
        
        cmds.separator (h = 10, w = self.width, style = 'in') 
                
        cmds.text(u"チェック結果", bgc = (0.1, 0.1, 0.1), align = 'left', width = self.width)     
        cmds.scrollField('resultField', wordWrap = True, text = 'blank', editable = False )                                            

        cmds.setParent('..')              
        cmds.setParent('..')                 
        cmds.setParent('..')  
  
        cmds.showWindow() 
        
#-----------------------------------------------------------------------------------
# UIメソッド	
#----------------------------------------------------------------------------------- 

    def doCheck(self, *args):
        
        key = ''
        self.objs = []  
        self.rootObjs = []  
        self.transforms = [] 
        self.joints = []        
        self.selectItem = ''
        self.uvs = []
        self.uvName = ''
        
#------------------------------#        
# チェックリスト   
#------------------------------#                
        # ■ 命名規則チェック                
        n1 = cmds.checkBox('nameChckBox1', q=True, value=True) 
        n2 = cmds.checkBox('nameChckBox2', q=True, value=True) 
        
        # ■ モデルチェック         
        m1 = cmds.checkBox('modelChckBox1', q=True, value=True)        
        m2 = cmds.checkBox('modelChckBox2', q=True, value=True)

        # ■ ジョイントチェック         
        j1 = cmds.checkBox('jointChckBox1', q=True, value=True) 
        j2 = cmds.checkBox('jointChckBox2', q=True, value=True) 
        j3 = cmds.checkBox('jointChckBox3', q=True, value=True) 
                        
#------------------------------#        
# リスト取得  
#------------------------------#          
        self.getAllNames(key)
        self.getAllNameUnderRoot(key)
        self.getAllGeoms(key)
        self.getAllJoints(key)
        
#------------------------------#        
# チェック実行  
#------------------------------#           
        print('-------------------------------------------------------')        
        print('-------------------------------------------------------')            
        print(u"* キャラクターチェック実行 *")
        print('-------------------------------------------------------')
                
        # 名前 
        
        if n1:
            print('-------------------------------------------------------')            
            self.nameCheck(key)
            print('-------------------------------------------------------')
        else:
            self.checkBoxColor('nameChckBox1', 2)                        

        if n2:
            print('-------------------------------------------------------')            
            self.nameUniqCheck(key)
            print('-------------------------------------------------------')
        else:
            self.checkBoxColor('nameChckBox2', 2)  
                      
        # モデル
            
        if m1:
            print('-------------------------------------------------------')            
            self.polyCountCheck(key)
            print('-------------------------------------------------------') 
        else:
            self.checkBoxColor('modelChckBox1', 2)  
                        
        if m2:
            print('-------------------------------------------------------')            
            self.uvSetCheck(key)
            print('-------------------------------------------------------')    
        else:
            self.checkBoxColor('modelChckBox2', 2) 
            
        # ジョイント
            
        if j1:
            print('-------------------------------------------------------')            
            self.jointLRCheck(key)
            print('-------------------------------------------------------')  
        else:
            self.checkBoxColor('jointChckBox1', 2)       
                  
        if j2:
            print('-------------------------------------------------------')            
            self.jointOrientCheck(key)
            print('-------------------------------------------------------') 
        else:
            self.checkBoxColor('jointChckBox2', 2) 
                                                                        
        if j3:
            print('-------------------------------------------------------')            
            self.transformLimitCheck(key)
            print('-------------------------------------------------------') 
        else:
            self.checkBoxColor('jointChckBox3', 2)                                                             
                        
            
#-----------------------------------------------------------------------------------
# 汎用メソッド	
#----------------------------------------------------------------------------------- 

#------------------------------#
# 全オブジェクト名取得
#------------------------------#

    def getAllNames(self, key, *args):               
        cmds.select(add = True, ado = True)
        self.objs = cmds.ls(sl = True)        

#------------------------------#
# root以下の全オブジェクト名取得
#------------------------------#

    def getAllNameUnderRoot(self, key, *args):
        cmds.select('root', r = True)
        self.rootObjs = cmds.listRelatives(ad = True)

#------------------------------#
# メッシュ名取得
#------------------------------#

    def getAllGeoms(self, key, *args):           
        self.transforms = cmds.ls(typ = "mesh")            

#------------------------------#
# ジョイント名取得
#------------------------------#

    def getAllJoints(self, key, *args):
        self.joints =  cmds.ls(typ = "joint")  

#------------------------------#
# 数値関連
#------------------------------#

    # 第一引数が第二引数以上か比較          
    def greaterThan(self, num, val, *args):             
        if abs(num) != val:
            return False
        else:                  
            return True
               
#------------------------------#
# リスト関連
#------------------------------#

    # 2つのリストの重複要素を削除して新規リスト作成
    def makeUniqList(self, list1, list2, *args):
        uniq = []
        uniq = list(set(list1)^set(list2))
        return uniq
        
    # リスト内の重複要素の削除
    def diffRemoveList(self, list, *args):
        uniq = []
        for x in list:
            if x not in uniq:
                uniq.append(x)
        return uniq                

    # リスト内の重複要素の割り出し    
    def diffSrchList(self, list, *args):
        c = Counter(list)
        return [i for i in c if c[i]>1]

    # リスト内を第二引数で指定した数の要素数のサブリストに分ける    
    def makeSubList(self,list, size, *args):
        return [list[i:i+size] for i in range(0, len(list), size)]    
                
#------------------------------#
# リネーム関連
#------------------------------# 
    # 文字列置き換え
    def nameReplace(self, name, sub, *args):
        r = re.compile(sub)
        replacedName = name.replace(sub, '')
        return replacedName  

    # 末尾削除        
    def nameDel(self, word, val, *args):
        d = word[:val]
        return d                                
        
#------------------------------#
# チェックボックス色替え
#------------------------------# 
    def checkBoxColor(self, chckBox, val, *args):        
        if val == 0:
            cmds.checkBox(chckBox, e = True, bgc = self.okc)        
        elif val == 1:
            cmds.checkBox(chckBox, e = True, bgc = self.ngc)
        else:
            cmds.checkBox(chckBox, e = True, bgc = self.ggc)                            
                            
#-----------------------------------------------------------------------------------          
#-----------------------------------------------------------------------------------
# チェックリスト
#-----------------------------------------------------------------------------------          
#-----------------------------------------------------------------------------------          

#-----------------------------------------------------------------------------------
# 命名規則	
#----------------------------------------------------------------------------------- 

#------------------------------#
# 1.半角英数チェック
#------------------------------#

    def nameCheck(self, key, *args):
        
        checked = False
        
        for a in self.objs:                    
            regexp = re.compile(r'^[0-9A-Za-z]+$')
            result = regexp.search("abcdefghijklmnopqrstuvwxyz0123456789")
            if result != None :
                checked = True
            else :
                print(str(a) + u" に半角英数でない文字が存在しています")
                               
        if checked :
            print(u"■ 命名規則 - 1 [OK]: オブジェクト名はすべて半角英数です")            
            self.checkBoxColor('nameChckBox1', 0)
        else :           
            print(u"■ 命名規則 - 1 [NG]: オブジェクト名に半角英数でない文字が存在しています")            
            self.checkBoxColor('nameChckBox1', 1)
                       
#------------------------------#
# 2. ユニーク名チェック
#------------------------------#

    def nameUniqCheck(self, key, *args):    

        checked = False        
        diff = self.diffSrchList(self.rootObjs)

        if len(diff) == 0:     
            print(u"■ 命名規則 - 2 [OK]: オブジェクト名はすべてユニーク名でした")
            checked = True
            self.checkBoxColor('nameChckBox2', 0)           
        else :
            print(u"■ 命名規則 - 2 [NG]: 次の名前が重複しています")            
            for a in diff:
                print(str(a))
            self.checkBoxColor('nameChckBox2', 1) 
                                                         
#-----------------------------------------------------------------------------------
# モデル	
#----------------------------------------------------------------------------------- 

#------------------------------#
# 1. ポリゴンカウントチェック
#------------------------------#

    def polyCountCheck(self, key, *args):
        
        checked = False       
        polyCount =  []
        resultCount = 0       
        
        for a in self.transforms:
            #print (a)
            cmds.select(a, r = True)
            polyCount.append(cmds.polyEvaluate(t = True))

        resultCount = sum(polyCount)
        
        if resultCount <= 8000 :
            print (u"■ モデル - 1 [OK]: ポリゴン数は8000以下です")
            print (str(resultCount) + ' tris')
            checked = True
            self.checkBoxColor('modelChckBox1', 0)            
        else :
            print (u"■ モデル - 1 [NG]: ポリゴン数が8000をオーバーしています")
            print (str(resultCount) + ' tris')
            self.checkBoxColor('modelChckBox1', 1)
               
#------------------------------#
# 2.UVセットチェック
#------------------------------#

    def uvSetCheck(self, key, *args):
        
        checked = False  
        count = 0
        indexNG = [] 
        uvCorrectCount = []
    
        for a in self.transforms :    
            self.uvs = cmds.polyUVSet (a, query = True , allUVSets = True)
            if len(self.uvs) > 1 :
                print (u"■ モデル - 2 [NG]: " + str(a) + u" に UVSet が " + str(unicode(len(self.uvs))) + u" 存在しています") 
            else :                 
                for b in self.uvs :
                    if b != 'map1':                        
                        checked = False
                        indexNG.append(count)
                    else :
                        uvCorrectCount.append(1)
            count += 1                        
            
        if not indexNG:
            print (u"■ モデル - 2 [OK]: UVSet は　1 メッシュに対して 1 つで、名前はすべて map1 です")
            checked = True
            self.checkBoxColor('modelChckBox2', 0) 
        else :
            print (u"■ モデル - 2 [NG]: 次のメッシュ の UVSet の名前が map1 ではありません")
            indexNG = self.diffRemoveList(indexNG)            
            for i in indexNG:
                print(self.transforms[i])                                   
            self.checkBoxColor('modelChckBox2', 1)    
                                                  
#-----------------------------------------------------------------------------------
# ジョイント	
#-----------------------------------------------------------------------------------
#------------------------------#
# 1. 左右対称チェック
#------------------------------#  
    def jointLRCheck(self, key, *args):
        
        checked = False
        lJoints = []
        rJoints = []
        
        reLJoints = []
        reRJoints = []
        
        dupliList = []
        
        l = '_l'
        r = '_r'            
                
        for a in self.joints:   
            last = (a[-2:])  
            if last == l:
                lJoints.append(str(a))                
            elif last == r:
                rJoints.append(str(a)) 
                                   
        if len(lJoints) == len(rJoints):
            print (u"■ ジョイント - 1 [OK]: _l に対する _r は同数です")
            checked = True
            self.checkBoxColor('jointChckBox1', 0)             
        else:
            for b in lJoints:
                reLJoints.append(b[:-2])
            for c in rJoints:          
                reRJoints.append(c[:-2])  
                   
            dupliList = self.makeUniqList(reLJoints, reRJoints)
            print (u"■ ジョイント - 1 [NG]: 次の ジョイント の _l と _r が同数になっていません") 
            self.checkBoxColor('jointChckBox1', 1)             
            for d in dupliList:
                print (d)                
                     
#------------------------------#
# 2. JointOrient チェック
#------------------------------#          
    def jointOrientCheck(self, key, *args):
        
        checked = False
        
        count = 0
        indexNG = []
        
        jntOrnt = []        
        jntOrntSub = []
        
        for a in self.joints:
            jntOrnt.append(cmds.getAttr(a+'.jointOrientX'))
            jntOrnt.append(cmds.getAttr(a+'.jointOrientY'))
            jntOrnt.append(cmds.getAttr(a+'.jointOrientZ'))

        jntOrntSub = self.makeSubList(jntOrnt, 3)   
        
        for b in jntOrntSub:
            for c in b:
                if not self.greaterThan(math.floor(c),0):       
                    indexNG.append(count)
                    checked = False
                else:
                    None
            count += 1  
                                  
        if not indexNG:
            checked = True 
            print (u"■ ジョイント - 2 [OK]: すべての ジョイント の JointOrient は 0 です") 
            self.checkBoxColor('jointChckBox2', 0)                                     
        else:                                                      
            print (u"■ ジョイント - 2 [NG]: 次の ジョイント の JointOrient が 0 になっていません")  
            indexNG = self.diffRemoveList(indexNG)
            self.checkBoxColor('jointChckBox2', 1)         
            for i in indexNG:
                print(self.joints[i])                     
            
#------------------------------#
# 3. Transform Limit チェック
#------------------------------#          
    def transformLimitCheck(self, key, *args):
        
        trnsChecked = False
        rotChecked = False
                
        trnsCount = 0
        trnsIndexNG = []
        
        rotCount = 0
        rotIndexNG = []
                
        trnsLimit = []        
        rotLimit = []
        
        trnsLimitSub = []
        rotLimitSub = []
                
        for a in self.joints:
            cmds.select(a)
            # Translate Limit の値を格納
            trnsLimit.append(cmds.transformLimits (q = True, enableTranslationX = True))
            trnsLimit.append(cmds.transformLimits (q = True, enableTranslationY = True))
            trnsLimit.append(cmds.transformLimits (q = True, enableTranslationZ = True))
            # Rotate Limit の値を格納
            rotLimit.append(cmds.transformLimits (q = True, enableRotationX = True))
            rotLimit.append(cmds.transformLimits (q = True, enableRotationY = True))
            rotLimit.append(cmds.transformLimits (q = True, enableRotationZ = True))
                                    
        trnsLimitSub = self.makeSubList(trnsLimit, 3) 

          
        rotLimitSub = self.makeSubList(rotLimit, 3)   
               
        # Translate Limit の値をチェック                
        for b in trnsLimitSub:
            for c in b:
                for d in c:
                        if d: 
                            print d
                            trnsIndexNG.append(trnsCount)
                            trnsChecked = False
                        else:
                            None
            trnsCount += 1  
            
        # Rotate Limit の値をチェック                
        for e in rotLimitSub:
            for f in e:
                for g in f:
                        if g: 
                            print g
                            rotIndexNG.append(rotCount)
                            rotChecked = False
                        else:
                            None
            rotCount += 1           

        if not trnsIndexNG:
            trnsChecked = True 
            print (u"■ ジョイント - 2 [OK]: すべての ジョイント の Translate の リミット は OFF です")                                     
        else:                                                      
            print (u"■ ジョイント - 2 [NG]: 次の ジョイント の Translate に リミット が指定されています")  
            trnsIndexNG = self.diffRemoveList(trnsIndexNG)               
            for i in trnsIndexNG:
                print(self.joints[i])    

        if not rotIndexNG:
            rotChecked = True 
            print (u"■ ジョイント - 2 [OK]: すべての ジョイント の Rotate の リミット は OFF です")                          
        else:                                                      
            print (u"■ ジョイント - 2 [NG]: 次の ジョイント の Rotate に リミット が指定されています")  
            rotIndexNG = self.diffRemoveList(rotIndexNG)
            for i in rotIndexNG:
                print(self.joints[i]) 

        if trnsChecked and rotChecked:
            self.checkBoxColor('jointChckBox3', 0)                             
        else:
            self.checkBoxColor('jointChckBox3', 1)       
#-----------------------------------------------------------------------------------                 
charaChecker = CharaChecker()
charaChecker.create()