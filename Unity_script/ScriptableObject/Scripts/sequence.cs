/** ***************************************************************************
 * @file     : ScriptableObjMaker.cs
 * @brief    : SGN共通エフェクトビューワーが扱う アニメーションシーケンス Scriptable Object
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
public class Effect_sequence : ScriptableObject
{
	// Model Name
	[SerializeField]private string model;

	// Element Name
	[SerializeField]private string name;

	// Animation Clip
	[SerializeField]private AnimationClip clip;

	// Effect
	// Start Frame
	[SerializeField]private bool[] isLoop = new bool[10];
	[SerializeField]private int[] startFrame = new int[10];	
	[SerializeField]private int[] endFrame = new int[10];

	// isLoop
	public bool getIsLoop(int index){return isLoop[index];}
	public void setIsLoop(int index, bool val){isLoop [index] = val;}
	// Start Frame
	public int getStartFrame(int index){return startFrame[index];} 
	public void setStartFrame(int index, int frame){startFrame[index] = frame;}
	// End Frame 
	public int getEndFrame(int index){return endFrame[index];} 
	public void setEndFrame(int index, int frame){endFrame[index] = frame;}


	//============================================================================
	// 公開プロパティ定義
	//============================================================================

	// Model Name
	public string Model{get{return model;} set{model = value;}}

	// Element Name
	public string Name{get{return name;} set{name = value;}}	

	// Effect Properties
	public AnimationClip AnimClip{get{return clip;} set{clip = value;}}	// Clip ※本来はAnimationClip



}

