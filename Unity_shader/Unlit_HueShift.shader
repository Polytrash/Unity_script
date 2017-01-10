Shader "Unlit/Unlit_HueShift"
{
	Properties
	{		   
		_MainTex ("Texture", 2D) = "white" {}
		_TintColor("Start Color", Color ) = (1,0,0,0)
		_Amount("Color Amount", Range(0,1)) = 0
		_Transition("Transition Speed", Range(0.1, 10)) = 1
	}
	SubShader
	{
		Tags { "RenderType"="Opaque" }

        Blend SrcAlpha OneMinusSrcAlpha
        Cull Off
		LOD 100

		Pass
		{
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			// make fog work
			#pragma multi_compile_fog
			
			#include "UnityCG.cginc"

			float4 _TintColor;
			sampler2D _MainTex;
            float4 _MainTex_ST;
			float _Amount;
			float _Transition;


            float3 rgb_to_hsv_no_clip(float3 RGB)
            {
                float3 HSV = 0;
 
                float minChannel, maxChannel;
 
                maxChannel = max(RGB.x, RGB.y);
                minChannel = min(RGB.x, RGB.y);
 
                maxChannel = max(RGB.z, maxChannel);
                minChannel = min(RGB.z, minChannel);
 
                HSV.z = maxChannel;
 
                float delta = maxChannel - minChannel;             //Delta RGB value
 
                    HSV.y = delta / HSV.z;
                    float3 delRGB = (HSV.zzz - RGB + 3*delta) / (6*delta);
                    if ( RGB.x == HSV.z ) HSV.x = delRGB.z - delRGB.y;
                    if ( RGB.y == HSV.z ) HSV.x = ( 1.0 / 3.0 ) + delRGB.x - delRGB.z;
                    if ( RGB.z == HSV.z ) HSV.x = ( 2.0 / 3.0 ) + delRGB.y - delRGB.x;

 
                return (HSV);
            }


             float3 hsv_to_rgb(fixed3 HSV)
            {
                float var_h = HSV.x * 6;
                //float var_i = floor(var_h);   // Or ... var_i = floor( var_h )
                float var_1 = HSV.z * ( 1.0 - HSV.y );
                float var_2 = HSV.z * ( 1.0 - HSV.y * (var_h-floor( var_h )));
                float var_3 = HSV.z * ( 1.0 - HSV.y * (1-(var_h-floor( var_h ))));
 
                float3 RGB = float3(HSV.z, var_1, var_2);
 
                if (var_h < 5)  { RGB = float3(var_3, var_1, HSV.z); }
                if (var_h < 4)  { RGB = float3(var_1, var_2, HSV.z); }
                if (var_h < 3)  { RGB = float3(var_1, HSV.z, var_3); }
                if (var_h < 2)  { RGB = float3(var_2, HSV.z, var_1); }
                if (var_h < 1)  { RGB = float3(HSV.z, var_3, var_1); }
 
                return (RGB);
            }


			struct v2f
			{
				float4 vertex : SV_POSITION;
				float2 uv : TEXCOORD0;

			};

			
			v2f vert (appdata_full v)
			{
				v2f o;
				o.vertex = mul(UNITY_MATRIX_MVP, v.vertex);
				o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
				return o;
			}
			
	fixed4 frag(v2f IN) : COLOR
	{
		fixed hueShift = (_Time.x );
		fixed4 c = tex2D (_MainTex, IN.uv); 
		fixed3 hsv =  rgb_to_hsv_no_clip(_TintColor);
		//fixed4 hsv = float4((_SinTime.x+1.0)*.5, (_Time.x+1.0)*.5, (_SinTime.x+1.0)*.5, 1.0);
		hsv.x +=    abs(fmod(_Time.w * _Transition, 2.0) - 1.0) * _Amount ;
		
		                 if ( hsv.x > 1.0 ) { hsv.x -= 1.0; }
		fixed3 final = c +(lerp((0.1, 0.1, 0.1), hsv_to_rgb(hsv), abs(fmod(_Time.w * _Transition, 2.0) - 1.0)) * _Amount);
		  return fixed4(final,1);
			   
	}
			ENDCG
		}
	}
}
