import sys
import shutil
import os
import pymel.core as pm
import maya.cmds as cmds

class backupManager(object):

	def __init__(self):
		self.window = 'backupManager';
		self.title = 'Backup Manager';
		self.size = (320, 320);
		self.width = 320;
		self.height = 320;
		
# GUIの定義

	def create(self):
		if(cmds.window('backupManager', exists = True)):
			cmds.deleteUI('backupManager');
		
		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		
		self.frameName = cmds.frameLayout(label = "バックアップ先の指定", bgc = (0.7, 0.3, 0.1), cll = True);

		self.columForm = cmds.columnLayout();
		self.fileNametext = cmds.text("1.バックアップ先とプロジェクト名を指定", bgc = (0.35, 0.35, 0.35));
		self.backupPathText = cmds.text("バックアップの保存先");
		self.backupPathField = cmds.textField("backupF", text = "backup Path", width = self.width);
		
		self.projNametext = cmds.text("プロジェクト名");
		self.projNameField = cmds.textField("projectNameF", text = "project Name", width = self.width);
		cmds.setParent("..");			
		
		self.executeButton = cmds.button(label = "実行", command = self.shutilTest);
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left');
		
		cmds.setParent("..");
		cmds.showWindow();
		

# ユーザー入力メソッドの定義		
		
	def backupPathField_input(self):
		self.backupPathInput = cmds.textField("backupF", query = True, text = True);	
		return self.backupPathInput; 
		
	def projectBackupField_input(self):
		self.projectBackupInput = cmds.textField("projectNameF", query = True, text = True);	
		return self.projectBackupInput; 

# カレントプロジェクトのフルパスを取得、ただしListなので''.joinで文字列に変換			
	
	def getCurrentProjectName(self, *args):
		self.currentWorkspace = cmds.workspace(listWorkspaces = True);
		strCurrentWorkspace = ''.join(self.currentWorkspace);
		return strCurrentWorkspace;

# shutilでエラーが出るためテストメソッドを定義		
	
	def shutilTest(self, *args):
		
		shutil.copytree("D:\\maya\\project\\test", "abc"); 
			
# 処理メソッドの定義		
	
	def projectBackup_execute(self, *args):
		

	
		# カレントワークスペースのフルパスを取得、ただしバックスラッシュ対応が必要
		
		self.currentWorkspaceName = self.getCurrentProjectName();
		sourceWorkspaceName = self.currentWorkspaceName.replace("/", "\\");
		
		# 最終的なバックアップ先を取得		
		
		# 1.パスを取得
		modifiedPath =	self.backupPathField_input();	
		#　2.プロジェクト名を取得
		self.projName = self.projectBackupField_input();

		#　3.最終的なパスを取得
		finalBackupPath = modifiedPath.replace("/", "\\") + "\\" + self.projName;	

		# バックアップ実行
		shutil.copytree(sourceWorkspaceName , finalBackupPath);
		
		# とりあえずテストでimagesフォルダを指定するが、できれば__init__()内でListで指定したい
		print(sourceWorkspaceName)		

		self.deleteElements = finalBackupPath + "\\images";
		
		# バックアップに不必要なフォルダを削除
		os.rmdir(self.deleteElemnts);
		
		print("バックアップ完了！")

testWindow = backupManager();
testWindow.create();
		
		

	
