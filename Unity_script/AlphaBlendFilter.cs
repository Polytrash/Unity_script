using UnityEngine;
using System.Collections;


[ExecuteInEditMode]
public class AlphaBlendFilter : MonoBehaviour {
	
		public Shader abShader;

		public Texture2D maskTex;
		public Color tintColor;
		public float blendAmount = 0.5f;

		private Material abMaterial = null;
		private bool isOpenGL;

		private Material GetMaterial()
		{
			if (abMaterial == null)
			{
				abMaterial = new Material(abShader);
				abMaterial.hideFlags = HideFlags.HideAndDontSave;
			}
			return abMaterial;
		}

		void Start()
		{
			if (abShader == null)
			{
				Debug.LogError("shader missing!", this);
			}
			isOpenGL = SystemInfo.graphicsDeviceVersion.StartsWith("OpenGL");
		}

		void OnRenderImage(RenderTexture source, RenderTexture dest)
		{
			//If we run in OpenGL mode, our UV coords are
			//not in 0-1 range, because of the texRECT sampler
			float ImageWidth = 1;
			float ImageHeight = 1;
			if (isOpenGL)
			{
				ImageWidth = source.width;
				ImageHeight = source.height;
			}
			GetMaterial ().SetTexture ("_MaskTex", maskTex);
			GetMaterial().SetColor("_TintColor", tintColor);
			GetMaterial ().SetFloat ("_BlendAmount", blendAmount);
			GetMaterial().SetFloat("_iHeight",ImageWidth);
			GetMaterial().SetFloat("_iWidth", ImageHeight);
			//ImageEffects.BlitWithMaterial(GetMaterial(), source, dest);

			Graphics.Blit (source, dest, GetMaterial());
		}
	}