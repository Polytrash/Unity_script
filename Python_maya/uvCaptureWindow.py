#UV Capture 

import maya.cmds as cmds
class uvCaptureWindow(object):

# 初期化メソッド

	def __init__(self):
		self.window = 'uvCaptureWindow';
		self.title = 'UV Capture Window';
		self.size = (320, 240);
		self.width = 320;
		self.height = 200;


# GUIメソッドの宣言
	
	def create(self):
		if cmds.window('uvCaptureWindow', exists = True):
			cmds.deleteUI('uvCaptureWindow' );

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		self.frameForm = cmds.frameLayout(label = " UV の出力先を設定します", bgc = (0.3, 0.4, 0.1), cll = False);
		self.columForm = cmds.columnLayout();
		self.fileNametext = cmds.text("ファイル名");
		self.fileNameField = cmds.textField("fileNameF", text = "OutUV1.png", width = self.width);
		self.savePathText = cmds.text("保存先");
		self.savePathField = cmds.textField("savePathF", text = "D:/maya", width = self.width);	
		cmds.setParent("..")
		
		self.executeButton = cmds.button(label = "UVを撮影", command = self.uvCapture);
		
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left');
		
		cmds.setParent("..")	
		cmds.showWindow();


# ユーザー入力メソッドの定義

	def fileNameField_input(self):	
		self.fileNameInput = cmds.textField("fileNameF", query = True, text = True);	
		return self.fileNameInput; 
		
	def savePathField_input(self):
		self.savePathInput = cmds.textField("savePathF", query = True, text = True);
		return self.savePathInput;	
	

# 処理メソッドの定義
			
	def uvCapture(self, *args):	
		self.fName = self.fileNameField_input()
		
		modifiedPath =	self.savePathField_input();
		finalPath = modifiedPath.replace("/", "\\") + "\\" + self.fName;	
		
		cmds.uvSnapshot(aa = True, n = finalPath, o = True, xr = 1024, yr = 1024, r = 0, g = 0, b = 0, fileFormat = 'png');

# 実行命令	

testWindow = uvCaptureWindow();
testWindow.create();