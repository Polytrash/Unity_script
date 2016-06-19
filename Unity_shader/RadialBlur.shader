// Upgrade NOTE: replaced 'samplerRECT' with 'sampler2D'
// Upgrade NOTE: replaced 'texRECT' with 'tex2D'

    Shader "Custom/RadialBlur" {
    Properties {
        _MainTex ("Input", 2D) = "white" {}
        _MaskTex("_MaskTex", 2D )= "white" {}
        _BlurStrength ("", Range(0, 10)) = 1.0
        _BlurWidth ("", Range(0, 1.0)) = 1.0
    }


    SubShader {
            Pass {
                ZTest Always Cull Off ZWrite On
                Fog { Mode off }
           
        CGPROGRAM
       
        #pragma vertex vert_img
        #pragma fragment frag
        #pragma target 3.0
        #pragma fragmentoption ARB_precision_hint_fastest
     
        #include "UnityCG.cginc"
     
        uniform sampler2D _MainTex;
        uniform sampler2D _MaskTex;
        uniform sampler2D _CameraDepthTexture;
        uniform half _BlurStrength;
        uniform half _BlurWidth;
        uniform half _iWidth;
        uniform half _iHeight;



        half4 frag (v2f_img i) : SV_Target {


            half4 color = tex2D(_MainTex, i.uv);
            half4 mask = tex2D(_MaskTex, i.uv);
            half4 colorW = half4(1.0, 1.0, 1.0, 1.0);


            // some sample positions
            float samples[10] = {-0.08,-0.05,-0.03,-0.02,-0.01,0.01,0.02,0.03,0.05,0.08};

            half2 center = half2((_iHeight + _iHeight)/2,(_iWidth + _iWidth)/2 );

            //vector to the middle of the screen
            half2 dir1 = 0.5 * half2(_iHeight / 1.5 , _iWidth) - i.uv; 		// diagonalR
            half2 dir2 = 0.5 * half2(_iHeight, (-1 *_iWidth)*1.5) - i.uv; 	// diagonalL
            half2 dir3 =  half2(_iHeight , 1) ; 						// horizontal
            half2 dir4 =  half2(1 , _iWidth) ; 							// vertical
            half2 dir5 =  half2(_iHeight/4 , _iWidth) ; 				// diagonalR vertical deep
            half2 dir6 =  half2(_iHeight , _iWidth/2) ; 				// diagonalR vertical shallow
            half2 dir7 =  half2((-1 *_iHeight/4 ), _iWidth); 			// diagonalL vertical deep
            half2 dir8 =  half2(_iHeight , ( -1 * _iWidth/2)) ;			// diagonalL vertical shallow


            //distance to center
            half dist = sqrt(dir1.x * dir1.x + dir1.y * dir1.y);
           
            //normalize dir1ection
            dir1 = dir1/dist;
            dir2 = dir2/dist;
            dir3 = dir3/dist;
            dir4 = dir4/dist;
            dir5 = dir5/dist;
            dir6 = dir6/dist;
            dir7 = dir7/dist;
            dir8 = dir8/dist;

            //additional samples towards center of screen
            half4 sum1 = color;
            half4 sum2 = color;
            half4 sum3 = color;
            half4 sum4 = color;
            half4 sum5 = color;
            half4 sum6 = color;
            half4 sum7 = color;
            half4 sum8 = color;

            for(int n = 0; n < 10; n++)
            {
            	//sum1 +=  1 -  color  * samples[n] *2 ;
            	//sum2 +=  1 -  color  * samples[n] / 2;
               sum1 += tex2D(_MainTex, i.uv + dir1 * samples[n] * (_BlurWidth * 0.0025) * _iWidth); // diagonalR
               sum2 += tex2D(_MainTex, i.uv + dir2 * samples[n] * (_BlurWidth * 0.0025) * _iWidth); // diagonalL
               sum3 += tex2D(_MainTex, i.uv + dir3 * samples[n] * (_BlurWidth * 0.0025) * _iWidth); // horizontal
               sum4 += tex2D(_MainTex, i.uv + dir4 * samples[n] * (_BlurWidth * 0.004) * _iWidth); // vertical
               sum5 += tex2D(_MainTex, i.uv + dir5 * samples[n] * (_BlurWidth * 0.003) * _iWidth); // diagonalR vertical deep
               sum6 += tex2D(_MainTex, i.uv + dir6 * samples[n] * (_BlurWidth * 0.002) * _iWidth); // diagonalR vertical shallow
               sum7 += tex2D(_MainTex, i.uv + dir7 * samples[n] * (_BlurWidth * 0.003) * _iWidth); // diagonalL vertical deep
               sum8 += tex2D(_MainTex, i.uv + dir8 * samples[n] * (_BlurWidth * 0.002) * _iWidth); // diagonalL vertical shallow

            }

            //eleven samples...
            sum1 *= 1.0/11.0;
            sum2 *= 1.0/11.0;
            sum3 *= 1.0/11.0;
            sum4 *= 1.0/11.0;
            sum5 *= 1.0/11.0;
            sum6 *= 1.0/11.0;
            sum7 *= 1.0/11.0;
            sum8 *= 1.0/11.0;                                   
            //weighten blur depending on distance to screen center
            half t = dist / _BlurStrength ;

            half4 screen1;
            half4 screen2;
            half4 screen3;
            half4 screen4;
            half4 screen5;
            half4 screen6;
            half4 screen7;
            half4 screen8;

            //blend original with blur


            screen1.r =  colorW.r - (colorW.r - lerp(color.r, sum1.r,  mask.a )) /colorW.r;
            screen1.g =  colorW.g - (colorW.g - lerp(color.g, sum1.g,  mask.a )) /colorW.g;
            screen1.b =  colorW.b - (colorW.b - lerp(color.b, sum1.b,  mask.a )) /colorW.b;
            screen1.a = 1.0;

            screen2.r =  colorW.r - (colorW.r - lerp(color.r, sum2.r,  mask.a )) /colorW.r;
            screen2.g =  colorW.g - (colorW.g - lerp(color.g, sum2.g,  mask.a )) /colorW.g;
            screen2.b =  colorW.b - (colorW.b - lerp(color.b, sum2.b,  mask.a )) /colorW.b;
            screen2.a = 1.0;

            screen3.r =  colorW.r - (colorW.r - lerp(color.r, sum3.r,  mask.a )) /colorW.r;
            screen3.g =  colorW.g - (colorW.g - lerp(color.g, sum3.g,  mask.a )) /colorW.g;
            screen3.b =  colorW.b - (colorW.b - lerp(color.b, sum3.b,  mask.a )) /colorW.b;
            screen3.a = 1.0;

            screen4.r =  colorW.r - (colorW.r - lerp(color.r, sum4.r,  mask.a )) /colorW.r;
            screen4.g =  colorW.g - (colorW.g - lerp(color.g, sum4.g,  mask.a )) /colorW.g;
            screen4.b =  colorW.b - (colorW.b - lerp(color.b, sum4.b,  mask.a )) /colorW.b;
            screen4.a = 1.0;

            screen5.r =  colorW.r - (colorW.r - lerp(color.r, sum5.r,  mask.a )) /colorW.r;
            screen5.g =  colorW.g - (colorW.g - lerp(color.g, sum5.g,  mask.a )) /colorW.g;
            screen5.b =  colorW.b - (colorW.b - lerp(color.b, sum5.b,  mask.a )) /colorW.b;
            screen5.a = 1.0;

            screen6.r =  colorW.r - (colorW.r - lerp(color.r, sum6.r,  mask.a )) /colorW.r;
            screen6.g =  colorW.g - (colorW.g - lerp(color.g, sum6.g,  mask.a )) /colorW.g;
            screen6.b =  colorW.b - (colorW.b - lerp(color.b, sum6.b,  mask.a )) /colorW.b;
            screen6.a = 1.0;

            screen7.r =  colorW.r - (colorW.r - lerp(color.r, sum7.r,  mask.a )) /colorW.r;
            screen7.g =  colorW.g - (colorW.g - lerp(color.g, sum7.g,  mask.a )) /colorW.g;
            screen7.b =  colorW.b - (colorW.b - lerp(color.b, sum7.b,  mask.a )) /colorW.b;
            screen7.a = 1.0;

            screen8.r =  colorW.r - (colorW.r - lerp(color.r, sum8.r,  mask.a )) /colorW.r;
            screen8.g =  colorW.g - (colorW.g - lerp(color.g, sum8.g,  mask.a )) /colorW.g;
            screen8.b =  colorW.b - (colorW.b - lerp(color.b, sum8.b,  mask.a )) /colorW.b;
            screen8.a = 1.0;




            half4 colorA = colorW - (colorW - lerp( screen1 , screen2, 0.5) / colorW);
            half4 colorB = colorW - (colorW - lerp( screen3 , screen4, 0.5) / colorW);

            half4 colorC = colorW - (colorW - lerp( screen5 , screen6, 0.5) / colorW);
            half4 colorD = colorW - (colorW - lerp( screen7 , screen8, 0.5) / colorW);

            half4 colorE = colorW - (colorW - lerp( colorA , colorB, 0.5) / colorW);
            half4 colorF = colorW - (colorW - lerp( colorC , colorD, 0.5) / colorW);

            half4 colorG = colorW - (colorW - lerp( colorE , colorF, 0.5) / colorW);

            //return depth;
            return lerp( colorG, color,  ( mask.a) / _BlurStrength );



            }
        ENDCG
            }
        }
    }
