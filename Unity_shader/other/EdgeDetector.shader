Shader "Custom/EdgeDetector" {
		Properties {
		_MainTex ("Base (RGB)", 2D) = "" {}
	}

	CGINCLUDE
	
	#include "UnityCG.cginc"
	
	struct v2f {
		float4 pos : SV_POSITION;
		float2 uv[5] : TEXCOORD0;
	};
	
	struct v2fd {
		float4 pos : SV_POSITION;
		float2 uv[2] : TEXCOORD0;
	};

	sampler2D _MainTex;
	uniform float4 _MainTex_TexelSize;
	half4 _MainTex_ST;

	sampler2D _CameraDepthNormalsTexture;
	half4 _CameraDepthNormalsTexture_ST;

	sampler2D_float _CameraDepthTexture;
	half4 _CameraDepthTexture_ST;

	uniform half4 _Sensitivity; 
	uniform half4 _BgColor;
	uniform half _BgFade;
	uniform half _SampleDistance;
	uniform float _Exponent;

	uniform float _Threshold;

	struct v2flum {
		float4 pos : SV_POSITION;
		float2 uv[3] : TEXCOORD0;
	}; 

//----------------------------------------------------------------------------//

 			// ノイズ生成用ハッシュ関数

			float hash( float n )
			{
				return frac(sin(n)*43758.5453);
			}

			// ノイズ関数

			float noise( float3 x )
			{
			// The noise function returns a value in the range -1.0f -> 1.0f


				float3 p = floor(x);
				float3 f = frac(x);					
				f = f*f*(3.0-2.0*f);

				float n = p.x + p.y*57.0 + 113.0*p.z;

				return lerp(lerp(lerp( hash(n+0.0), hash(n+1.0),f.x),
						lerp( hash(n+57.0), hash(n+58.0),f.x),f.y),
						lerp(lerp( hash(n+113.0), hash(n+114.0),f.x),
						lerp( hash(n+170.0), hash(n+171.0),f.x),f.y),f.z);
			}	
//----------------------------------------------------------------------------//

	v2flum vertLum (appdata_img v)
	{
		v2flum o;
		o.pos = mul (UNITY_MATRIX_MVP, v.vertex);


		float2 uv = MultiplyUV( UNITY_MATRIX_TEXTURE1, v.texcoord );
		
		o.uv[0] = UnityStereoScreenSpaceUVAdjust(uv, _MainTex_ST);
		o.uv[1] = UnityStereoScreenSpaceUVAdjust(uv + float2(-_MainTex_TexelSize.x, -_MainTex_TexelSize.y) * _SampleDistance, _MainTex_ST);
		o.uv[2] = UnityStereoScreenSpaceUVAdjust(uv + float2(+_MainTex_TexelSize.x, -_MainTex_TexelSize.y) * _SampleDistance, _MainTex_ST);
		
		return o;
	}


	fixed4 fragLum (v2flum i) : SV_Target
	{	


		fixed4 original = tex2D(_MainTex, i.uv[0]);

		// a very simple cross gradient filter
  		float n = noise(i.pos.xyz);

		half3 p1 = original.rgb;
		half3 p2 = tex2D(_MainTex, i.uv[1]).rgb;
		half3 p3 = tex2D(_MainTex, i.uv[2]).rgb;
	
		half3 diff = p1 * 2 - p2 - p3 ;
									 
		half len = dot(diff, _BgColor);
		len = step(len, _Threshold );
									
		
		//if(len >= _Threshold)
		//	original.rgb = 0;	   

		return   lerp(original, original*_BgColor, 1-len * _BgFade);			
	}	
	


	ENDCG 

Subshader {
	 Pass {
	  ZTest Always Cull Off ZWrite Off

      CGPROGRAM
	  #pragma target 3.0   
      #pragma vertex vertLum
      #pragma fragment fragLum
      ENDCG
  }
}

Fallback off
	
} // shader


