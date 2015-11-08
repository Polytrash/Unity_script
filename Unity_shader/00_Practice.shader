Shader "Custom/00_Practice"{
	Properties{

			_Color("Base Color", Color) = (1.0, 1.0, 1.0, 1.0)
			_MainTex("Diffuse Map", 2D) = "white"{}
			_RimColor("Rim Color", Color) = (1.0, 1.0, 1.0, 1.0)
 			_RimPower("Rim Power", Range(0.1, 10.0)) = 3.0
			_RimWidth("Rim Width", Range(0.1, 1.0)) = 0.1
		}
	SubShader{
			Pass{
			Tags {"LightMode" = "ForwardBase"}

			CGPROGRAM

			#pragma vertex vert
			#pragma fragment frag
			#pragma "UnityCG.cginc"

			// user defined variables
			uniform sampler2D _MainTex;
			uniform float4 _Color;
			uniform float4 _MainTex_ST;
			uniform float4 _RimColor;

			uniform float  _RimPower;
			uniform float  _RimWidth;
		    uniform float _CAMERA_FOV = 60.0f;

			// Unity defined variables
			uniform float4 _LightColor0;	
		
			// base input struct
			struct vertexInput{

				float4 vertex : POSITION;
				float4 color : COLOR;
				float3 normal : NORMAL;
				float4 texcoord : TEXCOORD0;
				
			};

			struct vertexOutput{

				float4 pos : SV_POSITION;
				float4 col : COLOR;
				float4 tex : TEXCOORD0;
				float3 posWorld : TEXCOORD1;
				float3 normalDir : TEXCOORD2;
			};

			// vertex function
			vertexOutput vert(vertexInput v){

				vertexOutput o;

				o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

				o.normalDir = normalize(mul(float4(v.normal, 1.0), _World2Object).xyz);
				o.posWorld = mul(_Object2World, v.vertex);	
				o.tex = v.texcoord;

				return o;

			}
	
			// fragment function
			float4 frag(vertexOutput i) : COLOR{

				// vectors
				float3 normalDirection = i.normalDir;
				float3 lightDirection = normalize(_WorldSpaceLightPos0.xyz);
				float3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz);
				float atten = 1.0;	

		
				// ToonShading

				float edgeDense = 1.0;




				float3 fragmentToLightSource = _WorldSpaceCameraPos.xyz - i.posWorld.xyz;
				float distance = length(fragmentToLightSource);

				if(dot(normalDirection, viewDirection) > _RimWidth)
				
					edgeDense =  1 ;

				else
	
					edgeDense = 0.0;
				

				float toon = saturate(dot(normalDirection, viewDirection));
				float3 toonShadingA =  max(edgeDense,(atten * pow(toon, _RimPower)));
				float3 toonShadingB =  _RimColor.rgb * (1 - max(edgeDense,(atten * pow(toon, _RimPower))));


				float3 lightingFinal = toonShadingA + toonShadingB;

				
				float4 tex = tex2D(_MainTex, i.tex.xy * _MainTex_ST.xy + _MainTex_ST.zw);

				return float4(tex.xyz * lightingFinal * _Color.rgb  , 1.0);
			}

			ENDCG
			}
	}
	// Fallback "Diffuse"
}