
using UnityEngine;


using System.Collections;


using System.Collections.Generic;


using System.Linq;


[System.Serializable]


public class EachLevel
	
	
{
	
	
    public uint mLevelID;
	
	
    public uint mSceneID;
	
	
};


[System.Serializable]


public class LevelData : ScriptableObject
	
	
{
	
	public EachLevel[] lvl = new EachLevel[5];

	
}
