Shader"Custom/03_Specular"{
	Properties{
			_Color("Base Color", Color) = (1.0, 1.0, 1.0, 1.0)
			_SpecColor("Specular Color", Color) = (1.0, 1.0, 1.0, 1.0)
			_Shininess("Shininess", Float) = 10
		}
		SubShader{
			Tags{"LightMode" = "ForwardBase"}
			Pass{

			CGPROGRAM
	
			#pragma vertex vert
			#pragma fragment frag

			// user defined variables
			uniform float4 _Color;
			uniform float4 _SpecColor;
			uniform float  _Shininess;

			// Unity defined variables
			uniform float4 _LightColor0;

			// base input struct
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

			// vertex functions
			vertexOutput vert(vertexInput v){
		
				vertexOutput o;

				// vectors
				float3 normalDirection = normalize(mul(float4(v.normal, 0.0), _World2Object).xyz);
				float3 lightDirection = normalize(_WorldSpaceLightPos0.xyz);
				float3 viewDirection = normalize(float3(float4(_WorldSpaceCameraPos.xyz, 1.0) - mul(_Object2World, v.vertex).xyz));
				float atten = 1.0;

				// lighting
				float3 diffuseReflection = atten * _LightColor0.xyz * saturate(dot(normalDirection, lightDirection));
				float3 specularReflection = diffuseReflection * _SpecColor.xyz * pow(saturate(dot(reflect(-lightDirection, normalDirection), viewDirection)),_Shininess);		
				float3 lightingFinal = diffuseReflection + specularReflection + UNITY_LIGHTMODEL_AMBIENT.xyz;


				o.col = float4(lightingFinal * _Color.rgb, 1.0);
				o.pos = mul(UNITY_MATRIX_MVP, v.vertex);				


				return o;
			}

			// fragment functions
			float4 frag( vertexOutput i) : COLOR{


				return i.col;
			}

			ENDCG
		}

	}
	// Fallback "Diffuse"
}




