Shader "Custom/01_FlatColor" {
	Properties{
		_Color ("BaseColor", Color) = (1.0, 1.0, 1.0, 1.0)
	}
	Subshader{
		Pass{
			Tags {"RenderType" = "Opaque"}
			CGPROGRAM

			#pragma vertex vert
			#pragma fragment frag
			#include "UnityCG.cginc"


			// user defined variables
			uniform float4 _Color;


			// base input scruct
			struct vertexInput{

				float4 vertex : POSITION;
				float4 color : COLOR;
			};

			struct vertexOutput{

				float4 pos : SV_POSITION;
				float4 col : COLOR;
			};			
			
			// vertex function
			vertexOutput vert(vertexInput v){
				vertexOutput o;
				o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
				
				return o;

			}

			// fragment function
			float4 frag(vertexOutput i) : COLOR{

				return _Color;

			}


			ENDCG
			}
		}
	// Fallback "Diffuse

}