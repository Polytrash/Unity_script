using UnityEngine;
using System.Collections;

public class TransCount : ScriptableObject {
	
	public int Value;

	public Vector3 pos = new Vector3(0,0,0);
	public Vector3 rot = new Vector3(0,0,0);
	public Vector3 scal = new Vector3(1,1,1);

	// Position Accessor

	public Vector3 Pos
	{
		set{ pos = value;}
		get{ return pos;}
	}

	public float PosX
	{
		set{ pos.x = value;}
		get{ return pos.x;}
	}

	public float PosY
	{
		set{ pos.y = value;}
		get{ return pos.y;}
	}

	public float PosZ
	{
		set{ pos.z = value;}
		get{ return pos.z;}
	}

	// Rotation Accessor

	public Vector3 Rot
	{
		set{ rot = value;}
		get{return rot;}
	}

	public float RotX
	{
		set{ rot.x = value;}
		get{ return rot.x;}
	}

	public float RotY
	{
		set{ rot.y = value;}
		get{ return rot.y;}
	}

	public float RotZ
	{
		set{ rot.z = value;}
		get{ return rot.z;}
	}

	// Scale Accessor

	public float ScalX
	{
		set{ scal.x = value;}
		get{ return scal.x;}
	}

	public float ScalY
	{
		set{ scal.y = value;}
		get{ return scal.y;}
	}

	public float ScalZ
	{
		set{ scal.z = value;}
		get{ return scal.z;}
	}
}


