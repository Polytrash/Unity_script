

Shader "Custom/00_Vertex color unlit" {
Properties {
	_MainTex ("Texture", 2D) = "white" {}
}

Category {
	Tags { "Queue"="Geometry" }
	Lighting Off
	BindChannels {
		Bind "Color", color
		Bind "Vertex", vertex
		Bind "TexCoord", texcoord
	}
	
	SubShader {
		Pass {
			SetTexture [_MainTex] {
				Combine texture * primary DOUBLE
			}
		}
	}
}
}


/*
Shader "Custom/VertexColor" {
	Properties {
		_Color ("Color", Color) = (1,1,1,1)
		
		}
	SubShader {
		Tags { "RenderType"="Opaque" }
		Pass{

		CGPROGRAM

		#pragma vertex vert
		#pragma fragment frag

		uniform float4 _Color;
		
		struct vertexInput {
			float4 vertex : POSITION;
			float4 color : COLOR;
	
		};


		struct vertexOutput {

			float4 pos : POSITION;
			float4 col : COLOR;

		};

		struct fragOut
        {

             float4 color : COLOR;

        };


		vertexOutput vert( vertexInput v, float3 normal : NORMAL) {
			
			vertexOutput o;

			o.col = v.color;
			o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

			return o;
		}

		fragOut frag(float4 color : COLOR){

			fragOut i;
			i.color = (1.0, 1.0, 1.0, 1.0);
			return i;

		}

		
		ENDCG
		} 
	}
	// FallBack "Diffuse"
}
*/