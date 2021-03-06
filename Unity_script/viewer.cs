
//============================================================================
// 名前空間
//============================================================================
using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;
using System.IO;

namespace sgnEffectViewer
{
	//============================================================================
	// クラス定義
	//============================================================================
	public class EffectViewer : MonoBehaviour {

		//============================================================================
		// 定数、内部クラス、構造体、列挙列定義
		//============================================================================
		//============================================================================
		// 静的変数定義
		//============================================================================

		static bool isAfterUnity51 = false;

		//============================================================================
		// 公開変数定義
		//============================================================================

		// sgnEffectViewer 公開変数


		[SerializeField]
		public GameObject model;	// chara から model に変更 [11/20]
		public Effect_sequence effectSequence ;
		public Effect_parameter[] effectParameter;

		[System.Serializable]
		public class EffectList {
			public string name;
			public AnimationClip animationClip;
			public Effect[] effects;

		};


		[System.Serializable]
		public class Effect {

			public GameObject effect;
			//public string effParamName;

			public string node;
			public bool isGlobal;	
			public Vector3 position;
			public Vector3 positionRandom;							// positionRandom追加 [11/20]
			public Vector3 rotation;
			public Vector3 rotationRandom;							// rotationRandom追加 [11/20]
			public Vector3 scale;									// localScale から scale に変更 Vector3.one　から new Vector3 に変更 [11/20]
			public Vector3 scaleRandom;								// scaleRandom追加 [11/20]
			public float particleScale;
			public bool isLoop;										// isLoop追加 [2/19]
			public int startFrame;
			public int endFrame;
			//public bool na_affectPlaySpeed;						// AffectPlaySpeed追加 [11/20]
			//public bool na_ignoreModelSpeed;						// IgnoreModelScaleSpeed追加 [11/20]
		 
		};


		public EffectList[] effectList;     


		//============================================================================

		// scriptable object generator 公開変数

		public static string EFFVIEWER_SETTING_NAME = string.Format("EffectViewer_setting");	
		public static string EFF_SEQUENCE_NAME = string.Format("Effect_sequence");	
		public static string EFF_PARAMETER_NAME = string.Format("Effect_parameter");	

		private static string text = string.Format("");


		//============================================================================
		// 非公開変数定義
		//============================================================================

		private Vector3 positionRandomTmp;
		private Vector3 rotationRandomTmp;
		private Vector3 scaleRandomTmp;

		private bool buttonPlay;			// EffectViewr 独自変数[ 11/26]	
		private bool buttonStop;			// EffectViewr 独自変数[ 12/2]	
		private bool buttonSave;			// EffectViewr 独自変数[ 11/24]		
		private bool buttonLoad;			// EffectViewr 独自変数[ 11/24]
		private bool buttonReset;			// EffectViewr 独自変数[ 11/26]
		private bool playOrNot = false;		

		private GameObject effectActivate = null;

		private string effectName = "";     	
		private Animation charaAnim;
		private float currentTime = 0f;			// 現在のタイムを指定
		private float actionStartTime = 0f;		// スタートフレーム指定

		private float frameTime = 1f/30f;
		private List<string> stopGoList;

		// private List<Effect> playList;		// playList廃止[2/19]
		// private List<Effect> removeList;		// removeList廃止[2/19]
		private List<GameObject> effectGameObjList;

		// ParticleTimeline 関連変数

		private float currentSlider = 0;						// HGParticleTimeline 独自変数[ 12/3]
		private float currentMaxDuration = 1000f;				// HGParticleTimeline 独自変数[ 12/3]
		private GameObject currentRootObj = null;				// HGParticleTimeline 独自変数[ 12/3]
		private EditorWindow currentAnimationWindow = null;		// HGParticleTimeline 独自変数[ 12/3]
		private bool isCheckTimeline = true; 					// HGParticleTimeline 独自変数[ 12/3]
		private bool isLoopOffset = true;	 					// HGParticleTimeline 独自変数[ 12/3]
		//private int frameCount = 0;							// HGParticleTimeline 追加変数[ 12/3]

		// Animation Slider用の変数
		//	private float hSliderValue = 0;		
		//	private bool sliderClick = false;	
		//	private AnimationState myAnimation;

		// Scriptable Object Generator 関連変数

		private bool buttonEVSN;		// EffectViewr 独自変数[ 11/26]	
		private bool buttonESN;			// EffectViewr 独自変数[ 12/2]	
		private bool buttonEPN;			// EffectViewr 独自変数[ 11/24]	





		//============================================================================
		// 公開プロパティ定義
		//============================================================================
		
		//============================================================================
		// 非公開プロパティ定義
		//============================================================================	
		
		//============================================================================
		// コンストラクタ、デストラクタ
		//============================================================================

		//============================================================================
		// 公開関数定義
		//============================================================================

		///////////////////////////
		///       　Play  		/// 
		///////////////////////////

		//　1.エフェクト：プレイ 
		
		void PlayEffect(Effect eff) {
			Transform node = GetNodeWithName(model.transform, eff.node);
			
			GameObject eff_go = 
				GameObject.Instantiate(eff.effect, node.position + eff.position, node.rotation * Quaternion.Euler(eff.rotation)) as GameObject;
			
			if (!eff.isGlobal) {
				
				// 親子関係を作る node → eff.transform.parent
				eff_go.transform.parent = node;		

			}
			// 1.スケール設定
			SetScale(eff_go, eff.particleScale, eff.scale);	

			Debug.Log ("Start:" + eff_go);
			PlayAll (eff_go);
			
		}

		///////////////////////////
		///       　Stop  		/// 
		///////////////////////////

		void StopEffect(Effect e, int stopGoListNum) {
			
			//Transform node = GetNodeWithName (model.transform, e.node);
			Debug.Log ("StopEffect_Run");

			int i = 0;
			string goName = "";
			GameObject go;

			foreach (string g in stopGoList) {
				
				if (g != null) {

					i += 1;
				}
			}

			Debug.Log ("stopGoList has : " + i + " GameObjects");


			goName = stopGoList [stopGoListNum];

			if (goName != null){
				
				go = GameObject.Find(goName) ;
				go.SetActive (false);

				Debug.Log (go + ".SetActive (false)");
			}

			//currentSlider = 0;

		
		}
	

		///////////////////////////
		/// StopGameObjListMake /// 
		///////////////////////////

		void StopGameObjListMake(){
				
			EffectList action = GetEffectWithName (effectList, effectName);

			int i = 0;
			string effOriginalName = "";
			string effRenamed = "";

			foreach(Effect eff in action.effects)
			{		
				effOriginalName = ReplaceEmpty(eff.effect.ToString(), " (UnityEngine.GameObject)");
				effRenamed = effOriginalName + "(Clone)";

				if (eff == null) {

					while (i == 1) {

						StopGameObjListMake ();
						i += 1;
					}
				}

				stopGoList.Add (effRenamed);

			}

		}


		///////////////////////////////////////////
		/// 									/// 
		///    Particle Play & Setup Method		/// 
		///										/// 
		///////////////////////////////////////////

		//-----------------------------------//
		// 1A.エフェクト：スケール設定用メソッド //
		//-----------------------------------//

		void SetScale(GameObject eff_go, float particleScale, Vector3 localScale) {
			eff_go.transform.localScale = localScale;
			var parts = eff_go.GetComponentsInChildren<ParticleSystem>();	// パーティクルシステム

			foreach (var p in parts) {
				p.gravityModifier *= particleScale;
				p.startSize *= particleScale;
				p.startSpeed *= particleScale;
			}

		}

		//-----------------------------------//

		//-----------------------------------//
		// 1B.エフェクト：ランダム位置設定用メソッド //
		//-----------------------------------//

		void SetRandomPos(GameObject eff_go, Vector3 posRandom) {
			eff_go.transform.localPosition = posRandom;

			var parts = eff_go.GetComponentsInChildren<ParticleSystem>();	// パーティクルシステム

			foreach (var p in parts) {
				p.transform.localPosition = 
					new Vector3(positionRandomTmp.x, positionRandomTmp.y, positionRandomTmp.z);

				Debug.Log (p.transform.localPosition);
			}
		}

		//-----------------------------------//

		//-----------------------------------//
		// 1B.エフェクト：ランダム回転設定メソッド //
		//-----------------------------------//

		void SetRandomRot(GameObject eff_go, Vector3 rotRandom) {
			eff_go.transform.localPosition = rotRandom;
				
			var parts = eff_go.GetComponentsInChildren<ParticleSystem>();	// パーティクルシステム

			foreach (var p in parts) {
				p.transform.localRotation = Quaternion.Euler(rotationRandomTmp.x, rotationRandomTmp.y, rotationRandomTmp.z);
				p.transform.eulerAngles = new Vector3(rotationRandomTmp.x, rotationRandomTmp.y, rotationRandomTmp.z);
				Debug.Log (p.transform.eulerAngles);
			}
		}

		//-----------------------------------//

		//-----------------------------------//
		// 1C.ランダム位置取得メソッド //
		//-----------------------------------//

		void GetRandomPos(Vector3 value) {
			
			positionRandomTmp =	new Vector3(UnityEngine.Random.Range(-value.x, value.x),
											UnityEngine.Random.Range(-value.y, value.y),
											UnityEngine.Random.Range(-value.z, value.z));

		}

		//-----------------------------------//
		//-----------------------------------//
		// 1C.ランダム回転取得メソッド //
		//-----------------------------------//

		void GetRandomRot(Vector3 value) {
			
			rotationRandomTmp =	new Vector3(UnityEngine.Random.Range(-value.x, value.x),
											UnityEngine.Random.Range(-value.y, value.y),
											UnityEngine.Random.Range(-value.z, value.z));

		}

		//-----------------------------------//

		//-----------------------------------//
		// 1C.ランダムスケール取得メソッド //
		//-----------------------------------//

		void GetRandomScale(Vector3 value) {

			scaleRandomTmp =	new Vector3(UnityEngine.Random.Range(-value.x, value.x),
											UnityEngine.Random.Range(-value.y, value.y),
											UnityEngine.Random.Range(-value.z, value.z));

		}

		//-----------------------------------//

		//--------------------------------------------------------------------//
		// 2A.エフェクト：スキルエフェクト配列から名前の合致するスキルエフェクトを取得 //
		//--------------------------------------------------------------------//

		EffectList GetEffectWithName(EffectList[] actions, string name) {
			foreach (EffectList s in actions) {
				if (s.name.Equals(name)) {
					return s;

				}
			}

			return new EffectList();
		}
		
		//--------------------------------------------------------------------//

		//----------------------------------------------------------------------------------------//
		// C1.エフェクト:引数の trans と name から, お互いの名前が合致するかもしくは name が空かの条件で,  //
		// trans が該当するオブジェクトかを判定し、trans を代入した node を返す						  //
		//----------------------------------------------------------------------------------------//

		Transform GetNodeWithName(Transform trans, string name) {
			Transform node = null;
			
			
			if (trans.name.Equals(name) || name.Length == 0) {
				node = trans;
				
			}
			if (!node) {
				foreach (Transform t in trans.transform) {
					node = GetNodeWithName2(t, name); 
					if (node) break;
				}
			}
			return node;
		}
		//----------------------------------------------------------------------------------------//

		//----------------------------------------------------------------------------------------------//
		// C2.エフェクト: 引数の trans と name から,お互いの名前が一致する場合には trans を代入した node を返す //
		//----------------------------------------------------------------------------------------------//

		Transform GetNodeWithName2(Transform trans, string name) {
			Transform node = null;
			
			if (trans.name.Equals(name)) {
				node = trans;
				
			}
			if (!node) {
				foreach (Transform t in trans.transform) {
					node = GetNodeWithName2(t, name);
					if (node) break;
				}
			}
			return node;
		}
		//----------------------------------------------------------------------------------------------//

		//------------------------------------------------------------------------------------------------------------------//
		// D1.引数の GameObject go の子供の <ParticleSystem>　で パーティクルを,　<Animation> で アニメーションを指定し,それぞれ再生 //
		//------------------------------------------------------------------------------------------------------------------//

		void PlayAll(GameObject go) {


			foreach (ParticleSystem p in go.GetComponentsInChildren<ParticleSystem>()) {
				
				p.transform.position = positionRandomTmp;
				p.transform.rotation = Quaternion.Euler (rotationRandomTmp);


				foreach (ParticleEmitter e in p.GetComponentsInChildren<ParticleEmitter>()) {

					e.transform.position = positionRandomTmp;
					e.transform.rotation = Quaternion.Euler (rotationRandomTmp);

				}
				p.Play ();
			}

			foreach (Animation anim in go.GetComponentsInChildren<Animation>()) {
				anim.Play();
			}
		}
		//------------------------------------------------------------------------------------------------------------------//

		//------------------------------------------------------------------------------------------------------------------//
		// D2.引数の GameObject go の子供の <ParticleSystem>　で パーティクルを,　<Animation> で アニメーションを指定し,それぞれ停止 //
		//------------------------------------------------------------------------------------------------------------------//

		void StopAll(GameObject go) {
			foreach (ParticleSystem p in go.GetComponentsInChildren<ParticleSystem>()) {
				p.Stop();
			}
			foreach (Animation anim in go.GetComponentsInChildren<Animation>()) {
				anim.Stop();
			}
			go.SetActive(false);
		}

		//------------------------------------------------------------------------------------------------------------------//
		// 文字列から特定文字列を削除する //
		//------------------------------------------------------------------------------------------------------------------//

		string ReplaceEmpty(string self, string oldValue)
		{
			return self.Replace(oldValue, string.Empty);
		}
		//------------------------------------------------------------------------------------------------------------------//


		//============================================================================
		// 非公開定義
		//============================================================================


		//------------------------------------------------------------------------------------------------------------------//
		// Effectlist[x].Effect.startFrame が 0 でない場合、 値分 Delayさせたうえで PlayEffect(e) 
		//------------------------------------------------------------------------------------------------------------------//

		private IEnumerator StartEffectMethod(float startFrame, float endFrame, Effect eff, int stopGoListNum)
		{
			actionStartTime = currentTime;

			float updateFrame = startFrame;

			// コルーチンとして--カウント
			if ((currentTime - actionStartTime) * frameTime < updateFrame * frameTime || (currentTime - actionStartTime) * frameTime == updateFrame * frameTime ) {
				while (updateFrame  > 0.0f) {

					yield return null;
					updateFrame--;
				}

				PlayEffect (eff);

				// EndFrameMethod()
				StartCoroutine(EndFrameMethod((float)eff.startFrame, (float)eff.endFrame, eff, stopGoListNum));
			}



		}
		//------------------------------------------------------------------------------------------------------------------//

		//------------------------------------------------------------------------------------------------------------------//
		// currentFrame が Effectlist[x].Effect.endFrame の 値に到達したら StopEffect(e) ※StartEffectMethod 内部にセット
		//------------------------------------------------------------------------------------------------------------------//
		private IEnumerator EndFrameMethod(float startFrame, float endFrame, Effect eff, int stopGoListNum)
		{
			
			actionStartTime = currentTime;
			float updateFrame = endFrame;

			if (startFrame <  endFrame) {
				
				GetRandomPos(eff.positionRandom);
				//Debug.Log ("Random Position: " + positionRandomTmp.x + " , " + positionRandomTmp.y + " , " + positionRandomTmp.z);
				GetRandomRot(eff.rotationRandom);
				//Debug.Log ("Random Rotaion: " + rotationRandomTmp.x + " , " + rotationRandomTmp.y + " , " + rotationRandomTmp.z);
				GetRandomScale(eff.scaleRandom);
				//Debug.Log ("Random Rotaion: " + scaleRandomTmp.x + " , " + scaleRandomTmp.y + " , " + scaleRandomTmp.z);
							
				while (updateFrame > startFrame)
				{

					GetRandomPos(eff.positionRandom);
					//Debug.Log ("Random Position: " + positionRandomTmp.x + " , " + positionRandomTmp.y + " , " + positionRandomTmp.z);
					GetRandomRot(eff.rotationRandom);
					//Debug.Log ("Random Rotaion: " + rotationRandomTmp.x + " , " + rotationRandomTmp.y + " , " + rotationRandomTmp.z);
					GetRandomScale(eff.scaleRandom);
					//Debug.Log ("Random Rotaion: " + scaleRandomTmp.x + " , " + scaleRandomTmp.y + " , " + scaleRandomTmp.z);

					updateFrame--;
					yield return null;

				}

				StopEffect (eff, stopGoListNum);

			}

		}
		//------------------------------------------------------------------------------------------------------------------//

		//------------------------------------------------------------------------------------------------------------------//
		// endFrame ジェネリックリストの降順ソート	※ currentMaxDuration の決定用途
		//------------------------------------------------------------------------------------------------------------------//

		private void CurrentMaxDurationSort(EffectList action)
		{
			// endFrame の 値から currentMaxDuration => currentSlider の終了地点 を決定する

			int max = 0;

			foreach (Effect eff in action.effects) {
				
				max = Mathf.Max (max, eff.endFrame);

			}

			currentMaxDuration = max;
		}
		//------------------------------------------------------------------------------------------------------------------//


		///////////////////////////////////////////
		/// 									/// 
		/// 		Effect Viewer Method		/// 
		///										/// 
		///////////////////////////////////////////


		///////////////////////////
		/// 					/// 
		///  Store Val to SOBJ	/// 
		///						/// 
		///////////////////////////
		
		//-----------------------------------------------------------//
		//　GameObject eff　の パラメータをScriptable Objectに保存する. //
		//-----------------------------------------------------------//

		void SaveParamToSOBJ(EffectList action , Effect e){

			for (int i = 0; i < action.effects.Length; i++) {
				
				////////////////
				// Model Name //
				////////////////			
				effectSequence.Model = model.name;	// string で　保存して Find.GameObjectで取得するか

				//////////////////
				// Element Name //
				//////////////////
				effectSequence.Name = effectName; //eff[i].effectName;

				///////////////////////
				// Effect Properties //
				///////////////////////			
				// AnimClip 
				effectSequence.AnimClip = action.animationClip;
				// Effect 						
				effectParameter[i].Effect = action.effects[i].effect;
				// Node		
				effectParameter[i].Node = action.effects[i].node;
				// isGlobal
				effectParameter[i].IsGlobal = action.effects[i].isGlobal; 

				///////////////
				// Transform //
				///////////////
				effectParameter[i].Position = action.effects[i].position;
				effectParameter[i].PositionRandom = action.effects[i].positionRandom;
				effectParameter[i].Rotation = action.effects[i].rotation;
				effectParameter[i].RotationRandom = action.effects[i].rotationRandom;
				effectParameter[i].Scale = action.effects[i].scale;
				effectParameter[i].ScaleRandom = action.effects[i].scaleRandom;
				// Particle Scale
				effectParameter[i].ParticleScale = action.effects[i].particleScale;

				///////////////
				//   Frame   //  
				///////////////
				effectSequence.setIsLoop(i,action.effects[i].isLoop);
				effectSequence.setStartFrame(i,action.effects[i].startFrame);
				effectSequence.setEndFrame (i, action.effects [i].endFrame);

			}

		}

		//-----------------------------------------------------------//		

		///////////////////////////
		/// 					/// 
		///  Load Val from SOBJ	/// 
		///						/// 
		///////////////////////////

		//-----------------------------------------------------------//
		//　GameObject eff　の パラメータをScriptable Objectから読み込む. //
		//-----------------------------------------------------------//

		void LoadParamFromSOBJ(EffectList action , Effect e){

			for (int i = 0; i < action.effects.Length; i++) {


				////////////////
				// Model Name //
				////////////////
				model.name = effectSequence.Model;		

				//////////////////
				// Element Name //
				//////////////////
				effectName = effectSequence.Name;  

				///////////////////////
				// Effect Properties //
				///////////////////////			
				// AnimClip 
				action.animationClip = effectSequence.AnimClip;
				// Effect 						
				action.effects[i].effect = effectParameter[i].Effect;
				// Node		
				action.effects[i].node = effectParameter[i].Node;
				// isGlobal 
				action.effects[i].isGlobal = effectParameter[i].IsGlobal; 
				
				///////////////
				// Transform //
				///////////////
				action.effects[i].position = effectParameter[i].Position;
				action.effects[i].positionRandom = effectParameter[i].PositionRandom;
				action.effects[i].rotation = effectParameter[i].Rotation;
				action.effects[i].rotationRandom = effectParameter[i].RotationRandom;
				action.effects[i].scale = effectParameter[i].Scale;
				action.effects[i].scaleRandom = effectParameter[i].ScaleRandom;
				// Particle Scale
				action.effects[i].particleScale = effectParameter[i].ParticleScale;

				///////////////
				//   Frame   //  
				///////////////
				action.effects[i].isLoop = effectSequence.getIsLoop(i);
				action.effects[i].startFrame = effectSequence.getStartFrame(i);
				action.effects[i].endFrame = effectSequence.getEndFrame (i);


			}

		}


		///////////////////////////////////////////
		/// 									/// 
		///      Create Scriptable Object		/// 
		///										/// 
		///////////////////////////////////////////

		// Scriptable Object 生成メソッド

		// scriptable object のラベルを登録する labels 
		readonly static string[] labels = {"Data", "ScriptableObject", string.Empty};

		//[MenuItem("Assets/Create ScriptableObject")]
		static void Create (string sobjName)
		{


			// パスの取得
			//string path = getSavePath (selectedObject);
			string path = string.Format ("{0}/{1}.asset", "Assets/Resources", sobjName );

			if (File.Exists (path))
				for (int i=1;; i++) {

					// {0} = dirPath と {1} = objectPath と i = number を結合して .asset を加えて path とする
					path = string.Format ("{0}/{1}({2}).asset", "Assets/Resources", sobjName, i);
					if (! File.Exists (path))
						break;

				}


			// "Empty" で登録されていた labels[2] に ScriptableObject の名称を登録
			labels[2] = EFF_PARAMETER_NAME;


			// インスタンスを生成
			ScriptableObject obj = ScriptableObject.CreateInstance (sobjName);

			// インスタンス obj を指定パスに生成
			AssetDatabase.CreateAsset (obj, path);

			// AssetDatabase.LoadAssetAtPath ->ラベルの追加
			//　指定の path 上に指定されたタイプのアセットを生成する。アセットファイルは複数のオブジェクトを含むことが可能
			// アセットパスの例)"Assets/MyTextures/hello.png".
			ScriptableObject sobj = AssetDatabase.LoadAssetAtPath (path, typeof(ScriptableObject)) as ScriptableObject;

			// ラベルは一つのアセットに複数登録して簡単に検索できるようにする仕組み
			AssetDatabase.SetLabels (sobj, labels);

			// ScriptableObject のリネーム
			AssetDatabase.RenameAsset(path, text);

			// ダーティフラグを設定してディスク上に保存させる
			EditorUtility.SetDirty (sobj);


		}




		//============================================================================
		// MonoBehaviour : Override関数
		//============================================================================

		///////////////////////////
		/// 					/// 
		///       Awake 		/// 
		///						/// 
		///////////////////////////
		
		void Awake(){
			
			
		}
		
		///////////////////////////
		/// 					/// 
		///       Start 		/// 
		///						/// 
		///////////////////////////
		
		
		// Use this for initialization
		void Start () {
			
			// Effect 設定

			stopGoList = new List<string> ();
			charaAnim = model.GetComponent<Animation>();
			
			#region Animation Slider定義
			/*
		// ※Animation Sliderの定義
			myAnimation = model.GetComponent<Animation>()["sc_idle_loop"];
			myAnimation.speed = 0;
			
		//
		*/
			#endregion
		}
		
				
		///////////////////////////
		/// 					/// 
		///       Update		/// 
		///						/// 
		///////////////////////////

		// ビューワーの再生 
		void Update() {

			currentTime += Time.deltaTime;

			if (playOrNot) {
				if (currentSlider < currentMaxDuration) {
					currentSlider++;
				}
			}

		}


			#region Animation Slider定義
			/*
		// ※Animation Sliderの定義

			// スライダーの値をアニメーション時間に適用

			myAnimation.time = hSliderValue;

			// 変数,状態 をスライダークリックのブールに適用

			sliderClick = false;

			if (Input.GetMouseButtonDown (0) == true || Input.GetMouseButtonDown (1) == true)
			{
				sliderClick = true;
			}
		*/
			#endregion
		
		
		//============================================================================
		// 非公開関数定義
		//============================================================================
			
		///////////////////////////
		/// 					/// 
		///       OnGUI 		/// 
		///						/// 
		///////////////////////////
			
			// プレイモードでのビューワー上に表示されるGUIの定義
			
		void OnGUI() {

			GUI.skin.textField.fontSize = 15;

			effectName = GUI.TextField(new Rect(10,10,210,20), effectName);
			// Elementの名称をここで取得[11/25]





		///////////////////////////
		///  Button to Play		/// 
		///////////////////////////
		#region buttonPlay定義

			buttonPlay = GUI.Button(new Rect(Screen.width / 1.5f, Screen.height * (1f/1.1f), 75, 50), "➤");
				


			if (buttonPlay) {
				EffectList action = GetEffectWithName(effectList, effectName);

				// 現時点のパラメータを ScriptableObject に保存 

				int i = 0;
				int j = 0;
					
				foreach(Effect e in action.effects) 
				{
					SaveParamToSOBJ (action,  action.effects[i]);
					i += 1;
				}					

				currentSlider = 0;
				playOrNot = true;


				CurrentMaxDurationSort(action);
				stopGoList.Clear ();

				//Skill Activate Effect	
				if (effectActivate != null) {	
	
					Transform hip = GetNodeWithName(model.transform, "hip");					
					GameObject.Instantiate(effectActivate, hip.transform.position, Quaternion.identity);

				}

				// Play Character Animation

				charaAnim.AddClip(action.animationClip, action.animationClip.name);	
				charaAnim.Play(action.animationClip.name);

				actionStartTime = currentTime;

				// stopGOList に Effect名(Clone)(UnityEngine.GameObject)を追加
				StopGameObjListMake ();

				// Play Effects
				foreach(Effect e in action.effects)
				{
					StartCoroutine(StartEffectMethod((float)e.startFrame, (float)e.endFrame, e , j));
					j += 1;
				}

				}

			#endregion
				
			///////////////////////////
			///  Button to Stop		/// 
			///////////////////////////
			#region buttonStop定義
				
				buttonStop = GUI.Button(new Rect(Screen.width / 1.27f, Screen.height * (1f/1.1f), 75, 50), "■");
				
				if (buttonStop) {

					playOrNot = false;
					int i = 0;

					EffectList action = GetEffectWithName(effectList, effectName);			

					actionStartTime = currentTime;

					foreach(Effect e in action.effects) {
					
						if (e.startFrame > 0) {
						
							if(e.effect != null){

								StopEffect(e, i);

							}
						}
						else {
							
						StopEffect(e, i);

						}

						stopGoList.Clear();

					i += 1;
					}
				}
		
			#endregion


				
			///////////////////////////
			///  Button to Load		/// 
			///////////////////////////

				
			buttonLoad = GUI.Button(new Rect(10,40,100,50), "Load");
				
				if (buttonLoad) {

					EffectList action = GetEffectWithName(effectList, effectName);

					for (int i = 0 ; i <  action.effects.Length; i++) 
					{

						LoadParamFromSOBJ (action, action.effects[i]);

					}

				}

				
				// Scriptable Object からパラメータを読み込み
				
			///////////////////////////
			///   Button to Reset	/// 
			///////////////////////////
				
				buttonReset = GUI.Button (new Rect (120, 40, 100, 50), "Reset");
				
				if (buttonReset) {
					
				EffectList action = GetEffectWithName (effectList, effectName);
					
				for(int i = 0; i <  action.effects.Length; ++i){
						
						
						//action.effects [i].effParamName = "";
						action.effects [i].node = "";
						action.effects [i].isGlobal = true;
						action.effects [i].position = new Vector3(0, 0, 0);
						action.effects [i].rotation = new Vector3(0, 0, 0);
						action.effects [i].scale = new Vector3(1, 1, 1);
						action.effects [i].particleScale = 1;
						action.effects [i].startFrame = 0;
						action.effects [i].endFrame = 100;
											
					}
				}


				//  ※Animation Slider フレーム数ボックスの定義
			    GUI.Box (new Rect (Screen.width / 1.27f, Screen.height * (1f/1.16f), 60, 30), currentSlider.ToString ());	

				GUI.HorizontalScrollbar(new Rect(60, Screen.height * (1f/1.2f), Screen.width * (1f/1.3f), 100), currentSlider, 0.0f, 0.0F, currentMaxDuration);


				/*Rect rect1 = new Rect (60, Screen.height * (1f / 1.08f), 150, Screen.height * (1f / 1.5f));
					isCheckTimeline = GUI.Toggle(rect1, isCheckTimeline, " タイムラインと同期");
				 Rect rect2 = new Rect (60, Screen.height * (1f / 1.05f), 300, Screen.height * (1f / 1.5f));
					isLoopOffset = GUI.Toggle(rect2, isLoopOffset, " ループパーティクルは1ループ後の表示とする");

			
				 frameCount = GUI.TextField(new Rect(Screen.width / 1.15f, Screen.height * (1f/1.12f),60, 30), string.Format ("{0:0.0}",currentSlider));
				*/


				/// <summary>
				/// Scriptable Object Generator
				/// </summary>

				text = GUI.TextField (new Rect(Screen.width * (1f/1.425f), Screen.height * (1f/80f), 200, 20), text, 40);


				buttonESN = GUI.Button (new Rect(Screen.width * (1f/1.425f), Screen.height * (1f/25f),  200, 30), "Sequence Data Generate ");

				if (buttonESN) {

					Create (EFF_SEQUENCE_NAME);

				}

				buttonEPN = GUI.Button (new Rect(Screen.width * (1f/1.425f), Screen.height * (1f/12f),200, 30), "Parameter Data Generate");

				if (buttonEPN) {

					Create (EFF_PARAMETER_NAME);

				}



			}

			
			#region Animation Slider定義
			/*
		    // ※Animation Sliderの定義
			GUI.Box (new Rect (10, Screen.height - 40, 360, 40), (30 * myAnimation.time).ToString ());


			// ■再生ボタン・停止ボタン
			if (myAnimation.speed == 1) {
				if (GUI.Button (new Rect (15, Screen.height - 30, 50, 20), "||")) // 停止
				{ 
					myAnimation.speed = 0;
				}
			}
			else
			{
				if(GUI.Button (new Rect(15, Screen.height-30,50, 20), "➤"))	// 再生
				{
					myAnimation.speed = 1;
				}
			}

			// ■スライダー部分をクリックするとアニメーションが停止する
			if (new Rect (70, Screen.height - 25, 275, 10).Contains (Event.current.mousePosition) && sliderClick == true) 
			{
				myAnimation.speed = 0;
			}

			// ■スライダー部分をドラッグするとアニメーションが逆再生
			hSliderValue = (GUI.HorizontalSlider (new Rect (70, Screen.height - 25, 275, 10), myAnimation.time, 0.0f, myAnimation.length));

			// ■アニメーションが最終フレームに達したら停止する
			if (myAnimation.time >= 83.2) 
			{
				myAnimation.speed = 0;
			}
			*/
			# endregion
			

			// HGParticleTimeline.cs--------------------------------------------------------------

			
			/// <summary>
			/// 非staticな初期化処理
			/// </summary>
			void InitNonStatic()
			{
				if (isAfterUnity51)
				{
					EditorApplication.update += Update;
				}
				OnSelectionChange();
			}
			

			/// <summary>
			/// Hierarchyの選択切替時に、処理対象のGameObjectを切り替える
			/// </summary>
			void OnSelectionChange()
			{
				GameObject sel = Selection.activeObject as GameObject;
				if (sel)
				{
					currentRootObj = GetRootGameObject(sel);
				}
			}
			

			/// <summary>
			/// 毎フレームの更新処理
			/// </summary>
			void UpdateAnimation()
			{
				EditorWindow w = EditorWindow.focusedWindow;
				if (w != null)
				{
					if (w.GetType().ToString().Equals("UnityEditor.AnimationWindow"))
					{
						currentAnimationWindow = w;
						
						if (currentRootObj != null)
						{
							if (currentAnimationWindow != null)
							{
								//currentTime = GetTimeFromAnimationWindow(currentAnimationWindow);	// ※リンクおかしいため一旦マスク[12/3]
							}
						}
					}
					else if (w.GetType().ToString().Equals("SgnLibD.HGParticleTimeline"))
					{
						currentAnimationWindow = null;
						currentMaxDuration = GetLongestDuration(currentRootObj);
						currentTime = currentSlider;
					}
				}
				
				if (!EditorApplication.isPlaying)
				{
					if (isCheckTimeline)
					{
						SimulateAllParticle(currentRootObj, currentTime);
					}
					
					//Repaint();
					
					if (currentAnimationWindow == null)
					{
						SceneView.RepaintAll();
					}
				}
			}
			

			/// <summary>
			/// ルートのGameObjectを得る
			/// </summary>
			GameObject GetRootGameObject(GameObject obj)
			{
				if (obj.transform.parent == null)
				{
					return obj;
				}
				return GetRootGameObject(obj.transform.parent.gameObject);
			}
			

			/// <summary>
			/// ツリー内ParticleSystemで、最長のdurationを得る
			/// </summary>
			float GetLongestDuration(GameObject obj)
			{
				float duration = 1f;
				if (obj != null)
				{
					var parts = obj.GetComponentsInChildren<ParticleSystem>();
					foreach (var p in parts)
					{
						if (p.duration > duration)
						{
							duration = p.duration;
						}
					}
				}
				return duration;
			}
			

			/// <summary>
			/// 指定ノード以下に存在するParticleSystemを指定時間のSimulate結果にする
			/// </summary>
			void SimulateAllParticle(GameObject root, float time)
			{
				if (root == null)
				{
					return;
				}
				
				ParticleSystem[] parts = root.GetComponentsInChildren<ParticleSystem>();
				foreach (var p in parts)
				{
					if (p.loop && isLoopOffset)
					{
						p.Simulate(time + p.duration);
					}
					else
					{
						p.Simulate(time);
					}
				}
			}
			
			/*
			/// <summary>
			/// AnimationWindowのタイムライン時間を得る
			/// </summary>
			float GetTimeFromAnimationWindow(EditorWindow w)
			{
				float time = 0f;
				
				FieldInfo fieldInfo;
				BindingFlags bindFlags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static;
				
				//Get Animation Editor
				fieldInfo = w.GetType().GetField("m_AnimEditor", bindFlags);
				if (fieldInfo != null)
				{
					//After Unity5.1
					
					var animEditor = fieldInfo.GetValue(w);
					//Debug.Log(animEditor);
					if (animEditor != null)
					{
						//Get Animation Window State
						fieldInfo = animEditor.GetType().GetField("m_State", bindFlags);
						var state = fieldInfo.GetValue(animEditor);
						//Debug.Log(state);
						if (state != null)
						{
							//Get Time and Frame
							time = (float)state.GetType().InvokeMember("currentTime", BindingFlags.GetProperty, null, state, null);
							//int frame = (int)state.GetType().InvokeMember("frame", BindingFlags.GetProperty, null, state, null);
						}
					}
				}
				else
				{
					//Legacy Unity
					time = (float)w.GetType().InvokeMember("get_time", BindingFlags.InvokeMethod, null, w, null);
				}
				
				return time;
			}
			*/
		
		


		}
	}


