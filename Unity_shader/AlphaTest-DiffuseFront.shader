Shader "Transparent/Cutout/DiffuseFront" {
Properties {
	_Color ("Main Color", Color) = (1,1,1,1)
	_MainTex ("Base (RGB) Trans (A)", 2D) = "white" {}
	_BumpMap ("Bump Map", 2D) = "bump" {}
	_EmissionPower ("Emission Power", Range(0,10)) = 4	
	_SpecTex ("Specular Tex", 2D) = "black" {}
	_Cutoff ("Alpha cutoff", Range(0,1)) = 0.5
}

SubShader {
	Tags {"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
	Cull Back
	LOD 200
	
CGPROGRAM
#pragma surface surf Lambert vertex:vert alphatest:_Cutoff 

void vert (inout appdata_full v) {
          v.normal = -v.normal;
      }

	sampler2D _MainTex;
	fixed4 _Color;
	uniform sampler2D _BumpMap;
	uniform sampler2D _SpecTex;
	int _EmissionPower;

struct Input {
	float2 uv_MainTex;
	float4 pos : SV_POSITION;
	float2 tex : TEXCOORD0;
	float3 lit : TEXCOORD1;
	float3 view : TEXCOORD2;
	float3 normalDir : TEXCOORD3;
	float4 posWorld : TEXCOORD4;


};

void surf (Input IN, inout SurfaceOutput o) {


	int i = 0;


	float3 fragmentToLightSource = _WorldSpaceLightPos0.xyz - IN.posWorld.xyz;

    	

	fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color;
	fixed4 addColor = c;

	while(i < 2){ 

	addColor.rgb += addColor.rgb;

	i += 1;};



	o.Albedo =  lerp(c.rgb, addColor.rgb, 1- fragmentToLightSource.y );
	o.Alpha = c.a;
}
ENDCG
}

Fallback "Transparent/Cutout/VertexLit"
}
