Shader "Custom/LensFlare_Filter" {
	Properties {
		_MainTex ("Base (RGB)", 2D) = "white" {}
		_uScale ("", Range(0.0,1.0)) = 1.0
		_uBias ("", Range(0.0,1.0)) = 1.0
		_Blend("", Float) = 0
		_BlendAmount ("", Range(0, 10)) = 1.0
	}
	SubShader 
	{
		Pass
		{
		
		CGPROGRAM
		#pragma vertex vert_img
		#pragma fragment frag
		#pragma fragmentoption ARB_precision_hint_fastest
		#pragma target 4.0
		#include "UnityCG.cginc"

		uniform sampler2D _MainTex;
		uniform float4 _uScale;
		uniform float4 _uBias;
 		uniform float  _BlendAmount;

         struct v2f{

        	float4 pos : POSITION;
        	half2  uv : TEXCOORD0;
        	half3  col : COLOR0;
        };

		v2f vert(appdata_img v){

	        v2f o;
    	    o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
        	o.uv = MultiplyUV(UNITY_MATRIX_TEXTURE0, v.texcoord.xy);
        	//o.uv1 = TRANSFORM_TEX (v.texcoord, _MaskTex1);

        	return o;
        }
		//struct v2p
		//{
		//	noperspective float2 vTexcoord : TEXCOORD0;
		//};
		
		//struct result
		//{
		//	float4 fResult : COLOR;
		//};
		
		//void main(in v2p IN, out result OUT)
		//{
			//OUT.fResult = max(float4(0,0,0,0), tex2D(_MainTex, IN.vTexcoord) + _uBias) * _uScale;
		//}
		
		float4 frag(v2f_img i) : COLOR
		{

			half4 color = tex2D(_MainTex, i.uv * _uScale);
			half4 colorW = half4(1.0, 1.0, 1.0, 1.0);
			float blendValue =  _BlendAmount ;

			color.r +=  colorW.r - (colorW.r - lerp(color.r,  color.r,  (1 -  color.r * blendValue) ) ) / colorW.r;
			color.g +=  colorW.g - (colorW.g - lerp(color.g,  color.g,  (1 -  color.r * blendValue) ) ) / colorW.g;
			color.b +=  colorW.b - (colorW.b - lerp(color.b,  color.b,  (1 -  color.r * blendValue) ) ) / colorW.b;
			
			float4 result = colorW - (colorW - lerp(color,  color,  blendValue) ) / colorW;
			result = max(float4(0,0,0,0), tex2D(_MainTex, i.uv * _uScale) + _uBias);
			return result;
		
		}

		ENDCG
		} 
	}
}