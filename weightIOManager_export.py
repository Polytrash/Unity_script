# weightIOManager export method

import maya.cmds as cmds
import math
import csv

# オブジェクト名の取得と不要な文字の削除、頂点数の取得

try:
	slctObjNameList = cmds.ls(sl = True);
	slctObjName = slctObjNameList[0].split('.vtx')[0];
	objVtxCount = cmds.polyEvaluate(v = True);

except:
	 
	print("ERROR:オブジェクトが選択されていません")



# 書き出し用CSVファイルを開く
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
