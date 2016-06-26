using UnityEngine;
using System.Collections;


[ExecuteInEditMode]
public class SSFogFilter : MonoBehaviour {

	public Shader ssFogShader;

	public Texture2D maskTex1;
	public Texture2D maskTex2;
	public Texture2D noiseTex;
	public Color tintColor;
	public float blendAmount = 0.5f;
	public float flowMapOffsetX = 0.0f;
	public float flowMapOffsetY = 0.0f;
	public float timeScale;

	bool reach = true;


	float m_fFlowMapOffset0 = 0.0f;
	float m_fFlowMapOffset1 = 0.0f;
	float m_fCycle = 0.1f;
	float m_fWaveSpeed = 0.1f;
	float m_fWaveMapScale = 2.0f;



	private Material ssFogMaterial = null;
	private bool isOpenGL;

	private Material GetMaterial()
	{
		if (ssFogMaterial == null)
		{
			ssFogMaterial = new Material(ssFogShader);
			ssFogMaterial.hideFlags = HideFlags.HideAndDontSave;
		}
		return ssFogMaterial;
	}

	void Start()
	{
		if (ssFogShader == null)
		{
			Debug.LogError("shader missing!", this);
		}
		isOpenGL = SystemInfo.graphicsDeviceVersion.StartsWith("OpenGL");
	}

	void Update()
	{

			m_fFlowMapOffset0 = Mathf.Repeat (m_fFlowMapOffset0 + m_fWaveSpeed * Time.deltaTime * timeScale, 1.0f);

			Debug.Log(m_fFlowMapOffset0);

		float _fHalfCycle = m_fCycle ;

		Shader.SetGlobalFloat ("flowMapOffset0", m_fFlowMapOffset0 );
		Shader.SetGlobalFloat ("halfCycle", m_fCycle);
		Shader.SetGlobalFloat ("fWaveSpeed", m_fWaveSpeed);
		Shader.SetGlobalFloat ("fWaveScale", m_fWaveMapScale);


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
		GetMaterial ().SetTexture ("_MaskTex1", maskTex1);
		GetMaterial ().SetTexture ("_MaskTex2", maskTex2);
		GetMaterial ().SetTexture ("_NoiseMap", noiseTex);
		GetMaterial().SetColor("_TintColor", tintColor);
		GetMaterial ().SetFloat ("_BlendAmount", blendAmount);
		GetMaterial().SetFloat("_iHeight",ImageWidth);
		GetMaterial().SetFloat("_iWidth", ImageHeight);
		//ImageEffects.BlitWithMaterial(GetMaterial(), source, dest);

		Graphics.Blit (source, dest, GetMaterial());
	}
}