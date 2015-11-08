# weightIOManager export method

import maya.cmds as cmds
import math
import csv

# �I�u�W�F�N�g���̎擾�ƕs�v�ȕ����̍폜�A���_���̎擾

try:
	slctObjNameList = cmds.ls(sl = True);
	slctObjName = slctObjNameList[0].split('.vtx')[0];
	objVtxCount = cmds.polyEvaluate(v = True);

except:
	 
	print("ERROR:�I�u�W�F�N�g���I������Ă��܂���")



# �����o���pCSV�t�@�C�����J��
f = open('D:\maya\weight1.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

i = 0;
j = 0;

while i < objVtxCount:
	weight = cmds.skinPercent( 'skinCluster1', str(slctObjName) + ".vtx[" + str(i) + "]", query = True, value = True);
	i += 1;
	print("[vtx" + str(i) + "] has " + str(weight));
	writer.writerow(weight);

		
f.close()
del num[:]
