using System;
using UnityEditor;
using UnityEngine;

[ExecuteInEditMode]
[AddComponentMenu("Image Effects/Dithering")]
public class Dithering : MonoBehaviour
{
    public Shader DitheringShader;
    public Material DitheringMaterial;
    public Texture DitheringTexture;

    public int RedSteps = 8;
    public int GreenSteps = 8;
    public int BlueSteps = 4;

    public int HueSteps = 8;
    public int SaturationSteps = 4;
    public int ValueSteps = 8;

    public int BrightnessSteps = 2;

    private bool isOpenGL;
    int _lastScreenX;
    int _lastScreenY;



    void Awake()
    {
        _lastScreenX = _lastScreenY = -1;
    }

    void Start()
    {
        if (DitheringMaterial == null)
        {
            Debug.LogError("shader missing!", this);
        }
        isOpenGL = SystemInfo.graphicsDeviceVersion.StartsWith("OpenGL");
    }


    Material GetMaterial()
    {
        if (DitheringMaterial == null)
        {
            DitheringMaterial = new Material(DitheringShader);
            DitheringMaterial.hideFlags = HideFlags.HideAndDontSave;
            DitheringMaterial.SetTexture("_DitheringTex", DitheringTexture);
            SetSteps(DitheringMaterial);
        }
        return DitheringMaterial;
    }

    void SetSteps(Material material)
    {

        material.SetFloat("_ColorStepsA", (BrightnessSteps - 1) / 3f);
        material.SetFloat("_ColorStepsB", 1f / (BrightnessSteps - 1));

    }

    public void Repaint()
    {
        DitheringMaterial = null;
        _lastScreenX = _lastScreenY = -1;
    }

    void OnEnable()
    {
        Repaint();
    }

    [ImageEffectOpaque]
    void OnRenderImage(RenderTexture source, RenderTexture destination)
    {

        Material material = GetMaterial();
        float ImageWidth = 1;
        float ImageHeight = 1;
        if (isOpenGL)
        {
            ImageWidth = source.width;
            ImageHeight = source.height;
        }

        if (DitheringMaterial == null)
        {
            DitheringShader = Shader.Find("Dither/ColoredHSVDithering");
            DitheringMaterial = CheckShaderAndCreateMaterial(DitheringShader, DitheringMaterial);
        }

        GetMaterial().SetFloat("_ColorSteps", BrightnessSteps);
        GetMaterial().SetFloat("_ColorStepsA", RedSteps);
        GetMaterial().SetFloat("_ColorStepsB", GreenSteps);


        Vector2 ditherUV = new Vector2(ImageWidth, ImageHeight);
        GetMaterial().SetVector("_SceenAndTex", new Vector4(ditherUV.x / (float)DitheringTexture.width, ditherUV.y / (float)DitheringTexture.height, 0, 0));

        Graphics.Blit(source, destination, GetMaterial());

    }

    protected virtual void OnDisable()
    {
        if (DitheringMaterial) DestroyImmediate(DitheringMaterial);
    }

    // Unity StandardAssets.ImageEffect 
    protected Material CheckShaderAndCreateMaterial(Shader s, Material m2Create)
    {
        if (!s)
        {
            Debug.Log("Missing shader in " + ToString());
            enabled = false;
            return null;
        }

        if (s.isSupported && m2Create && m2Create.shader == s)
            return m2Create;
        /*
        if (!s.isSupported)
        {
            NotSupported();
            Debug.Log("The shader " + s.ToString() + " on effect " + ToString() + " is not supported on this platform!");
            return null;
        }
        */
        m2Create = new Material(s);
        // createdMaterials.Add(m2Create);
        m2Create.hideFlags = HideFlags.DontSave;

        return m2Create;
    }
}