using UnityEngine;
using System.Collections;

public class Cube : MonoBehaviour {
	
	public ClickCount clickCount;

	
	void Start () {
		clickCount = Resources.Load<ClickCount>("ClickCount");
	}
	
	void OnGUI()
	{
		GUI.Label(new Rect(10, 5, 200, 80), this.clickCount.Value.ToString());
		GUI.Label(new Rect(10, 25, 200, 80), this.clickCount.Colour.ToString());
		if (GUI.changed)
			GetComponent<Renderer>().sharedMaterial.SetColor ("_Color", clickCount.Colour);
	}
	
	void OnMouseDown()
	{
		ClickCount.Instantiate(this.clickCount);
		this.clickCount.Value++;
		//ClickCount someInstance = ScriptableObject.CreateInstance("ClickCount") as ClickCount;
		this.clickCount = Resources.Load<ClickCount>("ClickCount");
		
		this.clickCount.Colour = new Color (1.0f * (float)Random.Range (0.1f, 0.9f), 1.0f * (float)Random.Range (0.1f, 0.9f), 1.0f * (float)Random.Range (0.1f, 0.9f));

		GetComponent<Renderer>().sharedMaterial.SetColor ("_Color", clickCount.Colour);

		
	}

	public void changeColor(){

		clickCount.Colour = Color.white;
		GetComponent<Renderer>().sharedMaterial.SetColor ("_Color", clickCount.Colour);
		Debug.Log (clickCount.Colour);
	}


}
