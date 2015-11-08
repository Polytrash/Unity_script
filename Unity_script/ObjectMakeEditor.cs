using UnityEngine;
using UnityEditor;
using System.Collections;

[CustomEditor(typeof(ObjectMakeScript))]
public class ObjectBuildEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        ObjectMakeScript myScript = (ObjectMakeScript)target;
        if(GUILayout.Button("Build Object"))
        {

            myScript.BuildObject();

        }


    }




}
