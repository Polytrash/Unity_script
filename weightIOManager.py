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
			
# GUI���\�b�h�̐錾		
	
		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		
# �E�F�C�g�����o�����\�b�h�̒�`
		
		self.frameForm = cmds.frameLayout(label = "�E�F�C�g�l�̏����o��", bgc = (0.7, 0.3, 0.1), cll = True);

		self.fileNametext = cmds.text("1.�����o���t�@�C�����Ə����o�����ݒ�", bgc = (0.35, 0.35, 0.35));

		self.columForm = cmds.columnLayout();
		self.fileNametext = cmds.text("�t�@�C����");
		self.fileNameField = cmds.textField("exportFileNameF", text = "ch_weight.csv", width = self.width);
		cmds.setParent("..")
		self.columForm = cmds.columnLayout();				
		self.savePathText = cmds.text("�ۑ���");
		self.savePathField = cmds.textField("savePathF", text = "D:/maya", width = self.width);	
		cmds.setParent("..")
		
		self.fileNametext = cmds.text("2.�ΏۃI�u�W�F�N�g��I��", bgc = (0.35, 0.35, 0.35));
		self.executeButton1 = cmds.button(label = "�����o��");
		cmds.setParent("..")
# �E�F�C�g�ǂݍ��݃��\�b�h�̒�`
		
		self.frameForm = cmds.frameLayout(label = "�E�F�C�g�l�̓ǂݍ���", bgc = (0.1, 0.3, 0.7), cll = False);	

		self.fileNametext = cmds.text("1.�ǂݍ��݃t�@�C�����w��", bgc = (0.35, 0.35, 0.35));
		
		self.fileNameField = cmds.textField("importFileNameF", text = "ch_weight.csv", width = self.width);
		self.fileNametext = cmds.text("2.�ΏۃI�u�W�F�N�g��I��", bgc = (0.35, 0.35, 0.35));
		self.executeButton2 = cmds.button(label = "�ǂݍ���");
					
		cmds.text("�y�₢���킹��z", bgc = (0.2, 0.2, 0.2), align = 'left');

		cmds.setParent("..")	
		cmds.showWindow();	
		
# ���[�U�[���̓��\�b�h�̒�`

	def fileNameField_input(self):	
		self.fileNameInput = cmds.textField("exportFileNameF", query = True, text = True);	
		return self.fileNameInput; 
		
	def savePathField_input(self):
		self.savePathInput = cmds.textField("savePathF", query = True, text = True);
		return self.savePathInput;		
		
	def fileNameField_input(self):	
		self.fileNameInput = cmds.textField("importFileNameF", query = True, text = True);	
		return self.fileNameInput; 	
		
# �������\�b�h�̒�`
			

# ���s����	

testWindow = weightIOManager();
testWindow.create();