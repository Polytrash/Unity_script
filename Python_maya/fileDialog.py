import maya.cmds as cmds

window = cmds.window(title='open file')
cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)] )
cmds.text( label='Maya Scene' )
front = cmds.textField(text = unicode(chosenFile))
cmds.showWindow( window )


chosenFile = cmds.fileDialog2(fm=3, ds=2, cap="Open", okc="Select scene file", hfe=0)
chosenFile = chosenFile.replace("u", "");