using UnityEngine;
using UnityEditor;
using System.Collections;

[CustomEditor(typeof(MaterialChangeScript))]

public class GameObjectSelector : Editor
{
    //private string stringToEdit = null;  // this variable use to selectGameObject which overloaded by string.

    public override void OnInspectorGUI()
    {        

    DrawDefaultInspector();
    
    MaterialChangeScript myScript = (MaterialChangeScript)target;


    //stringToEdit = GUILayout.TextField( stringToEdit, 25 );

    if(GUILayout.Button("Material Change"))
    {
        try
        {
           // myScript.selectGameObject();
            myScript.selectGameObject(myScript.selected);
        }
        catch (UnityException e)
        {
            Debug.Log(e);
            
        }

    }

    
    
    }
        
}
