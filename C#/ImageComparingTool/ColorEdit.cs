using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Runtime.InteropServices;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using System.Xml.Serialization;
using System.IO;

namespace ImageComparingTool
{

    ///////////////////////////////////////////////
    //                                           // 
    //             カラー → RGB分解             // 
    //                                           // 
    /////////////////////////////////////////////// 


    //------------ カラー分離用列挙体 ------------//

    public enum RGB { RGB3, RED, GREEN, BLUE };



    public class Color_RGB
    {

        public Bitmap Color_Split(Bitmap BMP, RGB rgbType)
        {

            //float RGB3 = 0;
            float R = 0;
            float G = 0;
            float B = 0;

            Bitmap Changed_BMP = new Bitmap(BMP.Width, BMP.Height);

            switch (rgbType)
            {

                case RGB.RGB3:

                    R = 0.0F;
                    G = 0.0F;
                    B = 0.0F;

                    Changed_BMP = ColorMatrix(BMP, R, G, B);

                    break;

                case RGB.RED:

                    R = 0.0F;
                    G = -1.0F;
                    B = -1.0F;

                    Changed_BMP = ColorMatrix(BMP, R, G, B);

                    break;

                case RGB.GREEN:

                    R = -1.0F;
                    G = 0.0F;
                    B = -1.0F;

                    Changed_BMP = ColorMatrix(BMP, R, G, B);

                    break;

                case RGB.BLUE:

                    R = -1.0F;
                    G = -1.0F;
                    B = 0.0F;

                    Changed_BMP = ColorMatrix(BMP, R, G, B);

                    break;

            }

            return Changed_BMP;

        }



        ///////////////////////////////////////////////
        //                                           // 
        //           カラー → マトリックス          // 
        //                                           // 
        /////////////////////////////////////////////// 

        private Bitmap ColorMatrix(Bitmap BMP, float R, float G, float B)
        {


            // ColorMatrixにセットする行列を 5 * 5 の配列で用意
            // (平行移動（加減算）だけ記述)
            float[][] matrixElement =
    
                 {  new float[]{1, 0, 0, 0, 0},

                    new float[]{0, 1, 0, 0, 0},

                    new float[]{0, 0, 1, 0, 0},

                    new float[]{0, 0, 0, 1, 0},

                    new float[]{R, G, B, 0, 1}  };

            // ColorMatrixオブジェクト作成
            ColorMatrix MATRIX = new ColorMatrix(matrixElement);


            //ImageAttributesにセット
            ImageAttributes ATTR = new ImageAttributes();
            ATTR.SetColorMatrix(MATRIX);

            int imgWIDTH = BMP.Width;
            int imgHEIGHT = BMP.Height;

            Bitmap Changed_BMP = new Bitmap(BMP.Width, BMP.Height);

            //新しいビットマップにImageAttributesを指定して
            //元のビットマップを描画
            Graphics GRAPH = Graphics.FromImage(Changed_BMP);


            GRAPH.DrawImage(BMP,
            new Rectangle(0, 0, imgWIDTH, imgHEIGHT),
            0, 0, imgWIDTH, imgHEIGHT,
            GraphicsUnit.Pixel,
            ATTR);

            GRAPH.Dispose();

            return Changed_BMP;

        }
    }


    ///////////////////////////////////////////////
    //                                           // 
    //              RGB値　→　HSV値             // 
    //                                           // 
    ///////////////////////////////////////////////

    public class HSVColor
    {
        private float _h;

        /// 色相 (Hue)

        public float H { get { return this._h; } }

        private float _s;

        /// 彩度 (Saturation)

        public float S { get { return this._s; } }

        private float _v;

        /// 明度 (Value, Brightness)

        public float V { get { return this._v; } }





        private HSVColor(float HUE, float SATURATION, float BRIGHTNESS)
        {
            if (HUE < 0f || 360f <= HUE)
            {
                throw new ArgumentException(
             "hueは0以上360未満の値です。", "hue");
            }
            if (SATURATION < 0f || 1f < SATURATION)
            {
                throw new ArgumentException(
             "saturationは0以上1以下の値です。", "saturation");
            }
            if (BRIGHTNESS < 0f || 1f < BRIGHTNESS)
            {
                throw new ArgumentException(
             "brightnessは0以上1以下の値です。", "brightness");
            }

            this._h = HUE;
            this._s = SATURATION;
            this._v = BRIGHTNESS;
        }


        ///////////////////////////////////////////////
        //                                           // 
        //              RGB to HSVメソッド           // 
        //                                           // 
        ///////////////////////////////////////////////

        public static HSVColor RGB_HSV(Color RGB)
        {
            float R = (float)RGB.R / 255f;
            float G = (float)RGB.G / 255f;
            float B = (float)RGB.B / 255f;

            float max = Math.Max(R, Math.Max(G, B));
            float min = Math.Min(R, Math.Min(G, B));

            float BRIGHTNESS = max;

            float HUE, SATURATION;
            if (max == min)
            {
                //undefined
                HUE = 0f;
                SATURATION = 0f;
            }
            else
            {
                float c = max - min;

                if (max == R)
                {
                    HUE = (G - B) / c;
                }
                else if (max == G)
                {
                    HUE = (B - R) / c + 2f;
                }
                else
                {
                    HUE = (R - G) / c + 4f;
                }
                HUE *= 60f;
                if (HUE < 0f)
                {
                    HUE += 360f;
                }

                SATURATION = c / max;
            }

            return new HSVColor(HUE, SATURATION, BRIGHTNESS);
        }


        /// 指定したHSVColorからColorを作成する

        public static Color ToRGB(HSVColor HSV)
        {
            float V = HSV.V;
            float S = HSV.S;

            float R, G, B;
            if (S == 0)
            {
                R = V;
                G = V;
                B = V;
            }
            else
            {
                float h = HSV.H / 360f;
                int i = (int)Math.Floor(h);
                float f = h - i;
                float p = V * (1f - S);
                float q;
                if (i % 2 == 0)
                {
                    //t
                    q = V * (1f - (1f - f) * S);
                }
                else
                {
                    q = V * (1f - f * S);
                }

                switch (i)
                {
                    case 0:
                        R = V;
                        G = q;
                        B = p;
                        break;
                    case 1:
                        R = q;
                        G = V;
                        B = p;
                        break;
                    case 2:
                        R = p;
                        G = V;
                        B = q;
                        break;
                    case 3:
                        R = p;
                        G = q;
                        B = V;
                        break;
                    case 4:
                        R = q;
                        G = p;
                        B = V;
                        break;
                    case 5:
                        R = V;
                        G = p;
                        B = q;
                        break;
                    default:
                        throw new ArgumentException(
                            "色相の値が不正です。", "hsv");
                }
            }

            return Color.FromArgb(
                (int)Math.Round(R * 255f),
                (int)Math.Round(G * 255f),
                (int)Math.Round(B * 255f));
        }
    }

}

