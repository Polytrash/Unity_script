using UnityEngine;
using UnityEditor;
using System.Collections;
using UnityEditor;
using System.IO;

public class CreateSOBJ : MonoBehaviour {

	public int SOBJSIZE = 2;
	public static string SOBJNAME = string.Format("LevelData");

	private string text = string.Format("");


	// Use this for initialization
	void Start () {
	
	}
	
	
	void OnGUI(){

		text = GUI.TextField (new Rect (100, 150, 50, 25), text, 40);
		

			


		if (GUI.Button (new Rect (100, 100, 100, 20), "LevelData")) {
			Create ();
			Debug.Log("Button clicked");
			
		}
		
	}

	// scriptable object のラベルを登録する labels 
	readonly static string[] labels = {"Data", "ScriptableObject", string.Empty};
	
	//[MenuItem("Assets/Create ScriptableObject")]
	static void Create ()
	{



		// 選択されたオブジェクトからオブジェクトを選択
		//foreach (Object selectedObject in Selection.objects) {
			//Selection.activeObject = AssetDatabase.LoadMainAssetAtPath("Assets/Resources/test.cs");

			// パスの取得
			//string path = getSavePath (selectedObject);
		string path = "Assets/Resources/NewSOBJ.asset";

			if (File.Exists (path))
				for (int i=1;; i++) {
			
					// {0} = dirPath と {1} = objectPath と i = number を結合して .asset を加えて path とする
					path = string.Format ("{0}/{1}({2}).asset", "Assets/Resources/", SOBJNAME, i);
					if (! File.Exists (path))
						break;

			}


			// "Empty" で登録されていた labels[2] に ScriptableObject の名称を登録
			labels[2] = SOBJNAME;

					
			// インスタンスを生成
			//ScriptableObject obj = ScriptableObject.CreateInstance (selectedObject.name);
			ScriptableObject obj = ScriptableObject.CreateInstance (SOBJNAME);

			// インスタンス obj を指定パスに生成
			AssetDatabase.CreateAsset (obj, path);
			//ScriptableObject obj = ScriptableObject.CreateInstance ("test");
			//AssetDatabase.CreateAsset (obj, "Assets/Resources/test.asset");

			// AssetDatabase.LoadAssetAtPath ->ラベルの追加
			//　指定の path 上に指定されたタイプのアセットを生成する。アセットファイルは複数のオブジェクトを含むことが可能
			// アセットパスの例)"Assets/MyTextures/hello.png".
			ScriptableObject sobj = AssetDatabase.LoadAssetAtPath (path, typeof(ScriptableObject)) as ScriptableObject;

			// ラベルは一つのアセットに複数登録して簡単に検索できるようにする仕組み
			AssetDatabase.SetLabels (sobj, labels);

			// ダーティフラグを設定してディスク上に保存させる
			EditorUtility.SetDirty (sobj);

	}
	
	static string getSavePath (Object selectedObject)
	{
		string objectName = selectedObject.name;

		// 選択されたオブジェクトのパスを取得
		string dirPath = Path.GetDirectoryName (AssetDatabase.GetAssetPath (selectedObject));
		// {0} = dirPath と {1} = objectPath を結合して .asset を加えて path とする
		string path = string.Format ("{0}/{1}.asset", dirPath, objectName);
		Debug.Log ("dirPath : " + dirPath);
		// ファイルが既に存在していた場合
		if (File.Exists (path))
		for (int i=1;; i++) {

			// {0} = dirPath と {1} = objectPath と i = number を結合して .asset を加えて path とする
			path = string.Format ("{0}/{1}({2}).asset", dirPath, objectName, i);
			if (! File.Exists (path))
				break;
		}
		Debug.Log ("objectName : " + objectName);
		return path;
	}
}
