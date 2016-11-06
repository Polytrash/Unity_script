Shader "Custom/WaterShader" {	
Properties {
 	_ShallowWaterTint("Shallow water tint", Color) = (.0, .26, .39, 1.0)
	_DeepWaterTint("Deep water tint", Color) = (.0, .26, .39, 1.0)
	_WaterAttenuation("Water attenuation", Range (0.0, 2.0)) = 1.0

	_MainTex("Main texture", 2D) = "bump" {}
	_Cube ("Cubemap", CUBE) = "" {}
	_WaterMap ("Depth (R), Foam (G), Transparency(B) Refr strength(A)", 2D) = "white" {}
	_WetCoastTint("Wet Coast tint", Color) = (.5, .5, .5, 1.0)
	_WaterWetness("Wet Wetness", 2D) = "white" {}
	_SecondaryRefractionTex("Refraction texture", 2D) = "bump" {}
	_AnisoMap ("AnisoDir(RGB), AnisoLookup(A)", 2D) = "bump" {}
	_AnisoTileX("Aniso Tile X", Range(1, 100)) = 1
	_AnisoTileY("Aniso Tile Y", Range(1, 100)) = 1
	_Shininess ("Shininess", Range (.05, 20.0)) = 1.0
	_Gloss("Gloss", Range(0.0, 20.0)) = 10.0
	_Fresnel0 ("fresnel0", Float) = 0.1
	_Reflectivity("Reflectivity", Range (.0, 1.0)) = .3
	_Refractivity("Refractivity", Range (1.0, 5.0)) = 1.0

	_CausticsAnimationTexture ("Caustics animation", 2D) = "white" {}
 	_CausticsStrength ("Caustics strength", Range (0.0, 1) ) = 0.1
	_CausticsScale ("Caustics scale", Range (0.1, 10.0) ) = 2.0	   	
	_normalStrength("Normal strength",  Range (.01, 5.0)) = .5
	_refractionsWetness("Refractions wetness", Range (.0, 1.0)) = .8   
	_Opaqueness("Opaqueness", Range(.0, 1.0)) = .9

 	_FoamDiffuse("Foam texture", 2D) = "white" {}
	_DUDVFoamMap ("Foam Map", 2D) = "white" {}
	_EdgeFoamStrength ("Edge foam strength", Range (.0, 5.0) ) = 1.0  	 
	_FoamRipple("Foam Ripple", Range(0, 2.0)) = 0.5

	_WaveWind("Wave Wind", Range(0, 1)) = 0.5
	_WaveSpeed("Wave Speed", Range(0.01, 1)) = 0.4
	_WaveHeight("Wave Height", Range(0, 50)) = 0.5
	_WaveTile1("Wave Tile X", Range(10, 500)) = 400
	_WaveTile2("Wave Tile Y", Range(10, 500)) = 400




	causticsOffsetAndScale("internal caustics animation offset and scale", Vector) = (.0, .0, .25, .0)
	causticsAnimationColorChannel("internal caustics animation color channel", Vector) = (1.0, .0, .0, .0)
}
Category {
	Tags {"Queue"="Transparent-10" "IgnoreProjector"="True" "LightMode" = "ForwardBase" "ForceNoShadowCasting" = "True"}
	Lighting on
		
	SubShader {
		Pass {
			ZWrite Off
	 
						    		
			CGPROGRAM
			#pragma multi_compile_fwdbase
			#pragma target 3.0
			#pragma vertex vert
			#pragma fragment frag
			#include "UnityCG.cginc"
			#include "Lighting.cginc"
			#include "AutoLight.cginc"

	
	uniform sampler2D _MainTex, _WaterMap, _WaterWetness, _SecondaryRefractionTex, _AnisoMap ,_CausticsAnimationTexture, _DUDVFoamMap,  _FoamDiffuse;
	uniform float4 _MainTex_ST , _WaterMap_ST, _WaterWetness_ST, _SecondaryRefractionTex_ST, _AnisoMap_ST ,_CausticsAnimationTexture_ST, _DUDVFoamMap_ST;
	uniform samplerCUBE _Cube;

	uniform half _Reflectivity;
	uniform half _Refractivity;	 

	uniform half _WaterAttenuation;
	uniform fixed3 _ShallowWaterTint;
	uniform fixed3 _DeepWaterTint;

	uniform half _Shininess;
	uniform half _Gloss;
	uniform half _Fresnel0;
				
	uniform half _AnisoTileX;
	uniform half _AnisoTileY;

	uniform half _EdgeFoamStrength;
	uniform half _CausticsStrength;
	uniform half _CausticsScale;
 	uniform half _normalStrength;	

	uniform half _FoamRipple;

	uniform half3 _WetCoastTint;
	uniform half _WaveWind;
	uniform half _WaveSpeed;
	uniform half _WaveHeight;
	uniform half _WaveTile1;
	uniform half _WaveTile2;



	uniform half _refractionsWetness; 
	uniform half _Opaqueness;
	
	uniform half3 causticsOffsetAndScale;
	uniform half4 causticsAnimationColorChannel;

	float4 costMaskF(float2 posUV) { return tex2Dlod(_WaterMap, float4(posUV,1.0,1.0)); }	

	struct v2f {
    	float4  pos : SV_POSITION;
    	float2	uv_MainTex : TEXCOORD0;	       	
    	half2	uv_WaterMap : TEXCOORD1;		     	
    	fixed3	viewDir	: COLOR;			    	
       	fixed3	lightDir : TEXCOORD2;
		float4  islandFoam : TEXCOORD3;
		float2  uv_Aniso : TEXCOORD4;
     	float2  uv_SecondaryRefrTex : TEXCOORD5;
	};
	
	////////////////////////////////////
	//								  //
	//          VertexShader          //
	//								  //
	////////////////////////////////////

	v2f vert (appdata_base a)
	{
	    v2f o;

		float2 uv = a.texcoord.xy;
		float4 pos = a.vertex;

		// Coast Setup
		float2 posUV = uv;
		float4 coastMask = costMaskF(posUV);	// mask for coast in blue channel
		float  animTimeX = uv.y * _WaveTile1 + _Time.w * _WaveSpeed;	// add time for shore X
		float  animTimeY = uv.y * _WaveTile2 + _Time.w * _WaveSpeed;	// add time for shore Y

		float waveXCos = cos(animTimeX) + 1;
		float waveYCos = cos(animTimeY);

		// Coast Waves
		pos.z += (waveXCos * _WaveWind * coastMask) * coastMask;
		pos.y += (waveYCos * _WaveHeight * _WaveWind * 0.25) * coastMask;

	    o.pos = mul (UNITY_MATRIX_MVP, pos);
		float2 foamUV = float2(a.vertex.x *_FoamRipple, a.vertex.z *_FoamRipple);

		o.islandFoam.xy = posUV;
		o.islandFoam.zw = foamUV + float2(1 - _Time.x, 1 - _Time.x)*0.5;

	    o.uv_MainTex = TRANSFORM_TEX (a.texcoord, _MainTex);    
		o.uv_WaterMap = a.texcoord;// TRANSFORM_TEX(v.texcoord, _WaterMap);	   
	    o.viewDir = WorldSpaceViewDir(a.vertex);	
	    o.lightDir = normalize(WorldSpaceLightDir( a.vertex ));	  
		o.uv_SecondaryRefrTex = TRANSFORM_TEX (a.texcoord, _SecondaryRefractionTex);


	    


	    TRANSFER_VERTEX_TO_FRAGMENT(o);

	    return o;
	}
	
	////////////////////////////////////
	//            Caustics            //
	////////////////////////////////////
	
	// Causticsの値を制御するためにwaterMapValue追加
	inline half CalculateCaustics(float2 uv, half waterAttenuationValue, fixed4 waterMapValue, fixed4 waterWetness) 
	{
		half4 causticsFrame = tex2D(_CausticsAnimationTexture, frac(uv * _CausticsScale) * causticsOffsetAndScale.zz + causticsOffsetAndScale.xy );

		return (causticsAnimationColorChannel.x * causticsFrame.r
				+ causticsAnimationColorChannel.y * causticsFrame.g
				+ causticsAnimationColorChannel.z * causticsFrame.b) *  lerp( waterWetness * waterMapValue.b * _WaterAttenuation , 0.0, _CausticsStrength ) ;
	}	  

	////////////////////////////////////
	//      NormalInTangentSpace      //
	////////////////////////////////////
		
	inline fixed3 CalculateNormalInTangentSpace(half2 uv_MainTex, out half2 _displacedUV,
												 fixed3 normViewDir, half4 waterMapValue)
	{	
		return fixed3(0.0, 0.0, 1.0);
	}
	
	////////////////////////////////////
	//            Refraction          //
	////////////////////////////////////
			
	inline fixed3 CalculateRefraction(float2 uv_Caustics, half refrStrength, fixed4 waterWetness, float2 uv_SecondaryRefrTex,												
											fixed4 waterMapValue,  half waterAttenuationValue,	fixed3 normViewDir,	float2 _dudvValue)
	{	
		// waterMapValue.b を掛けて砂浜のRefraction除去 	   
		float2 dudvValue = _dudvValue * _Refractivity * waterMapValue.g/ 100000.0 ;
		fixed3 refractionColor;

		refractionColor = tex2D(_SecondaryRefractionTex, uv_SecondaryRefrTex + dudvValue * _SecondaryRefractionTex_ST.x).rgb * _refractionsWetness;	
		refractionColor += CalculateCaustics(uv_Caustics + dudvValue, waterAttenuationValue, waterMapValue, waterWetness);
																						
		return refractionColor;
	}

	////////////////////////////////////
	//             Combine            //
	////////////////////////////////////
	
	inline fixed3 CombineEffectsWithLighting( fixed3 refraction, half refrStrength,	fixed3 reflection,  fixed3 pNormal,
												fixed3 normViewDir,	fixed3 normLightDir, half2 uv_MainTex, half2 uv_Aniso, half waterAttenuationValue, half waterWetnessValue,
												fixed3 foam, fixed3 mask, inout half foamAmount,	fixed foamValue, fixed3 lightDir )
	{
		half nDotView = dot(pNormal, normViewDir);		//Masking  
		fixed3 halfView = normalize ( normLightDir + normViewDir );	//No need in anisotropic
		half nDotHalf = saturate( dot (pNormal, halfView) );
			
		fixed3 anisoDir = normalize( cross(pNormal, lightDir) );

		half lightDotT = dot(normLightDir, anisoDir);
		half viewDotT = dot(normViewDir, anisoDir);
		

		//half spec = tex2D(_AnisoMap, ( float2(lightDotT, viewDotT) + 1.0 ) * .5).a;		
		// AnisoMap に AnisoTile を掛けて反射を直接調整
		half spec = tex2D(_AnisoMap, (   float2(nDotView* _AnisoTileX, viewDotT  * _AnisoTileY  ) + 1.0 ) * .5).a;
		spec = lerp( 0.0, pow(1-spec, _Shininess * 128.0), waterAttenuationValue);
						  		    
		fixed specularComponent = spec;

		half fresnel = .5 - nDotView;
		fresnel = max(0.0, fresnel);
		    
 		specularComponent *= fresnel;	  	    
 	    specularComponent = specularComponent * specularComponent * 10.0;
	    	    
		fixed3 finalColor;
	    finalColor = lerp(_ShallowWaterTint, _DeepWaterTint, waterAttenuationValue );
	   	     	
		//!!!!!!!!!!!!!!!!!!!!
		//!Magic! Don't touch!
		//!!!!!!!!!!!!!!!!!!!!
		
		// shallowWaterTint と 白波 の境界を調整   	
		refraction = lerp(refraction, _ShallowWaterTint, refrStrength * 5 );
		    	
		half refrAmount = saturate( max(waterAttenuationValue, refrStrength * .5) * .8  );

		finalColor = lerp(refraction, finalColor, refrAmount );
		 
		finalColor = lerp(finalColor, reflection, clamp(fresnel * waterAttenuationValue,0.0 , _Reflectivity));

		// 掛けるfoamの回数でfoamの濃さを制御
	    foamAmount = foamAmount * foam;
 		// 編集前
		//finalColor.rgb = lerp(finalColor, fixed3(foamValue, foamValue, foamValue), foamAmount);
		finalColor.rgb = lerp(finalColor, fixed3(1, 1, 1),foamAmount   );
		return (finalColor * _LightColor0.rgb + specularComponent) + UNITY_LIGHTMODEL_AMBIENT.rgb * .5;

	}

	////////////////////////////////////
	//								  //
	//         FragmentShader         //
	//								  //
	////////////////////////////////////

	fixed4 frag (v2f i) : COLOR
	{
		fixed4 outColor;	
		fixed4 waterMapValue = tex2D (_WaterMap, i.uv_WaterMap);		
		//波打ち際
		fixed4 waterWetnessValue = tex2D (_WaterWetness, i.uv_WaterMap);	 
				
		fixed3 normViewDir = normalize(i.viewDir);

		fixed3 pNormal = fixed3(0.0, 1.0, 0.0);
		 	    
		half waterAttenuationValue = saturate( waterMapValue.r * _WaterAttenuation );


		fixed3 dudvFoamValue = tex2D(_DUDVFoamMap, i.uv_MainTex).rgb;	
		
		// Foam scroll		  
	    float2 dudvValue = dudvFoamValue.rg;
		dudvValue = dudvValue * 2.0 - float2(1.0, 1.0);


	    // Refractivity		
		fixed3 refrColor = CalculateRefraction(	i.uv_MainTex, waterMapValue.a, waterWetnessValue, i.uv_SecondaryRefrTex,
												 waterMapValue, waterAttenuationValue,	normViewDir, dudvValue);

	    // Reflectivity
		fixed3 refl = reflect( -normViewDir, pNormal);
		fixed3 reflectCol = texCUBE( _Cube , refl ).rgb ;

		fixed foamRipple = dudvValue.x * _FoamRipple;

		fixed foamValue = dudvFoamValue.b ;
		half foamAmount = waterMapValue.g * _EdgeFoamStrength;
		// 編集前
		//fixed3 foam0 = float3(tex2D(_FoamDiffuse, float2(i.islandFoam.z, i.islandFoam.w - _Time.x)).r, 1.0, 1.0);
		// foamRipple を足すことで白波を馴染ませる
		fixed3 foam = float3(tex2D(_FoamDiffuse, i.uv_SecondaryRefrTex + foamRipple).r, 0, 0) * foamValue;
		fixed3 mask = tex2D(_WaterMap, i.islandFoam.xy ).rgb * foamAmount;		
	    // Combine		
		outColor.rgb = CombineEffectsWithLighting(refrColor, waterMapValue.a, reflectCol, pNormal, normViewDir,
												 i.lightDir, i.uv_MainTex, i.uv_Aniso,  waterAttenuationValue, waterWetnessValue, foam, mask, foamAmount, foamValue, i.lightDir );
		  		
		outColor.a = 1;	  
		//outColor.a *= _Opaqueness;
		outColor.a = waterMapValue.b;
	    return outColor;
	}	
	ENDCG
	}
    }
    FallBack "Diffuse"	}
}