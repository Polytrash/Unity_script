Shader "Dither/ColoredHSVDithering" 
{
	Properties 
	{
		_MainTex ("Base (RGB)", 2D) = "white" {}
		_DitheringTex ("Dithering(R)", 2D) = "white" {}
		_RGBToHSV ("_RGBToHSV", 3D) = "white" {}
		_HSVToRGB ("_HSVToRGB", 3D) = "white" {}
		_ColorSteps ("Color Steps", Vector) = (4,0.25,0,0)
		_ColorStepsA ("Color StepsA", Vector) = (4, 4, 4, 0)
		_ColorStepsB ("Color StepsB", Vector) = (0.25, 0.25, 0.25, 0)

		_SceenAndTex ("SceenAndTex", Vector) = (1024,768,2,2)
	}

	SubShader 
	{
		Pass 
		{
			ZTest Always ZWrite Off
			Fog { Mode off }
					
			CGPROGRAM

			#pragma vertex vert_img
			#pragma fragment frag

			#include "UnityCG.cginc"

			uniform sampler2D _MainTex;
			uniform sampler2D _DitheringTex;
			uniform float3 _ColorStepsA;
			uniform float3 _ColorStepsB;
			uniform float4 _SceenAndTex;




			inline float3 rgb_to_hsv(float3 rgb)
			{
				float4 a = (rgb.g < rgb.b) ? float4(rgb.bg, -1, 2/3) : float4(rgb.gb, 0, -1/3);
				float4 b = (rgb.r < a.x) ? float4(a.xyw, rgb.r) : float4(rgb.r, a.yzx);
				float c = b.x - min(b.w, b.y);
				const float eps = 1e-10;
				float h = abs((b.w - b.y) / (6 * c + eps) + b.z);
				float3 hcv = float3(h, c, b.x);
				float S = hcv.y / (hcv.z + eps);
				return float3(hcv.x, S, hcv.z);
			}

			inline float3 hsv_to_rgb(float3 hsv)
			{
				float3 rgb = float3(0,2,2) + float3(1,-1,-1) * abs(hsv.x * 6 - float3(3,2,4)) - float3(1,0,0);
				rgb = saturate(rgb);
				return ((rgb - 1) * hsv.y + 1) * hsv.z;
			}


			fixed4 frag (v2f_img i) : COLOR
			{		
				fixed4 original = tex2D(_MainTex, i.uv);	
				float dithering = tex2D(_DitheringTex, i.uv * _SceenAndTex.xy).r;

				float3 hsv = rgb_to_hsv(original.rgb);
				hsv *= _ColorStepsA;				
				hsv = (floor(hsv) + (frac(hsv) > dithering)) * _ColorStepsB;
				
				return float4(hsv_to_rgb(hsv), original.a);
				//return float4(tex3D(_HSVToRGB, HSV).rgb, original.a);
			}




			ENDCG

		}
	}

	Fallback off

}