using UnityEngine;
using System.Collections;

public class Cube1 : MonoBehaviour {
	
	public TransCount transCount;

	
	void Start () {
		transCount = Resources.Load<TransCount>("TransCount");
	}
	
	void OnGUI()
	{
		GUI.Label(new Rect(800, 5, 200, 80), this.transCount.Value.ToString());

		GUI.Label(new Rect(800, 25, 200, 80), this.transCount.PosX.ToString());
		GUI.Label(new Rect(900, 25, 200, 80), this.transCount.PosY.ToString());
		GUI.Label(new Rect(1000, 25, 200, 80), this.transCount.PosZ.ToString());

		GUI.Label(new Rect(800, 45, 200, 80), this.transCount.Rot.ToString());

		GUI.Label(new Rect(800, 65, 200, 80), this.transCount.ScalX.ToString());
		GUI.Label(new Rect(900, 65, 200, 80), this.transCount.ScalX.ToString());
		GUI.Label(new Rect(1000, 65, 200, 80), this.transCount.ScalX.ToString());

	}

	void SetPosition(float vX, float vY, float vZ){
		transform.position = new Vector3(vX, vY, vZ);
		
	}

	void SetRotation(float vX, float vY, float vZ){
		transform.localEulerAngles = new Vector3 (vX, vY, vZ);
	}

	void SetScale(float vX, float vY, float vZ){
		transform.localScale = new Vector3 (vX, vY, vZ);
	}

	void OnMouseDown()
	{

		this.transCount.Value++;

		transCount.PosX = GetComponent<Transform>().position.x ;
		transCount.PosY = GetComponent<Transform>().position.y ;
		transCount.PosZ = GetComponent<Transform>().position.z ;

		transCount.Rot = GetComponent<Transform>().localEulerAngles;

		transCount.ScalX = GetComponent<Transform>().localScale.x ;
		transCount.ScalY = GetComponent<Transform>().localScale.y ;
		transCount.ScalZ = GetComponent<Transform>().localScale.z ;

		SetPosition (transCount.PosX, transCount.PosY, transCount.PosZ);
		SetRotation (transCount.RotX, transCount.RotY, transCount.RotZ);
		SetScale (transCount.ScalX, transCount.ScalY, transCount.ScalZ);
		
	}

	void Update(){


	}
}
