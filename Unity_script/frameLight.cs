using UnityEngine;
using System.Collections;

public class frameLight : MonoBehaviour {
	public Light FrameLight;
	public float animVal;
	public float fps = 25;
	public float frameIntensity = 0;

	float interval = 1f;
	float smooth = 0.5f;
	float slope = 0.5f;
	float tNext = 0;

	Vector3 defaultPos; 

	bool moved = true;


	//public float fps = 25;
	//public Material material;

	void Start() {

		FrameLight = GetComponent<Light>();

		defaultPos = FrameLight.transform.position;
	}

	void Update () {
		animVal = Time.time * fps;		

		if (Time.time > tNext) {
			tNext += interval * (0.5f + Random.value);
		}
		smooth += slope * Time.deltaTime;

		if (smooth > 1 || smooth < 0)
			smooth = Mathf.Clamp (smooth, 0.5f, 1.0f);
		
		frameIntensity = Random.Range(0.35f * smooth , 0.4f * smooth);
		FrameLight.intensity = frameIntensity;
		/*
		if (moved == false) {

			FrameLight.transform.position =
				new Vector3 (FrameLight.transform.position.x + (smooth / 10.0f),
				FrameLight.transform.position.y + (smooth / 10.0f),
				FrameLight.transform.position.z + (smooth / 10.0f));
				
			moved = true;

		} else {
			FrameLight.transform.position = defaultPos; 

			moved = false;

		}
		*/

		Debug.Log( frameIntensity);
	}
}