//-
// ==========================================================================
// Copyright 1995,2006,2008 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+
// Description:
//      A command which exercises the various NURBS closestPoint methods
//  available in the API. The command expects all data it needs to work
//  with to be on the selection list.
//
// Usage:
//      Before calling this command, the selection list needs to have
//      the following nodes selected in order:
//
//      o  A NURBS surface, such as nurbsPlaneShape1. The surface may
//         be transformed in the DAG, if desired.
//      o  The transform node of a locator. The user should place the
//         locator at the point in 3-space for which they want to find
//         the closest point on the NURBS surface.
//
//      When invoked with the above items in order on the selection list,
//      the command proceeds to calculate the closest point on the NURBS
//      surface, moving "locator2" to the computed closest point to allow
//      the user to visually see what closest point was calculated.
//
// Example:
//      1. Compile and load this plug-in into Maya.
//      2. Create a NURBS surface, such as a NURBS plane. Move some CVs
//         to obtain a wavy surface.
//      3. Create two locators, locator1 and locator2, (both should be
//         children of the world because the plug-in translates locator2
//         to the calculated closest point value for display purposes).
//      4. Position the first locator somewhere in 3D space over the
//         surface. Note that the second locator will be automatically
//         moved to the closest point on the surface by the command.
//      5. Select the two objects:
//              MEL> select nurbsPlaneShape1 locator1 locator2;
//      6. Invoke this command:
//              MEL> closestPointOnNurbsSurface;
//      7. You should see locator2 move to the point on the NURBS
//         surface which is closest to locator1.
//      8. Move locator1 to different positions and invoke this
//         command again. You should see locator2 move to the correct
//         closest location each time.
//      9. Try rotating, scaling and translating the NURBS surface's
//         transform node and you should see the closest point being
//         correctly computed.
//
#define _USE_MATH_DEFINES
#include <math.h>
#include <stdlib.h>
#include <ctime>

// MAYA HEADERS
#include <maya/MIOStream.h>
#include <maya/MArgList.h>
#include <maya/MPxCommand.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MNurbsIntersector.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnTransform.h>
#include <maya/MVector.h>
#include <maya/MFnPlugin.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MTypes.h>
#include <maya/MMeshIntersector.h>

#include <maya/MTransformationMatrix.h>

#include "objectScatterCmd.h"
#include <algorithm>


#define PI 3.1415926535

#define MAX(a,b) (((a) > (b)) ? (a) : (b))
#define MIN(a,b) (((a) < (b)) ? (a) : (b))


int randomGen()
{
	int random, max_value = 360, min_value = 0;
	random = rand() % ((max_value + min_value) + min_value);
	return random;
}


// CONSTRUCTOR:
objectScatterCmd::objectScatterCmd()
{
}
// DESTRUCTOR:
objectScatterCmd::~objectScatterCmd()
{
}
// FOR CREATING AN INSTANCE OF THIS COMMAND:
void* objectScatterCmd::creator()
{
   return new objectScatterCmd();
}
// MAKE THIS COMMAND NOT UNDOABLE:
bool objectScatterCmd::isUndoable() const
{
   return false;
}

MStatus objectScatterCmd::doIt(const MArgList& args)
{
    bool debug = false;    // if判定用ブール
    bool treeBased = true; // アルゴリズム実行判定用ブール

	float fX = 0;
    float fY = 0;
	float fZ = 0;

	MStatus status;
	
    // ユーザー入力の取得
    for ( int i = 0; i < args.length(); i++ )
	{
        // 生成する数を指定
		if ( args.asString( i ) == MString( "-c" ) && MS::kSuccess == status )
        {
            int inputCount = args.asInt( ++i );
            if ( MS::kSuccess == status )
                count = inputCount;
        }

		// ターゲットオブジェクトの名前を取得(コンストレインのため)
        else if (args.asString( i ) ==  MString( "-n" ) && MS::kSuccess == status )
        {
			MString inputName = args.asString( ++i );
            if ( MS::kSuccess == status )
				targetObjName = inputName;
        }

		// オブジェクト間の距離を指定
        else if (args.asString( i ) ==  MString( "-r" ) && MS::kSuccess == status )
        {
            double inputRadius = args.asDouble( ++i );
            if ( MS::kSuccess == status )
                radius = inputRadius;
        }


		// 配置範囲の幅を指定
        else if ( args.asString( i ) == MString( "-w" ) && MS::kSuccess == status )
        {
            double inputWidth = args.asDouble( ++i );
            if ( MS::kSuccess == status )
				width = inputWidth;

		}

		// 配置範囲の高さを指定
        else if ( args.asString( i ) == MString( "-h" ) && MS::kSuccess == status )
        {
            double inputHeight = args.asDouble( ++i );
            if ( MS::kSuccess == status )
				height = inputHeight;
        }


		// 配置範囲の幅を指定
        else if ( args.asString( i ) == MString( "-d" ) && MS::kSuccess == status )
        {
            double inputDepth = args.asDouble( ++i );
            if ( MS::kSuccess == status )
				depth = inputDepth;
        }

		// ランダム回転を適用
        else if ( args.asString( i ) == MString( "-random" ) && MS::kSuccess == status )
        {
            bool inputRandom = args.asBool( ++i );
            if ( MS::kSuccess == status )
				random = inputRandom;
        }

		else
        {
            MString msg = "Invalid flag: ";
            msg += args.asString( i );
            displayError( msg );
            return MS::kFailure;
        }
	}


    MStatus stat = MStatus::kSuccess;
    if(debug) cout << "objectScatterCmd::doIt\n";
    
	// 1.選択リストを取得
    MSelectionList list;
    stat = MGlobal::getActiveSelectionList(list);
	// 2.statがFAILの場合
    if(!stat) {
        if(debug) cout << "getActiveSelectionList FAILED\n";
        return( stat );
    }

	//-------------------------------------------------------
	// メッシュ1の判定
	//-------------------------------------------------------

	// 1A.取得パス
	MDagPath path1;	
	// 1B.取得メッシュ
	MObject meshObject;   

	stat = list.getDependNode(0,meshObject);

	// 2.statがFAILの場合
	if(!stat)
        if(debug) cout << "getDependNode FAILED\n";
   
	MFnDagNode nodeFn1(meshObject);

	// meshObjectのノードへのパスを判定する
	MDagPath::getAPathTo(meshObject, path1);

	// 1.取得したDagNodeの子供をカウントし 0 かどうかを判定
	// ※トランスフォームではなくシェイプを使う
    if(nodeFn1.childCount() > 0) {
        MObject child = nodeFn1.child(0);
        nodeFn1.setObject(child);
    }

	// リストからDAGパスを取得
    list.getDagPath(0,path1);
    if(debug) cout << "Working with: " << path1.partialPathName() << endl;
    
	// 名前取得用MString
	MString targetMeshName;
	targetMeshName = nodeFn1.name();

	//-------------------------------------------------------
	// ロケーターの判定
	//-------------------------------------------------------
	
	// loc1Objectの宣言
    MObject loc1Object;


	// 1.取得したノードがディペンデンシーノードかを判定(インデックス, オブジェクト)
	// ※トランスフォームではなくシェイプを使う
    stat = list.getDependNode(1, loc1Object); 

	// 2.statがFAILの場合
    if(!stat) {
        if(debug) cout << "FAILED grabbing locator1\n";
        return( stat );
    }
	

	//-------------------------------------------------------
	// 以下、loc2Objectの改造および追加部分 メッシュ2の判定
	//-------------------------------------------------------


	// 1A.取得パス
	MDagPath path2;	
	// 1B.取得メッシュ
	MObject dupliMesh;

	// 1.取得したノードがディペンデンシーノードかを判定(インデックス, オブジェクト)
	// ※トランスフォームではなくシェイプを使う
	stat = list.getDependNode(2, dupliMesh); 	
	if(!stat) {
		if(debug) cout << "FAILED grabbing meshObject to duplicate\n";
		return( stat );
	}

	// 名前取得用MString
	MString dupliMeshName;
	// MFnDagNode として MObject を取得
	MFnDagNode nodeFn2(dupliMesh);	

	// dupliMesh のノードへのパスを判定する
	MDagPath::getAPathTo(dupliMesh, path2);

	// 1.取得したDagNodeの子供をカウントし 0 かどうかを判定
	// ※トランスフォームではなくシェイプを使う
    if(nodeFn2.childCount() > 0) {
        MObject child = nodeFn2.child(0);
        nodeFn2.setObject(child);
    }

	// リストからDAGパスを取得
    list.getDagPath(0,path2);
    if(debug) cout << "Working with: " << path2.partialPathName() << endl;

	dupliMeshName = nodeFn2.name();

	//-------------------------------------------------------

        MMeshIntersector intersector;

		// MDagPath で取得したDAGノードからマトリックスとノード情報を取得
        MMatrix matrix = path1.inclusiveMatrix();
        MObject node = path1.node();

		// MMeshIntersector.create のステータスを取得
        stat = intersector.create( node, matrix );

        if ( stat )
        {

			MPointOnMesh pointInfo;


			
			for(int i = 0; i <= count; i++){


				// cellSize を汎用的に使用できるようにするため、PoissonDiskSampler3Dから外部に出した
				double radius = 10.0;
				double cellSize = radius / sqrt (3);

				// サンプルとするランダム値のMVectorを取得
				MVector s = AddSample(MVector((double)rand()/ RAND_MAX,(double)rand()/ RAND_MAX,(double)rand()/ RAND_MAX),cellSize);

				// Poisson Discメソッド scatterObjecgt による移動値を取得
				MVector t = GenerateRandomPointAround (s, 10.0);

				// ロケーター1の移動値を指定
				MFnTransform loc1Fn(loc1Object);
				loc1Fn.setTranslation(t, MSpace::kObject );	

				//-------------------------------------------------------



				MPoint poissonPt(t[0], t[1], t[2]);
				MPoint limitPt = PoissonDiskSampler3D(width, height, depth, cellSize);

				// limtPt の範囲に poissonPt が無ければ実行しない(範囲指定にするか、数指定にするかで切り替える?)
				stat = IsContains(poissonPt,limitPt);
				if(stat)
				{
					stat = IsFarEnough(poissonPt, cellSize, radius);
					if(stat)
					{
						// レイを飛ばしてロケーターとオブジェクト表面の最短距離を求める
						stat = intersector.getClosestPoint( poissonPt, pointInfo);
						if ( stat )
						{			
										
							createObject( pointInfo, matrix, poissonPt, dupliMeshName, targetMeshName);
		
						}
						else
						{
							MGlobal::displayError("Failed to get closest point");
						}
					}
				}
			}
		}
		else
		{
			MGlobal::displayError("Failed to create intersector");
		}

        return stat;

}


// UNDO THE COMMAND
MStatus objectScatterCmd::undoIt()
{
    MStatus status;
    // undo not implemented
    return status;
}

// 適切な移動値を得る→ループでぶん回す→POISSON DISCの結果でばら撒く

// Poisson Disc 適用範囲のボクセルグリッドを生成
MPoint objectScatterCmd::voxelPos(MPoint point,  double cellSize)
{

  MVector grid = point / cellSize;   
  MPoint voxelGrid(grid[0], grid[1], grid[2]);

  return voxelGrid;
}

// EntryPoint 使い方を読む

MPoint objectScatterCmd::PoissonDiskSampler3D(double width, double height, double depth, double cellSize)
{
		MPoint cube = MPoint(width, height, depth);
		//double radius2  = radius * radius;
		// cellSize を汎用的に使用できるようにするため、PoissonDiskSampler3Dから外部に出した
		//double cellSize = radius / sqrt (3);
		MPoint voxelGrid = MVector((width /cellSize), (height/cellSize), (depth /cellSize));

		return voxelGrid;
}

// MSelectionListで取得した MObject もしくは list 引数を追加して、objectScatterCmd 実行時に
// 配置する meshObject を取得 

void objectScatterCmd::createObject(  MPointOnMesh& info, MMatrix& matrix, MPoint pt, MString dupliMeshName , MString targetMeshName )
{

		//MTransformationMatrix meshNormal = info.getNormal;
		//MMatrix rotateMatrix = meshNormal.eulerRotation;

	    MPoint worldPoint( info.getPoint() );	// 参照したメッシュ情報からポイント座標を取得
        worldPoint = worldPoint * matrix;		// 取得したポイント座標にワールドマトリックスを掛けてワールド座標に変換

        MVector worldNormal( info.getNormal() );	// 法線ベクトルを取得
        worldNormal = worldNormal * matrix;					// 取得した法線ベクトルにワールドマトリックスを掛けてワールド座標に変換
        worldNormal.normalize();
		
		//std::srand(std::time(0));		// use current time as seed for random generator
		//MVector  randomVector = MVector((double)0 + rand() % (0 - 360),(double)0 + rand() % (0 - 360),(double)0 + rand() % (0 - 360)) * matrix;		

			// name を複製して交差判定で検出したマトリクスに配置
			MString strCommandString = "select -r " + dupliMeshName + ";";		

			strCommandString += "string $dupliObjects[] = `duplicate -rr`;";
			strCommandString += "$dupliObjName = $dupliObjects[0];";
			strCommandString += "setAttr ($dupliObjName + \".tx\") ";
			strCommandString += worldPoint.x;
			strCommandString += ";";
			strCommandString += "setAttr ($dupliObjName + \".ty\") ";
			strCommandString += worldPoint.y;
			strCommandString += ";";
			strCommandString += "setAttr ($dupliObjName + \".tz\") ";
			strCommandString += worldPoint.z;
			strCommandString += ";";
		
			
			strCommandString += "select -r " ;
			strCommandString += targetObjName;
			strCommandString += ";";
			strCommandString += "select -tgl $dupliObjName ;" ;
			strCommandString += "geometryConstraint -w 1.0 ; ";
			
			strCommandString += "normalConstraint -weight 1 -aimVector 0.0  1.0  0.0 -upVector 0.0 1.0 0.0 ;" ;
			/*
			strCommandString += "setAttr ($dupliObjName + \".rx\") ";
			strCommandString += worldNormal.x * 180.0 / PI;
			strCommandString += ";";
			strCommandString += "setAttr ($dupliObjName + \".ry\") ";
			strCommandString += worldNormal.y * 180.0 / PI;
			strCommandString += ";";
			strCommandString += "setAttr ($dupliObjName + \".rz\") ";
			strCommandString += worldNormal.z * 180.0 / PI;
			strCommandString += ";";
			*/
			MGlobal::executeCommand(strCommandString);


        // その他の情報の表示(法線ベクトルもここに使用)
        cout << "Normal: " << matrix << " face id: " << 
                " triangle id: " <<  endl;
}

// LOCATOR TRANSLATOR: 既存のポイントの周囲に min distance - max distance の間に新たなポイントを生成
// doIt内で使用
MVector objectScatterCmd::GenerateRandomPointAround (MVector sample, double mindist)
{
  	// ロケーター1のトランスフォーム
    //MFnTransform loc1Fn(locator);

	// loc1Fn のオブジェクト空間での移動値を取得
	// t を pt に代入
	// ロケーター1のトランスフォーム から オブジェクト座標を取得
    MVector v = sample;


	//-------------------------------------------------------

  
	double r1 = ((double)rand()/ RAND_MAX) - ((double)rand()/ RAND_MAX); //random point between 0 and 1
	double r2 = ((double)rand()/ RAND_MAX) - ((double)rand()/ RAND_MAX); 
	double r3 = ((double)rand()/ RAND_MAX) - ((double)rand()/ RAND_MAX); 

	//random radius between mindist and 2* mindist
	double radius = mindist * (r1 + 1.0);
	//random angle
	double angle1 = 2.0 * M_PI * r2;
	double angle2 = 2.0 * M_PI * r3;
	

	//the new point is generated around the point (x, y, z)
	double newX = v[0] + radius * cos(angle1) * sin(angle2);
	double newY = v[1] + radius * sin(angle1) * sin(angle2);
	double newZ = v[2] + radius * cos(angle2);

	return MVector (newX, newY, newZ);
}


MStatus objectScatterCmd::IsContains (MPoint v, MPoint area)
{
		if (abs(v.x) >= 0 && abs(v.x) < area.x &&
		    abs(v.x) >= 0 && abs(v.x) < area.y &&
		    abs(v.x) >= 0 && abs(v.x) < area.z) {
				return MStatus::kSuccess;
				
		} else {
			return MStatus::kFailure;
		}
}

MStatus objectScatterCmd::IsFarEnough(MPoint point, double cellSize, double radius)
{
	MPoint pos = voxelPos(point, cellSize);
	MVector null = MVector(0,0,0);

	double xmin = MAX(pos.x - 2, 0);
	double ymin = MAX(pos.y - 2, 0);
	double zmin = MAX(pos.z - 2, 0);
	
	
	double xmax = MIN(pos.x + 2, null.x - 1 );
	double ymax = MIN(pos.y + 2, null.y - 1 );
	double zmax = MIN(pos.z + 2, null.z - 1 );

	for(int z = zmin; z <= zmax; z++){
		for(int y = ymin; y <= ymax; y++){
			for(int x = xmin; x <= xmax; x++){
				MVector s = MVector(x,y,z);
				if(x != 0)
				{
					MVector d = s - point;
					if(d.x * d.x + d.y * d.y + d.z * d.z < radius)
						return MStatus::kFailure;
				}
			}
		}
	}
	return MStatus::kSuccess;
}

/// grid が 戻る前に サンプルキューにアクティブなサンプルを追加
MVector objectScatterCmd::AddSample(MPoint sample, double cellSize)
{
		
		MPoint pos = voxelPos(sample, cellSize);
		MVector(pos.x, pos.y, pos.z) = sample;
		return sample;
}


// Mayaの register/unregister
// 
//
MStatus initializePlugin( MObject obj )
{
    MStatus   status;
    MFnPlugin plugin( obj, PLUGIN_COMPANY, "8.5", "Any");
    status = plugin.registerCommand( "objectScatter",
            objectScatterCmd::creator);
    if (!status) {
        status.perror("registerCommand");
        return status;
    }
    return status;
}


MStatus uninitializePlugin( MObject obj)
{
    MStatus   status;
    MFnPlugin plugin( obj );
    status = plugin.deregisterCommand( "objectScatter" );
    if (!status) {
        status.perror("deregisterCommand");
        return status;
    }
    return status;
}
