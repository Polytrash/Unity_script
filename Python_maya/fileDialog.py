import maya.cmds as cmds
import pymel.core as pm

class fileDialog2Test(object):

	def __init__(self):
		pass


	def create(self):
		if cmds.window('chosenWindow', exists = True):
			cmds.deleteUI('chosenWindow');
			
		def chosenFile(self, *args):
			chosenFileDialog = cmds.fileDialog2(fm=3, ds=2, cap="Open", okc="Select scene file")
			uniToStr=str(chosenFileDialog)
			filePath = uniToStr.split("'")[1]
			cmds.textField(pathText, edit=True, text=unicode(filePath))
			global newName
			newName=filePath
			print(newName)
			
		window = cmds.window('chosenWindow', title='open file', widthHeight = (300, 100), rtf = True)
		cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)] )

		cmds.text( label='Select Folder')
		pathText = cmds.textField(chosenFile)
		chosenButton = cmds.button(label = "fileDialog2Open" , command = chosenFile);
		
		cmds.setParent("..")
		cmds.showWindow( window )


testWindow = fileDialog2Test()
testWindow.create()
