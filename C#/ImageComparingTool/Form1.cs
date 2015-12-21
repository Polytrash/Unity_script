using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace ImageComparingTool
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            // ホイールイベントの追加
            this.pictureBox1.MouseWheel
                += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseWheel);
            // リサイズイベントを強制実行
            Form1_Resize(null, null);
            // 最前面表示OFF
            this.TopMost = true;
        }

        Bitmap _BMP = new Bitmap(1, 1);    // カラーピッカー用ビットマップ

        // 表示するBitmap
        private Bitmap bmp1 = null;
        private Bitmap bmp2 = null;
        // 描画用Graphicsオブジェクト
        private Graphics g1 = null;
        private Graphics g2 = null;
        // マウスダウンフラグ
        private bool MouseDownFlg1 = false;
        private bool MouseDownFlg2 = false;
        // マウスクリックした位置
        private PointF OldPoint1;
        private PointF OldPoint2;
        // アフィン変換行列
        private System.Drawing.Drawing2D.Matrix mat1;
        private System.Drawing.Drawing2D.Matrix mat2;

        // 最前面表示フラグ
        private bool topMost = true; 


        private void Form1_Resize(object sender, EventArgs e)
        {

            if (g1 != null)
            {
                mat1 = g1.Transform;
                g1.Dispose();
                g1 = null;
            }

            // PictureBoxと同じ大きさのBitmapクラスを作成する
            Bitmap bmpPicBox1 = new Bitmap(pictureBox1.Width, pictureBox1.Height);
            // 空のBitmapをPictureBoxのImageに指定
            pictureBox1.Image = bmpPicBox1;
            // Graphicsオブジェクトの作成(FromImageを使用)
            g1 = Graphics.FromImage(pictureBox1.Image);
            // アフィン変換の設定
            if (mat1 != null)
            {
                g1.Transform = mat1;
            }

            // 補完モードの設定(基本NearestNeighbor)
            g1.InterpolationMode
                = System.Drawing.Drawing2D.InterpolationMode.NearestNeighbor;
            // 画像の描画
            DrawImage1();


            if (g2 != null)
            {
                mat2 = g2.Transform;
                g2.Dispose();
                g2 = null;
            }

            // PictureBoxと同じ大きさのBitmapクラスを作成する
            Bitmap bmpPicBox2 = new Bitmap(pictureBox2.Width, pictureBox2.Height);
            // 空のBitmapをPictureBoxのImageに指定
            pictureBox2.Image = bmpPicBox2;
            // Graphicsオブジェクトの作成(FromImageを使用)
            g2 = Graphics.FromImage(pictureBox2.Image);
            // アフィン変換の設定
            if (mat2 != null)
            {
                g2.Transform = mat1;
            }

            // 補完モードの設定(基本NearestNeighbor)
            g2.InterpolationMode
                = System.Drawing.Drawing2D.InterpolationMode.NearestNeighbor;
            // 画像の描画
            DrawImage2();
        }



        ///////////////////////////////////////////////
        //                                           //
        //         　　ビットマップ描画              //
        //                                           //
        ///////////////////////////////////////////////


        // ビットマップの描画
        private void DrawImage1()
        {
            if (bmp1 == null) return;

            // アフィン変換行列の設定
            if ((mat1 != null))
            {
                g1.Transform = mat1;
            }
            // pictureBoxのクリア
            g1.Clear(pictureBox1.BackColor);
            // 描画
            g1.DrawImage(bmp1, 0, 0);
            // 再描画
            pictureBox1.Refresh();
        }


        // ビットマップの描画
        private void DrawImage2()
        {
            if (bmp2 == null) return;

            // アフィン変換行列の設定
            if ((mat2 != null))
            {
                g2.Transform = mat2;
            }
            // pictureBoxのクリア
            g2.Clear(pictureBox2.BackColor);
            // 描画
            g2.DrawImage(bmp2, 0, 0);
            // 再描画
            pictureBox2.Refresh();
        }



        ///////////////////////////////////////////////
        //                                           //
        //         　　　　画像を開く                //
        //                                           //
        ///////////////////////////////////////////////


        private void FileOpen_Click1(object sender, EventArgs e)
        {
            // ファイルを開くダイアログの作成
            OpenFileDialog dlg = new OpenFileDialog();
            // ファイルフィルタ
            dlg.Filter = "画像ファイル|*.bmp;*.gif;*.jpg;*.png|全てのファイル|*.*";
            // ダイアログ表示
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.Cancel) return;
            // 取得したファイル名
            String FileName = dlg.FileName;

            // Bitmapの確保
            if (bmp1 != null)
            {
                bmp1.Dispose();
            }
            bmp1 = new Bitmap(FileName);

            // アフィン変換行列の初期化
            if (mat1 != null)
            {
                mat1.Dispose();
            }
            mat1 = new System.Drawing.Drawing2D.Matrix();
            // 画像の描画
            DrawImage1();
        }


        private void FileOpen_Click2(object sender, EventArgs e)
        {
            // ファイルを開くダイアログの作成
            OpenFileDialog dlg = new OpenFileDialog();
            // ファイルフィルタ
            dlg.Filter = "画像ファイル|*.bmp;*.gif;*.jpg;*.png|全てのファイル|*.*";
            // ダイアログ表示
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.Cancel) return;
            // 取得したファイル名
            String FileName = dlg.FileName;

            // Bitmapの確保
            if (bmp2 != null)
            {
                bmp2.Dispose();
            }
            bmp2 = new Bitmap(FileName);

            // アフィン変換行列の初期化
            if (mat2 != null)
            {
                mat2.Dispose();
            }
            mat2 = new System.Drawing.Drawing2D.Matrix();
            // 画像の描画
            DrawImage2();
        }


        ///////////////////////////////////////////////
        //                                           // 
        //               編集画像の保存              // 
        //                                           // 
        ///////////////////////////////////////////////

        protected void FileSave_Click(object sender, EventArgs e)
        {
            Bitmap bmp = Bitmap_Chain();

            try
            {
                SaveFileDialog SFD = new SaveFileDialog();
                SFD.Filter = "Bitmap Image|*.bmp|Jpeg Image|*.jpg|Gif Image|*.gif";
                SFD.DefaultExt = "bmp";
                if (SFD.ShowDialog() == DialogResult.OK)
                {

                    if (SFD.FileName != "")
                    {

                        System.IO.FileStream FS = (System.IO.FileStream)SFD.OpenFile();

                        

                        switch (SFD.FilterIndex)
                        {
                            case 1:
                                bmp.Save(FS, System.Drawing.Imaging.ImageFormat.Bmp);
                                break;
                            case 2:
                                bmp.Save(FS, System.Drawing.Imaging.ImageFormat.Jpeg);
                                break;
                            case 3:
                                bmp.Save(FS, System.Drawing.Imaging.ImageFormat.Gif);
                                break;
                        }

                    }
                }
            }


            catch (System.Exception)
            {
                MessageBox.Show("保存できませんでした。");
            }      
        }



        ///////////////////////////////////////////////
        //                                           // 
        //               フォームの終了              // 
        //                                           // 
        ///////////////////////////////////////////////

        protected Bitmap Bitmap_Chain()
        {

            Control picBox1 = pictureBox1;
            System.Drawing.Bitmap bmp1 = new System.Drawing.Bitmap(picBox1.Width, picBox1.Height);
            picBox1.DrawToBitmap(bmp1, picBox1.ClientRectangle);

            Control picBox2 = pictureBox2;
            System.Drawing.Bitmap bmp2 = new System.Drawing.Bitmap(picBox2.Width, picBox2.Height);
            picBox2.DrawToBitmap(bmp2, picBox2.ClientRectangle);

            Bitmap bmp = new Bitmap(pictureBox1.Width + pictureBox2.Width, pictureBox2.Height);
            using (Graphics g = Graphics.FromImage(bmp))
            {

                g.DrawImage(bmp1, new Point(0, 0));
                g.DrawImage(bmp2, new Point(bmp1.Width, 0));
            }                     


            return bmp;
        }


    
        ///////////////////////////////////////////////
        //                                           // 
        //               フォームの終了              // 
        //                                           // 
        ///////////////////////////////////////////////

        protected void Form_Close(object sender, EventArgs e)
        {
            this.Close();
        }



        ///////////////////////////////////////////////
        //                                           // 
        //           スクリーンキャプチャー1         // 
        //                                           // 
        ///////////////////////////////////////////////

        protected void screenCapture1(object sender, EventArgs e)
        {

            //Bitmapの作成
            bmp1 = new Bitmap(Screen.PrimaryScreen.Bounds.Width,
            Screen.PrimaryScreen.Bounds.Height);
            //Graphicsの作成
            Graphics g = Graphics.FromImage(bmp1);

            //画面全体をコピーする
            g.CopyFromScreen(new Point(0, 0), new Point(0, 0), bmp1.Size);
            //解放
            g.Dispose();
            
            // アフィン変換行列の初期化
            if (mat1 != null)
            {
                mat1.Dispose();
            }
            mat1 = new System.Drawing.Drawing2D.Matrix();
            // 画像の描画
            DrawImage1();        
            // 表示

        }

        ///////////////////////////////////////////////
        //                                           // 
        //      切り抜きスクリーンキャプチャー1      // 
        //                                           // 
        ///////////////////////////////////////////////

        protected void screenSnipping1(object sender, EventArgs e)
        {

            // Bitmapの作成
            bmp1 = new Bitmap(Screen.PrimaryScreen.Bounds.Width,
            Screen.PrimaryScreen.Bounds.Height);

            // Graphicsの作成
            Graphics g = Graphics.FromImage(bmp1);

            // 切り抜き用Rectangle　※(座標,座標,サイズ,サイズ)なのでMouse指定の場合は無理
             
            Rectangle rect = new Rectangle(20, 90, 400, 100);
            Bitmap bmpNew = bmp1.Clone(rect, bmp1.PixelFormat);

            //画面全体をコピーする
            g.CopyFromScreen(new Point(0, 0), new Point(0, 0), bmpNew.Size);
            //解放
            g.Dispose();

            // アフィン変換行列の初期化
            if (mat1 != null)
            {
                mat1.Dispose();
            }
            mat1 = new System.Drawing.Drawing2D.Matrix();
            // 画像の描画
            DrawImage1();
            // 表示

        }

        
        ///////////////////////////////////////////////
        //                                           // 
        //           スクリーンキャプチャー2         // 
        //                                           // 
        ///////////////////////////////////////////////

        protected void screenCapture2(object sender, EventArgs e)
        {

            //Bitmapの作成
            bmp2 = new Bitmap(Screen.PrimaryScreen.Bounds.Width,
            Screen.PrimaryScreen.Bounds.Height);
            //Graphicsの作成
            Graphics g = Graphics.FromImage(bmp2);
            //画面全体をコピーする
            g.CopyFromScreen(new Point(0, 0), new Point(0, 0), bmp2.Size);
            //解放
            g.Dispose();

            // アフィン変換行列の初期化
            if (mat2 != null)
            {
                mat2.Dispose();
            }

            mat2 = new System.Drawing.Drawing2D.Matrix();
            // 画像の描画
            DrawImage2();

        }



        ///////////////////////////////////////////////
        //                                           //
        //         pictureBox1 マウスイベント        //
        //                                           //
        ///////////////////////////////////////////////


        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
                        MouseDownFlg1 = false;
            // 右ボタンがクリックされたとき
            if (e.Button == System.Windows.Forms.MouseButtons.Right)
            {
                // アフィン変換行列に単位行列を設定する
                mat1.Reset();
                // 画像の描画
                DrawImage1();

                return;
            }
            // フォーカス設定
            // ※クリックしただけではMouseWheelイベントが有効にならない
            pictureBox1.Focus();
            // マウスをクリックした位置の記録
            OldPoint1.X = e.X;
            OldPoint1.Y = e.Y;
            // マウスダウンフラグ
            MouseDownFlg1 = true;
        }



        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            MouseDownFlg1 = false;
        }



        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            // マウスをクリックしながら移動の場合
            if (MouseDownFlg1 == true)
            {
                // 画像の移動
                try
                {
                    mat1.Translate(e.X - OldPoint1.X, e.Y - OldPoint1.Y, System.Drawing.Drawing2D.MatrixOrder.Append);

                // 画像の描画
                DrawImage1();

                // ポインタ位置の保持
                OldPoint1.X = e.X;
                OldPoint1.Y = e.Y;
                }
                catch(Exception){
                
                }
            }
        }



        private void pictureBox1_MouseWheel(object sender, MouseEventArgs e)
        {
            // ポインタの位置→原点に移動
            mat1.Translate(-e.X, -e.Y, System.Drawing.Drawing2D.MatrixOrder.Append);
            if (e.Delta > 0)
            {
                // 拡大
                if (mat1.Elements[0] < 100)   // X方向の倍率をチェック
                {
                    mat1.Scale(1.5f, 1.5f, System.Drawing.Drawing2D.MatrixOrder.Append);
                }
            }
            else
            {

                // 縮小
                if (mat1.Elements[0] > 0.01)  // X方向の倍率をチェック
                {
                    mat1.Scale(1.0f / 1.5f, 1.0f / 1.5f, System.Drawing.Drawing2D.MatrixOrder.Append);
                }
            }
            // 原点 → ポインタの位置へ移動(元の位置へ戻す)
            mat1.Translate(e.X, e.Y, System.Drawing.Drawing2D.MatrixOrder.Append);
            // 画像の描画
            DrawImage1();
        }




        ///////////////////////////////////////////////
        //                                           //
        //         pictureBox2 マウスイベント        //
        //                                           //
        ///////////////////////////////////////////////


        private void pictureBox2_MouseDown(object sender, MouseEventArgs e)
        {
            // 右ボタンがクリックされたとき
            if (e.Button == System.Windows.Forms.MouseButtons.Right)
            {
                // アフィン変換行列に単位行列を設定する
                mat2.Reset();
                // 画像の描画
                DrawImage2();

                return;
            }
            // フォーカス設定
            // ※クリックしただけではMouseWheelイベントが有効にならない
            pictureBox2.Focus();
            // マウスをクリックした位置の記録
            OldPoint2.X = e.X;
            OldPoint2.Y = e.Y;
            // マウスダウンフラグ
            MouseDownFlg2 = true;
        }



        private void pictureBox2_MouseUp(object sender, MouseEventArgs e)
        {
            MouseDownFlg2 = false;
        }



        private void pictureBox2_MouseMove(object sender, MouseEventArgs e)
        {
            // マウスをクリックしながら移動の場合
            if (MouseDownFlg2 == true)
            {
                try
                {
                    // 画像の移動
                    mat2.Translate(e.X - OldPoint2.X, e.Y - OldPoint2.Y, System.Drawing.Drawing2D.MatrixOrder.Append);
                    // 画像の描画
                    DrawImage2();

                    // ポインタ位置の保持
                    OldPoint2.X = e.X;
                    OldPoint2.Y = e.Y;
                }
                catch (Exception)
                {

                }
            }
        }



        private void pictureBox2_MouseWheel(object sender, MouseEventArgs e)
        {
            // ポインタの位置→原点に移動
            mat2.Translate(-e.X, -e.Y, System.Drawing.Drawing2D.MatrixOrder.Append);
            if (e.Delta > 0)
            {
                // 拡大
                if (mat2.Elements[0] < 100)   // X方向の倍率をチェック
                {
                    mat2.Scale(1.5f, 1.5f, System.Drawing.Drawing2D.MatrixOrder.Append);
                }
            }
            else
            {

                // 縮小
                if (mat2.Elements[0] > 0.01)  // X方向の倍率をチェック
                {
                    mat2.Scale(1.0f / 1.5f, 1.0f / 1.5f, System.Drawing.Drawing2D.MatrixOrder.Append);
                }
            }
            // 原点 → ポインタの位置へ移動(元の位置へ戻す)
            mat2.Translate(e.X, e.Y, System.Drawing.Drawing2D.MatrixOrder.Append);
            // 画像の描画
            DrawImage2();
        }




        ///////////////////////////////////////////////
        //                                           // 
        //         カーソル位置のRGB値の取得1        // 
        //                                           // 
        ///////////////////////////////////////////////


        protected void Timer1_Tick(object sender, EventArgs e)
        {
            if (lockCheck1.Checked == false)
            {
                Color COLOR = _BMP.GetPixel(0, 0);


                int X = System.Windows.Forms.Cursor.Position.X;
                int Y = System.Windows.Forms.Cursor.Position.Y;

                Graphics G = Graphics.FromImage(_BMP);
                G.CopyFromScreen(new Point(X, Y), new Point(0, 0), new Size(1, 1));


                RtextBox1.Text = COLOR.R.ToString();
                GtextBox1.Text = COLOR.G.ToString();
                BtextBox1.Text = COLOR.B.ToString();

                HSVColor HSV_COLOR = HSVColor.RGB_HSV(COLOR);

                HtextBox1.Text = HSV_COLOR.H.ToString();
                StextBox1.Text = HSV_COLOR.S.ToString();
                VtextBox1.Text = HSV_COLOR.V.ToString();

                pictureBox1.BackColor = COLOR;

                Cursor.Current = Cursors.Default;
            }
        }

        ///////////////////////////////////////////////
        //                                           // 
        //         カーソル位置のRGB値の取得2        // 
        //                                           // 
        ///////////////////////////////////////////////


        protected void Timer2_Tick(object sender, EventArgs e)
        {
            if (lockCheck2.Checked == false)
            {
                Color COLOR = _BMP.GetPixel(0, 0);


                int X = System.Windows.Forms.Cursor.Position.X;
                int Y = System.Windows.Forms.Cursor.Position.Y;



                Graphics G = Graphics.FromImage(_BMP);
                G.CopyFromScreen(new Point(X, Y), new Point(0, 0), new Size(1, 1));

                RtextBox2.Text = COLOR.R.ToString();
                GtextBox2.Text = COLOR.G.ToString();
                BtextBox2.Text = COLOR.B.ToString();

                HSVColor HSV_COLOR = HSVColor.RGB_HSV(COLOR);

                HtextBox2.Text = HSV_COLOR.H.ToString();
                StextBox2.Text = HSV_COLOR.S.ToString();
                VtextBox2.Text = HSV_COLOR.V.ToString();

                pictureBox2.BackColor = COLOR;

                Cursor.Current = Cursors.Default;
            }

        }



        ///////////////////////////////////////////////
        //                                           // 
        //   ショートカットキーによる取得値の固定　  // 
        //                                           // 
        ///////////////////////////////////////////////

        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            // Ctrl + K をボタンのショートカットキーとして処理する
            if ((int)keyData == (int)Keys.Control + (int)Keys.K)
            {
                if (lockCheck1.Checked == true)
                {
                    this.lockCheck1.Checked = false;

                }
                else                    

                    this.lockCheck1.Checked = true;
            }
            // Ctrl + L をボタンのショートカットキーとして処理する
            if ((int)keyData == (int)Keys.Control + (int)Keys.L)
            {
                if (lockCheck2.Checked == true)
                {
                    this.lockCheck2.Checked = false;

                }
                else
                
                    this.lockCheck2.Checked = true;
            }

            return base.ProcessCmdKey(ref msg, keyData);
        }




        ///////////////////////////////////////////////
        //                                           // 
        //           常に最前面に表示する 　         // 
        //                                           // 
        ///////////////////////////////////////////////

        private void TOPMOSTToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (topMost == true)
            {
                this.TopMost = false;
                topMost = false;
            }
            else
            {
                this.TopMost = true;
                topMost = true;
            }
        }


        private void ファイルToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }



    }

}
