using System;
using UnityEngine;

namespace UnityStandardAssets.ImageEffects
{
    [ExecuteInEditMode]
    [RequireComponent(typeof(Camera))]
    [AddComponentMenu("Image Effects/Edge Detection/Edge Detection")]
    public class EdgeDetector  : PostEffectsBase {


        public float sensitivityDepth = 1.0f;
        public float sensitivityNormals = 1.0f;
        public float lumThreshold = 0.2f;
        public float edgeExp = 1.0f;
        public float sampleDist = 1.0f;
        public float edgesOnly = 0.0f;
        public Color edgesOnlyBgColor = Color.white;

        public Shader edgeDetectorShader;
        private Material edgeDetectorMaterial = null;
        private bool isOpenGL;



        private Material GetMaterial()
        {
            if (edgeDetectorMaterial == null)
            {
                edgeDetectorMaterial = new Material(edgeDetectorShader);
                edgeDetectorMaterial.hideFlags = HideFlags.HideAndDontSave;
            }
            return edgeDetectorMaterial;
        }


        new void Start()
        {
            edgeDetectorMaterial = CheckShaderAndCreateMaterial(edgeDetectorShader, edgeDetectorMaterial);
            if (edgeDetectorShader == null)
            {
                Debug.LogError("shader missing!", this);
            }
            isOpenGL = SystemInfo.graphicsDeviceVersion.StartsWith("OpenGL");
        }


        [ImageEffectOpaque]
        void OnRenderImage(RenderTexture source, RenderTexture destination)
        {
            float ImageWidth = 1;
            float ImageHeight = 1;
            if (isOpenGL)
            {
                Graphics.Blit(source, destination);
                ImageWidth = source.width;
                ImageHeight = source.height;
            }

            Vector2 sensitivity = new Vector2(sensitivityDepth, sensitivityNormals);
            edgeDetectorMaterial.SetVector("_Sensitivity", new Vector4(sensitivity.x, sensitivity.y, 1.0f, sensitivity.y));
            edgeDetectorMaterial.SetFloat("_BgFade", edgesOnly);
            edgeDetectorMaterial.SetFloat("_SampleDistance", sampleDist);
            edgeDetectorMaterial.SetVector("_BgColor", edgesOnlyBgColor);
            edgeDetectorMaterial.SetFloat("_Exponent", edgeExp);
            edgeDetectorMaterial.SetFloat("_Threshold", lumThreshold);

            Graphics.Blit(source, destination, edgeDetectorMaterial);
        }
    }
}
