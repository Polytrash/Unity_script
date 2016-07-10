# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
import string as st
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
      
        # �����o���p
        self.exportObjNameList = []
        self.transform = []

        # �ǂݍ��ݗp
        self.importObjCount = 0
        self.importObjNameList = []
        self.objPosition = []
        self.objRotation = []
        self.objScale = []

    def create(self):

        if cmds.window('objectTransformExporterWindow', exists = True):
            cmds.deleteUI('objectTransformExporterWindow')

#-----------------------------------------------------------------------------------
# 1.�g�����X�t�H�[���������o���I�u�W�F�N�g��I��
#-----------------------------------------------------------------------------------  


        self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
        self.frameFrm1 = cmds.frameLayout(label = u"1.�g�����X�t�H�[���������o���I�u�W�F�N�g��I��", bgc = (0.5, 0.25, 0.3), cll = True)

        self.srchBtn = cmds.button( l = u"���X�g�ɒǉ�", command = self.nameSearch, height = 30 )
        
        self.textScllist = cmds.textScrollList('objL', ams = True, dkc = self.removeAt)
        cmds.separator (h = 10, w = self.width, style = 'in') 


        cmds.setParent('..')     

#-----------------------------------------------------------------------------------
# 2.XML�t�@�C���������o��
#-----------------------------------------------------------------------------------  
                      
        self.frameFrm2 = cmds.frameLayout(label = u"2.XML�t�@�C���������o��", bgc = (0.5, 0.25, 0.3), cll = True)

        self.rowForm1 =	cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)])
        self.exportPathText = cmds.text(u"�p�X�̎w��", font = 'smallBoldLabelFont', align = 'left')


        try:
            self.pathText1 = cmds.textField(self.chosenPath, editable =False);
        except:
            self.pathText1 = cmds.textField(text = self.exportPath, editable =False)  

        self.chosenButton1 = cmds.button(label = u"�Q��" , command = self.chosenPath)
        

        cmds.setParent('..')    

        self.exportFileNameText = cmds.text(u"�t�@�C����", font = 'smallBoldLabelFont', align = 'left')          
        self.fileNameFld = cmds.textField('fileNameF1')

        self.exportXmlBtn = cmds.button(l = u"�����o��",command = self.getTransform, height = 30)


#-----------------------------------------------------------------------------------
# 3.XML�t�@�C����ǂݍ���
#-----------------------------------------------------------------------------------

        self.frameFrm3 = cmds.frameLayout(label = u"3.XML�t�@�C����ǂݍ���", bgc = (0.5, 0.25, 0.3), cll = True)

        self.rowForm2 =	cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)])
        self.importPathText = cmds.text(u"�t�@�C���̎w��", font = 'smallBoldLabelFont', align = 'left')


        try:
            self.pathText2 = cmds.textField(self.chosenPath, editable =False);
        except:
            self.pathText2 = cmds.textField(text = self.exportPath, editable =False)  

        self.chosenButton2 = cmds.button(label = u"�Q��" , command = self.chosenFile)


        cmds.setParent('..')

        self.importXmlBtn = cmds.button(l = u"�ǂݍ���/�X�V",command = self.setTransform, height = 30)

        
        cmds.setParent('..')


        cmds.showWindow()

#===================================================================================
# �ėp���\�b�h�̒�`
#===================================================================================
     
#-----------------------------------------------------------------------------------
# �G���[�`�F�b�N	
#----------------------------------------------------------------------------------- 

    def errorCheck(self, key, val, *args):

        if not val:
            print ("XML�t�@�C����" + str(key) + " �� " + str(val) + " �l�������Ă��܂���")

        elif val == '':
            print ("XML�t�@�C����" + str(key) + " �� " + str(val) + " �l�������Ă��܂���")
        else:
            return val  

    
#===================================================================================
# �����o���t�H���_�Q�ƃ��\�b�h�̒�`
#===================================================================================

    def chosenPath(self, *args):
        try:
            dialogText = cmds.fileDialog2(fm=3, ds=2, cap= 'Open', okc = u"�I��")
            uniToStr=str(dialogText)
            dirPath = uniToStr.split("'")[1]
        except Exception:
            print(u" Info: Export Folder Reference Error: Tool <Object Transform Exporter> 142")			
        else:					
            fPath = cmds.textField(self.pathText1, edit=True, text=unicode(dirPath))
            self.dirPath = dirPath
            print('current userPath -> ' + self.dirPath)	
 

#===================================================================================
# �ǂݍ��݃t�@�C���Q�ƃ��\�b�h�̒�`
#===================================================================================

    def chosenFile(self, *args):
        try:
            dialogText = cmds.fileDialog2(fm=4, ds=2, cap= 'Open', okc = u"�I��")
            uniToStr=str(dialogText)
            filePath = uniToStr.split("'")[1]
        except Exception:
            print(u" Info: Import File Reference Error: Tool <Object Transform Exporter> 159")			
        else:					
            fPath = cmds.textField(self.pathText2, edit=True, text=unicode(filePath))
            self.filePath = filePath
            print('current userFile -> ' + self.filePath)            
            
                                  	
#===================================================================================
# ���[�U�[���̓��\�b�h�̒�`	
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
        
                    print("Already exist in the list.") 
                
                else:

                    self.exportObjNameList.append(selection[i])
                    cmds.textScrollList(self.textScllist, e = True , append = selection[i])
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
# �Q�b�g�g�����X�t�H�[��(�����o���Ɏg�p)	
#=================================================================================== 

    def getTransform(self, *args):


        # �����o����p�X�̎擾

        dirPath = self.dirPath
        
        sourceWorkspaceName = dirPath.replace("/", "\\\\") + "\\\\"
        
        fileName = cmds.textField('fileNameF1', query =True, text = True)
        
        exportXml = sourceWorkspaceName + fileName + ".xml"

        print exportXml



        # XML �����o��

        root = Element('UserData')

        root.set('version', '1.0')
        root.append(Comment('Generated at :'))
        

        tree = et.ElementTree(root)

        # �I�u�W�F�N�g������g�����X�t�H�[���擾

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
# �g�����X�t�H�[�������o��
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


        # �I�u�W�F�N�g��
        object = SubElement(root, 'object', id = name)
        position = SubElement(object, 'position')
        rotation = SubElement(object, 'rotation')
        scale = SubElement(object, 'scale')

        # �ړ��l        
        for p in object.iter('position'):

            p.set('X', str(pos[0]))
            p.set('Y', str(pos[1]))
            p.set('Z', str(pos[2]))

        # ��]�l
        for r in object.iter('rotation'):

            r.set('X', str(rot[0]))
            r.set('Y', str(rot[1]))
            r.set('Z', str(rot[2]))
            
        # �X�P�[���l
        for s in object.iter('scale'):

            s.set('X', str(scl[0]))
            s.set('Y', str(scl[1]))
            s.set('Z', str(scl[2]))
                    

#===================================================================================
# �Z�b�g�g�����X�t�H�[��(�ǂݍ��݂Ɏg�p)
#===================================================================================    

    def setTransform(self, *args):

        filePath = self.filePath
        sourceFileName = filePath.replace("/", "\\")
        print sourceFileName

        # XML�I�u�W�F�N�g�쐬
        tree = et.parse(sourceFileName)
        root = tree.getroot()

        # XML�̏����O���[�o�����X�g�ɂ��ꂼ��i�[
        for object in root.iter('object'):
            self.importObjNameList.append(object.attrib)

                           
            for position in object.iter('position'):
                self.objPosition.append(position.attrib)


            for rotation in object.iter('rotation'):
                self.objRotation.append(rotation.attrib)


            for scale in object.iter('scale'):
                self.objScale.append(scale.attrib)


        # �ǂݍ��ݏ��̊m�F�p�v�����g
        print "Imported Data List:"
        print ( self.importObjNameList)
        print ( self.objPosition)
        print ( self.objRotation)
        print ( self.objScale)

   
        #�g�����X�t�H�[�����s
        self.transformObject()
        
   
#===================================================================================
# �g�����X�t�H�[�����s	
#===================================================================================    

    def transformObject(self, *args):
        
        positionList = {}
        rotationList = {}
        scaleList = {}
        i = 0      

        cmds.select(cl = True)

        for n in self.importObjNameList:

            n = str(n['id']) 
          
            # �O���[�o�����X�g�̊e�l�����[�J�������Ɋi�[                     
            positionList = self.objPosition[i]
            rotationList = self.objRotation[i]
            scaleList = self.objScale[i]
            
            # �ʒu(�L�[�ŃI�u�W�F�N�g������)
            xPos = positionList["X"]
            yPos = positionList["Y"]
            zPos = positionList["Z"]

            # ��](�L�[�ŃI�u�W�F�N�g������)
            xRot = rotationList["X"]
            yRot = rotationList["Y"]
            zRot = rotationList["Z"]

            # �X�P�[��(�L�[�ŃI�u�W�F�N�g������)
            xScl = scaleList["X"]
            yScl = scaleList["Y"]
            zScl = scaleList["Z"]

            # �g�����X�t�H�[�����v�����g
            print "-----------------------------------------------------------------------"
            print ("Name : " + n)
            print ("Position: ")
            print ("X : " + xPos + " Y : " + yPos + " Z : " + zPos)
            print ("Rotation: ")
            print ("X : " + xRot + " Y : " + yRot + " Z : " + zRot)
            print ("Scale: ")
            print ("X : " + xScl + " Y : " + yScl + " Z : " + zScl)
            print "-----------------------------------------------------------------------"

            # �g�����X�t�H�[�����s

            try:
                cmds.select(str(n), r = True)
                cmds.xform(a = True, ws = True, ro = [float(xRot), float(yRot), float(zRot)], s = [float(xScl), float(yScl), float(zScl)], t = [float(xPos), float(yPos), float(zPos)])
            except Exception:
                print(u" Info: Value Empty Error: Tool <Object Transform Exporter> 422")	

            # ���[�J���������N���A
            positionList.clear()
            rotationList.clear()
            scaleList.clear()

            i +=1

        # ���̓ǂݍ��݂ɔ����ăO���[�o�����X�g�̒l���N���A
        del self.importObjNameList[:]
        del self.objPosition[:]
        del self.objRotation[:]
        del self.objScale [:] 
        
          
                 

objectPlacer = objectPlacement()

objectPlacer.create()