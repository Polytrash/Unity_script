Shader "Particles/DoFParticle"{

    Properties {
//        _Color ("Main Color", Color) = (1,1,1,1)
        _MainTex ("Base (RGB)", 2D) = "white" {}
        _TintColor("Tint Color", Color) = (0.5, 0.5, 0.5, 0.5)
        _InvFade("Soft Particle Factor", Range(0.01, 3.0)) = 1.0


        _Zero("Zero ", Range(0, 100)) = 10
        _One("One", Range(0, 100)) = 20
        _Two("Two", Range(0, 100)) = 30
        _Three("Three", Range(0, 100)) = 40
        _Four("Four", Range(0, 100)) = 50
        _Five("Five", Range(0, 100)) = 60
        _Six("Six", Range(0, 100)) = 70

    }
Category{
       	Tags{ "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" }
       	Blend SrcAlpha OneMinusSrcAlpha
       	ColorMask RGB
       	Cull Off Lighting Off ZWrite Off
       	LOD 200

    SubShader {
    	Pass{
        CGPROGRAM
    
        #pragma vertex vert 
        #pragma fragment frag
        //#pragma glsl
        #include "UnityCG.cginc"



        uniform sampler2D _MainTex;
        uniform float4 _MainTex_ST;

        uniform fixed4 _TintColor;
        uniform float _Near;
        uniform float _Middle;
        uniform float _Far;

        uniform float _Zero;
        uniform float _One;
        uniform float _Two;
        uniform float _Three;
        uniform float _Four;
        uniform float _Five;
        uniform float _Six;


        uniform float dist;




 
        struct vertexInput {

			float4 vertex : POSITION;
			float4 color : COLOR;
			float2 texcoord : TEXCOORD0;
			float3 dist : TEXCOORD1;

        };

        struct vertexOutput {

        	float4 vertex : SV_POSITION;
        	float4 color : COLOR;
        	float2 texcoord : TEXCOORD0;

        	UNITY_FOG_COORDS(1)
        	#ifdef SOFTPARTICLES_ON
        	float4 projPos : TEXCOORD1;
        	#endif
        	float3 posWorld : TEXCOORD2;
        	float3 dist : TEXCOORD3;

        };




        vertexOutput vert(vertexInput v)
        {    
        	vertexOutput o;

        	o.posWorld = mul(_Object2World, v.vertex);
            o.vertex = mul(UNITY_MATRIX_MVP, v.vertex);
            #ifdef SOFTPARTICLES_ON
            o.pojPos = ComputeScreenPos(o.vertex);
            COMPUTE_EYEDEPTH(o.projPos.z);
            #endif
            o.color = v.color;
            o.texcoord = TRANSFORM_TEX(v.texcoord, _MainTex);
            UNITY_TRANSFER_FOG(o, o.vertex);

            o.dist = float3(distance(o.posWorld, _WorldSpaceCameraPos.xyz), 0, 0);          

            return o;

        }




        float4 frag(vertexOutput i) : SV_Target{

        	#ifdef SOFTPARTICLES_ON
        	float sceneZ = LinearEyeDepth(SAMPLE_DEPTH_TEXTURE_PROJ(_CameraDepthTexture, UNITY_PROJ_COORD(i.projPos)));
        	float partZ = i.projPos.z;
        	float fade = saturate(_InvFade * (sceneZ - partZ));
        	i.color.a *= fade;
        	#endif

        	float4 col;

        	if(i.dist.r < _Zero){


        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 7));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}
        	else if(i.dist.r >= _Zero && i.dist.r < _One){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 6));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}
        	else if(i.dist.r >= _One && i.dist.r < _Two){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 5));
        	UNITY_APPLY_FOG(i.fogCoord, col);
        
        	}
        	else if(i.dist.r >= _Two && i.dist.r < _Three){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 4));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}
        	else if(i.dist.r >= _Three && i.dist.r < _Four){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 3));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}
        	else if(i.dist.r >= _Four && i.dist.r < _Five){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 2));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}
        	else if(i.dist.r >= _Five && i.dist.r < _Six){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 1));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}
        	else if(i.dist.r <= _Six){

        	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 0));
        	UNITY_APPLY_FOG(i.fogCoord, col);

        	}

        	else{

         	col =  2.0f * i.color * _TintColor * tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 0));
        	UNITY_APPLY_FOG(i.fogCoord, col);


        	}

        	col.a = col.a;

 			return col;          
 
        }

        ENDCG
        }
    }
    FallBack "Diffuse"
}


}