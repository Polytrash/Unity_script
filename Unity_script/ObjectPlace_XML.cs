using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Xml;
using System.Xml.Serialization;
using System.IO;
using System.Text;
using System.Linq;
using System.Text.RegularExpressions;

public class UserData
{
	public iUserData _iUser;

	public UserData() {}

	public struct iUserData
	{
		public string name;


		public float xPos ;
		public float yPos ;
		public float zPos ;

		public float xRot ;
		public float yRot ;
		public float zRot ;

		public float xScl ;
		public float yScl ;
		public float zScl ;

	}

}


[ExecuteInEditMode]
public class ObjectPlace_XML : MonoBehaviour {

	Rect _Save, _Load, _SaveMSG, _LoadMSG;
	bool _ShouldSave, _ShouldLoad, _SwitchSave, _SwitchLoad;
	string _FileLocation, _FileName;
	public GameObject _Player;

	UserData myData;
	List<Dictionary<string,string>> objData = new List<Dictionary<string,string>>();
	Dictionary<string, string> obj;

	string _PlayerName;
	string _data;

	Vector3 VPosition;
	Vector3 VRotation;
	Vector3 VScale;


	private XmlDocument xmlDoc;

	// Use this for initialization
	void Start () {
	
		// メッセージ用の矩形を設定
		_Save = new Rect (10, 80, 100, 20);
		_Load = new Rect (10, 100, 100, 20);
		_SaveMSG = new Rect (10, 120, 400, 40);
		_LoadMSG = new Rect (10, 140, 400, 40);


		// データの保存先と読み込み先を指定
		_FileLocation = Application.dataPath;
		_FileName = "PlacementData.xml";

		// 名前を設定
		_PlayerName = this.gameObject.name;
	
		// 情報の格納先として確保
		myData = new UserData();
	}


	// Update is called once per frame
	void Update () {
	
	}



	void OnGUI()
	{
		if (GUI.Button(_Load, "Load")){

			GUI.Label(_LoadMSG, "Loading from: " + _FileLocation);

			// myData に UserData をロードして格納
			xmlDoc = LoadXML();
			/*
			if(_data.ToString() != "")
			{


			*/

			ParseXML (xmlDoc);

			string objname = "";

			string XPos = ""; string YPos = ""; string ZPos = "";
			string XRot = ""; string YRot = ""; string ZRot = "";
			string XScl = ""; string YScl = ""; string ZScl = "";

			foreach (var o in objData) {

				foreach (KeyValuePair<string, string> pair in o) {
									
						//Debug.Log (pair.Key + ":" + pair.Value);

					if (GameObject.Find (pair.Value)) {
						
						objname = pair.Value.ToString();
						GameObject go = GameObject.Find(pair.Value);



					XPos = getVal(objname + "xPos");
					YPos = getVal(objname + "yPos");
					ZPos = getVal(objname + "zPos");

					XRot = getVal(objname + "xRot");
					YRot = getVal(objname + "yRot");
					ZRot = getVal(objname + "zRot");

					XScl = getVal(objname + "xScl");
					YScl = getVal(objname + "yScl");
					ZScl = getVal(objname + "zScl");

					VPosition = new Vector3(float.Parse(XPos), float.Parse(YPos), float.Parse(ZPos));
					VRotation = new Vector3(float.Parse(XRot), float.Parse(YRot), float.Parse(ZRot));
					VScale = new Vector3(float.Parse(XScl), float.Parse(YScl), float.Parse(ZScl));

					Debug.Log ("VPosition : " + VPosition);
					Debug.Log ("VRotation : " + VRotation);
					Debug.Log ("VScale : " + VScale);

					go.transform.position = VPosition;
						go.transform.Rotate (new Vector3 (0, 0, 0), VRotation.x );
						go.transform.Rotate (new Vector3 (-10, 0,-10), VRotation.y);
						go.transform.Rotate (new Vector3 (-10, -10, 0), VRotation.z);
					go.transform.localScale = VScale;
					}
					}



				}
							
			}

		if (GUI.Button (_Save, "Save")) {

			GUI.Label (_SaveMSG, "Saving to: " + _FileLocation); 

			myData._iUser.name = _Player.name;
			
			myData._iUser.xPos = _Player.transform.position.x;
			myData._iUser.yPos = _Player.transform.position.y;
			myData._iUser.zPos = _Player.transform.position.z;

			myData._iUser.xRot = _Player.transform.localEulerAngles.x;
			myData._iUser.yRot = _Player.transform.localEulerAngles.y;
			myData._iUser.zRot = _Player.transform.localEulerAngles.z;

			myData._iUser.xScl = _Player.transform.localScale.x;
			myData._iUser.yScl = _Player.transform.localScale.y;
			myData._iUser.zScl = _Player.transform.localScale.z;



			// オリジナルのXMLを生成

			_data = SerializeObject (myData);
			// serialization process からの最終的な XML　
			CreateXML ();
			Debug.Log (_data);

		}
	}


	// objData から Value 値を取得

	private string getVal(string key)
	{
		string tmpValue = "";

		foreach (var o in objData) {
			foreach (KeyValuePair<string, string> pair in o) {
				
				if (pair.Key == key) {
					tmpValue = pair.Value;
					Debug.Log (key + ":" + tmpValue);
				}
			}
		}
		return tmpValue;
	
	}


	private void ParseXML(XmlDocument xmlDoc)
	{

		objData.Clear ();

		//Debug.Log ("UserData" + all.InnerText);				// 子ノード含むすべてのタグ

		//objectData.Add(new UserData.iUserData(iU.InnerText,)))

		XmlNodeList iUser = xmlDoc.GetElementsByTagName ("_iUser");

		foreach (XmlNode iUserData in iUser) {

			XmlNodeList content = iUserData.ChildNodes;

			string objName = "";
			string newKey = "";
			obj = new Dictionary<string, string> ();

			foreach (XmlNode contents in content) {

					if (contents.Name == "name") {
					
						objName = contents.InnerText;
						obj.Add ("name", contents.InnerText);
						
					}

					// 移動値
					if (contents.Name == objName + "xPos") {
						newKey = objName + "xPos";
						obj.Add (newKey, contents.InnerText);
						//Debug.Log ("xPos :" + contents.InnerText);
					}
					if (contents.Name == objName + "yPos") {
						newKey = objName + "yPos";
						obj.Add (newKey, contents.InnerText);
						//Debug.Log ("yPos :" + contents.InnerText);
					}
					if (contents.Name == objName + "zPos") {
						newKey = objName + "zPos";
						obj.Add (newKey, contents.InnerText);
						//Debug.Log ("zPos :" + contents.InnerText);
					}

					// 回転値
					if (contents.Name ==  objName + "xRot") {
						newKey = objName + "xRot";
						obj.Add (newKey, contents.InnerText);
					}
					if (contents.Name ==  objName + "yRot") {
						newKey = objName + "yRot";
						obj.Add (newKey, contents.InnerText);
					}
					if (contents.Name ==  objName + "zRot") {
						newKey = objName + "zRot";
						obj.Add (newKey, contents.InnerText);
					}

					// スケール値
					if (contents.Name ==  objName + "xScl") {
						newKey = objName + "xScl";
						obj.Add (newKey, contents.InnerText);
					}
					if (contents.Name == objName +  "yScl") {
						newKey = objName + "yScl";
					obj.Add (newKey, contents.InnerText);
					}
					if (contents.Name == objName +  "zScl") {
						newKey = objName + "zScl";
						obj.Add (newKey, contents.InnerText);
					}

				}
				objData.Add (obj);
			}

	}



	string UTF8ByteArrayToString(byte[] characters)
	{
			UTF8Encoding encoding = new UTF8Encoding();
			string constructedString = encoding.GetString(characters);
			return (constructedString);
	}

	byte[] StringToUTF8ByteArray(string pXmlString)
	{
		UTF8Encoding encoding = new UTF8Encoding ();
		byte[] byteArray = encoding.GetBytes (pXmlString);
		return byteArray;

	}

	string SerializeObject(object pObject)
	{
		string XmlizedString = null;
		MemoryStream memoryStream = new MemoryStream ();
		XmlSerializer xs = new XmlSerializer (typeof(UserData));
		XmlTextWriter xmlTextWriter = new XmlTextWriter (memoryStream, Encoding.UTF8);
		xs.Serialize (xmlTextWriter, pObject);
		memoryStream = (MemoryStream)xmlTextWriter.BaseStream;
		XmlizedString = UTF8ByteArrayToString (memoryStream.ToArray ());
		return XmlizedString;
	}
		
	object DeserializeObject(string pXmlizedString)
	{
		XmlSerializer xs = new XmlSerializer (typeof(UserData));
		MemoryStream memoryStream = new MemoryStream (StringToUTF8ByteArray (pXmlizedString));
		XmlTextWriter xmlTextWriter = new XmlTextWriter (memoryStream, Encoding.UTF8);
		return xs.Deserialize (memoryStream);
	}

	void CreateXML()
	{
		StreamWriter writer;
		FileInfo t = new FileInfo (_FileLocation + "\\" + _FileName);
		if (!t.Exists) {
			writer = t.CreateText ();
		} else {
			t.Delete ();
			writer = t.CreateText ();
		}
		writer.Write (_data);
		writer.Close ();
		Debug.Log ("File written.");
	}

	XmlDocument LoadXML()
	{

		StreamReader r = File.OpenText (_FileLocation + "\\" + _FileName);

		XmlDocument xmlDoc = new XmlDocument ();
		xmlDoc.Load (r);

		//Debug.Log ("File Read");

		return xmlDoc;

	}

}

