// Upgrade NOTE: replaced '_Object2World' with 'unity_ObjectToWorld'
// Upgrade NOTE: replaced '_World2Object' with 'unity_WorldToObject'

Shader "Custom/Sea_light" {
    Properties {
			
		_ShallowColor ("Shallow Color", Color) = (0.5,0.5,0.5,1)
		_DeepColor ("Deep Color", Color) = (0.5,0.5,0.5,1)
		_Blend("Shallow Range", Range(0,1)) = 1
        _RampMap ("Gradient Map", 2D) = "white" {}
        _SandMap ("Sand Map", 2D) = "white" {}

		//[MaterialToggle] _IgnoreNormal ("Ignore Normal (Default:ON)", Float ) = 0
		_BorderMap ("Border Map", 2D) = "white" {}

		_SpecColor ("Specular Color", Color) = (1.0, 1.0, 1.0, 1)  	
		_Shininess("Shininess", Range(0.0, 1)) = 0.3			
		_SpecMap ("Specular Map", 2D) = "white"{}


    }
    SubShader {
        Tags {
            "RenderType"="Opaque"
        }

        Pass {
            Name "Forward"
            Tags {
				"Queue" = "Overlay" 
            }
			ZWrite On	  
	    	Cull Front
            
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "UnityPBSLighting.cginc"
            #include "UnityStandardBRDF.cginc"

            #pragma fragmentoption ARB_precision_hint_fastest
            #pragma multi_compile_shadowcaster
            #pragma multi_compile_fog

            #pragma target 3.0
            #pragma glsl

            uniform sampler2D _RampMap, _SandMap, _SpecMap, _BorderMap; 
			uniform half4 _RampMap_ST, _SandMap_ST, _SpecMap_ST, _BorderMap_ST;
            uniform half4 _ShallowColor;
			uniform half4 _DeepColor;	 
			uniform half  _Shininess;
            uniform fixed _IgnoreNormal;
			uniform half _Blend;		
											  
            struct VertexInput {
                half4 vertex : POSITION;
                half4 color : COLOR;
				half3 normal : NORMAL;
				half2 uv_Main : TEXCOORD0;
                half2 uv_Sand : TEXCOORD1;		  				
            };

            struct VertexOutput {
				half4 color : COLOR;
                half4 pos : SV_POSITION;
				half3 normal : NORMAL;
                half2 uv_Main : TEXCOORD0;
				half2 uv_Sand : TEXCOORD1;


            };

			half4 Contrast(half4 color, half contrast){

                half factor = (1.015686 * (contrast + 1.0)) / (1.0 * (1.015686 - contrast));

				half newRed   = (factor * (color.r - .5) + .5)	 ;
				half newGreen = (factor * (color.g - .5) + .5)	;
				half newBlue  = (factor * (color.b - .5) + .5)	  ;

				half4 result = (newRed, newGreen, newBlue, 1) ;
				return result;

			}
			////////////////////////////////////
			//								  //
			//          VertexShader          //
			//								  //
			////////////////////////////////////

            VertexOutput vert (VertexInput v) {

                VertexOutput o;

                o.uv_Main = v.uv_Main;
				o.uv_Sand = v.uv_Sand;
				o.normal = normalize(mul(v.normal, unity_WorldToObject));

                o.pos = mul(UNITY_MATRIX_MVP, v.vertex ); 	 
                return o;
            }

			////////////////////////////////////
			//								  //
			//         FragmentShader         //
			//								  //
			////////////////////////////////////

            half4 frag(VertexOutput i) : SV_Target {

				half4x4 modelMatrix = unity_ObjectToWorld;
				half3x3 modelMatrixInverse = unity_WorldToObject;					 
				half3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.pos.xyz); 
				half3 lightDirection = normalize(_WorldSpaceLightPos0.xyz);	   
				half3 halfVector = normalize(lightDirection + viewDirection);

				half attenuation = 1.0;				 
				
                half4 _RampMap_var = tex2D(_RampMap,TRANSFORM_TEX(i.uv_Main, _RampMap)); // Ramp Texture
                half4 _SandMap_var = tex2D(_SandMap,TRANSFORM_TEX(i.uv_Sand, _SandMap)); // Sand Texture
				half4 _BorderMap_var = tex2D(_BorderMap,TRANSFORM_TEX(i.uv_Main, _BorderMap)); // Water or Sand Border
				half4 _SpecMap_var = tex2D(_SpecMap,TRANSFORM_TEX(i.uv_Main, _SpecMap)); // Specular mask Texture

				// if max(1.0, = camera & light direction ignore
				half3 specularLighting =   pow( max( 0.0, dot( reflect( -lightDirection, i.normal ), viewDirection ) ), 1 - _Shininess ) * _LightColor0.rgb * _SpecMap_var.rgb * _SpecColor.rgb * (1 - _Shininess * 0.1);

				half3 SeaColor = lerp(_ShallowColor, _DeepColor,  _RampMap_var.a * _Blend)  + UNITY_LIGHTMODEL_AMBIENT.rgb + specularLighting;
				half3 finalColor = lerp( SeaColor , _SandMap_var, _BorderMap_var.r) ;


                return half4(finalColor, 1);

            }
            ENDCG
        }
    }
    FallBack "Diffuse"
    CustomEditor "ShaderForgeMaterialInspector"
}