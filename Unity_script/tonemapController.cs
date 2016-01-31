using UnityEngine;
using System.Collections;
using UnityStandardAssets.ImageEffects;

public class tonemapController : MonoBehaviour {

	public float vSliderValue = 1.0f;

	public Tonemapping tone;

	void OnGUI(){
		
		vSliderValue = GUI.HorizontalSlider (new Rect (400, 50, 800, 30), vSliderValue, 8.0f, 0.001f);

		GUI.Label(new Rect(350, 50, 200, 20), "Tonemap:" + vSliderValue);

	}



	// Use this for initialization
	void Start () {

		tone = GetComponent<Tonemapping>();

	}
	
	// Update is called once per frame
	void Update () {
	
		Debug.Log (vSliderValue.ToString());
		tone.exposureAdjustment = vSliderValue;

	}
}
