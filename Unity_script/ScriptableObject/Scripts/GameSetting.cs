using UnityEngine;
using System.Collections;
[System.Serializable]


public class EachLevel
{
	
    public uint mLevelID;
    public uint mSceneID;
	
};

[System.Serializable]
public class GameSetting : ScriptableObject
{
	
	
    public EachLevel[] lvl;
	public void Init ( uint id1, uint id2 )
		
    {
		
         lvl = new EachLevel[2];
         lvl[0].mLevelID = id1;
		 lvl [0] = new EachLevel ();
         lvl[0].mSceneID = id2;
		 lvl [1] = new EachLevel ();
         lvl[1].mLevelID = id2;
         lvl[1].mSceneID = id1;
     }
	
	
}

		


	

