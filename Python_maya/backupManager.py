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
		
# GUI�̒�`

	def create(self):
		if(cmds.window('backupManager', exists = True)):
			cmds.deleteUI('backupManager');
		
		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		
		self.frameName = cmds.frameLayout(label = "�o�b�N�A�b�v��̎w��", bgc = (0.7, 0.3, 0.1), cll = True);

		self.columForm = cmds.columnLayout();
		self.fileNametext = cmds.text("1.�o�b�N�A�b�v��ƃv���W�F�N�g�����w��", bgc = (0.35, 0.35, 0.35));
		self.backupPathText = cmds.text("�o�b�N�A�b�v�̕ۑ���");
		self.backupPathField = cmds.textField("backupF", text = "backup Path", width = self.width);
		
		self.projNametext = cmds.text("�v���W�F�N�g��");
		self.projNameField = cmds.textField("projectNameF", text = "project Name", width = self.width);
		cmds.setParent("..");			
		
		self.executeButton = cmds.button(label = "���s", command = self.shutilTest);
		cmds.text("�y�₢���킹��z", bgc = (0.2, 0.2, 0.2), align = 'left');
		
		cmds.setParent("..");
		cmds.showWindow();
		

# ���[�U�[���̓��\�b�h�̒�`		
		
	def backupPathField_input(self):
		self.backupPathInput = cmds.textField("backupF", query = True, text = True);	
		return self.backupPathInput; 
		
	def projectBackupField_input(self):
		self.projectBackupInput = cmds.textField("projectNameF", query = True, text = True);	
		return self.projectBackupInput; 

# �J�����g�v���W�F�N�g�̃t���p�X���擾�A������List�Ȃ̂�''.join�ŕ�����ɕϊ�			
	
	def getCurrentProjectName(self, *args):
		self.currentWorkspace = cmds.workspace(listWorkspaces = True);
		strCurrentWorkspace = ''.join(self.currentWorkspace);
		return strCurrentWorkspace;

# shutil�ŃG���[���o�邽�߃e�X�g���\�b�h���`		
	
	def shutilTest(self, *args):
		
		shutil.copytree("D:\\maya\\project\\test", "abc"); 
			
# �������\�b�h�̒�`		
	
	def projectBackup_execute(self, *args):
		

	
		# �J�����g���[�N�X�y�[�X�̃t���p�X���擾�A�������o�b�N�X���b�V���Ή����K�v
		
		self.currentWorkspaceName = self.getCurrentProjectName();
		sourceWorkspaceName = self.currentWorkspaceName.replace("/", "\\");
		
		# �ŏI�I�ȃo�b�N�A�b�v����擾		
		
		# 1.�p�X���擾
		modifiedPath =	self.backupPathField_input();	
		#�@2.�v���W�F�N�g�����擾
		self.projName = self.projectBackupField_input();

		#�@3.�ŏI�I�ȃp�X���擾
		finalBackupPath = modifiedPath.replace("/", "\\") + "\\" + self.projName;	

		# �o�b�N�A�b�v���s
		shutil.copytree(sourceWorkspaceName , finalBackupPath);
		
		# �Ƃ肠�����e�X�g��images�t�H���_���w�肷�邪�A�ł����__init__()����List�Ŏw�肵����
		print(sourceWorkspaceName)		

		self.deleteElements = finalBackupPath + "\\images";
		
		# �o�b�N�A�b�v�ɕs�K�v�ȃt�H���_���폜
		os.rmdir(self.deleteElemnts);
		
		print("�o�b�N�A�b�v�����I")

testWindow = backupManager();
testWindow.create();
		
		

	
