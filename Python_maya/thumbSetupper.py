import os
import sys
import maya.cmds as cmds
import pymel.core as pm

class thumbJointOrientModifier(object):
	
# ジョイント名格納用リスト
	def __init__(self):
		self.window = 'thumbJointOrientModifyWindow';
		self.title = 'Thumb Joint Orient Modify Window';
		self.size = (320, 150);
		self.width = 320;
		self.height = 50;
		
		self.jntOrientValue = -45;
		
		self.childNames = [];
		self.jointName = '';
		self.rootJointName = '';
		self.rootJointBool = True;



# GUIメソッドの宣言
	
	def create(self):
		if cmds.window('thumbJointOrientModifyWindow', exists = True):
			cmds.deleteUI('thumbJointOrientModifyWindow' );

		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size);
		self.frameForm = cmds.frameLayout(label = " 選択した骨以下のジョイントオリエントの値を合わせます", bgc = (0.3, 0.4, 0.1), cll = False);
		self.columForm = cmds.columnLayout();	
		cmds.setParent("..")
		self.executeButton = cmds.button(label = "実行" , command = self.executeJointOrientModify, height = 30 );

		
		cmds.text("【問い合わせ先】", bgc = (0.2, 0.2, 0.2), align = 'left');	
		cmds.setParent("..")	

		cmds.showWindow();

# ジョイントオリエントメソッドの実行

	def executeJointOrientModify(self, *args):

		self.thumbJointOrientModify();

	
# ジョイントオリエント設定の可否判断メソッド

	def rootJointOrientExam(self, *args):
		
		self.jointName = cmds.ls(sl = True)
		self.rootJointName = cmds.pickWalk(d = "up")
		
		self.strRootJointName = str(self.rootJointName)
		self.splittedRootJointName = self.strRootJointName.split("'")[1]
		self.rootJointFinalName = unicode(self.splittedRootJointName)
		
		self.strJointName = str(self.jointName)
		self.splittedJointName = self.strJointName.split("'")[1]
		self.jointFinalName = unicode(self.splittedJointName)
		
		self.rootJntOrientValX = cmds.getAttr(self.jointFinalName +  u".jointOrientX");
		self.rootJntOrientValY = cmds.getAttr(self.jointFinalName +  u".jointOrientY");
		self.rootJntOrientValZ = cmds.getAttr(self.jointFinalName +  u".jointOrientZ");
		
		print(u"jointOrientX : " + self.rootJntOrientValX)
		print(u"jointOrientY : " + self.rootJntOrientValY)
		print(u"jointOrientZ : " + self.rootJntOrientValZ)
		
		if self.rootJntOrientValX != 0 or self.rootJntOrientValY != -45 or self.rootJntOrientVal != 0:
			cmds.warning(self.rootJointFinalName + u" 以上のジョイント方向(Joint Orient)のいずれかに不正な値が入っています。フリーズしたうえで再度実行してください。");
			return False




# ジョイントオリエント設定メソッド

	def thumbJointOrientModify(self, *args):
		# 選択したジョイントの親の名を取得(最後の親子付けを戻す処理に必要ため)
		self.jointName = cmds.ls(sl = True)
		self.rootJointName = cmds.pickWalk(d = "up")
		cmds.select(clear = True)

		cmds.select(self.jointName)
		cmds.parent(self.jointName, world = True)
		cmds.select(clear = True)

		# 再度ジョイントを選択
		cmds.select(self.jointName)
		cmds.makeIdentity(apply = True, t = False, r = True, s =  False, n = False, pn = False, jointOrient = True)
		cmds.select(clear = True)

		# 子ジョイントの数を取得

		cmds.select(self.jointName)
		self.childCount = cmds.listRelatives( ad=True, type='joint', fullPath=False)
		num = len(self.childCount)


		self.strRootJointName = str(self.rootJointName)
		self.splittedRootJointName = self.strRootJointName.split("'")[1]
		self.rootJointFinalName = unicode(self.splittedRootJointName)


		self.strJointName = str(self.jointName)
		self.splittedJointName = self.strJointName.split("'")[1]
		self.jointFinalName = unicode(self.splittedJointName)


		# ジョイント名をchildNamesリストに追加
		self.childNames.append(self.jointFinalName)

		self.jntOrientValX = cmds.getAttr(self.jointFinalName + u".jointOrientX")
		self.jntOrientValY = cmds.getAttr(self.jointFinalName + u".jointOrientY")
		self.jntOrientValZ = cmds.getAttr(self.jointFinalName + u".jointOrientZ")

		print (u"[" + self.jointFinalName + u".jointOrient" + u"]")
		print (u"X : " + unicode(self.jntOrientValX))
		print (u"Y : " + unicode(self.jntOrientValY))
		print (u"Z : " + unicode(self.jntOrientValZ))


		for a in self.childCount:
	
			self.childJointName = cmds.pickWalk(d = "down")
			cmds.select(self.childJointName)
			cmds.parent(world = True)
	
			self.strChildJointName = str(self.childJointName)
			self.splitedChildJointName = self.strChildJointName.split("'")[1]
			self.childJointFinalName = unicode(self.splitedChildJointName)

			# ジョイント名をchildNamesリストに追加	
			self.childNames.append(self.childJointFinalName)

			cmds.setAttr(self.childJointFinalName + u".jointOrientX", 0)
			cmds.setAttr(self.childJointFinalName + u".jointOrientY", 0)
			cmds.setAttr(self.childJointFinalName + u".jointOrientZ", 0)
	
		cNum = 0;

		for a in self.childNames:
	
			cmds.select(self.childNames[cNum])
			cmds.setAttr(self.childNames[cNum] + u".jointOrientY", -45)
			cmds.select(clear = True)
			cNum += 1;
	
		cmds.setAttr(self.jointFinalName + u".jointOrientX", 0)
		cmds.setAttr(self.jointFinalName + u".jointOrientY", 0)
		cmds.setAttr(self.jointFinalName + u".jointOrientZ", 0)
	
		cmds.setAttr(self.jointFinalName + u".rotateX", 0)
		cmds.setAttr(self.jointFinalName + u".rotateY", self.jntOrientValue)
		cmds.setAttr(self.jointFinalName + u".rotateZ", 0)	

		i = -1
		j = -2
		for a in self.childNames:
			try:
				cmds.select(self.childNames[i])
				cmds.select(self.childNames[j], add = True)
				cmds.Parent(performParent = False)
				i -= 1
				j -= 1

			except:
				pass	

	
		cmds.connectJoint( self.jointFinalName, self.rootJointFinalName,  pm = True )

		cmds.select(self.jointName)
		
		
thumbWindow = thumbJointOrientModifier()
thumbWindow.create()