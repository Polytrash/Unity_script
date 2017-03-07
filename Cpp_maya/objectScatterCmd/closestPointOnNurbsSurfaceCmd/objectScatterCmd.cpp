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
    bool debug = false;    // if����p�u�[��
    bool treeBased = true; // �A���S���Y�����s����p�u�[��

	float fX = 0;
    float fY = 0;
	float fZ = 0;

	MStatus status;
	
    // ���[�U�[���͂̎擾
    for ( int i = 0; i < args.length(); i++ )
	{
        // �������鐔���w��
		if ( args.asString( i ) == MString( "-c" ) && MS::kSuccess == status )
        {
            int inputCount = args.asInt( ++i );
            if ( MS::kSuccess == status )
                count = inputCount;
        }

		// �^�[�Q�b�g�I�u�W�F�N�g�̖��O���擾(�R���X�g���C���̂���)
        else if (args.asString( i ) ==  MString( "-n" ) && MS::kSuccess == status )
        {
			MString inputName = args.asString( ++i );
            if ( MS::kSuccess == status )
				targetObjName = inputName;
        }

		// �I�u�W�F�N�g�Ԃ̋������w��
        else if (args.asString( i ) ==  MString( "-r" ) && MS::kSuccess == status )
        {
            double inputRadius = args.asDouble( ++i );
            if ( MS::kSuccess == status )
                radius = inputRadius;
        }


		// �z�u�͈͂̕����w��
        else if ( args.asString( i ) == MString( "-w" ) && MS::kSuccess == status )
        {
            double inputWidth = args.asDouble( ++i );
            if ( MS::kSuccess == status )
				width = inputWidth;

		}

		// �z�u�͈͂̍������w��
        else if ( args.asString( i ) == MString( "-h" ) && MS::kSuccess == status )
        {
            double inputHeight = args.asDouble( ++i );
            if ( MS::kSuccess == status )
				height = inputHeight;
        }


		// �z�u�͈͂̕����w��
        else if ( args.asString( i ) == MString( "-d" ) && MS::kSuccess == status )
        {
            double inputDepth = args.asDouble( ++i );
            if ( MS::kSuccess == status )
				depth = inputDepth;
        }

		// �����_����]��K�p
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
    
	// 1.�I�����X�g���擾
    MSelectionList list;
    stat = MGlobal::getActiveSelectionList(list);
	// 2.stat��FAIL�̏ꍇ
    if(!stat) {
        if(debug) cout << "getActiveSelectionList FAILED\n";
        return( stat );
    }

	//-------------------------------------------------------
	// ���b�V��1�̔���
	//-------------------------------------------------------

	// 1A.�擾�p�X
	MDagPath path1;	
	// 1B.�擾���b�V��
	MObject meshObject;   

	stat = list.getDependNode(0,meshObject);

	// 2.stat��FAIL�̏ꍇ
	if(!stat)
        if(debug) cout << "getDependNode FAILED\n";
   
	MFnDagNode nodeFn1(meshObject);

	// meshObject�̃m�[�h�ւ̃p�X�𔻒肷��
	MDagPath::getAPathTo(meshObject, path1);

	// 1.�擾����DagNode�̎q�����J�E���g�� 0 ���ǂ����𔻒�
	// ���g�����X�t�H�[���ł͂Ȃ��V�F�C�v���g��
    if(nodeFn1.childCount() > 0) {
        MObject child = nodeFn1.child(0);
        nodeFn1.setObject(child);
    }

	// ���X�g����DAG�p�X���擾
    list.getDagPath(0,path1);
    if(debug) cout << "Working with: " << path1.partialPathName() << endl;
    
	// ���O�擾�pMString
	MString targetMeshName;
	targetMeshName = nodeFn1.name();

	//-------------------------------------------------------
	// ���P�[�^�[�̔���
	//-------------------------------------------------------
	
	// loc1Object�̐錾
    MObject loc1Object;


	// 1.�擾�����m�[�h���f�B�y���f���V�[�m�[�h���𔻒�(�C���f�b�N�X, �I�u�W�F�N�g)
	// ���g�����X�t�H�[���ł͂Ȃ��V�F�C�v���g��
    stat = list.getDependNode(1, loc1Object); 

	// 2.stat��FAIL�̏ꍇ
    if(!stat) {
        if(debug) cout << "FAILED grabbing locator1\n";
        return( stat );
    }
	

	//-------------------------------------------------------
	// �ȉ��Aloc2Object�̉�������ђǉ����� ���b�V��2�̔���
	//-------------------------------------------------------


	// 1A.�擾�p�X
	MDagPath path2;	
	// 1B.�擾���b�V��
	MObject dupliMesh;

	// 1.�擾�����m�[�h���f�B�y���f���V�[�m�[�h���𔻒�(�C���f�b�N�X, �I�u�W�F�N�g)
	// ���g�����X�t�H�[���ł͂Ȃ��V�F�C�v���g��
	stat = list.getDependNode(2, dupliMesh); 	
	if(!stat) {
		if(debug) cout << "FAILED grabbing meshObject to duplicate\n";
		return( stat );
	}

	// ���O�擾�pMString
	MString dupliMeshName;
	// MFnDagNode �Ƃ��� MObject ���擾
	MFnDagNode nodeFn2(dupliMesh);	

	// dupliMesh �̃m�[�h�ւ̃p�X�𔻒肷��
	MDagPath::getAPathTo(dupliMesh, path2);

	// 1.�擾����DagNode�̎q�����J�E���g�� 0 ���ǂ����𔻒�
	// ���g�����X�t�H�[���ł͂Ȃ��V�F�C�v���g��
    if(nodeFn2.childCount() > 0) {
        MObject child = nodeFn2.child(0);
        nodeFn2.setObject(child);
    }

	// ���X�g����DAG�p�X���擾
    list.getDagPath(0,path2);
    if(debug) cout << "Working with: " << path2.partialPathName() << endl;

	dupliMeshName = nodeFn2.name();

	//-------------------------------------------------------

        MMeshIntersector intersector;

		// MDagPath �Ŏ擾����DAG�m�[�h����}�g���b�N�X�ƃm�[�h�����擾
        MMatrix matrix = path1.inclusiveMatrix();
        MObject node = path1.node();

		// MMeshIntersector.create �̃X�e�[�^�X���擾
        stat = intersector.create( node, matrix );

        if ( stat )
        {

			MPointOnMesh pointInfo;


			
			for(int i = 0; i <= count; i++){


				// cellSize ��ėp�I�Ɏg�p�ł���悤�ɂ��邽�߁APoissonDiskSampler3D����O���ɏo����
				double radius = 10.0;
				double cellSize = radius / sqrt (3);

				// �T���v���Ƃ��郉���_���l��MVector���擾
				MVector s = AddSample(MVector((double)rand()/ RAND_MAX,(double)rand()/ RAND_MAX,(double)rand()/ RAND_MAX),cellSize);

				// Poisson Disc���\�b�h scatterObjecgt �ɂ��ړ��l���擾
				MVector t = GenerateRandomPointAround (s, 10.0);

				// ���P�[�^�[1�̈ړ��l���w��
				MFnTransform loc1Fn(loc1Object);
				loc1Fn.setTranslation(t, MSpace::kObject );	

				//-------------------------------------------------------



				MPoint poissonPt(t[0], t[1], t[2]);
				MPoint limitPt = PoissonDiskSampler3D(width, height, depth, cellSize);

				// limtPt �͈̔͂� poissonPt ��������Ύ��s���Ȃ�(�͈͎w��ɂ��邩�A���w��ɂ��邩�Ő؂�ւ���?)
				stat = IsContains(poissonPt,limitPt);
				if(stat)
				{
					stat = IsFarEnough(poissonPt, cellSize, radius);
					if(stat)
					{
						// ���C���΂��ă��P�[�^�[�ƃI�u�W�F�N�g�\�ʂ̍ŒZ���������߂�
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

// �K�؂Ȉړ��l�𓾂遨���[�v�łԂ�񂷁�POISSON DISC�̌��ʂł΂�T��

// Poisson Disc �K�p�͈͂̃{�N�Z���O���b�h�𐶐�
MPoint objectScatterCmd::voxelPos(MPoint point,  double cellSize)
{

  MVector grid = point / cellSize;   
  MPoint voxelGrid(grid[0], grid[1], grid[2]);

  return voxelGrid;
}

// EntryPoint �g������ǂ�

MPoint objectScatterCmd::PoissonDiskSampler3D(double width, double height, double depth, double cellSize)
{
		MPoint cube = MPoint(width, height, depth);
		//double radius2  = radius * radius;
		// cellSize ��ėp�I�Ɏg�p�ł���悤�ɂ��邽�߁APoissonDiskSampler3D����O���ɏo����
		//double cellSize = radius / sqrt (3);
		MPoint voxelGrid = MVector((width /cellSize), (height/cellSize), (depth /cellSize));

		return voxelGrid;
}

// MSelectionList�Ŏ擾���� MObject �������� list ������ǉ����āAobjectScatterCmd ���s����
// �z�u���� meshObject ���擾 

void objectScatterCmd::createObject(  MPointOnMesh& info, MMatrix& matrix, MPoint pt, MString dupliMeshName , MString targetMeshName )
{

		//MTransformationMatrix meshNormal = info.getNormal;
		//MMatrix rotateMatrix = meshNormal.eulerRotation;

	    MPoint worldPoint( info.getPoint() );	// �Q�Ƃ������b�V����񂩂�|�C���g���W���擾
        worldPoint = worldPoint * matrix;		// �擾�����|�C���g���W�Ƀ��[���h�}�g���b�N�X���|���ă��[���h���W�ɕϊ�

        MVector worldNormal( info.getNormal() );	// �@���x�N�g�����擾
        worldNormal = worldNormal * matrix;					// �擾�����@���x�N�g���Ƀ��[���h�}�g���b�N�X���|���ă��[���h���W�ɕϊ�
        worldNormal.normalize();
		
		//std::srand(std::time(0));		// use current time as seed for random generator
		//MVector  randomVector = MVector((double)0 + rand() % (0 - 360),(double)0 + rand() % (0 - 360),(double)0 + rand() % (0 - 360)) * matrix;		

			// name �𕡐����Č�������Ō��o�����}�g���N�X�ɔz�u
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


        // ���̑��̏��̕\��(�@���x�N�g���������Ɏg�p)
        cout << "Normal: " << matrix << " face id: " << 
                " triangle id: " <<  endl;
}

// LOCATOR TRANSLATOR: �����̃|�C���g�̎��͂� min distance - max distance �̊ԂɐV���ȃ|�C���g�𐶐�
// doIt���Ŏg�p
MVector objectScatterCmd::GenerateRandomPointAround (MVector sample, double mindist)
{
  	// ���P�[�^�[1�̃g�����X�t�H�[��
    //MFnTransform loc1Fn(locator);

	// loc1Fn �̃I�u�W�F�N�g��Ԃł̈ړ��l���擾
	// t �� pt �ɑ��
	// ���P�[�^�[1�̃g�����X�t�H�[�� ���� �I�u�W�F�N�g���W���擾
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

/// grid �� �߂�O�� �T���v���L���[�ɃA�N�e�B�u�ȃT���v����ǉ�
MVector objectScatterCmd::AddSample(MPoint sample, double cellSize)
{
		
		MPoint pos = voxelPos(sample, cellSize);
		MVector(pos.x, pos.y, pos.z) = sample;
		return sample;
}


// Maya�� register/unregister
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
