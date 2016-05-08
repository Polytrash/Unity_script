Shader "Anio/AAA Plants (PBS)" 
{
	Properties 
	{
		[Header(Scaling)]
		_ScaleX ("x:", float) = 1
        _ScaleY ("y:", float) = 1
				
		[Header(Cutoff)]_Cutoff ("", Range(0, 1)) = 0.25		
		
        [Header(Albedo)]_MainTint ("Tint", color) = (1,1,1,1)
        [NoScaleOffset]_MainTex ("Base (RGB)", 2D) = "white" {} 
		
		[Header(Normal maping)]
		_NormalMapPower ("", Range(0, 2)) = 1
        [NoScaleOffset]_NormalMap ("Map", 2D) = "bump" {}
		
		[Header(AO)]
		_OcclusionPower ("", Range(0, 2)) = 0.4			
		[Toggle]_AOPBSState ("PBS", float) = 0
        [NoScaleOffset]_Occlusion ("Map", 2D) = "white" {}

		[Header(Smoothness)]
		_SmoothnessPower ("", Range(0, 1)) = 0.4

		[Header(Metallic)]
		_MetallicPower ("", Range(0,1)) = 0.0
		[Toggle]_MetallicMapingState ("Maping state", float) = 0
		[NoScaleOffset]_Metallic ("Map", 2D) = "black" {}
			
		[Header(Emission)]
		_EmissionPower ("", Range(0,1)) = 0.0			
        _EmissionTint ("Main tint", color) = (1,1,1,0)
		[Toggle]_EmissionMapingState ("Maping state", float) = 0
		[NoScaleOffset]_Emission ("Map", 2D) = "black" {}

		[Header(Translucency)]
		_TransCommonPower  ("", Range(0,3)) = 1	
		_TransForwardPower ("Forward trans", Range(0,3)) = 1	
		_TransDifusePower  ("Difuse trans", Range(0,3)) = 1	
		_DifuseReflPower   ("Difuse reflection", Range(0,3)) = 1	
		_Shading ("Shading", Range(0,1)) = 0.3
		_Sharpness ("Sharpness", Range(0,100)) = 10
		_DiffuseTranslucentColor ("Diffuse Translucent Color", Color) 
		= (1,1,1,1) 
		_ForwardTranslucentColor ("Forward Translucent Color", Color) 
		= (1,1,1,1) 
		[Toggle]_TransMapingState ("Maping state", float) = 0
		[NoScaleOffset]_TransMap ("Map", 2D) = "black" {}
	}

	SubShader 
	{
		Tags {  } 
		Cull Off
 
		CGPROGRAM
 
		#pragma surface surf Standard vertex:vert
		#pragma target 4.0
		
 		#include "UnityCG.cginc"
 
        uniform sampler2D _Emission;
        uniform sampler2D _Occlusion;
        uniform sampler2D _Metallic;
        uniform sampler2D _MainTex;
        uniform sampler2D _NormalMap;
        uniform sampler2D _TransMap;
		
		fixed _ScaleX, _ScaleY;
		fixed _Cutoff;

        fixed _EmissionPower;
        fixed _OcclusionPower;
        fixed _NormalMapPower;
		fixed _MetallicPower;
		fixed _SmoothnessPower;
		fixed _TransForwardPower, _TransCommonPower, _TransDifusePower, _DifuseReflPower;
		uniform fixed _Sharpness, _Shading;		
		fixed _MetallicMapingState, _EmissionMapingState, _AOPBSState, _TransMapingState;

		float4 _MainTint, _EmissionTint;

		uniform float4 _DiffuseTranslucentColor; 
		uniform float4 _ForwardTranslucentColor; 

 		struct appdata{
			float4 vertex    : POSITION;  // The vertex position in model space.
			float3 normal    : NORMAL;    // The vertex normal in model space.
			float4 texcoord  : TEXCOORD0; // The first UV coordinate.
			float4 texcoord1 : TEXCOORD1; // The second UV coordinate.
			float4 texcoord2 : TEXCOORD2; // The third UV coordinate.
			float4 tangent   : TANGENT;   // The tangent vector in Model Space (used for normal mapping).
			float4 color     : COLOR;     // Per-vertex color.
		};

		struct Input 
		{
			float2 uv_MainTex;
            float4 pos : SV_POSITION;
            float4 posWorld : TEXCOORD0;
            float3 normalDir : TEXCOORD1;
		};

		void vert (inout appdata v, out Input o) 
		{
			UNITY_INITIALIZE_OUTPUT(Input,o);
			o.posWorld = mul(_Object2World, v.vertex);
			o.normalDir = normalize(
               mul(float4(v.normal, 0.0), _World2Object).xyz);
			o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
		}

		void surf (Input IN, inout SurfaceOutputStandard o) 
		{ 
			float3 normalDirection = normalize(IN.normalDir);
            float3 viewDirection = normalize(
               _WorldSpaceCameraPos - IN.posWorld.xyz);
 
            normalDirection = faceforward(normalDirection,
               -viewDirection, normalDirection);
               // flip normal if dot(-viewDirection, normalDirection)>0
 
            float3 lightDirection;
            float attenuation;
 
            if (0.0 == _WorldSpaceLightPos0.w) // directional light?
            {
               attenuation = 1.0; // no attenuation
               lightDirection = normalize(_WorldSpaceLightPos0.xyz);
            } 
            else // point or spot light
            {
               float3 vertexToLightSource = 
                  _WorldSpaceLightPos0.xyz - IN.posWorld.xyz;
               float distance = length(vertexToLightSource);
               attenuation = 1.0 / distance; // linear attenuation 
               lightDirection = normalize(vertexToLightSource);
            }
 
            // Computation of the Phong reflection model:
 
            float3 ambientLighting = 
               UNITY_LIGHTMODEL_AMBIENT.rgb;
			   
            float3 diffuseReflection = 
               attenuation * _LightColor0.rgb
               * max(_Shading, dot(normalDirection, lightDirection));
			 
            float3 diffuseTranslucency = 
               attenuation * _LightColor0.rgb 
               * _DiffuseTranslucentColor.rgb 
               * max(_Shading, dot(lightDirection, -normalDirection));
 
            float3 forwardTranslucency;
            if (dot(normalDirection, lightDirection) > 0.0) 
               // light source on the wrong side?
            {
               forwardTranslucency = float3(0.0, 0.0, 0.0); 
                  // no forward-scattered translucency
            }
            else // light source on the right side
            {
               forwardTranslucency = attenuation * _LightColor0.rgb
                  * _ForwardTranslucentColor.rgb * pow(max(0.0, 
                  dot(-lightDirection, viewDirection)), _Sharpness);
            }
 
            // Computation of the complete illumination:
 
            float3 transLight = ambientLighting 
							+ diffuseReflection   * _DifuseReflPower 
							+ diffuseTranslucency * _TransDifusePower
							+ forwardTranslucency * _TransForwardPower;

			if(_TransMapingState)
				transLight *= tex2D(_TransMap, fixed2(IN.uv_MainTex.x * _ScaleX, IN.uv_MainTex.y * _ScaleY));
			//--------
						
            half4 c = tex2D(_MainTex, fixed2(IN.uv_MainTex.x * _ScaleX, IN.uv_MainTex.y * _ScaleY)) * _MainTint;
			if(c.a < _Cutoff)
				discard;
            o.Albedo = c.rgb;
			o.Albedo = lerp(o.Albedo, transLight * o.Albedo, _TransCommonPower);
				
			//Ambient Occlusion
			float4 occlustionMap = tex2D(_Occlusion, fixed2(IN.uv_MainTex.x * _ScaleX, IN.uv_MainTex.y * _ScaleY));
			if(_AOPBSState == 0)
				o.Albedo = lerp(o.Albedo, o.Albedo * occlustionMap.rgb, _OcclusionPower);
			else
				o.Occlusion = occlustionMap * _OcclusionPower;
			
			//Normal
            o.Normal = UnpackNormal(tex2D(_NormalMap, fixed2(IN.uv_MainTex.x * _ScaleX, IN.uv_MainTex.y * _ScaleY))* _NormalMapPower);

			//Metallic
			if(_MetallicMapingState == 0)
				o.Metallic = _MetallicPower;
			else
				o.Metallic = tex2D(_Metallic, fixed2(IN.uv_MainTex.x * _ScaleX, IN.uv_MainTex.y * _ScaleY)) * _MetallicPower;
					
			//Emission
			if(_EmissionMapingState == 0)
				o.Emission = _EmissionPower * _EmissionTint;
			else
				o.Emission = tex2D(_Emission, fixed2(IN.uv_MainTex.x * _ScaleX, IN.uv_MainTex.y * _ScaleY)) * _EmissionPower * _EmissionTint;

			o.Smoothness = _SmoothnessPower;					
		}          
		ENDCG
	}
}