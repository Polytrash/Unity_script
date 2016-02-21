/** ***************************************************************************
 * @file     : ScriptableObjMaker.cs
 * @brief    : SGN共通エフェクトビューワーが扱う エフェクトパラメータ Scriptable Object
 * @since    : 2015/12/3
 * @author   : Shinichi Muraoka
 *                                                             (C)SEGANETWORKS
*************************************************************************** **/
//============================================================================
// 名前空間
//============================================================================

using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;

//============================================================================
// クラス定義
//============================================================================

[System.Serializable]
public class Effect_parameter : ScriptableObject
{

	//============================================================================
	// 公開変数定義
	//============================================================================
	

	// Effect Properties
	//[SerializeField]private string effectParamName;
	[SerializeField]private GameObject effect;
	[SerializeField]private string node;
	[SerializeField]private bool isGlobal;
	[SerializeField]private bool isLoop;
	
	// Transform
	[SerializeField]private Vector3 position;
	[SerializeField]private Vector3 positionRandom;
	[SerializeField]private Vector3 rotation;
	[SerializeField]private Vector3 rotationRandom;
	[SerializeField]private Vector3 scale;
	[SerializeField]private Vector3 scaleRandom;
	[SerializeField]private float particleScale;

	//============================================================================
	// 公開プロパティ定義
	//============================================================================

	public GameObject Effect{get{return effect;} set{effect = value;}}	// Effect ※ 本来はGameObject
	public string Node{get{return node;} set{node = value;}}
	public bool IsGlobal{get{return isGlobal;} set{isGlobal = value;}}

	// Transform
	public Vector3 Position{get{return position;} set{position = value;}}
	public Vector3 PositionRandom{get{return positionRandom;} set{positionRandom = value;}}
	public Vector3 Rotation{get{return rotation;} set{rotation = value;}}
	public Vector3 RotationRandom{get{return rotationRandom;} set{rotationRandom = value;}}
	public Vector3 Scale{get{return scale;} set{scale = value;}}
	public Vector3 ScaleRandom{get{return scaleRandom;} set{scaleRandom = value;}}
	public float ParticleScale{get{return particleScale;} set{particleScale = value;}}		
	
	// Start Frame

}

