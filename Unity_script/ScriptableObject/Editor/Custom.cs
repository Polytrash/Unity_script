using UnityEngine;
using UnityEditor;
using System.Collections;

[CustomEditor(typeof(CustomEditor))]
public class NewBehaviourScript : Editor{

	public override void OnInspectorGUI()
	{
	
		Cube cubeScript = (Cube)target;

		if (GUI.changed) {

			cubeScript.changeColor();
		}
	}
}