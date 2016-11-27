Shader "Custom/LensFlare_Shader" {
	Properties 
	{
		_MainTex ("Base (RGB)", 2D) = "white" {}
	}
	SubShader 
	{
		Pass
		{
		
		CGPROGRAM
		#pragma vertex vert_img
		#pragma fragment frag
		#pragma fragmentoption ARB_precision_hint_fastest
		#pragma target 3.0
		#include "UnityCG.cginc"
		

		uniform sampler2D _MainTex;
		uniform float4 _uLensColor;
		uniform float _uDispersal;
		uniform float _uHaloWidth;
		uniform float _uDistortion;
		uniform int _uSamples;
		uniform float _HorizontalSize;

//--------------Distortion Function---------------------------------------*/
		float4 texDistorted(in sampler2D tex, in float2 texcoord, in float2 direction, in float3 distortion)
		 {
			return float4(tex2D(tex, texcoord + direction * distortion.r).r,
						tex2D(tex, texcoord + direction * distortion.g).g,
						tex2D(tex, texcoord + direction * distortion.b).b, 1.0);
		}
		
//----------------------------------------------------------------------------*/
		
		float4 frag(v2f_img i) : COLOR
		{
			float2 texcoord = -i.uv + float2(1.0, 1.0); //Flip the texcoordinates
			float2 texelSize = 1.0 / _HorizontalSize;
			
			float2 ghostVec = (float2(0.5, 0.5) - texcoord) * _uDispersal;
			float2 haloVec = normalize(ghostVec) * _uHaloWidth;
			
			float3 distortion = float3(-texelSize.x * _uDistortion, 0.0, texelSize.x * _uDistortion);
			
			//sample ghost
			//unroll (8)]
			float4 result = float4(0, 0, 0, 0);
			for (int i = 0; i < 8; i++) 
			{
				float2 offset = frac(texcoord + ghostVec * float(i));
				
				float weight = length(float2(0.5, 0.5) - offset) / length(float2(0.5, 0.5));
				weight = pow(1.0 - weight, 10.0);
				
				result += texDistorted(_MainTex, offset, normalize(ghostVec), distortion) * weight;
			}
				float2 thistex = length(float2(0.5, 0.5) - texcoord) / length(float2(0.5, 0.5));
			
				result *= _uLensColor;
				
			//sample halo
			half thislength = length(float2(0.5, 0.5) - frac(texcoord + haloVec));
			float weight = thislength / length(float2(0.5, 0.5));
			weight = pow(1.0 - weight, 10.0);
			result += texDistorted(_MainTex, frac(texcoord + haloVec), normalize(ghostVec), distortion) * weight;
			
			return result;
			
			}
		

		ENDCG
		
	 }
  }
}