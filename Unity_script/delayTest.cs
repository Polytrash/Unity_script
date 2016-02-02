using UnityEngine;
using System.Collections;


public class delayTest : MonoBehaviour {


	private IEnumerator loop(int frame)
	{
		while (frame > 0) {

			yield return null;
			Debug.Log ("looop");
			frame--;
		}
		doSomething ();
	}

	int a = 10;


	private void doSomething(){
	
		Debug.Log ("Done!");
	}


	// Use this for initialization
	void Start () {

			StartCoroutine(loop(a));

	}
	
	// Update is called once per frame
	void Update () {



	
	}

}