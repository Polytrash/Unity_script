Shader "Nekoden/NekodenShader_Ghibli" {
    Properties {
		// カラー
		[HDR]_BaseModifyColor ("Base Modify Color", Color) = (0,0,0,1)
        _MainTex ("Base Map", 2D) = "white" {}


		// 影カラー/マスク
		[HDR]_KageModifyColor ("Kage Modify Color", Color) = (0,0,0,1)
        _KageTexture ("Kage Map", 2D) = "white" {}
        _KageMaskMap ("Kage Mask", 2D) = "white" {}

		// ノーマル	
        _BumpMap ("Normal Map", 2D) = "bump" {}
		// 境界の法線
		_BorderNormal("Border Detail", Range(0, 1) ) = 0	   
					
		// ハイライト
		[HDR]_HighlightColor ("Highlight Color", Color) = (0,0,0,1)
		_HighlightMaskMap ("Highlight Mask", 2D) = "white"{}
		_HighlightIntensity("Highlight Intensity", Range(0, 10)) = 0
        _HighlightRadius ("Highlight Radius", Range(0.1, 10)) = 1
        _HighlightScale ("Highlight Scale", Range(-10, 10)) = 0
			
		// スペキュラー
		_SpecMaskMap ("Specular Mask", 2D) = "white"{}
		_Spec_Color("Specular Color", Color) = (0.5,0.5,0.5,1)
		_Spec_Power("Specular Power", Range(0.0, 100)) = 0
		_Shininess("Shininess", Range(0.0, 100)) = 10 
		 			   
		// リムライト   
		_Rim_Color("Rim Color", Color) = (1.0,1.0,1.0,1)	
		_Rim_Power("Rim Power", Range(1.0, 100)) = 1
		_Rim_Width("Rim Width", Range(0.1, 10)) = 0
							
		// アウトライン 1				  
		_Line_Color ("Outline Color", Color) = (0.5,0.5,0.5,1)
        _Outline_Width ("Outline Width", Range(-1, 1)) = 0
		[MaterialToggle] _IgnoreNormal ("Ignore Normal (Default:OFF)", Float ) = 0
 		_Outline_Vector ("XYZ Offset", VECTOR) = (0.1,0.1,0)
		//_Scribbliness("Scribbliness", Float) = 0.01
					


    }
    SubShader {
        Tags {
            "RenderType"="Opaque"
        }
//----------------------------------------------------------------------------//
// アウトライン用パス1
//----------------------------------------------------------------------------//

        Pass {
            Name "Outline"
            Tags {
			"Queue" = "Overlay" 
            }

			ZWrite On  
	    	Cull Front

	    	// アウトラインのマスクは描画されて欲しくないので、カラー情報が既にフレームバッファ上にあるかないかに関わらず、
			// シーンのライティングに影響されずにカラーリングする仕様となっている
            
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #define _GLOSSYENV 1

            #include "UnityCG.cginc"
            #include "UnityPBSLighting.cginc"
            #include "UnityStandardBRDF.cginc"

            #pragma fragmentoption ARB_precision_hint_fastest
            #pragma multi_compile_shadowcaster
            #pragma multi_compile_fog
            #pragma exclude_renderers d3d11_9x xbox360 xboxone ps3 psp2 
            #pragma target 3.0
            #pragma glsl

            uniform sampler2D _MainTex; uniform float4 _MainTex_ST;
            uniform fixed _IgnoreNormal;
			uniform float _Outline_Width;
            uniform float4 _Line_Color;
			uniform float4 _Outline_Vector;

            struct VertexInput {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float2 texcoord : TEXCOORD0;
				float4 color : COLOR;
            };

            struct VertexOutput {
                float4 pos : SV_POSITION;
                float2 texcoord : TEXCOORD0;
				float4 color : COLOR;
				float3 normal : NORMAL;
                UNITY_FOG_COORDS(1)
            };

 			// 法線計算の切り替え
			float3 vertexNormalSwitch1(VertexInput v)
			{
				float3 norm = normalize(mul((float3x3)UNITY_MATRIX_IT_MV, v.normal));
				if(_IgnoreNormal) 
				norm = mul( (float3x3)UNITY_MATRIX_IT_MV,(v.color.xyz * 2) - 1);

				return norm;
			}

//----------------------------------------------------------------------------//

			////////////////////////////////////
			//								  //
			//          VertexShader          //
			//								  //
			////////////////////////////////////
              VertexOutput vert (VertexInput v) {
                VertexOutput o;
				o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

				float3 norm = vertexNormalSwitch1(v);
				float2 offset = TransformViewToProjection(norm.xy);	 
					 
				#ifdef UNITY_Z_0_FAR_FROM_CLIPSPACE 
					o.pos.xy += offset * UNITY_Z_0_FAR_FROM_CLIPSPACE(o.pos.z) * (v.color.r + 0.5) * _Outline_Width * 0.001;
				#else
					o.pos.xy += offset *  (v.color.r + 0.5) * _Outline_Width * 0.01;							
					o.pos.x +=  o.pos.x * (v.color.r + 0.5) * _Outline_Width * 0.01 * _Outline_Vector.x;
					o.pos.y +=  o.pos.y * (v.color.r + 0.5) * _Outline_Width * 0.01 * _Outline_Vector.y;
					o.pos.z +=  o.pos.z * (v.color.r + 0.5) * _Outline_Width * 0.01 * _Outline_Vector.z;	
				
				#endif
				o.color = _Line_Color;
				UNITY_TRANSFER_FOG(o,o.pos);
				return o;


			}

			////////////////////////////////////
			//								  //
			//         FragmentShader         //
			//								  //
			////////////////////////////////////

            float4 frag(VertexOutput i, float facing : VFACE) : COLOR {
                float isFrontFace = ( facing >= 0 ? 1 : 0 );
                float faceSign = ( facing >= 0 ? 1 : -1 );
                float4 _BaseTex_var = tex2D(_MainTex,TRANSFORM_TEX(i.texcoord, _MainTex)); // 通常Color用テクスチャ
                return fixed4(_Line_Color.rgb,0);
            }

//----------------------------------------------------------------------------//

            ENDCG

        }
		

//----------------------------------------------------------------------------//
// シェーディング用パス
//----------------------------------------------------------------------------//

        Pass {
            Name "FORWARD"
            Tags {

                "LightMode"="ForwardBase"
				"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"
            } 

			ZWrite On
            ZTest LEqual

            
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #define UNITY_PASS_FORWARDBASE
            #define _GLOSSYENV 1

            #include "UnityCG.cginc"
            #include "AutoLight.cginc"
            #include "UnityPBSLighting.cginc"
            #include "UnityStandardBRDF.cginc"

            #pragma multi_compile_fwdbase_fullshadows
            #pragma multi_compile_fogBorderNormal

            #pragma exclude_renderers d3d11_9x xbox360 xboxone ps3 psp2 
            #pragma target 3.0
            #pragma glsl

            uniform sampler2D _MainTex; uniform float4 _MainTex_ST;
            uniform float _Mix_BaseTexture;
			uniform float4 _BaseModifyColor;

            uniform sampler2D _KageTexture; uniform float4 _KageTexture_ST;
            uniform float _Mix_KageTexture;
			uniform float4 _KageModifyColor;
			
            uniform sampler2D _KageMaskMap; uniform float4 _KageMaskMap_ST;									
			uniform sampler2D _SpecMaskMap; uniform float4 _SpecMaskMap_ST;		

			uniform float4 _Spec_Color;
			uniform float  _Spec_Power;
			uniform float  _Shininess;

			uniform float4 _Rim_Color;
			uniform float _Rim_Power;
 			uniform float _Rim_Width;

            uniform sampler2D _BumpMap; uniform float4 _BumpMap_ST;

			uniform float  _HighlightIntensity;
			uniform float  _HighlightRadius;
			uniform float4 _HighlightColor;
			uniform sampler2D _HighlightMaskMap; uniform float4 _HighlightMaskMap_ST; 
			uniform fixed  _BorderNormal;
            uniform fixed  _HighlightScale;
			
			uniform fixed4 _Random;
            
			struct VertexInput {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float4 tangent : TANGENT;
                float2 texcoord : TEXCOORD0;

            };

            struct VertexOutput {
                float4 pos : SV_POSITION;
                float2 texcoord : TEXCOORD0;
                float4 posWorld : TEXCOORD1;
                float3 normalDir : TEXCOORD2;
                float3 tangentDir : TEXCOORD3;
                float3 bitangentDir : TEXCOORD4;

				float2 screenPos : TEXCOORD8;

                
				LIGHTING_COORDS(5,6)
                UNITY_FOG_COORDS(7)
								
            };

			////////////////////////////////////
			//								  //
			//          VertexShader          //
			//								  //
			////////////////////////////////////

            VertexOutput vert (VertexInput v) {

                VertexOutput o = (VertexOutput)0;

                o.texcoord = v.texcoord;

                o.normalDir = UnityObjectToWorldNormal(v.normal);
                o.tangentDir = normalize( mul( unity_ObjectToWorld, float4( v.tangent.xyz, 0.0 ) ).xyz );
                o.bitangentDir = normalize(cross(o.normalDir, o.tangentDir) * v.tangent.w);

                o.posWorld = mul(unity_ObjectToWorld, v.vertex);
                o.pos = mul(UNITY_MATRIX_MVP, v.vertex );

				o.screenPos = ComputeScreenPos(o.pos);


                UNITY_TRANSFER_FOG(o,o.pos);
                TRANSFER_VERTEX_TO_FRAGMENT(o)
                return o;
            }
			

			////////////////////////////////////
			//								  //
			//         FragmentShader         //
			//								  //
			////////////////////////////////////

            float4 frag(VertexOutput i, float facing : VFACE) : COLOR {

                float isFrontFace = ( facing >= 0 ? 1 : 0 );
                float faceSign = ( facing >= 0 ? 1 : -1 );

				// 面の向き
                i.normalDir = normalize(i.normalDir);
                i.normalDir *= faceSign;
				// タンジェント変換
                float3x3 tangentTransform = float3x3( i.tangentDir, i.bitangentDir, i.normalDir);
				// 視線方向 
                float3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz);
				// 法線方向 
                float3 _BumpMap_var = UnpackNormal(tex2D(_BumpMap,TRANSFORM_TEX(i.texcoord, _BumpMap)));
                float3 normalLocal = _BumpMap_var.rgb;
                float3 normalDirection = normalize(mul( normalLocal, tangentTransform )); // Perturbed normals
				// 反射方向
                float3 viewReflectDirection = reflect( -viewDirection, normalDirection );
                // ライト方向
				float3 lightDirection = normalize(_WorldSpaceLightPos0.xyz);
				

				float attenuation = 1.0;	


			


////// Lighting ////// 
////// Emissive ////// 


                float4 _BaseTex_var = tex2D(_MainTex,TRANSFORM_TEX(i.texcoord, _MainTex));								// 通常Color用テクスチャ
                float4 _KageTex_var = tex2D(_KageTexture,TRANSFORM_TEX(i.texcoord, _KageTexture));						// 影Color用テクスチャ
				float4 _SpecMaskMap_var = tex2D (_SpecMaskMap,TRANSFORM_TEX(i.texcoord, _SpecMaskMap));					// スペキュラマスク用テクスチャ 
				float4 _HighlightMaskMap_var = tex2D (_HighlightMaskMap,TRANSFORM_TEX(i.texcoord, _HighlightMaskMap)); // ハイライトマスク用テクスチャ 
                float4 _KageMaskMap_var = tex2D(_KageMaskMap, TRANSFORM_TEX(i.texcoord, _KageMaskMap));				// 強制的に影にしたい部分をテクスチャで指定する
                float coeff = 1.0;

				// ブレンド用変数
				float4 baseModify_var;
				float4 kageModify_var;
				   
				// スペキュラライト
				float3 specularLighting = saturate(pow(max(0.0, dot( reflect(-lightDirection, lerp(i.normalDir, normalDirection, _BorderNormal)), viewDirection)),_Shininess))* _LightColor0 * attenuation  * _Spec_Color.rgb  *_SpecMaskMap_var.r * _KageMaskMap_var.r * _Spec_Power ;
				
				// リムライト
				float rim =  1 -  saturate(dot( i.normalDir, viewDirection));			
				float3 rimLighting =  _Rim_Color * saturate(dot(normalDirection, viewDirection)) * pow(rim * _Rim_Width, _Rim_Power);
								
				// ブレンド用リム
				float rimBlend =  (_HighlightRadius -((_HighlightScale * 0.1) + pow(dot(lerp( i.normalDir, normalDirection, _BorderNormal), lightDirection),_HighlightScale)));

				// ブレンド値
				float blendAmount = saturate((coeff + (((1.0 - (dot(i.normalDir, lightDirection) + 2)) * rimBlend) * ((1.0 - _KageMaskMap_var.rgb).r - coeff)) /  rimBlend));
				
				// 影ブレンド制御
				float3 blendedColor = saturate((_HighlightRadius -((_HighlightScale * 0.1) + pow(dot(lerp( i.normalDir, normalDirection, _BorderNormal),lightDirection),_HighlightScale))))  * _HighlightIntensity * _HighlightColor;
				
				// ベースカラー調整
				baseModify_var.r = (1 - blendAmount) * _BaseTex_var.r + (1.0 - (1 - blendAmount)) * _BaseModifyColor.r;
				baseModify_var.g = (1 - blendAmount) * _BaseTex_var.g + (1.0 - (1 - blendAmount)) * _BaseModifyColor.g;
				baseModify_var.b = (1 - blendAmount) * _BaseTex_var.b + (1.0 - (1 - blendAmount)) * _BaseModifyColor.b;
				baseModify_var.a = 1;

				// 影カラー調整
				kageModify_var.r = blendAmount * (_KageTex_var.r + (1.0 -  blendAmount)) + _KageModifyColor.r;
				kageModify_var.g = blendAmount * (_KageTex_var.g + (1.0 -  blendAmount)) + _KageModifyColor.g;
				kageModify_var.b = blendAmount * (_KageTex_var.b + (1.0 -  blendAmount)) + _KageModifyColor.b;
				kageModify_var.a = 1;

				

				// シェーディング計算
                float3 emissive =lerp( _KageTex_var * kageModify_var + rimLighting + UNITY_LIGHTMODEL_AMBIENT.rgb * _LightColor0 ,
									    _BaseTex_var * baseModify_var + rimLighting  + (specularLighting * _KageMaskMap_var.r)  + UNITY_LIGHTMODEL_AMBIENT.rgb * _LightColor0 ,				
				
								 // ベース(スペキュラ)と影カラーのブレンド
								  blendAmount * _KageMaskMap_var.r )

								 // ベースのハイライト制御
								 + ((blendedColor * _HighlightColor ) * _HighlightMaskMap_var) ;

								 // 環境光
;


				float3 finalColor = emissive ;
                fixed4 finalRGBA = fixed4(finalColor,_BaseTex_var.a);

				// The UNITY_FOG_COORDS マクロはフォグの座標を保持する構造体を生成する
                UNITY_APPLY_FOG(i.fogCoord, finalRGBA);
                return finalRGBA;

            }
            ENDCG
        }
    }
    FallBack "Diffuse"
    CustomEditor "ShaderForgeMaterialInspector"
}
