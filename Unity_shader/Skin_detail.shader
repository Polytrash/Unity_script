Shader "Easy Skin Shading/Skin_detail" {
	Properties {
		_MainTex ("Base (RGB)", 2D) = "white" {}
		_BumpMap ("Bump Map", 2D) = "bump" {}
		_DetailMap ("Detail Map", 2D) = "bump"{} // EDIT! ディテールマップ追加
		_DetailScale("Detail Scale", Range(0.01, 1)) = 0.5	// EDIT! ディテールマップスケール追加
		_SpecTex ("Specular Tex", 2D) = "black" {}
		_BeckmannTex ("Beckmann Tex", 2D) = "white" {}
		_SubsurfaceColor ("Subsurface Color", Color) = (1, 0.2, 0.2, 1)
		_RollOff ("Roll Off", Range(0.0, 0.99)) = 0.2
		_BumpBias ("Bump Map Blurring", Range(0, 3)) = 2.0
		_DiffuseWrap ("Diffuse Wrap", Vector) = (0.75, 0.375, 0.1875, 0)
		_SpecRoughness  ("Specular Roughness", Range(0.01, 1)) = 0.15
		_SpecularMult("Specular Multiplier", Range(0.0, 0.99)) = 1.0
		_SpecBrightness ("Specular Brightness", Range(0, 1)) = 0.75
	}
	SubShader {
		Pass {
			Tags { "RenderType" = "Opaque" "IgnoreProjector" = "True"  "LightMode" = "ForwardBase" }
		
			CGPROGRAM
			#include "UnityCG.cginc"
			#include "Lighting.cginc"
			#include "AutoLight.cginc"
		
			#pragma vertex vert
			#pragma fragment frag
			#pragma multi_compile_fwdbase
			
			uniform sampler2D _MainTex;
			uniform float4 _MainTex_ST;

			uniform sampler2D _BumpMap;
			uniform sampler2D _DetailMap; // EDIT! ディテールマップ追加
			uniform float4 _DetailMap_ST; // EDIT! ディテールマップスケール追加

			uniform sampler2D _SpecTex;
		
			uniform sampler2D _BeckmannTex;

			uniform float _SpecularMult;
			uniform float4 _SubsurfaceColor;
			uniform float _RollOff;
			uniform float _BumpBias;
			half _DetailScale;

			uniform float3 _DiffuseWrap;
			uniform float _SpecRoughness;
			uniform float _SpecBrightness;



			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			struct v2f
			{
				float4 pos : SV_POSITION;
				float2 tex : TEXCOORD0;
				float3 lit : TEXCOORD1;
				float3 view : TEXCOORD2;
				LIGHTING_COORDS(3, 4)
			};
			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			v2f vert (appdata_tan v)
			{
				TANGENT_SPACE_ROTATION;

				v2f o;
				o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
				o.tex = TRANSFORM_TEX(v.texcoord, _MainTex);
				o.lit = mul(rotation, ObjSpaceLightDir(v.vertex));
				o.view = mul(rotation, ObjSpaceViewDir(v.vertex));
				TRANSFER_VERTEX_TO_FRAGMENT(o);
				half _DetailScale;
				return o;
			}
			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			float FresnelReflectance (float3 H, float3 V, float F0)
			{
				float base = 1.0 - dot(V, H);
				float exponential = pow(base, 5.0);
				return exponential + F0 * (1.0 - exponential);
			}
			float SkinSpecular(
				float3 N,     // Bumped surface normal
				float3 L,     // Points to light
				float3 V,     // Points to eye
				float m,      // Roughness
				float rho_s   // Specular brightness
			)
			{
				float ndotl = max(dot(N, L), 0.0000001);	// EDIT! max(dot(N,L), 0.0) : 暗部の明度調整(スペキュラー制御)



				float3 h = L + V;          // Unnormalized half-way vector
				float3 H = normalize(h);
				float ndoth = dot(N, H);

				// EDIT! float2(ndoth, m)).x : パラメータ反転 、暗部の明度調整(フレネル制御)、
				float PH = pow(2.0 * tex2D(_BeckmannTex, float2(ndoth, (1-m))).x, 10.0) ;

				float F = FresnelReflectance(H, V, 0.028);
				float frSpec = max(PH * F / dot(h, h), 0.0);

				return ndotl * rho_s * frSpec;
			}


			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			float4 frag (v2f i) : SV_TARGET
			{
				float2 UVCoord = i.tex * _DetailMap_ST.xy;

				fixed4 N = tex2D(_BumpMap, i.tex);  // EDIT! ディテールマップ追加
				fixed4 D = tex2D(_DetailMap, UVCoord)* float4(_DetailScale, _DetailScale, 0, 0);  // EDIT! ディテールマップ追加

				float3 NF = UnpackNormal( N + D);  // EDIT! _Bump と _Detail 合成して法線定義

				float specMask = tex2D(_SpecTex, i.tex).r;
		
				float3 L = normalize(i.lit);
				float3 V = normalize(i.view);
				float ldn = dot(L, N);


				// diffuse part
				float diffuseWeightFull = max(ldn, 0.0); 
				float diffuseWeightHalf = max(0.6 * ldn + 0.6, 0.0); // EDIT!  max(0.5 * ldn + 0.5, 0.0) : ディフューズ制御
				float3 diffuseWeight =   lerp(diffuseWeightFull.xxx, diffuseWeightHalf.xxx, _DiffuseWrap);
				float3 diffColor = diffuseWeight * _LightColor0.rgb;
			
				// specular part
				float specularWeight = SkinSpecular(NF, L, V, _SpecRoughness, _SpecBrightness  );
				float3 specColor = specularWeight * _LightColor0.rgb  * (specMask * 0.1); // EDIT! * specMask : スペキュラー制御
			
				// subsurface part
				float sl = smoothstep(-_RollOff, 1, ldn) - smoothstep(0, 1, ldn);
				sl = max(0, sl);
				float3 subsurfaceColor = sl * _SubsurfaceColor;

				// Reflection part
				float3 coords = normalize(i.lit);
				float4 ReflectProbeColor = 1.0;
				float4 val = UNITY_SAMPLE_TEXCUBE(unity_SpecCube0, coords);
				ReflectProbeColor.xyz = DecodeHDR(val, unity_SpecCube0_HDR);
				ReflectProbeColor.w = 1.0;


				float3 litColor = (diffColor + subsurfaceColor) * LIGHT_ATTENUATION(i) + pow(specColor , (1- _SpecularMult) ) + UNITY_LIGHTMODEL_AMBIENT.rgb + (ReflectProbeColor.xyz /2);	// EDIT! + specColor : スペキュラー制御
				float4 mainColor = tex2D(_MainTex, i.tex);

				return mainColor * float4(litColor, 1);
			}
				ENDCG

		
		}

	}
	FallBack "Diffuse"
}