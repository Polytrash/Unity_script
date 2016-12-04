Shader "SSwave" {
	Properties{
		_Color("Tint Color", Color) = (0.5,0.5,0.5,1)
		_MainTex("Base (RGB)", 2D) = "white" {}
		[Enum(OFF,0,FRONT,1,BACK,2)] _CullMode("Cull Mode", int) = 2 //OFF/FRONT/BACK
		
		[MaterialToggle] _ScreenXY ("X Direction ", Float ) = 0			
		_Position("Position", Range( -2, 2)) = 0
		_Width("Offse Width", float) = 0.005
		[MaterialToggle] _Randomness ("Randomness", Float ) = 0
		_Power("Power", Range(-10, 10)) = 0.01
		_Edge("Border Edge", Range(0, 10)) = 0.1
		//_Tess("Tessellation", Range(1, 32)) = 4
	}

		SubShader{
		Pass{
		Tags{ "RenderType" = "Opaque" }
		LOD 200
			ZWrite On  
	    	Cull [_CullMode]

		CGPROGRAM
        #pragma vertex vert
        #pragma fragment frag	
		#pragma multi_compile_shadowcaster
        #pragma multi_compile_fog	
		#pragma target 3.0
		#pragma glsl

		#include "UnityCG.cginc"
        #include "UnityPBSLighting.cginc"
        #include "UnityStandardBRDF.cginc"

		uniform float4 _Color;
		uniform sampler2D _MainTex;

        uniform fixed _ScreenXY;
		uniform float _Position;
		uniform float _Width;
        uniform fixed _Randomness;

		uniform float _Power;
		uniform float _Edge;

				   
		struct VertexInput {
			float4 vertex : POSITION;
			float3 normal : NORMAL;
			float2 texcoord : TEXCOORD0;
			float4 color : COLOR;
		};

		struct VertexOutput {
			float4 pos : SV_POSITION;
			float2 texcoord : TEXCOORD0;
			float4 posWorld : TEXCOORD1;
			float4 color : COLOR;
			float3 normal : NORMAL;
			float2 screenPos : TEXCOORD2;
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

			 float rand(float3 myVector) {
             return frac(sin(_Time[0] * dot(myVector ,float3(12.9898,78.233,45.5432))) * 43758.5453);
         }
//----------------------------------------------------------------------------//
		VertexOutput vert(VertexInput v) {
			VertexOutput o;
			o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

			float4x4 modelMatrix = unity_ObjectToWorld;
			float4x4 modelMatrixInverse = unity_WorldToObject;

			float3 normalDirection = normalize(mul(v.normal, modelMatrixInverse)).xyz;
			float3 viewDirection = normalize(_WorldSpaceCameraPos - mul(modelMatrix, v.vertex).xyz);
			float dotValue = saturate(dot(normalDirection, viewDirection));
					
			float2 uv = v.texcoord.xy;	  	
			float power = -_Power;
			float n = noise(v.vertex);


			o.texcoord = v.texcoord;
			o.screenPos = ComputeScreenPos(v.vertex);

			if (dotValue < _Edge) {
				
				if(_ScreenXY <= 0)	{

					if (abs(viewDirection.y  - _Position) < _Width) {
						//ゾワゾワを表現する部分はとりあえずいろいろ試して個人的にいい感じになった数式で特に思想があるわけではありません。
						//float3 value = v.normal * _Power * pow(_Gap * (sin(v.vertex.y * _Fineness) + sin(v.vertex.x * _Fineness) + sin(v.vertex.z * _Fineness)), _Power);
		
						float3 value = normalDirection *  lerp(1, rand(v.vertex), _Randomness) * power ;  
						o.pos.x += value.x ;
						o.pos.y += value.y ;
						o.pos.z += value.z ;	
					}

				}else{

				  	if (abs(viewDirection.x  - _Position) < _Width) {
						//ゾワゾワを表現する部分はとりあえずいろいろ試して個人的にいい感じになった数式で特に思想があるわけではありません。
						//float3 value = v.normal * _Power * pow(_Gap * (sin(v.vertex.y * _Fineness) + sin(v.vertex.x * _Fineness) + sin(v.vertex.z * _Fineness)), _Power);
		
						float3 value = normalDirection *  lerp(1, rand(v.vertex), _Randomness) * power ;  
						o.pos.x += value.x ;
						o.pos.y += value.y ;
						o.pos.z += value.z ;	
					}
				}
			}
			return o;
		}	   

		float4 frag(VertexOutput i,float facing : VFACE) : COLOR{
				                 float isFrontFace = ( facing >= 0 ? 1 : 0 );
                float faceSign = ( facing >= 0 ? 1 : -1 );
				float lightDir = -_WorldSpaceLightPos0.xyz;
				
				float atten = 1.0;

			   	half d = dot(i.normal, lightDir) * 0.5 + 0.5;
				half3 color = tex2D(_MainTex, i.texcoord) ;
								// 影カラー調整
				color.r = ( .5) * color.r + (1.0 - ( .5 )) * _Color.r;
				color.g = ( .5) * color.g + (1.0 - ( .5 )) * _Color.g;
				color.b = ( .5) * color.b + (1.0 - ( .5 )) * _Color.b;

				color.rgb = color * _LightColor0.rgb * (atten * 2);
										  
				return fixed4(color.rgb,0);				   
			}
		ENDCG	 
		} 
 		


		}
	Fallback "Diffuse"
}