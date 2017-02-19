# -*- coding: utf-8 -*-

#2017/1/15最終更新

import re
import string
import math
import itertools
from collections import Counter

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

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
        self.meshes = []
        self.joints = []
        self.uvs = []
                
        # 選択対象        
        self.selectItem = ''
        self.uvName = ''
        
        self.result = u""



                     
    def create(self, *args):
        if cmds.window('CharaCheckerWindow', exists = True):
            cmds.deleteUI('CharaCheckerWindow')
            
        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.nameFrm = cmds.frameLayout(label = u"【キャラクターチェック項目】", bgc = (0.15, 0.15, 0.15))        
        self.nameFrm = cmds.frameLayout(label = u"■ 命名規則", bgc = (0.1, 0.2, 0.4), cll = True)
        cmds.checkBox('nameChckBox1', l = u"1. 名前 に 半角英数以外 が 含まれていないか", bgc = (0.2, 0.2, 0.2), v = True)    
        cmds.checkBox('nameChckBox2', l = u"2. root 以下の ノード が 全て ユニーク名 になっているか", bgc = (0.2, 0.2, 0.2), v = True)    
        cmds.checkBox('nameChckBox3', l = u"3. 名前の 末尾 が 大文字 になっていないか", bgc = (0.2, 0.2, 0.2), v = True)    
        cmds.setParent('..')  
          
        self.modelFrm = cmds.frameLayout(label = u"■ モデル", bgc = (0.4, 0.1, 0.4), cll = True)
        cmds.checkBox('modelChckBox1', l = u"1. ポリゴン数は ～8000 tris 以下か", bgc = (0.2, 0.2, 0.2), v = True)           
        cmds.checkBox('modelChckBox2', l = u"2. UVSet は 1 つだけで、UVSet 名は map1 になっているか", bgc = (0.2, 0.2, 0.2), v = True)          
        cmds.checkBox('modelChckBox3', l = u"3. モデルに頂点カラーが含まれていないか", bgc = (0.2, 0.2, 0.2), v = True)          
        cmds.setParent('..')        
            
        self.jntFrm = cmds.frameLayout(label = u"■ ジョイント", bgc = (0.4, 0.4, 0.0), cll = True)      
        cmds.checkBox('jointChckBox1', l = u"1. ジョイント名の _l  に対して同数の _r  が存在しているか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.checkBox('jointChckBox2', l = u"2. Joint Orient が全て 0 になっているか", bgc = (0.2, 0.2, 0.2), v = True)   
        cmds.checkBox('jointChckBox3', l = u"3. 移動値・回転値 に リミット が指定されていないか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.checkBox('jointChckBox4', l = u"4. mant , tail , hair 関連の ジョイント は X軸 が 子方向 に 向いているか", bgc = (0.2, 0.2, 0.2), v = True)
        cmds.setParent('..')       
             
        self.renameBtn = cmds.button( l = u"チェック実行" ,command = self.doCheck )   
        
        cmds.separator (h = 10, w = self.width, style = 'in') 
        self.nameFrm = cmds.frameLayout(label = u"【キャラクターチェック結果】", bgc = (0.15, 0.15, 0.15))                     
   
        cmds.scrollField('resultField', wordWrap = True, text = self.result, editable = False )
                                                    
        cmds.rowColumnLayout(nc = 3)
        cmds.text(label='オブジェクト名 : ')       
        self.uvNameFld = cmds.textField( 'nameF',w = 200, ec = self.srchName)         
        self.renameBtn = cmds.button( l = u"検索", w = 100 , command = self.srchName )  
        cmds.setParent('..') 
           
        cmds.text(u"【問い合わせ先：】", bgc = (0.1, 0.1, 0.1), align = 'left', width = self.width)  
     
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
        self.mesheses = [] 
        self.joints = []        
        self.selectItem = ''
        self.uvs = []
        self.uvName = ''
        
        self.result = u""
        
#------------------------------#        
# チェックリスト   
#------------------------------#                
        # ■ 命名規則チェック                
        n1 = cmds.checkBox('nameChckBox1', q=True, value=True) 
        n2 = cmds.checkBox('nameChckBox2', q=True, value=True) 
        n3 = cmds.checkBox('nameChckBox3', q=True, value=True) 
                
        # ■ モデルチェック         
        m1 = cmds.checkBox('modelChckBox1', q=True, value=True)        
        m2 = cmds.checkBox('modelChckBox2', q=True, value=True)
        m3 = cmds.checkBox('modelChckBox3', q=True, value=True)
        
        # ■ ジョイントチェック         
        j1 = cmds.checkBox('jointChckBox1', q=True, value=True) 
        j2 = cmds.checkBox('jointChckBox2', q=True, value=True) 
        j3 = cmds.checkBox('jointChckBox3', q=True, value=True) 
        j4 = cmds.checkBox('jointChckBox4', q=True, value=True) 
        
#------------------------------#        
# リスト取得  
#------------------------------#          
        self.getAllNames(key)
        self.getAllNameUnderRoot(key)
        self.getAllMeshes(key)
        
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
            
        if n3:
            print('-------------------------------------------------------')            
            self.nameUpperCheck(key)
            print('-------------------------------------------------------')
        else:
            self.checkBoxColor('nameChckBox3', 3) 
                                   
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
            
        if m3:
            print('-------------------------------------------------------')            
            self.vtxColorCheck(key)
            print('-------------------------------------------------------')    
        else:
            self.checkBoxColor('modelChckBox3', 2)             
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

        if j4:
            print('-------------------------------------------------------')            
            self.jntsTwistCheck(key)
            print('-------------------------------------------------------') 
        else:
            self.checkBoxColor('jointChckBox3', 2)

                        
        self.outputResult('resultField', 'result')
                           
#-----------------------------------------------------------------------------------
# 汎用メソッド	
#----------------------------------------------------------------------------------- 
#------------------------------#
# オブジェクト名検索
#------------------------------#
    def srchName(self, *args):
        name = ''
        name = cmds.textField('nameF', query =True, text = True)  
        cmds.select(str(name))
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
        root = []
        child = []
        
        objs = [] # 文字列走査用に使用(unicode to string)
        
        jnt1 = [] # joint格納用に使用   
        jnt2 = [] # 文字列走査用に使用(unicode to string)
        jntTmp = [] 
        
        mesh = []
        

        root = cmds.ls(assemblies = True)
        
        # transform と joint を選別
        for a in root:
            if cmds.objectType(a) == 'transform':
                print ('transform : ' + a)
                child.append(cmds.listRelatives(a, ad = True, type = 'transform'))                             
            elif cmds.objectType(a) == 'joint':                                   
                jnt1.append(cmds.listRelatives(a, ad = True, type = 'joint')) 
                # root Joint は 追加されないので、一旦　jntTmp に格納し、後処理で リストに追加・削除
                jntTmp.append(a)
                print ('joint : ' + a)             
                
        jnt1 = list(itertools.chain(*filter(None, jnt1)))                
        child = list(itertools.chain(*filter(None, child))) 
                                   
        # self.objs を string に変換
        for o in root: 
            o = self.uniToStr(o)
            objs.append(o)
            
        self.objs = list(objs)  

        # self.joints を string に変換                   
        for j in jnt1: 
            j = self.uniToStr(j)
            jnt2.append(j)
                               
        self.joints = list(jnt2) 
       
        # 選別で精査しきれなかった jntTmp を self.objs から削除、 self.joints に追加
        for x in jntTmp:
            print x
            self.objs.remove(x)
            self.joints.append(x)
  
       
        print ('-------------------------------------------------------')                             
        print ('All transforms : ' + str(self.objs))
        print ('All joints : ' + str(self.joints))
 
#------------------------------#
# メッシュ名取得
#------------------------------#

    def getAllMeshes(self, key, *args):           
        
        meshes = []
        tmp = ''
        
        self.meshes = cmds.ls(sn = True, typ = "mesh") 
        for a in self.meshes: 
            a = self.uniToStr(a)
            tmp = re.sub('Shape', '', a)
            meshes.append(tmp)
            
                   
        self.meshes = list(meshes)          
                  
        print ('All meshes : ' + str(self.meshes))
        
#------------------------------#
# Unicode to String
#------------------------------#

    def uniToStr(self, key, *args):
        key = ''.join(unicode(key))
        result = key.replace("[u'", "").replace("']", "").replace("/", "\\")
        return str(result)
        
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
# ジョイント関連
#------------------------------#            
    # 与えられた joint から root joint を取得
    def getHierarchyRootJoint(self, jnt ,*args):   
        # Search through the rootJoint's top most joint parent node
        rootJoint = jnt

        while (True):
            parent = cmds.listRelatives( rootJoint, parent=True, type='joint' )
            if not parent:
                break;
            rootJoint = parent[0]

        return rootJoint  
                       
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
        x=set(list)
        dup=[]
        for c in x:
            if(list.count(c)>1):
                dup.append(c)
        return dup

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

    # 指定文字で文字列を分割
    def nameSplit(self, word , val , *args):
        d = ''
        d = word.split(val)
        return d
                
    # 文字列が小文字かどうか
    def nameLowerCheck(self, str, *args):
        for char in str:
            if 'A' <= char <= 'Z':
                return False
        return True 
               
    # ネストされたリストをリストに変換        
    def flattenList(self, listOfLists, *args):
        "Flatten one level of nesting"
        return chain.from_iterable(listOfLists)
                 
        
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

#------------------------------#
# 結果テキスト格納
#------------------------------# 
    def storeResult(self, sentence, *args):   
   
        self.result += (sentence + '\n')                    

#------------------------------#
# 結果テキスト出力
#------------------------------#                             
    def outputResult(self, sF, result, *args):  
             
        cmds.scrollField(sF, e = True, text = self.result)         

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
            print(u"■ 命名規則 - 1 [OK]: 名前はすべて半角英数です") 
            self.storeResult(u"■ 命名規則 - 1 [OK]: 名前はすべて半角英数です")   
                    
            self.checkBoxColor('nameChckBox1', 0)
        else :           
            print(u"■ 命名規則 - 1 [NG]: 名前に半角英数でない文字が存在しています")
            self.storeResult(u"■ 命名規則 - 1 [NG]: 名前に半角英数でない文字が存在しています")                         
            
            self.checkBoxColor('nameChckBox1', 1)
                       
#------------------------------#
# 2. ユニーク名チェック
#------------------------------#

    def nameUniqCheck(self, key, *args):    

        checked = False        
        diff = self.diffSrchList(self.objs)

        if len(diff) == 0:     
            print(u"■ 命名規則 - 2 [OK]: 名前はすべてユニーク名でした") 
            self.storeResult(u"■ 命名規則 - 2 [OK]: 名前はすべてユニーク名でした")                                  
            checked = True
            self.checkBoxColor('nameChckBox2', 0)           
        else :
            print(u"■ 命名規則 - 2 [NG]: 次の名前が重複しています") 
            self.storeResult(u"■ 命名規則 - 2 [NG]: 次の名前が重複しています")                       
            for a in diff:
                print(str(a))
                self.storeResult(str(a))
            self.checkBoxColor('nameChckBox2', 1) 

#------------------------------#
# 2. 名前 末尾大文字チェック
#------------------------------#
    def nameUpperCheck(self, key, *args):

        checked = False  
        count = []
        
        i = 0      
        last = ''        

        for a in self.objs:
            last = a[-1:]
            # 末尾が小文字かチェック
            if not self.nameLowerCheck(last): 
                # 末尾が数値かチェック
                if re.findall("\D+", last):
                    count.append(i)            
            else:
                None
            i += 1

        if not count:
            print (u"■ 命名規則 - 3 [OK]: 名前の末尾は小文字か数字になっています")
            self.storeResult(u"■ 命名規則 - 3 [OK]: 名前の末尾は小文字か数字になっています")               
            self.checkBoxColor('nameChckBox3', 0)             
            checked = True                        
        else:
            print (u"■ 命名規則 - 3 [NG]: 次の名前がの末尾が大文字になっています")
            self.storeResult(u"■ 命名規則 - 3 [NG]: 次の名前がの末尾が大文字になっています")               
            self.checkBoxColor('nameChckBox3', 1)             
            for b in count:
                self.storeResult(self.objs[b])                
                print(self.objs[b])                                                      
                        
                                                         
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
        
        for a in self.meshes:
            #print (a)
            try:
                cmds.select(a, r = True)
                polyCount.append(cmds.polyEvaluate(t = True))
            except ValueError:
                print (str(a) + ' is not found so Remove from meshes list')  
                self.meshes.remove(a)  
                
        resultCount = sum(polyCount)
        
        if resultCount <= 8000 :
            print (u"■ モデル - 1 [OK]: ポリゴン数は 8000tris 以下です")
            self.storeResult(u"■ モデル - 1 [OK]: ポリゴン数は8000tris 以下です")               
            print (str(resultCount) + ' tris')
            self.storeResult(str(resultCount) + ' tris')               
            checked = True
            self.checkBoxColor('modelChckBox1', 0)            
        else :
            print (u"■ モデル - 1 [NG]: ポリゴン数が 8000tris をオーバーしています")
            self.storeResult(u"■ モデル - 1 [NG]: ポリゴン数が 8000tris をオーバーしています")            
            print (str(resultCount) + ' tris')
            self.storeResult(str(resultCount) + ' tris')              
            self.checkBoxColor('modelChckBox1', 1)
               
#------------------------------#
# 2.UVセットチェック
#------------------------------#

    def uvSetCheck(self, key, *args):
        
        checked = False  
        count = 0
        indexNG = [] 
        uvCorrectCount = []
    
        for a in self.meshes :    
            try:
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
            except ValueError:
                print (str(a) + ' is not found so Remove from meshes list')  
                self.meshes.remove(a)              
            
        if not indexNG:
            print (u"■ モデル - 2 [OK]: UVSet は　1 メッシュに対して 1 つで、名前はすべて map1 です")
            self.storeResult(u"■ モデル - 2 [OK]: UVSet は　1 メッシュに対して 1 つで、名前はすべて map1 です")            
            checked = True
            self.checkBoxColor('modelChckBox2', 0) 
        else :
            print (u"■ モデル - 2 [NG]: 次のメッシュ の UVSet の名前が map1 ではありません")
            self.storeResult(u"■ モデル - 2 [NG]: 次のメッシュ の UVSet の名前が map1 ではありません")             
            indexNG = self.diffRemoveList(indexNG)            
            for i in indexNG:
                self.storeResult(self.meshes[i])                
                print(self.meshes[i])                                   
            self.checkBoxColor('modelChckBox2', 1)  
            
#------------------------------#
# 3.頂点カラーチェック
#------------------------------#              

    def vtxColorCheck(self, key, *args):
        
        checked = False 
        vtxCol = False   
             
        verts = [] 
        vtxCount = ''
        vertsName = '' 

        tmpRGB = []
                
        i = 0    
        errCountA = 0  
        errCountB = 0 
        errMesh = [] 
                                                   
        for a in self.meshes:    
            try:
                cmds.select(a, r = True)
                vtxCount = cmds.polyEvaluate( v = True )   
                               
                # polyColorPerVertex は 親子関係 になっていると正しく取得できないので注意。                       
                errCountA = 0
                while(i < vtxCount):                                                         
                    tmpRGB = cmds.polyColorPerVertex(str(a) + '.vtx[' + str(i) + ']', query = True, rgb = True)                        
                    for b in tmpRGB:

                        c = int(round(b))
                        if not c :                       
                            None                         
                        else:                        
                            errCountA += 1                            
                    i += 1                                                                                 
                     
            except ValueError:
                pass
            except RuntimeError:
                pass               
                         
            if errCountA:                                            
                errMesh.append(a)                 
                checked = False
                errCountB += 1                          
            else:  
                checked = True                                                                           
            
   
        if checked :
            if errCountB == 0:
                print(u"■ モデル - 3 [OK]: メッシュに頂点カラーは含まれていません") 
                self.storeResult(u"■ モデル - 3 [OK]: メッシュに頂点カラーは含まれていません")                 
                self.checkBoxColor('modelChckBox3', 0)
            else :
                print(u"■ モデル - 3 [NG]: 次のメッシュ に 頂点カラー が含まれています")
                self.storeResult(u"■ モデル - 3 [NG]: 次のメッシュ に 頂点カラー が含まれています")                                                       
                self.checkBoxColor('modelChckBox3', 1)
                for a in errMesh:
                    print(a)
                    self.storeResult(a)               
        else : 
            print(u"■ モデル - 3 [NG]: 次のメッシュ に 頂点カラー が含まれています")
            self.storeResult(u"■ モデル - 3 [NG]: 次のメッシュ に 頂点カラー が含まれています")                                                       
            self.checkBoxColor('modelChckBox3', 1)
            for a in errMesh:
                print(a)
                self.storeResult(a)  
                                            
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
            print (u"■ ジョイント - 1 [OK]: ジョイント名の _l に対する _r は同数です")
            self.storeResult(u"■ ジョイント - 1 [OK]: ジョイント名の _l に対する _r は同数です")               
            checked = True
            self.checkBoxColor('jointChckBox1', 0)             
        else:
            for b in lJoints:
                reLJoints.append(b[:-2])
            for c in rJoints:          
                reRJoints.append(c[:-2])  
                   
            dupliList = self.makeUniqList(reLJoints, reRJoints)
            print (u"■ ジョイント - 1 [NG]: 次の ジョイント名 の _l と _r が同数になっていません")
            self.storeResult(u"■ ジョイント - 1 [NG]: 次の ジョイント名 の _l と _r が同数になっていません")              
            self.checkBoxColor('jointChckBox1', 1)             
            for d in dupliList:
                print (d)                
                self.storeResult(d)                      
                
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
            self.storeResult(u"■ ジョイント - 2 [OK]: すべての ジョイント の JointOrient は 0 です")              
            self.checkBoxColor('jointChckBox2', 0)                                     
        else:                                                      
            print (u"■ ジョイント - 2 [NG]: 次の ジョイント の JointOrient が 0 になっていません")
            self.storeResult(u"■ ジョイント - 2 [NG]: 次の ジョイント の JointOrient が 0 になっていません")               
            indexNG = self.diffRemoveList(indexNG)
            self.checkBoxColor('jointChckBox2', 1)         
            for i in indexNG:
                print(self.joints[i])                     
                self.storeResult(self.joints[i])             
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
            self.storeResult(u"■ ジョイント - 2 [OK]: すべての ジョイント の Translate の リミット は OFF です")                                                 
        else:                                                      
            print (u"■ ジョイント - 2 [NG]: 次の ジョイント の Translate に リミット が指定されています") 
            self.storeResult(u"■ ジョイント - 2 [NG]: 次の ジョイント の Translate に リミット が指定されています")              
            trnsIndexNG = self.diffRemoveList(trnsIndexNG)               
            for i in trnsIndexNG:
                print(self.joints[i])    
                self.storeResult(self.joints[i])
                
        if not rotIndexNG:
            rotChecked = True 
            print (u"■ ジョイント - 2 [OK]: すべての ジョイント の Rotate の リミット は OFF です")
            self.storeResult(u"■ ジョイント - 2 [OK]: すべての ジョイント の Rotate の リミット は OFF です")                                       
        else:                                                      
            print (u"■ ジョイント - 2 [NG]: 次の ジョイント の Rotate に リミット が指定されています")
            self.storeResult(u"■ ジョイント - 2 [NG]: 次の ジョイント の Rotate に リミット が指定されています")                
            rotIndexNG = self.diffRemoveList(rotIndexNG)
            for i in rotIndexNG:
                print(self.joints[i]) 
                self.storeResult(self.joints[i])
                
        if trnsChecked and rotChecked:
            self.checkBoxColor('jointChckBox3', 0)                             
        else:
            self.checkBoxColor('jointChckBox3', 1)      
            
#------------------------------#
# 4. X軸ねじれ チェック (※ 構造が枝分かれしない前提)
#------------------------------#             
    def jntsTwistCheck(self, key, *args):
        
        checked = True  
        errCount = 0             
        
        rootJnt = []
        hrchyJnt = []
        errJnt = []

        i = 0
        j = 0
        k = 0
        l = 0
        m = 0

        for a in self.joints:
            rootJnt.append(self.uniToStr(self.getHierarchyRootJoint(a)))
            
        rootJnt = self.diffRemoveList(rootJnt)   
        
        # root Joint 取得
        for b in rootJnt: 
            cmds.select(b)       
            hrchyJnt.append(cmds.listRelatives(ad = True))        
        cmds.select(cl = True)   
        # root Joint と chilld Joint を hrchyJnt　にネストして階層ごとに格納 
        for x in hrchyJnt:
            hrchyJnt[i].append(rootJnt[i])
            i += 1             
               
        rotateXVal = [[] for _ in xrange(len(rootJnt))] 
        subXVal = []
        errJnt = []
                 
        # hrchyJnt の　joint　から rotate X 値を取得                     
        for c in hrchyJnt:
            for jnt in c:
                rotateXVal[j].append(cmds.getAttr(str(jnt) + '.rotateX' ))                   
            j += 1
            
        # rotateXVal の 各ネスト内の 値同士の差を取得して subXVal に格納
        for d in rotateXVal:
            subXVal.append( [abs(j-i) for i,j in zip(d, d[1:])])
            # root Joint は 値が入っていても 0.0 扱いとして最後に追加(また、ジョイント名をリストする際にインデックス指定を合わせる)
            subXVal[k].append(float(0.0))
            k += 1
        
        for e in subXVal:
            for f in e:
                if f != 0.0: 
                    errJnt.append(hrchyJnt[l][m])
                    errCount += 1
                else:                                       
                    pass
                m += 1                    
            l += 1 
            m = 0                        
                  
        print ('rotateX : ' + str(rotateXVal ))
        print ('substract rotateX : ' + str(subXVal ))

        if errCount == 0:
            print(u"■ ジョイント - 2 [OK]: mant/tail/hair が存在しない or すべての mant/tail/hair ジョイントの Rotate:X は 子供 の方向を向いています")
            self.storeResult(u"■ ジョイント - 2 [OK]: mant/tail/hair が存在しない or すべての mant/tail/hair ジョイントの Rotate:X は子供 の方向を向いています")              
            checked = True                                       
        else:                                                      
            print(u"■ ジョイント - 3 [NG]: 次の ジョイント の階層で Rotate:X がねじれています")     
            self.storeResult(u"■ ジョイント - 3 [NG]: 次の ジョイント の階層で Rotate:X がねじれています")                      
            for i in errJnt:
                print i
                self.storeResult(i)
            checked = False                
   
        if checked:
            self.checkBoxColor('jointChckBox4', 0)                             
        else:
            self.checkBoxColor('jointChckBox4', 1)     
         
        
         
#-----------------------------------------------------------------------------------                 
charaChecker = CharaChecker()
charaChecker.create()