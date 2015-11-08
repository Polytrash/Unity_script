# Weight IO Manager

import maya.cmds as cmds
class weightIOManager(object):
	
	def __init__(self):
		self.window = 'weightIOManager_12';
		self.title = 'Weight IO Manager';
		self.size = (320, 480);
		self.width = 320;
		self.height = 480;
		
	def create(self):
		
		if cmds.window('weightIOManger', exists = True):
			cmds.deleteUI('weightIOManager');
			
# GUIメソッドの宣言		
	
		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		
# ウェイト書き出しメソッドの定義
		
		self.frameForm = cmds.frameLayout(label = "ウェイト値の書き出し", bgc = (0.7, 0.3, 0.1), cll = True);

		self.fileNametext = cmds.text("1.書き出しファイル名と書き出し先を設定", bgc = (0.35, 0.35, 0.35));

		self.columForm = cmds.columnLayout();
		self.fileNametext = cmds.text("ファイル名");
		self.fileNameField = cmds.textField("exportFileNameF", text = "ch_weight.csv", width = self.width);
		cmds.setParent("..")
		self.columForm = cmds.columnLayout();				
		self.savePathText = cmds.text("保存先");
		self.savePathField = cmds.textField("savePathF", text = "D:/maya", width = self.width);	
		cmds.setParent("..")
		
		self.fileNametext = cmds.text("2.対象オブジェクトを選択", bgc = (0.35, 0.35, 0.35));
		self.executeButton1 = cmds.button(label = "書き出し");
		cmds.setParent("..")
# ウェイト読み込みメソッドの定義
		
		self.frameForm = cmds.frameLayout(label = "ウェイト値の読み込み", bgc = (0.1, 0.3, 0.7), cll = False);	

		self.fileNametext = cmds.text("1.読み込みファイルを指定", bgc = (0.35, 0.35, 0.35));
		
		self.fileNameField = cmds.textField("importFileNameF", text = "ch_weight.csv", width = self.width);
		self.fileNametext = cmds.text("2.対象オブジェクトを選択", bgc = (0.35, 0.35, 0.35));
		self.executeButton2 = cmds.button(label = "読み込み");
					
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left');

		cmds.setParent("..")	
		cmds.showWindow();	
		
# ユーザー入力メソッドの定義

	def fileNameField_input(self):	
		self.fileNameInput = cmds.textField("exportFileNameF", query = True, text = True);	
		return self.fileNameInput; 
		
	def savePathField_input(self):
		self.savePathInput = cmds.textField("savePathF", query = True, text = True);
		return self.savePathInput;		
		
	def fileNameField_input(self):	
		self.fileNameInput = cmds.textField("importFileNameF", query = True, text = True);	
		return self.fileNameInput; 	
		
# 処理メソッドの定義
			

# 実行命令	

testWindow = weightIOManager();
testWindow.create();