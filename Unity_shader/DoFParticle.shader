Shader "Unlit/DoFParticle"
{

    Properties {
//        _Color ("Main Color", Color) = (1,1,1,1)
        _NearTex ("Base (RGB)", 2D) = "white" {}
        _Near("Near", Range(0, 10)) = 1
        _Middle("Middle", Range(0, 10)) = 2
        _Far("Far", Range(0, 10)) = 3

    }
    SubShader {
       	Tags{ "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"}
       	Cull Back

        CGPROGRAM
        #pragma surface surf Lambert alpha 
        #pragma vertex:vert 
        #pragma surface:surf
        //#pragma glsl
        #pragma target 3.0



        sampler2D _NearTex;
        float _Near;
        float _Middle;
        float _Far;

 
        struct Input {
            float4 c;
           	fixed2 uv_NearTex;
			fixed3 tangent_input;

        };
       
        void vert(inout appdata_full v, out Input o)
        {    
        	fixed4 color;
        	float3 vertexPos = mul(_Object2World, v.vertex).xyz;
            float dist = distance(vertexPos, _WorldSpaceCameraPos.xyz);



        	if(dist < _Near)
        	{

            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 10));
             	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;


            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 2.5);	
            		
        	}else if(dist > _Near) {


            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 5));
            	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;


            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);

        	}else if(dist > _Middle){


            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 0));
               	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;


            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);


        	}else{

          	
            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 0));
              	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;


            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);



        	}
        	           

        }
 
        void surf (Input IN, inout SurfaceOutput o) {

        	fixed4 c = tex2D(_NearTex, IN.uv_NearTex);
            o.Albedo = c.rgb;
            o.Alpha = c.a;



        }
        ENDCG
    }
    FallBack "Diffuse"
}