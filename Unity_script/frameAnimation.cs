using UnityEngine;
using System.Collections;

public class frameAnimation : MonoBehaviour {
	public Texture[] PlayerTexture;
	public float animTex = 0;
	public float fps = 25;
	public Material material;

	void Update () {
		animTex = Time.time * fps;
		animTex = animTex % PlayerTexture.Length;
		material.mainTexture = PlayerTexture[(int)animTex];
		material.SetTexture("_EmissionMap",PlayerTexture[(int)animTex]);

		Debug.Log( Mathf.Floor(animTex));
	}
}