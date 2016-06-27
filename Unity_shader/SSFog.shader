Shader "Custom/SSFog" {
	   Properties {
        _MainTex ("Input", 2D) = "white" {}
        _MaskTex1("_MaskTex1", 2D ) = "white" {}
        _MaskTex2("_MaskTex2", 2D ) = "white" {}
        _NoiseMap("NoiseMap(RGB)", 2D ) = "white"{}
        _TintColor ("Tint Color", Color) = (1.0, 1.0, 1.0, 1.0)
        _BlendAmount ("", Range(0, 10)) = 0.5
        _WaveScale("WaveScale", Range(0.02, 0.15)) = 0.075
        _FlowVector("FlowVector", VECTOR) = (0,0,0,0)

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
        uniform sampler2D _MaskTex1;
        uniform sampler2D _MaskTex2;
        uniform sampler2D _NoiseMap;

        uniform float4 _MaskTex1_ST;
        uniform float4 _MaskTex2_ST;
        uniform sampler2D _CameraDepthTexture;
        uniform half4 _TintColor;                                              
		uniform half _BlendAmount;
		uniform half _iWidth;
        uniform half _iHeight;

        uniform float fWaveSpeed;
    	uniform float fWaveMapScale = 1.0f;
        uniform half halfCycle;

        uniform half flowMapOffset0;
        uniform float4 _FlowVector;

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



        fixed4 frag (v2f i) : COLOR {

            float2 flowUV = i.uv * _MaskTex1_ST.xy + _MaskTex1_ST.zw + float2(_FlowVector.x * _Time.y , _FlowVector.y * _Time.y);
            float2 maskUV = i.uv * _MaskTex2_ST.xy + _MaskTex2_ST.zw;

            half4 color = tex2D(_MainTex, i.uv);
            half4 mask1 = tex2D(_MaskTex1, flowUV);
            half4 mask2 = tex2D(_MaskTex2, maskUV);  

            half4 colorW = half4(1.0, 1.0, 1.0, 1.0);

			half2 flowmap = tex2D(_MaskTex1, i.uv)* 2.0f - 1.0f;
			float cycleOffset = tex2D(_NoiseMap, i.uv);

			float phase0 = cycleOffset * .5f + flowMapOffset0;

			half4 flowT0 = tex2D(_MaskTex1,  i.uv  + flowmap * phase0 );

			float f = (abs(halfCycle - flowMapOffset0) / halfCycle);

			flowT0 = 2.0f * flowT0 - 1.0f;

			half4 flowT = (flowT0,flowT0,flowT0, flowT0);

			float blendValue =  _BlendAmount ;

            mask1.r +=  colorW.r - (colorW.r - lerp(color.r,  _TintColor.r,  (1 -  mask1.a * blendValue) ) ) / colorW.r;
            mask1.g +=  colorW.g - (colorW.g - lerp(color.g,  _TintColor.g,  (1 -  mask1.a * blendValue) ) ) / colorW.g;
            mask1.b +=  colorW.b - (colorW.b - lerp(color.b,  _TintColor.b,  (1 -  mask1.a * blendValue) ) ) / colorW.b;

            //half4 screen = flowT +  mask1,  mask1.a * 0.95 ) ) / colorW;
            half4 finalColor = colorW - (colorW - lerp(color,  mask1,  mask2.r * blendValue) ) / colorW;
//            half4 screen =  colorW - (colorW - lerp(color,  flowT,  mask2.a * blendValue) ) / colorW;

            //half4 screen =  colorW - (colorW - lerp(color,  flowT,  mask2.a * blendValue) ) / colorW;
            //screen.a = 1.0;

            return  finalColor;

            //return depth;


            }
        ENDCG
            }
        }
    }	
    //float tmp = (original.r + original.g) * 0.5;
//original.r = original.g = tmp;