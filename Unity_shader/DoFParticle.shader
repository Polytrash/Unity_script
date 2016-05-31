Shader "Unlit/DoFParticle"{

    Properties {
//        _Color ("Main Color", Color) = (1,1,1,1)
        _MainTex ("Base (RGB)", 2D) = "white" {}
        _Zero("Zero ", Range(0, 100)) = 10
        _One("One", Range(0, 100)) = 20
        _Two("Two", Range(0, 100)) = 30
        _Three("Three", Range(0, 100)) = 40
        _Four("Four", Range(0, 100)) = 50
        _Five("Five", Range(0, 100)) = 60
        _Six("Six", Range(0, 100)) = 70

    }
    SubShader {
    	Pass{
       	Tags{ "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" }
       	LOD 200

       	ZWrite OFF
       	Blend SrcAlpha OneMinusSrcAlpha

        CGPROGRAM
    
        #pragma vertex vert 
        #pragma fragment frag
        //#pragma glsl
        #include "UnityCG.cginc"



        uniform sampler2D _MainTex;
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
			float3 normal : NORMAL;
			float4 texcoord : TEXCOORD0;
			float3 dist : TEXCOORD1;

        };

        struct vertexOutput {

        	float4 pos : SV_POSITION;
        	float4 color : COLOR;
        	float4 texcoord : TEXCOORD0;
        	float3 posWorld : TEXCOORD1;
        	float3 norDir : TEXCOORD2;
        	float3 dist : TEXCOORD3;

        };


        vertexOutput vert(vertexInput v)
        {    
        	vertexOutput o;


            o.posWorld = mul(_Object2World, v.vertex);
            o.norDir = normalize(mul(float4(v.normal, 0.0), _World2Object).xyz);
            o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
            o.texcoord = v.texcoord;


            o.dist = float3(distance(o.posWorld, _WorldSpaceCameraPos.xyz), 0, 0);          

            return o;

        }

        float4 frag(vertexOutput i) : COLOR{


        	float3 normalDirection = i.norDir;
        	float3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz);
        	float4 tex;

        	if(i.dist.r < _Zero){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 7));

        	}
        	else if(i.dist.r >= _Zero && i.dist.r < _One){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 6));

        	}
        	else if(i.dist.r >= _One && i.dist.r < _Two){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 5));
        
        	}
        	else if(i.dist.r >= _Two && i.dist.r < _Three){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 4));

        	}
        	else if(i.dist.r >= _Three && i.dist.r < _Four){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 3));

        	}
        	else if(i.dist.r >= _Four && i.dist.r < _Five){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 2));

        	}
        	else if(i.dist.r >= _Five && i.dist.r < _Six){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 1));

        	}
        	else if(i.dist.r <= _Six){

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 0));

        	}

        	else{

        	tex = tex2Dlod(_MainTex, float4(i.texcoord.xy, 0.0, 0));

        	}

        	tex.a = tex.a;

 			return tex;       	           
 			      
 
        }

        ENDCG
        }
    }
    FallBack "Diffuse"
}