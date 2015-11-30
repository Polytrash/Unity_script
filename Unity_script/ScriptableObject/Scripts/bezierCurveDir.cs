using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;


[System.Serializable]
public class bezierCurveDir :MonoBehaviour {

	public int a;
	public dirPos p0;
	public dirPos p1;
	public dirPos p2;
}


[System.Serializable]
public class dirPos {
	public Vector3 pos;
	public float dir;
	public float Dir {get{return dir;}set{dir = value;}}
};

