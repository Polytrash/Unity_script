using UnityEngine;
using System.Collections;

public class guiSample : MonoBehaviour 
{

	#region debug
	[Header("Debug")]
	public bool showDebugMenu = false;

	#endregion

	#region floats

	public float myFloat = 1;

	#endregion

	#region strings

	public string coolString1 = "Super Cool!";

	#endregion


	[SerializeField]
	private string huga;

	[System.Serializable]
	public class GameData {
		public int Score;
		public int CurrentStage;
	}

	[System.Serializable]
	public class Test: MonoBehaviour{

		public int p = 5;
		public Color col = Color.white;
		public Vector3 vec;
		public Transform trans;
		public GameData game;
	}



}
