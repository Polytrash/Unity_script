using UnityEngine;
using System.Collections;

public class GameParam : MonoBehaviour {
	
	public GameSetting gameSetting;

	
	void Start () {
		gameSetting = Resources.Load<GameSetting>("GameSetting");
	}
	
	void OnGUI()
	{

	}
	



}
