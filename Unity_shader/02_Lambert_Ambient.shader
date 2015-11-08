Shader "Custom/02_Lambert_AMBIENT"{
	Properties{
		_Color ("BaseColor", Color) = (1.0, 1.0, 1.0, 1.0)

	}	
	Subshader{
		Pass{
		Tags{"LightMode" = "ForwardBase"}
		CGPROGRAM

		#pragma vertex vert
		#pragma fragment frag
		#include "UnityCG.cginc"

		// user defined variables
		uniform float4 _Color;
		
		// Unity defined variables
		uniform float4 _LightColor0;

		struct vertexInput{
			float4 vertex : POSITION;
			float4 color : COLOR;
			float3 normal : NORMAL;
		};

		struct vertexOutput{	
			float4 pos : SV_POSITION;
			float4 col : COLOR;
			float3 nor : NORMAL;
		};
		

			
			// vertex function 
			vertexOutput vert(vertexInput v){

				vertexOutput o;
				float3 normalDirection = normalize(mul(float4(v.normal, 0.0), _World2Object).xyz);
				float3 lightDirection;
				float atten = 1.0;

				lightDirection = normalize(_WorldSpaceLightPos0.xyz);

				float3 diffuseReflection = atten * _LightColor0.xyz * _Color.xyz * saturate(dot(normalDirection, lightDirection));
				float3 lightingFinal = diffuseReflection + UNITY_LIGHTMODEL_AMBIENT.xyz;

				o.col = float4(lightingFinal * _Color.rgb, 1.0);

				o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
				return o;
			
			}

			// fragment function			
			float4 frag(vertexOutput i) : COLOR{

				return i.col;
			}


		ENDCG
		}
	}
}