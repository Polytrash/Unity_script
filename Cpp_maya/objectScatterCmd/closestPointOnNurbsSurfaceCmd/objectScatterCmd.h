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

		// ���[�U�[���͗p�ϐ�(������)
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
		// Poisson Disc �Ő������� MVector ��Ԃ�
		void generate_poisson(MObject& locator, MPointOnMesh& info, MMatrix& matrix, MString name, double width, double height, double depth, double min_dist);
		// ���P�[�^�[�̈ʒu�𐶐�(���P�[�^�[�ʒu���N�_�Ƃ��Đ������ꂽ MMatrix ��Ԃ�)
		MVector GenerateRandomPointAround (MVector sample, double radius);
		// Poisson Disc �K�p�͈͂̃{�N�Z���O���b�h�𐶐�
		MPoint voxelPos(MPoint point,  double cellSize);
		// �{�N�Z���O���b�h���Ɋ܂܂�邩�𔻒�
		MStatus IsContains (MPoint v, MPoint area);
		// PoissonDiskSampler3D �̎��s���\�b�h
		MPoint PoissonDiskSampler3D(double width, double height, double depth, double cellSize);
		// �����_���|�C���g �̋������ߗׂ̃|�C���g�Ƌ߂Â������Ă��Ȃ����`�F�b�N
		MStatus IsFarEnough(MPoint point, double cellSize, double radius);
		// �T���v���|�C���g�z��� �T���v���|�C���g��V���ɒǉ�
		MVector AddSample(MPoint sample, double cellSize);
		// �T���v���|�C���g��ɃI�u�W�F�N�g�𐶐�
        void createObject(  MPointOnMesh& info, MMatrix& matrix, MPoint pt, MString dupliMeshName, MString targetMeshName );  

        virtual MStatus doIt(const MArgList&);
        virtual MStatus undoIt();

MTypeId     objectScatterCmd::id;

};
