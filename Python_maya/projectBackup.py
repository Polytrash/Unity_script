import sys
import shutil
import os
import pymel.core as pm
pm.mel.eval(' setProject "D:/maya/projects/test" ')

shutil.copytree("D:/maya/projects/test", "D:/maya/projects/test2")
print os.rmdir("D:/maya/projects/test/aaa")

import maya.cmds as cmds
import pymel.core as pm

eval.performSurfaceSampling()