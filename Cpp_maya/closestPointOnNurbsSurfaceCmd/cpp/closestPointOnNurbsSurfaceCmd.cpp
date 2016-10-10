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
#include <math.h>
// MAYA HEADERS
#include <maya/MIOStream.h>
#include <maya/MArgList.h>
#include <maya/MPxCommand.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MPoint.h>
#include <maya/MNurbsIntersector.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnTransform.h>
#include <maya/MVector.h>
#include <maya/MFnPlugin.h>
#include <maya/MFnNurbsSurface.h>

#include <maya/MMeshIntersector.h>

#include "closestPointOnNurbsSurfaceCmd.h"
// CONSTRUCTOR:
closestPointOnNurbsSurfaceCmd::closestPointOnNurbsSurfaceCmd()
{
}
// DESTRUCTOR:
closestPointOnNurbsSurfaceCmd::~closestPointOnNurbsSurfaceCmd()
{
}
// FOR CREATING AN INSTANCE OF THIS COMMAND:
void* closestPointOnNurbsSurfaceCmd::creator()
{
   return new closestPointOnNurbsSurfaceCmd;
}
// MAKE THIS COMMAND NOT UNDOABLE:
bool closestPointOnNurbsSurfaceCmd::isUndoable() const
{
   return false;
}
MStatus closestPointOnNurbsSurfaceCmd::doIt(const MArgList& args)
{
    bool debug = false;    // if����p�u�[��
    bool treeBased = true; // �A���S���Y�����s����p�u�[��

	float fX = 0;
    float fY = 0;
	float fZ = 0;

    MStatus stat = MStatus::kSuccess;
    if(debug) cout << "closestPointOnNurbsSurfaceCmd::doIt\n";
    
	// 1.�I�����X�g���擾
    MSelectionList list;
    stat = MGlobal::getActiveSelectionList(list);
	// 2.stat��FAIL�̏ꍇ
    if(!stat) {
        if(debug) cout << "getActiveSelectionList FAILED\n";
        return( stat );
    }

	// 1.�擾�����m�[�h
	MDagPath path;
	
	// poly
	MObject meshObject;    
	stat = list.getDependNode(0,meshObject);
	// 2.stat��FAIL�̏ꍇ
	if(!stat)
        if(debug) cout << "getDependNode FAILED\n";

   
	MFnDagNode nodeFn(meshObject);

	// meshObject�̃m�[�h�ւ̃p�X�𔻒肷��
	MDagPath::getAPathTo(meshObject, path);

	// 1.�擾����DagNode�̎q�����J�E���g�� 0 ���ǂ����𔻒�
	// ���g�����X�t�H�[���ł͂Ȃ��V�F�C�v���g��
    if(nodeFn.childCount() > 0) {
        MObject child = nodeFn.child(0);
        nodeFn.setObject(child);
    }

	// ���X�g����DAG�p�X���擾
    list.getDagPath(0,path);
    if(debug) cout << "Working with: " << path.partialPathName() << endl;
    
	// �t�s����擾
	MMatrix matrix1 = path.inclusiveMatrix();
    if(debug) cout << matrix1 << endl;


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

	// ���P�[�^�[1�̃g�����X�t�H�[��
    MFnTransform loc1Fn(loc1Object);

	// loc1Fn �̃I�u�W�F�N�g��Ԃł̈ړ��l���擾
	// t �� pt �ɑ��
    MVector t = loc1Fn.getTranslation(MSpace::kObject);

	//-------------------------------------------------------

	 MPoint pt(t[0], t[1], t[2]);
 
                

//-------------------------------------------------------

	// ���̕ӂ��ύX���ĕ��ʈȊO�ł����������o�ł���悤�ɂ���B
        MMeshIntersector intersector;

		// MDagPath �Ŏ擾����DAG�m�[�h����}�g���b�N�X�ƃm�[�h�����擾
        MMatrix matrix = path.inclusiveMatrix();
        MObject node = path.node();


		// MMeshIntersector.create �̃X�e�[�^�X���擾
        stat = intersector.create( node, matrix );

        if ( stat )
        {

                MPointOnMesh pointInfo;


                cout << "Using point: " << pt << endl;

                stat = intersector.getClosestPoint( pt, pointInfo );
	                if ( stat )
                {
					createObject( pointInfo, matrix );

                }
                else
                {
                        MGlobal::displayError("Failed to get closest point");
                }
        }
        else
        {
                MGlobal::displayError("Failed to create intersector");
        }

        return stat;



/*
    MMeshIntersector meshIntersect;

	// MDagPath �Ŏ擾����DAG�m�[�h����}�g���b�N�X�ƃm�[�h�����擾

    MMatrix matrix = path.inclusiveMatrix();
    MObject node = path.node();
	
	// MMeshIntersector.create
	stat = meshIntersect.create(meshObject, matrix1);
    if(!stat) {
    if(debug) cout << "MNurbsIntersector::create FAILED\n";
		return( stat );
    }
	
    if ( stat )
    {

		MPoint resultPoint;
        MPointOnMesh pointInfo;
		// arr �̐錾
		MDoubleArray arr;


			cout << "Using point: " << pt << endl;

			stat = meshIntersect.getClosestPoint( pt, pointInfo );

			// resultPoint �� pointInfo ���i�[
			resultPoint = pointInfo.getPoint();
	        if ( stat )
			{
				// resultPoint(NURBS��̃|�C���gptON)�ɑ΂���path(MDagPath)�̋t�s����|����
				MPoint worldResultPoint = resultPoint * path.inclusiveMatrix();
				if(debug) cout << "local space result point: " << resultPoint << endl;
				if(debug) cout << "world space result point: " << worldResultPoint << endl;

				// arr �̒l�̐�Βl �� worldResultPoint �̍��� 0.0001 ���傫�����Ƃ��m�F
				if ( fabs( fX - worldResultPoint.x ) > 0.0001
					|| fabs( fY - worldResultPoint.y ) > 0.0001
					|| fabs( fZ - worldResultPoint.z ) > 0.0001 ) {

					cout << "check results: pointOnSurface does not match world point: " << arr << endl;
					return( MS::kFailure );

				}
				// �Ԃ��Ă������[���h��Ԃ̃|�C���g��2�ڂ̃��P�[�^�[���ړ�
				// ����͏��NURBS�T�[�t�F�[�X��ł���ׂ�
				// Note: ���̃��P�[�^�[�͑o�����[���h�̎q���ł��邱�Ƃ�O��Ƃ��Ă���
				//

				// loc2Object �̐錾
				MObject loc2Object;


	
				// 1.�擾�����m�[�h���f�B�y���f���V�[�m�[�h���𔻒�(�C���f�b�N�X, �I�u�W�F�N�g)
				// ���g�����X�t�H�[���ł͂Ȃ��V�F�C�v���g��
				stat = list.getDependNode(2, loc2Object); 	
				if(!stat) {
					if(debug) cout << "FAILED grabbing locator2\n";
					return( stat );
				}

				// ���P�[�^�[2�̃g�����X�t�H�[��
				MFnTransform loc2Fn(loc2Object);
				// loc2Fn �� worldResultPoint �Ɉړ�����
				stat = loc2Fn.setTranslation(worldResultPoint, MSpace::kTransform);

				// worldResultPoint �� �X�t�B�A���쐬
				createObject( worldResultPoint );
				return stat;
	

				}
				else
				{
				    MGlobal::displayError("Failed to get closest point");
					return( stat );
				}
		}
        else
        {
			MGlobal::displayError("Failed to create intersector");
			return( stat );

        }
	
*/
}


// UNDO THE COMMAND
MStatus closestPointOnNurbsSurfaceCmd::undoIt()
{
    MStatus status;
    // undo not implemented
    return status;
}




void closestPointOnNurbsSurfaceCmd::createObject(  MPointOnMesh& info, MMatrix& matrix )
{
	    MPoint worldPoint( info.getPoint() );	// �Q�Ƃ������b�V����񂩂�|�C���g���W���擾
        worldPoint = worldPoint * matrix;		// �擾�����|�C���g���W�Ƀ��[���h�}�g���b�N�X���|���ă��[���h���W�ɕϊ�

        MVector worldNormal( info.getNormal() );	// �@���x�N�g�����擾
        worldNormal = worldNormal * matrix;			// �擾�����@���x�N�g���Ƀ��[���h�}�g���b�N�X���|���ă��[���h���W�ɕϊ�
        worldNormal.normalize();


        MString strCommandString = "string $strBall[] = `polySphere -r 0.5`;";	// �R�}���h�����s���ăX�t�B�A�����W�ɔz�u
        strCommandString += "$strBallName = $strBall[0];";
        strCommandString += "setAttr ($strBallName + \".tx\") ";
		strCommandString += worldPoint.x;
        strCommandString += ";";
        strCommandString += "setAttr ($strBallName + \".ty\") ";
		strCommandString += worldPoint.y;
        strCommandString += ";";
        strCommandString += "setAttr ($strBallName + \".tz\") ";
		strCommandString += worldPoint.z;
        strCommandString += ";";

        MGlobal::executeCommand(strCommandString);

        // ���̑��̏��̕\��(�@���x�N�g���������Ɏg�p)
        cout << "Normal: " << matrix << " face id: " << 
                " triangle id: " <<  endl;
}



// Maya�� register/unregister
// 
//
MStatus initializePlugin( MObject obj )
{
    MStatus   status;
    MFnPlugin plugin( obj, PLUGIN_COMPANY, "8.5", "Any");
    status = plugin.registerCommand( "closestPointOnNurbsSurface",
            closestPointOnNurbsSurfaceCmd::creator );
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
    status = plugin.deregisterCommand( "closestPointOnNurbsSurface" );
    if (!status) {
        status.perror("deregisterCommand");
        return status;
    }
    return status;
}
