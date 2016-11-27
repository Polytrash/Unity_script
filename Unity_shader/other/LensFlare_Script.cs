using UnityEngine;
using System.Collections;


[ExecuteInEditMode]
public class LensFlare_Script : MonoBehaviour
{
    public Shader LensFlare_Shader;
    public Shader BrightPassFilterShader;


    public float Threshold = 0.0f;
    public int Downsampling = 1;
    public Color LensColor;
    public float HaloWidth = 1.0f;
    public float Dispersal = 1.0f;
    public float Distortion = 1.0f;

    private Material BrightPassFilterMaterial = null;
    private Material LensFlare_Material = null;

    private bool isOpenGL;

    private Material GetMaterial()
    {
        if (LensFlare_Material == null)
        {
            LensFlare_Material = new Material(LensFlare_Shader);
            LensFlare_Material.hideFlags = HideFlags.HideAndDontSave;
        }
        return LensFlare_Material;
    }

    private Material GetIEMaterial()
    {
        if (BrightPassFilterMaterial == null)
        {
            BrightPassFilterMaterial = new Material(BrightPassFilterShader);
            BrightPassFilterMaterial.hideFlags = HideFlags.HideAndDontSave;
        }
        return BrightPassFilterMaterial;
    }

    // Use this for initialization
    void Start()
    {
        if (!SystemInfo.supportsImageEffects)
        {
            enabled = false;
            return;
        }

        if (LensFlare_Shader == null)
        {
            Debug.LogError("shader missing!", this);
        }

        if (BrightPassFilterShader == null)
        {
            Debug.LogError("shader missing!", this);
        }

        isOpenGL = SystemInfo.graphicsDeviceVersion.StartsWith("OpenGL");
    }

    // Update is called once per frame
    void Update()
    {
        Threshold = Mathf.Clamp(Threshold, -1.0f, 0.0f);
    }

    void OnRenderImage(RenderTexture source, RenderTexture dest)
    {
        int ImageWidth = 1;
        int ImageHeight = 1;

        if (isOpenGL)
        {
            ImageWidth = source.width;
            ImageHeight = source.height;
        }


            //Step #1: Downsample screen, extract bright parts
            RenderTexture Extract = RenderTexture.GetTemporary(ImageWidth, ImageHeight, 0);
            GetIEMaterial().SetVector("_uScale", new Vector4(Downsampling, Downsampling, Downsampling, Downsampling));
            GetIEMaterial().SetVector("_uBias", new Vector4(Threshold, Threshold, Threshold, Threshold));
            Graphics.Blit(source, Extract, GetIEMaterial());

            //Step #2: Render Lens flare on Screen
            GetMaterial().SetFloat("_HorizontalSize", Screen.width);
            GetMaterial().SetFloat("_uHaloWidth", HaloWidth);
            GetMaterial().SetFloat("_uDistortion", Distortion);
            GetMaterial().SetFloat("_uDispersal", Dispersal);
            GetMaterial().SetColor("_uLensColor", LensColor);

            Graphics.Blit(Extract, dest, GetMaterial());


            RenderTexture.ReleaseTemporary(Extract);

        

    }

    void OnDisable()
    {
            DestroyImmediate(GetIEMaterial());
    }

}