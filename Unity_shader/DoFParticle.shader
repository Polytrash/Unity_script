Shader "Unlit/DoFParticle"
{

    Properties {
//        _Color ("Main Color", Color) = (1,1,1,1)
        _NearTex ("Base (RGB)", 2D) = "white" {}
        _MidTex("Base (RGB)", 2D) = "white" {}
        _FarTex("Base (RGB)", 2D) = "white" {}
        _Near("Near", Range(0, 10)) = 1
        _Middle("Middle", Range(0, 10)) = 2
        _Far("Far", Range(0, 10)) = 3

    }
    SubShader {
       	Tags{ "RenderType"="Transparent"  "Queue" = "Transparent"}


        CGPROGRAM
        #pragma surface surf Lambert vertex:vert 
        #pragma glsl
        #pragma target 3.0



        sampler2D _NearTex;
        sampler2D _MidTex;
        sampler2D _FarTex;
        float _Near;
        float _Middle;
        float _Far;

        float dist;
 
        struct Input {
            float4 c;
           	fixed2 uv_NearTex;
			fixed3 tangent_input;
			float3 objPos;
        };
       
        void vert(inout appdata_full v)
        {    

  
        	fixed4 color;

            float4 worldSpace = mul( _Object2World, v.vertex );
            dist = length(_WorldSpaceCameraPos.xyz - worldSpace.xyz);

        	if(dist < _Near)
        	{
            	#if !defined(SHADER_API_OPENGL)

            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 0));
             	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;
           		#endif

            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);	
            		
        	}else if(dist < _Middle) {

        		#if !defined(SHADER_API_OPENGL)

            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 3));
            	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;
           		#endif

            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);

        	}else if(dist < _Far){

        	   	#if !defined(SHADER_API_OPENGL)

            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 7));
               	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;
           		#endif

            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);


        	}else{

        	    #if !defined(SHADER_API_OPENGL)
            	
            	float4 tex = tex2Dlod (_NearTex, float4(v.texcoord.xy, 0, 7));
              	//v.vertex.x += tex.r  + tex.g  + tex.b ;
            	//v.vertex.y += tex.r  + tex.g  + tex.b ;
           		#endif

            	uint idx = color.r*255 + color.g * 255 + color.b * 255;
            	float2 uv = 1.0 / 512;
            	uv.x *= 0.5;
            	float4 texCoord = float4((float)idx * uv.x, uv.y ,0, 0);



        	}
        	           

        }
 
        void surf (Input IN, inout SurfaceOutput o) {

        	IN.objPos;


        	if(dist < _Near){

            o.Albedo = tex2D(_NearTex, IN.uv_NearTex).rgb;
            o.Alpha = tex2D(_NearTex, IN.uv_NearTex).a;

            }else if(dist < _Middle){

            o.Albedo = tex2D(_MidTex, IN.uv_NearTex).rgb;
            o.Alpha = tex2D(_MidTex, IN.uv_NearTex).a;

            }else if(dist < _Far){

            o.Albedo = tex2D(_FarTex, IN.uv_NearTex).rgb;
            o.Alpha = tex2D(_FarTex, IN.uv_NearTex).a;

            }else{

            o.Albedo = tex2D(_NearTex, IN.uv_NearTex).rgb;
            o.Alpha = tex2D(_NearTex, IN.uv_NearTex).a;

            }

        }
        ENDCG
    }
    FallBack "Diffuse"
}