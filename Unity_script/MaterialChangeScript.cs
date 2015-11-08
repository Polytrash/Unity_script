using UnityEngine;
using System.Collections;

public class MaterialChangeScript : MonoBehaviour {

    public GameObject selected;
    public Material material = null;

    // default constructor
    public void selectGameObject()
    {
        selected = GameObject.Find("GameObject");
        //selected.transform.Translate(0, 1, 0);
        //selected.transform.Rotate(0, 90, 90);
        selected.GetComponent<Renderer>().material = material;

    }

    // overloaded by string
    public void selectGameObject(string text)
    {
        selected = GameObject.Find(text);
        //selected.transform.Translate(0, 1, 0);
        //selected.transform.Rotate(0, 90, 90);
        selected.GetComponent<Renderer>().material = material;

    }

    // overloaded by GameObject
    public void selectGameObject(GameObject go)
    {
        selected = go;
        //selected.transform.Translate(0, 1, 0);
        //selected.transform.Rotate(0, 90, 90);
        selected.GetComponent<Renderer>().material = material;

    }

    // overloaded by GameObject & Change Function

    //public void selectGameObject(){ }

}
