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
// MAYA HEADERS
#include <maya/MArgList.h>
#include <maya/MPxCommand.h>

#include <maya/MGlobal.h>
// MAIN CLASS 
class objectScatterCmd : public MPxCommand
{
    public:
        objectScatterCmd();
        virtual ~objectScatterCmd();

		// ユーザー入力用変数(生成数)
		MString targetObjName;
		int count;
		double radius;
		double width, height, depth;
		bool random;


        static void* creator();
        bool isUndoable() const;
		
		
		MPoint imageToVoxel(MPoint pt, double cellSize);

		MPoint in_Voxel(MPoint point);

		MStatus inNeighbourhood(MPoint voxel, MPoint point, double min_dist, double cellSize);
		// Poisson Disc で生成した MVector を返す
		void generate_poisson(MObject& locator, MPointOnMesh& info, MMatrix& matrix, MString name, double width, double height, double depth, double min_dist);
		// ロケーターの位置を生成(ロケーター位置を起点として生成された MMatrix を返す)
		MVector GenerateRandomPointAround (MVector sample, double radius);
		// Poisson Disc 適用範囲のボクセルグリッドを生成
		MPoint voxelPos(MPoint point,  double cellSize);
		// ボクセルグリッド内に含まれるかを判定
		MStatus IsContains (MPoint v, MPoint area);
		// PoissonDiskSampler3D の実行メソッド
		MPoint PoissonDiskSampler3D(double width, double height, double depth, double cellSize);
		// ランダムポイント の距離が近隣のポイントと近づきすぎていないかチェック
		MStatus IsFarEnough(MPoint point, double cellSize, double radius);
		// サンプルポイント配列に サンプルポイントを新たに追加
		MVector AddSample(MPoint sample, double cellSize);
		// サンプルポイント上にオブジェクトを生成
        void createObject(  MPointOnMesh& info, MMatrix& matrix, MPoint pt, MString dupliMeshName, MString targetMeshName );  

        virtual MStatus doIt(const MArgList&);
        virtual MStatus undoIt();

MTypeId     objectScatterCmd::id;

};
