using UnityEngine;
using UnityEditor;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;


public class bezierGet : MonoBehaviour{


	public Vector3 b;
	public float d;
	

	void Awake(){

		//GameObject GO = GameObject.Find ("bezierGet");
		//GO.GetComponent<dirPos>().Dir = 10f;
		GameObject GO = GameObject.Find ("bezierCurveDir");
		GO.GetComponent<bezierCurveDir>().p0.Dir = 10000f;


	}
}