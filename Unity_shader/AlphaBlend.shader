Shader "Custom Shader/AlphaBlend" {
	   Properties {
        _MainTex ("Input", 2D) = "white" {}
        _MaskTex("_MaskTex", 2D )= "white" {}
        _TintColor ("Tint Color", Color) = (1.0, 1.0, 1.0, 1.0)
        _BlendAmount ("", Range(0, 10)) = 0.5

    }


    SubShader {
            Pass {
                ZTest Always Cull Off ZWrite Off
                Fog { Mode off }
           
        CGPROGRAM
       
        #pragma vertex vert
        #pragma fragment frag
        #pragma fragmentoption ARB_precision_hint_fastest
     
        #include "UnityCG.cginc"
     
        uniform sampler2D _MainTex;
        uniform sampler2D _MaskTex;
        uniform sampler2D _CameraDepthTexture;
        uniform half4 _TintColor;                                              
		uniform half _BlendAmount;
		uniform half _iWidth;
        uniform half _iHeight;

        struct v2f{

        	float4 pos : POSITION;
        	half2 uv : TEXCCOORD0;
        };

        v2f vert(appdata_img v){

	        v2f o;
    	    o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
        	o.uv = MultiplyUV(UNITY_MATRIX_TEXTURE0, v.texcoord.xy);
        	return o;
        }



        fixed4 frag (v2f i) : COLOR {

            half4 color = tex2D(_MainTex, i.uv);
            half4 mask = tex2D(_MaskTex, i.uv);
            half4 colorW = half4(1.0, 1.0, 1.0, 1.0);
                                                                   
            half4 screenA = tex2D(_MaskTex, i.uv);
            half4 screenB = tex2D(_MaskTex, i.uv);

			screenA.r =  mask.r - (mask.r - lerp(color.r,  _TintColor.r,  (1 -  mask.a * _BlendAmount) ) ) / colorW.r;
			screenA.g =  mask.g - (mask.g - lerp(color.g,  _TintColor.g,  (1 -  mask.a * _BlendAmount) ) ) / colorW.g;
			screenA.b =  mask.b - (mask.b - lerp(color.b,  _TintColor.b,  (1 -  mask.a * _BlendAmount) ) ) / colorW.b;
            screenA.a = 1.0;

            screenB =  color - (color - lerp(mask,  color,  mask.a * _BlendAmount) );

            // 最後にかけると良いかも.
            //screenC = (1 - mask.r / _BlendAmount) * color + (1 - screenB) * (mask.r / _BlendAmount);

            return  screenB ;

            //return depth;


            }
        ENDCG
            }
        }
    }	
    //float tmp = (original.r + original.g) * 0.5;
	//original.r = original.g = tmp;