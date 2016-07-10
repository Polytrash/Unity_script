# -*- coding: utf-8 -*-
# 最終更新:2016/1/6

# import maya
import sys
import traceback
import shutil
import glob
import os
import pymel.core as pm
import maya.cmds as cmds

class smProjectBackupManager():

# 初期化

	def __init__(self):
		self.window = 'backupManager'
		self.title = 'Project Backup Manager'
		self.backupPath = ''
		self.projectName = ''
		self.size = (380, 250)
		self.width = 385;
		self.height = 250;
		self.deleteDirList = ["\\assets", "\\autosave", "\\cache", "\\clips", "\\data", "\\images",
		                      "\\movies", "\\renderData", "\\scenes", "\\scripts", "\\sound", "\\sourceimages"] 
		                      
		self.pathText = ''
		self.sceneName = ''
		self.texFiles = []

#===================================================================================	       	
# GUIの定義

# ファイル参照ウィンドウの定義
#===================================================================================

	def create(self):
	    
		if(cmds.window('backupManager', exists = True)):
			cmds.deleteUI('backupManager');


#===================================================================================    									    
# フォルダ参照ウィンドウの定義        
#===================================================================================   

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size, rtf = True)		
		self.frameName = cmds.frameLayout(label = u"Mayaプロジェクトのバックアップを保存します",borderStyle='out', bgc = (0.2, 0.2, 0.6))
		self.columnForm = cmds.columnLayout();


		self.rowForm =	cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)])	
		self.backupPathText = cmds.text(u"■ バックアップ先", font = 'smallBoldLabelFont', align = 'left')
		
		try:
			self.pathText = cmds.textField(self.chosenPath, editable =False);
		except:
			self.pathText = cmds.textField(text = self.backupPath, editable =False)

		self.chosenButton = cmds.button(label = u"参照" , command = self.chosenPath)
		
		cmds.setParent('..');
		cmds.separator (h = 10, w = self.width, style = "in") 
					
		self.rowForm =	cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 280)])
		self.projNametext = cmds.text(u"■ プロジェクト名", font = "smallBoldLabelFont", align = 'left')
		self.projNameField = cmds.textField("projectNameF", text = self.getCurrentSceneName1(), width =300)
		cmds.setParent('..')		
		cmds.separator (h = 10, w = self.width, style = "in") 

		self.projNametext = cmds.text(u"■ バックアッププロジェクトに残すフォルダ", font = "smallBoldLabelFont", align = 'left');		
		self.dltDirCheckBox1 = pm.checkBoxGrp('dltDirCheckB1', labelArray3 = (u"assets",  u"autosave", u"cache"), value1 = False, v2 = False, v3 = False, numberOfCheckBoxes = 3)
		self.dltDirCheckBox2 = pm.checkBoxGrp('dltDirCheckB2', labelArray3 = (u"clips",  u"data", u"images"), v1 = False, v2 = False, v3 = False, numberOfCheckBoxes = 3)		
		self.dltDirCheckBox3 = pm.checkBoxGrp('dltDirCheckB3', labelArray3 = (u"movies",  u"renderData", u"scenes"), v1 = False, v2 = False, v3 = True, numberOfCheckBoxes = 3)
		self.dltDirCheckBox4 = pm.checkBoxGrp('dltDirCheckB4', labelArray3 = (u"scripts",u"sound",  u"sourceimages"), v1 = False, v2 = False, v3 = True, numberOfCheckBoxes = 3)				

		cmds.separator (h = 10, w = self.width, style = 'in') 	
			
		self.executeButton = cmds.button(label = u"バックアップ実行", command = self.projectBackup_execute, width = self.width)
		
		cmds.text(u"【問い合わせ先】：TAセクション.村岡", bgc = (0.2, 0.2, 0.2), align = 'left', width = self.width)
		cmds.setParent("..")
		cmds.setParent("..")
		cmds.showWindow()
		
	def chosenPath(self, *args):
		try:
			dialogText = cmds.fileDialog2(fm=3, ds=2, cap= 'Open', okc = u"保存先に設定")
			uniToStr=str(dialogText)
			filePath = uniToStr.split("'")[1]
		except Exception:
			print(u" Info: IndexError: Tool <Project Backup Manager> [参照がキャンセルされました]")			
		else:					
			fPath = cmds.textField(self.pathText, edit=True, text=unicode(filePath))
			# ユーザーが設定するパス global newName
			global	userPath 
			userPath = filePath
			print('current userPath -> ' + userPath)		

#===================================================================================
# フォルダ参照ウィンドウの定義
#===================================================================================	
	def browse(self, *args):
		self.browsePathDialog = u""
			  
		# ※fileDialog2 から textFieldGrp への入力をどうするか
			  
		self.browsePathDialog = pm.fileDialog2(fm=3, okc='selectFolder', cap='Select Export Folder')[0]
		pm.optionVar['pbExportPath'] = self.browsePathDialog
		
		self.browsePathDialog = str(self.browsePathDialog)
		self.browsePathDialog = self.browsePathDialog.replace("[u'", "").replace("']", "").replace("/", "\\")
		
		cmds.textFieldButtonGrp(self.browsePath, query = True, text = True)
			
		self.backupPath = unicode(self.browsePathDialog)      
		print(self.browsePathDialog)


#===================================================================================
# 確認ウィンドウの定義
#===================================================================================

	def confirm(self, finalBackupPath):
		self.confirmWindow = cmds.confirmDialog(title = "Backup Manager",m = finalBackupPath + u"\nバックアップ完了", ma = "center", b = "OK")	

	def pathAlert(self,finalBackupPath):
		self.confirmWindow = cmds.confirmDialog(title = "Backup Manager",m = finalBackupPath + u"\nバックアップ先が指定されていません", ma = "center", b = "OK")	

	def existAlert(self, finalBackupPath):
		self.confirmWindow = cmds.confirmDialog(title = "Backup Manager",m = finalBackupPath + u"\nバックアップ先が既に存在しています", ma = "center", b = "OK")	


#===================================================================================
# プロジェクト名　(self.projNameField)取得用 シーン名取得メソッドの定義	
#===================================================================================

	def getCurrentSceneName1(self, *args):

		currentSceneName = cmds.file(q = True, sceneName = True)
		sceneWorkSpaceName = currentSceneName.replace('/', '\\')	
		print sceneWorkSpaceName	
		sceneNameSplitted = str(sceneWorkSpaceName).split('\\')[-1]
		print sceneNameSplitted
		
		finalSceneName = sceneNameSplitted.split(".")[0]
		
		return finalSceneName
		
		
#===================================================================================
# シーン名取得メソッドの定義	
#===================================================================================

	def getCurrentSceneName(self, *args):

		currentSceneName = cmds.file(q = True, sceneName = True)
		sceneWorkSpaceName = currentSceneName.replace('/', '\\')		
		sceneNameSplitted = str(sceneWorkSpaceName).split('\\')[-1]
		
		#シーン削除ルールをもっとゆるくしたい場合、プロジェクト名取得と同様に以下を使用する
		#finalSceneName = sceneNameSplitted.split(".")[0]
		
		self.sceneName = sceneNameSplitted
		
		
#===================================================================================
# シーンファイル削除メソッドの定義		
#===================================================================================

	def removeScenes(self, *args):
	    
		allSceneFiles = []
		   

		sourcePath = ''.join(unicode(self.backupPath))
		scenesDir = sourcePath + '\\scenes\\*.*'
		scenesWorkspaceName = str(scenesDir.replace('/', '\\'))

		allSceneFiles = glob.glob(scenesWorkspaceName)
		
		
		print u"[ 使用していないシーンファイルを scene から削除 ]"		
		
		for filePath in allSceneFiles:				
			if os.path.exists(filePath):
				if not self.sceneName in filePath:
					os.remove(filePath) 	
					print(u'Delete Scene ： ' + filePath)
				else:
					pass
	

#===================================================================================
# テクスチャファイルリスト取得メソッドの定義
#===================================================================================	

	def getTexturePath(self, *args): 
		fileNameList = []
		texFilePath = []

		fileList = cmds.ls(type='file')


		for file in fileList:
			fileName = cmds.getAttr(file + '.fileTextureName')
			fileNameList.append(fileName)

			for tex in fileNameList:
				texName = os.path.basename(tex)
				texNameSplitted = os.path.splitext(texName)[0]
				self.texFiles.append(texNameSplitted)

			
		#print self.texFiles	
			
		
#===================================================================================
# テクスチャファイル削除メソッドの定義
# ※ texList は self.getTexturePath() で取得したシーン上のテクスチャを指定
#===================================================================================
	def removeTextures(self, texList):
	    
		i = 0
		bool = True
		
		sceneTexList = []
		allTexList = []
		

		   
		for tex in texList:
			texWorkSpaceName = tex.replace('/', '\\')
			texNameSplitted = str(texWorkSpaceName).split('\\')[-1]
			finalTexName = texNameSplitted.split(".")[0]
			sceneTexList.append(finalTexName)

		sourcePath = ''.join(unicode(self.backupPath))
		sourceImgDir = sourcePath + '\\sourceimages\\*.*'
		sourceImgWorkspaceName = str(sourceImgDir.replace('/', '\\'))

		allFiles = glob.glob(sourceImgWorkspaceName)


		for fileName in allFiles: 
			fileNameSplitted = fileName.split('\\')
			finalFileName = str(fileNameSplitted[-1]).split('.')[0]
			allTexList.append(finalFileName)


		setList = set(allTexList) - set(sceneTexList)
		diffList = set(setList)
		
		print u"[ 使用していないテクスチャ/ファイルを sourceimages から削除 ]"		
		
		for filePath in allFiles:
		    for diff in diffList:
		        bool = diff in filePath
		        if os.path.exists(filePath):
		            if bool == True:
		                os.remove(filePath)
		                print("Deleted Texture ：" + filePath)
		        else:
		            pass
		    else:
		        pass

#===================================================================================
# ユーザー入力メソッドの定義		
#===================================================================================

    # バックアップ先
		
	def backupPathField_input(self):
		self.backupPathInput = cmds.textFieldButtonGrp("backupF", query = True, text = True)	
		return self.backupPathInput

    # プロジェクト名

	def projectBackupField_input(self):
		self.projectBackupInput = cmds.textField("projectNameF", query = True, text = True)	
		return self.projectBackupInput 

    # カレントプロジェクトのフルパス

	def getCurrentProjectName(self, *args):
		currentWorkspace = cmds.workspace(query = True, fullName = True)
		strCurrentWorkspace = ''.join(currentWorkspace)
		return strCurrentWorkspace		

    # バックアップ用プロジェクトから削除するフォルダ

    # 0:assets / 1:autosave / 2:cache 

	def dltDirCheckBox11_input(self):
		if pm.checkBoxGrp("dltDirCheckB1", query = True, value1 = True):
		    pass
		else:			
			deleteElements = self.backupPath + self.deleteDirList[0]
			shutil.rmtree(deleteElements) 	
			print(u"Delete Folder： " + deleteElements)


	def dltDirCheckBox12_input(self):
		if cmds.checkBoxGrp("dltDirCheckB1", query = True, value2 = True):	
		    pass
		else:	
			deleteElements = self.backupPath + self.deleteDirList[1];
			shutil.rmtree(deleteElements)
			print(u"Delete Folder： " + deleteElements)
			
	def dltDirCheckBox13_input(self):
		if cmds.checkBoxGrp("dltDirCheckB1", query = True, value3 = True):
		    pass
		else:	
			deleteElements = self.backupPath + self.deleteDirList[2];
			shutil.rmtree(deleteElements) 	
			print(u"Delete Folder： " + deleteElements)			               	

    # 3:clips / 4:data / 5:movies

	def dltDirCheckBox21_input(self):
		if pm.checkBoxGrp("dltDirCheckB2", query = True, value1 = True):
		    pass
		else:		
			deleteElements = self.backupPath + self.deleteDirList[3]
			shutil.rmtree(deleteElements)
			print(u"Delete Folder： " + deleteElements);
			
	def dltDirCheckBox22_input(self):
		if pm.checkBoxGrp("dltDirCheckB2", query = True, value2 = True):
		    pass
		else:		
			deleteElements = self.backupPath + self.deleteDirList[4]
			shutil.rmtree(deleteElements) 	
			print(u"Delete Folder： " + deleteElements);			
			
	def dltDirCheckBox23_input(self):
		if pm.checkBoxGrp("dltDirCheckB2", query = True, value3 = True):
		    pass
		else:		
			deleteElements = self.backupPath + "\\images";
			shutil.rmtree(deleteElements) 	
			print(u"Delete Folder： " + deleteElements);	

    # 6:renderData / 7:scenes / 8:scripts

	def dltDirCheckBox31_input(self):
		if pm.checkBoxGrp("dltDirCheckB3", query = True, value1 = True):	
			pass
		else:	
			deleteElements = self.backupPath + "\\movies";
			shutil.rmtree(deleteElements); 	
			print(u"Delete Folder： " + deleteElements);			

	def dltDirCheckBox32_input(self):
		if pm.checkBoxGrp("dltDirCheckB3", query = True, value2 = True):	
			pass
		else:	
			deleteElements = self.backupPath + "\\renderData";
			shutil.rmtree(deleteElements); 	
			print(u"Delete Folder： " + deleteElements);			

	def dltDirCheckBox33_input(self):
		if pm.checkBoxGrp("dltDirCheckB3", query = True, value3 = True):	
			pass
		else:	
			deleteElements = self.backupPath + "\\scenes";
			shutil.rmtree(deleteElements); 	
			print(u"Delete Folder： " + deleteElements);	
					
    # 9:scripts / 10:sound / 11:sourceimages

	def dltDirCheckBox41_input(self):
		if pm.checkBoxGrp("dltDirCheckB4", query = True, value1 = True):
		    pass
		else:	
			deleteElements = self.backupPath + "\\scripts";
			shutil.rmtree(deleteElements); 	
			print(u"Delete Folder： " + deleteElements);			

	def dltDirCheckBox42_input(self):
		if pm.checkBoxGrp("dltDirCheckB4", query = True, value2 = True):
		    pass
		else:	
			deleteElements = self.backupPath + "\\sound";
			shutil.rmtree(deleteElements); 	
			print(u"Delete Folder： " + deleteElements);	
			
	def dltDirCheckBox43_input(self):
		if pm.checkBoxGrp("dltDirCheckB4", query = True, value3 = True):
		    pass
		else:	
			deleteElements = self.backupPath + "\\sourceimages";
			shutil.rmtree(deleteElements); 	
			print(u"Delete Folder： " + deleteElements);		

#===================================================================================			
# 処理メソッドの定義		
#===================================================================================

    # 不要なフォルダ削除メソッド		  
			
			
    # プロジェクトのバックアップメソッド
	def projectBackup_execute(self, *args):
	    
		# カレントワークスペースのフルパスを取得、ただしバックスラッシュ対応が必要
		
		currentWorkspaceName = self.getCurrentProjectName();
		print(currentWorkspaceName)
		sourceWorkspaceName = currentWorkspaceName.replace("/", "\\");
		self.backupPath = sourceWorkspaceName		

				
		if sourceWorkspaceName != sourceWorkspaceName.startswith("default"):
		    sourceWorkspaceName = sourceWorkspaceName.replace("default", ""); 
		    
		
		    # 最終的なバックアップ先を取得		
		
		    # 1.パスを取得   
		    modifiedPath =	userPath;	
		
		    # 2.プロジェクト名を取得
		    self.projName = "\\" + self.projectBackupField_input();
		    self.projectName = self.projName;

		    # 3.最終的なパスを取得
		    finalPath = modifiedPath.replace("/", "\\") + self.projName;	
		    self.backupPath = finalPath;
		    # if 既にプロジェクトが存在している
		    if os.path.exists(finalPath):
		        # アラート    
		        confirmCheck = self.existAlert(self.backupPath);  		    

		    # if バックアップ先が正しく指定されている
		    
		    if os.path.exists(userPath):
		        print u"[プロジェクトのバックアップ開始]"		    	
		        print(sourceWorkspaceName + " =======> " + finalPath);

		    # バックアップ実行
		        
		    shutil.copytree(sourceWorkspaceName , finalPath);
		    #print(self.projectName);
		    
		    # バックアップに不必要なフォルダを削除   
		    
		    print u"[ 不必要なフォルダをバックアッププロジェクトから削除 ]"	
		    
		    self.assets = self.dltDirCheckBox11_input();
		    self.autosave = self.dltDirCheckBox12_input(); 
		    self.cache = self.dltDirCheckBox13_input(); 
		    self.clips = self.dltDirCheckBox21_input();                                                
		    self.data = self.dltDirCheckBox22_input(); 
		    self.movies = self.dltDirCheckBox23_input(); 
		    self.renderData = self.dltDirCheckBox31_input(); 
		    self.scenes = self.dltDirCheckBox32_input(); 
		    self.scripts = self.dltDirCheckBox33_input();                                                                 
		    self.sound = self.dltDirCheckBox41_input();                                                                 
		    self.sourceimages = self.dltDirCheckBox42_input();   
		    
		    # 確認メッセージ      		                                                             	                                            
		    confirmCheck = self.confirm(self.backupPath);   
		                             
		# if バックアップ先が正しく指定されていない
		else:
		    print(u"バックアップ先が正しく指定されていません")		    
		    # アラート
		    confirmCheck = self.pathAlert(self.backupPath);   
		    
		# scenes から 使用していないシーンファイルを削除
		self.getCurrentSceneName()    
		self.removeScenes()
						    
		# sourceimages から 使用していないテクスチャファイルを削除		    
		self.getTexturePath()                                   
		self.removeTextures(self.texFiles)
		
#---------------------------------------------------------------------------------------------#

#実行
ProjectBackupManagerWindow = smProjectBackupManager()
ProjectBackupManagerWindow.create()