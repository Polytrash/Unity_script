Shader "Custom/05_MultipleLight"{
	Properties{
				_Color("Base Color", Color) = (1.0, 1.0, 1.0, 1.0)
				_SpecColor("Spec Color", Color) = (1.0, 1.0, 1.0, 1.0)
				_Shininess("Shininess", Float) = 10
				_RimColor("Rim Color", Color) = (1.0, 1.0, 1.0, 1.0)
				_RimPower("Rim Power", Range(0.1, 10.0)) = 3.0
			}
	Subshader{
		
		Pass{
		Tags {"LightMode" = "ForwardBase"}
				CGPROGRAM
	
				#pragma vertex vert
				#pragma fragment frag
				#include "UnityCG.cginc"

				// user defined variables
				uniform float4 _Color;
				uniform float4 _SpecColor;
				uniform float4 _RimColor;
				uniform float  _Shininess;
			    uniform float  _RimPower;

				// Unity defined variables
				uniform float4 _LightColor0;

				// base input struct
				struct vertexInput{
	
					float4 vertex : POSITION;
					float4 color  : COLOR;
					float3 normal : NORMAL;
				};

				struct vertexOutput{
			
					float4 pos : SV_POSITION;
					float4 col : COLOR;
					float4 posWorld : TEXCOORD0;
					float3 normalDir : TEXCOORD1;
				};

				// vertex function
				vertexOutput vert(vertexInput v){
			
					vertexOutput o;

					o.posWorld = mul(_Object2World, v.vertex);
					o.normalDir = normalize(mul(float4(v.normal, 0.0), _World2Object).xyz);
					o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

					return o;
				}

				// fragment function
				float4 frag(vertexOutput i) : COLOR{

					// vectors
					float3 normalDirection = i.normalDir;
					float3 lightDirection;
					float3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz); 
					float atten;					
					
					if(_WorldSpaceLightPos0.w == 0.0){

						atten = 1.0;
						lightDirection = normalize(_WorldSpaceLightPos0.xyz);
				
					}else{
		
						float3 fragmentToLightSource = _WorldSpaceLightPos0.xyz - i.posWorld.xyz;
						float distance = length(fragmentToLightSource);
						atten  = 1 / distance ;
                        lightDirection = normalize(fragmentToLightSource);

					}
				
					// Lighting
					float3 diffuseReflection = atten * _LightColor0.rgb * saturate(dot(normalDirection, lightDirection));			
					float3 specularReflection = diffuseReflection * _LightColor0.rgb * _SpecColor.rgb * pow(saturate(dot(reflect(-lightDirection, normalDirection), viewDirection)), _Shininess);
					
	
					float  rim = 1 -  saturate(dot(normalize(viewDirection), normalDirection)); 
					float3 rimLighting = atten * _LightColor0.rgb * _RimColor * saturate(dot(normalDirection, lightDirection)) * pow(rim, _RimPower);  
					float3 lightingFinal = diffuseReflection + specularReflection + rimLighting + UNITY_LIGHTMODEL_AMBIENT.rgb;				

					return float4(lightingFinal * _Color.rgb, 1.0);
		
					
				}
				ENDCG
			}

	Pass{
		Tags {"LightMode" = "ForwardAdd"}
		Blend One One
				CGPROGRAM
	
				#pragma vertex vert
				#pragma fragment frag
				#include "UnityCG.cginc"

				// user defined variables
				uniform float4 _Color;
				uniform float4 _SpecColor;
				uniform float4 _RimColor;
				uniform float  _Shininess;
			    uniform float  _RimPower;

				// Unity defined variables
				uniform float4 _LightColor0;

				// base input struct
				struct vertexInput{
	
					float4 vertex : POSITION;
					float4 color  : COLOR;
					float3 normal : NORMAL;
				};

				struct vertexOutput{
			
					float4 pos : SV_POSITION;
					float4 col : COLOR;
					float4 posWorld : TEXCOORD0;
					float3 normalDir : TEXCOORD1;
				};

				// vertex function
				vertexOutput vert(vertexInput v){
			
					vertexOutput o;

					o.posWorld = mul(_Object2World, v.vertex);
					o.normalDir = normalize(mul(float4(v.normal, 0.0), _World2Object).xyz);
					o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

					return o;
				}

				// fragment function
				float4 frag(vertexOutput i) : COLOR{

					// Vector
					float3 normalDirection = i.normalDir;
					float3 lightDirection;
					float3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz); 
					float atten;					
					
					if(_WorldSpaceLightPos0.w == 0.0){

						atten = 1.0;
						lightDirection = normalize(_WorldSpaceLightPos0.xyz);
				
					}else{
		
						float3 fragmentToLightSource = _WorldSpaceLightPos0.xyz - i.posWorld.xyz;
						float distance = length(fragmentToLightSource);
						atten  = 1 / distance ;
                        lightDirection = normalize(fragmentToLightSource);

					}
				
					// Lighting
					float3 diffuseReflection = atten * _LightColor0.rgb * saturate(dot(normalDirection, lightDirection));			
					float3 specularReflection = diffuseReflection * _LightColor0.rgb * _SpecColor.rgb * pow(saturate(dot(reflect(-lightDirection, normalDirection), viewDirection)), _Shininess);
					
	
					float  rim = 1 -  saturate(dot(normalize(viewDirection), normalDirection)); 
					float3 rimLighting = atten * _LightColor0.rgb * _RimColor * saturate(dot(normalDirection, lightDirection)) * pow(rim, _RimPower);  
					float3 lightingFinal = diffuseReflection + specularReflection + rimLighting + UNITY_LIGHTMODEL_AMBIENT.rgb;				

					return float4(lightingFinal * _Color.rgb, 1.0);
		
					
				}
				ENDCG
		}		
	}
		// Fallback "Diffuse"
}
