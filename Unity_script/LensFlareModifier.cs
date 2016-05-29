using UnityEngine;
using System.Collections;

public class LensFlareModifier : MonoBehaviour {

	public LensFlare obj;
	public Camera cam;

	public float FlareMin;
	public float FlareMax;

	public float flareMultiplier = 1.0f;
	public float degree;

	private float LensFlareDefaultBrightness = 0.0f;
	private float angle;
	private float inverseLerp;

	public void LensFlareTransition(){
		

		float currentAngle;

		Vector3 objPosition = obj.transform.position;
		Vector3 camPosition = cam.transform.position;
		Vector3 camDirection = cam.transform.forward;

		float angle = Vector3.Angle(camDirection, objPosition - camPosition);

		currentAngle = angle;
		///Debug.Log ("currentAngle is " + currentAngle);

		inverseLerp = InvLerp(-1 * (degree /2) , degree /2, currentAngle);
		//Debug.Log ("current inverseLerp is " + inverseLerp);

		obj.brightness = ( LensFlareDefaultBrightness - inverseLerp ) * flareMultiplier;	

		if (obj.brightness <= FlareMin) {

			obj.brightness = FlareMin;
		}

		if (obj.brightness >= FlareMax) {

			obj.brightness = FlareMax;
		}

		Debug.Log (obj.brightness);

	}

	public float InvLerp(float a, float b, float value)
	{	
		inverseLerp = Mathf.InverseLerp (a, b, value);

		return inverseLerp;
	}

	// Use this for initialization
	void Start () {
		
		LensFlareDefaultBrightness = obj.brightness;
		LensFlareTransition ();
	
	}
	
	// Update is called once per frame
	void Update () {
	
		LensFlareTransition ();



	}
}
