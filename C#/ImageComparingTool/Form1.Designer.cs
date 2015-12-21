namespace ImageComparingTool
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージ リソースが破棄される場合 true、破棄されない場合は false です。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.scrnCapButton1 = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.FILEToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.OPEN1ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.OPEN2ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.SAVEToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.CLOSEToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.VIEWToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.TOPMOSTToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.pictureBox2 = new System.Windows.Forms.PictureBox();
            this.scrnCapButton2 = new System.Windows.Forms.Button();
            this.ImgPixelColGrp1 = new System.Windows.Forms.GroupBox();
            this.LockGroupBox1 = new System.Windows.Forms.GroupBox();
            this.lockCheck1 = new System.Windows.Forms.CheckBox();
            this.Vlabel1 = new System.Windows.Forms.Label();
            this.VtextBox1 = new System.Windows.Forms.TextBox();
            this.Slabel1 = new System.Windows.Forms.Label();
            this.StextBox1 = new System.Windows.Forms.TextBox();
            this.Hlabel1 = new System.Windows.Forms.Label();
            this.HtextBox1 = new System.Windows.Forms.TextBox();
            this.Blabel1 = new System.Windows.Forms.Label();
            this.BtextBox1 = new System.Windows.Forms.TextBox();
            this.Glabel1 = new System.Windows.Forms.Label();
            this.GtextBox1 = new System.Windows.Forms.TextBox();
            this.Rlabel1 = new System.Windows.Forms.Label();
            this.RtextBox1 = new System.Windows.Forms.TextBox();
            this.ImgPixelColGrp2 = new System.Windows.Forms.GroupBox();
            this.LockGroupBox2 = new System.Windows.Forms.GroupBox();
            this.lockCheck2 = new System.Windows.Forms.CheckBox();
            this.VlabelBox2 = new System.Windows.Forms.Label();
            this.RtextBox2 = new System.Windows.Forms.TextBox();
            this.VtextBox2 = new System.Windows.Forms.TextBox();
            this.RlabelBox2 = new System.Windows.Forms.Label();
            this.SlabelBox2 = new System.Windows.Forms.Label();
            this.GtextBox2 = new System.Windows.Forms.TextBox();
            this.StextBox2 = new System.Windows.Forms.TextBox();
            this.GlabelBox2 = new System.Windows.Forms.Label();
            this.HlabelBox2 = new System.Windows.Forms.Label();
            this.BtextBox2 = new System.Windows.Forms.TextBox();
            this.HtextBox2 = new System.Windows.Forms.TextBox();
            this.BlabelBox2 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.menuStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            this.ImgPixelColGrp1.SuspendLayout();
            this.LockGroupBox1.SuspendLayout();
            this.ImgPixelColGrp2.SuspendLayout();
            this.LockGroupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(12, 36);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(360, 360);
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            this.pictureBox1.WaitOnLoad = true;
            this.pictureBox1.MouseDown += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseDown);
            this.pictureBox1.MouseMove += new System.Windows.Forms.MouseEventHandler(this.Timer1_Tick);
            this.pictureBox1.MouseMove += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseMove);
            this.pictureBox1.MouseUp += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseUp);
            this.pictureBox1.MouseWheel += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseWheel);
            // 
            // scrnCapButton1
            // 
            this.scrnCapButton1.Location = new System.Drawing.Point(15, 486);
            this.scrnCapButton1.Name = "scrnCapButton1";
            this.scrnCapButton1.Size = new System.Drawing.Size(350, 23);
            this.scrnCapButton1.TabIndex = 1;
            this.scrnCapButton1.Text = "Screen Capture";
            this.scrnCapButton1.UseVisualStyleBackColor = true;
            this.scrnCapButton1.Click += new System.EventHandler(this.screenCapture1);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.FILEToolStripMenuItem,
            this.VIEWToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(744, 24);
            this.menuStrip1.TabIndex = 2;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // FILEToolStripMenuItem
            // 
            this.FILEToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.OPEN1ToolStripMenuItem,
            this.OPEN2ToolStripMenuItem,
            this.SAVEToolStripMenuItem,
            this.CLOSEToolStripMenuItem});
            this.FILEToolStripMenuItem.Name = "FILEToolStripMenuItem";
            this.FILEToolStripMenuItem.Size = new System.Drawing.Size(66, 20);
            this.FILEToolStripMenuItem.Text = "ファイル(&F)";
            this.FILEToolStripMenuItem.Click += new System.EventHandler(this.ファイルToolStripMenuItem_Click);
            // 
            // OPEN1ToolStripMenuItem
            // 
            this.OPEN1ToolStripMenuItem.Name = "OPEN1ToolStripMenuItem";
            this.OPEN1ToolStripMenuItem.Size = new System.Drawing.Size(116, 22);
            this.OPEN1ToolStripMenuItem.Text = "開く1(&O)";
            this.OPEN1ToolStripMenuItem.Click += new System.EventHandler(this.FileOpen_Click1);
            // 
            // OPEN2ToolStripMenuItem
            // 
            this.OPEN2ToolStripMenuItem.Name = "OPEN2ToolStripMenuItem";
            this.OPEN2ToolStripMenuItem.Size = new System.Drawing.Size(116, 22);
            this.OPEN2ToolStripMenuItem.Text = "開く2(&P)";
            this.OPEN2ToolStripMenuItem.Click += new System.EventHandler(this.FileOpen_Click2);
            // 
            // SAVEToolStripMenuItem
            // 
            this.SAVEToolStripMenuItem.Name = "SAVEToolStripMenuItem";
            this.SAVEToolStripMenuItem.Size = new System.Drawing.Size(116, 22);
            this.SAVEToolStripMenuItem.Text = "保存(&S)";
            this.SAVEToolStripMenuItem.Click += new System.EventHandler(this.FileSave_Click);
            // 
            // CLOSEToolStripMenuItem
            // 
            this.CLOSEToolStripMenuItem.Name = "CLOSEToolStripMenuItem";
            this.CLOSEToolStripMenuItem.Size = new System.Drawing.Size(116, 22);
            this.CLOSEToolStripMenuItem.Text = "終了(&X)";
            // 
            // VIEWToolStripMenuItem
            // 
            this.VIEWToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.TOPMOSTToolStripMenuItem});
            this.VIEWToolStripMenuItem.Name = "VIEWToolStripMenuItem";
            this.VIEWToolStripMenuItem.Size = new System.Drawing.Size(58, 20);
            this.VIEWToolStripMenuItem.Text = "表示(&V)";
            // 
            // TOPMOSTToolStripMenuItem
            // 
            this.TOPMOSTToolStripMenuItem.Checked = true;
            this.TOPMOSTToolStripMenuItem.CheckOnClick = true;
            this.TOPMOSTToolStripMenuItem.CheckState = System.Windows.Forms.CheckState.Checked;
            this.TOPMOSTToolStripMenuItem.DoubleClickEnabled = true;
            this.TOPMOSTToolStripMenuItem.Name = "TOPMOSTToolStripMenuItem";
            this.TOPMOSTToolStripMenuItem.Size = new System.Drawing.Size(176, 22);
            this.TOPMOSTToolStripMenuItem.Text = "最前面に表示する(&T)";
            this.TOPMOSTToolStripMenuItem.Click += new System.EventHandler(this.TOPMOSTToolStripMenuItem_Click);
            // 
            // pictureBox2
            // 
            this.pictureBox2.Location = new System.Drawing.Point(372, 36);
            this.pictureBox2.Name = "pictureBox2";
            this.pictureBox2.Size = new System.Drawing.Size(360, 360);
            this.pictureBox2.TabIndex = 3;
            this.pictureBox2.TabStop = false;
            this.pictureBox2.WaitOnLoad = true;
            this.pictureBox2.MouseDown += new System.Windows.Forms.MouseEventHandler(this.pictureBox2_MouseDown);
            this.pictureBox2.MouseMove += new System.Windows.Forms.MouseEventHandler(this.Timer2_Tick);
            this.pictureBox2.MouseMove += new System.Windows.Forms.MouseEventHandler(this.pictureBox2_MouseMove);
            this.pictureBox2.MouseUp += new System.Windows.Forms.MouseEventHandler(this.pictureBox2_MouseUp);
            this.pictureBox2.MouseWheel += new System.Windows.Forms.MouseEventHandler(this.pictureBox2_MouseWheel);
            // 
            // scrnCapButton2
            // 
            this.scrnCapButton2.Location = new System.Drawing.Point(377, 486);
            this.scrnCapButton2.Name = "scrnCapButton2";
            this.scrnCapButton2.Size = new System.Drawing.Size(342, 23);
            this.scrnCapButton2.TabIndex = 4;
            this.scrnCapButton2.Text = "Screen Capture";
            this.scrnCapButton2.UseVisualStyleBackColor = true;
            this.scrnCapButton2.Click += new System.EventHandler(this.screenCapture2);
            // 
            // ImgPixelColGrp1
            // 
            this.ImgPixelColGrp1.Controls.Add(this.LockGroupBox1);
            this.ImgPixelColGrp1.Controls.Add(this.Vlabel1);
            this.ImgPixelColGrp1.Controls.Add(this.VtextBox1);
            this.ImgPixelColGrp1.Controls.Add(this.Slabel1);
            this.ImgPixelColGrp1.Controls.Add(this.StextBox1);
            this.ImgPixelColGrp1.Controls.Add(this.Hlabel1);
            this.ImgPixelColGrp1.Controls.Add(this.HtextBox1);
            this.ImgPixelColGrp1.Controls.Add(this.Blabel1);
            this.ImgPixelColGrp1.Controls.Add(this.BtextBox1);
            this.ImgPixelColGrp1.Controls.Add(this.Glabel1);
            this.ImgPixelColGrp1.Controls.Add(this.GtextBox1);
            this.ImgPixelColGrp1.Controls.Add(this.Rlabel1);
            this.ImgPixelColGrp1.Controls.Add(this.RtextBox1);
            this.ImgPixelColGrp1.Location = new System.Drawing.Point(15, 403);
            this.ImgPixelColGrp1.Name = "ImgPixelColGrp1";
            this.ImgPixelColGrp1.Size = new System.Drawing.Size(350, 77);
            this.ImgPixelColGrp1.TabIndex = 5;
            this.ImgPixelColGrp1.TabStop = false;
            this.ImgPixelColGrp1.Text = "Image1 Pixel Color";
            // 
            // LockGroupBox1
            // 
            this.LockGroupBox1.Controls.Add(this.lockCheck1);
            this.LockGroupBox1.Location = new System.Drawing.Point(243, 15);
            this.LockGroupBox1.Name = "LockGroupBox1";
            this.LockGroupBox1.Size = new System.Drawing.Size(95, 52);
            this.LockGroupBox1.TabIndex = 12;
            this.LockGroupBox1.TabStop = false;
            this.LockGroupBox1.Text = "Lock1";
            // 
            // lockCheck1
            // 
            this.lockCheck1.AutoSize = true;
            this.lockCheck1.Location = new System.Drawing.Point(13, 23);
            this.lockCheck1.Name = "lockCheck1";
            this.lockCheck1.Size = new System.Drawing.Size(67, 16);
            this.lockCheck1.TabIndex = 14;
            this.lockCheck1.Text = " Ctrl + k";
            this.lockCheck1.UseVisualStyleBackColor = true;
            // 
            // Vlabel1
            // 
            this.Vlabel1.AutoSize = true;
            this.Vlabel1.Location = new System.Drawing.Point(161, 52);
            this.Vlabel1.Name = "Vlabel1";
            this.Vlabel1.Size = new System.Drawing.Size(19, 12);
            this.Vlabel1.TabIndex = 11;
            this.Vlabel1.Text = "V :";
            // 
            // VtextBox1
            // 
            this.VtextBox1.Location = new System.Drawing.Point(180, 48);
            this.VtextBox1.Name = "VtextBox1";
            this.VtextBox1.Size = new System.Drawing.Size(52, 19);
            this.VtextBox1.TabIndex = 10;
            // 
            // Slabel1
            // 
            this.Slabel1.AutoSize = true;
            this.Slabel1.Location = new System.Drawing.Point(85, 52);
            this.Slabel1.Name = "Slabel1";
            this.Slabel1.Size = new System.Drawing.Size(18, 12);
            this.Slabel1.TabIndex = 9;
            this.Slabel1.Text = "S :";
            // 
            // StextBox1
            // 
            this.StextBox1.Location = new System.Drawing.Point(104, 48);
            this.StextBox1.Name = "StextBox1";
            this.StextBox1.Size = new System.Drawing.Size(52, 19);
            this.StextBox1.TabIndex = 8;
            // 
            // Hlabel1
            // 
            this.Hlabel1.AutoSize = true;
            this.Hlabel1.Location = new System.Drawing.Point(9, 52);
            this.Hlabel1.Name = "Hlabel1";
            this.Hlabel1.Size = new System.Drawing.Size(19, 12);
            this.Hlabel1.TabIndex = 7;
            this.Hlabel1.Text = "H :";
            // 
            // HtextBox1
            // 
            this.HtextBox1.Location = new System.Drawing.Point(28, 48);
            this.HtextBox1.Name = "HtextBox1";
            this.HtextBox1.Size = new System.Drawing.Size(52, 19);
            this.HtextBox1.TabIndex = 6;
            // 
            // Blabel1
            // 
            this.Blabel1.AutoSize = true;
            this.Blabel1.Location = new System.Drawing.Point(161, 27);
            this.Blabel1.Name = "Blabel1";
            this.Blabel1.Size = new System.Drawing.Size(19, 12);
            this.Blabel1.TabIndex = 5;
            this.Blabel1.Text = "B :";
            // 
            // BtextBox1
            // 
            this.BtextBox1.Location = new System.Drawing.Point(180, 23);
            this.BtextBox1.Name = "BtextBox1";
            this.BtextBox1.Size = new System.Drawing.Size(52, 19);
            this.BtextBox1.TabIndex = 4;
            // 
            // Glabel1
            // 
            this.Glabel1.AutoSize = true;
            this.Glabel1.Location = new System.Drawing.Point(85, 27);
            this.Glabel1.Name = "Glabel1";
            this.Glabel1.Size = new System.Drawing.Size(19, 12);
            this.Glabel1.TabIndex = 3;
            this.Glabel1.Text = "G :";
            // 
            // GtextBox1
            // 
            this.GtextBox1.Location = new System.Drawing.Point(104, 23);
            this.GtextBox1.Name = "GtextBox1";
            this.GtextBox1.Size = new System.Drawing.Size(52, 19);
            this.GtextBox1.TabIndex = 2;
            // 
            // Rlabel1
            // 
            this.Rlabel1.AutoSize = true;
            this.Rlabel1.Location = new System.Drawing.Point(9, 27);
            this.Rlabel1.Name = "Rlabel1";
            this.Rlabel1.Size = new System.Drawing.Size(19, 12);
            this.Rlabel1.TabIndex = 1;
            this.Rlabel1.Text = "R :";
            // 
            // RtextBox1
            // 
            this.RtextBox1.Location = new System.Drawing.Point(28, 23);
            this.RtextBox1.Name = "RtextBox1";
            this.RtextBox1.Size = new System.Drawing.Size(52, 19);
            this.RtextBox1.TabIndex = 0;
            // 
            // ImgPixelColGrp2
            // 
            this.ImgPixelColGrp2.Controls.Add(this.LockGroupBox2);
            this.ImgPixelColGrp2.Controls.Add(this.VlabelBox2);
            this.ImgPixelColGrp2.Controls.Add(this.RtextBox2);
            this.ImgPixelColGrp2.Controls.Add(this.VtextBox2);
            this.ImgPixelColGrp2.Controls.Add(this.RlabelBox2);
            this.ImgPixelColGrp2.Controls.Add(this.SlabelBox2);
            this.ImgPixelColGrp2.Controls.Add(this.GtextBox2);
            this.ImgPixelColGrp2.Controls.Add(this.StextBox2);
            this.ImgPixelColGrp2.Controls.Add(this.GlabelBox2);
            this.ImgPixelColGrp2.Controls.Add(this.HlabelBox2);
            this.ImgPixelColGrp2.Controls.Add(this.BtextBox2);
            this.ImgPixelColGrp2.Controls.Add(this.HtextBox2);
            this.ImgPixelColGrp2.Controls.Add(this.BlabelBox2);
            this.ImgPixelColGrp2.Location = new System.Drawing.Point(377, 403);
            this.ImgPixelColGrp2.Name = "ImgPixelColGrp2";
            this.ImgPixelColGrp2.Size = new System.Drawing.Size(350, 77);
            this.ImgPixelColGrp2.TabIndex = 6;
            this.ImgPixelColGrp2.TabStop = false;
            this.ImgPixelColGrp2.Text = "Image2 Pixel Color";
            // 
            // LockGroupBox2
            // 
            this.LockGroupBox2.Controls.Add(this.lockCheck2);
            this.LockGroupBox2.Location = new System.Drawing.Point(247, 15);
            this.LockGroupBox2.Name = "LockGroupBox2";
            this.LockGroupBox2.Size = new System.Drawing.Size(95, 52);
            this.LockGroupBox2.TabIndex = 27;
            this.LockGroupBox2.TabStop = false;
            this.LockGroupBox2.Text = "Lock2";
            // 
            // lockCheck2
            // 
            this.lockCheck2.AutoSize = true;
            this.lockCheck2.Location = new System.Drawing.Point(13, 23);
            this.lockCheck2.Name = "lockCheck2";
            this.lockCheck2.Size = new System.Drawing.Size(64, 16);
            this.lockCheck2.TabIndex = 14;
            this.lockCheck2.Text = " Ctrl + l";
            this.lockCheck2.UseVisualStyleBackColor = true;
            // 
            // VlabelBox2
            // 
            this.VlabelBox2.AutoSize = true;
            this.VlabelBox2.Location = new System.Drawing.Point(165, 52);
            this.VlabelBox2.Name = "VlabelBox2";
            this.VlabelBox2.Size = new System.Drawing.Size(19, 12);
            this.VlabelBox2.TabIndex = 26;
            this.VlabelBox2.Text = "V :";
            // 
            // RtextBox2
            // 
            this.RtextBox2.Location = new System.Drawing.Point(32, 23);
            this.RtextBox2.Name = "RtextBox2";
            this.RtextBox2.Size = new System.Drawing.Size(52, 19);
            this.RtextBox2.TabIndex = 15;
            // 
            // VtextBox2
            // 
            this.VtextBox2.Location = new System.Drawing.Point(184, 48);
            this.VtextBox2.Name = "VtextBox2";
            this.VtextBox2.Size = new System.Drawing.Size(52, 19);
            this.VtextBox2.TabIndex = 25;
            // 
            // RlabelBox2
            // 
            this.RlabelBox2.AutoSize = true;
            this.RlabelBox2.Location = new System.Drawing.Point(13, 27);
            this.RlabelBox2.Name = "RlabelBox2";
            this.RlabelBox2.Size = new System.Drawing.Size(19, 12);
            this.RlabelBox2.TabIndex = 16;
            this.RlabelBox2.Text = "R :";
            // 
            // SlabelBox2
            // 
            this.SlabelBox2.AutoSize = true;
            this.SlabelBox2.Location = new System.Drawing.Point(89, 52);
            this.SlabelBox2.Name = "SlabelBox2";
            this.SlabelBox2.Size = new System.Drawing.Size(18, 12);
            this.SlabelBox2.TabIndex = 24;
            this.SlabelBox2.Text = "S :";
            // 
            // GtextBox2
            // 
            this.GtextBox2.Location = new System.Drawing.Point(108, 23);
            this.GtextBox2.Name = "GtextBox2";
            this.GtextBox2.Size = new System.Drawing.Size(52, 19);
            this.GtextBox2.TabIndex = 17;
            // 
            // StextBox2
            // 
            this.StextBox2.Location = new System.Drawing.Point(108, 48);
            this.StextBox2.Name = "StextBox2";
            this.StextBox2.Size = new System.Drawing.Size(52, 19);
            this.StextBox2.TabIndex = 23;
            // 
            // GlabelBox2
            // 
            this.GlabelBox2.AutoSize = true;
            this.GlabelBox2.Location = new System.Drawing.Point(89, 27);
            this.GlabelBox2.Name = "GlabelBox2";
            this.GlabelBox2.Size = new System.Drawing.Size(19, 12);
            this.GlabelBox2.TabIndex = 18;
            this.GlabelBox2.Text = "G :";
            // 
            // HlabelBox2
            // 
            this.HlabelBox2.AutoSize = true;
            this.HlabelBox2.Location = new System.Drawing.Point(13, 52);
            this.HlabelBox2.Name = "HlabelBox2";
            this.HlabelBox2.Size = new System.Drawing.Size(19, 12);
            this.HlabelBox2.TabIndex = 22;
            this.HlabelBox2.Text = "H :";
            // 
            // BtextBox2
            // 
            this.BtextBox2.Location = new System.Drawing.Point(184, 23);
            this.BtextBox2.Name = "BtextBox2";
            this.BtextBox2.Size = new System.Drawing.Size(52, 19);
            this.BtextBox2.TabIndex = 19;
            // 
            // HtextBox2
            // 
            this.HtextBox2.Location = new System.Drawing.Point(32, 48);
            this.HtextBox2.Name = "HtextBox2";
            this.HtextBox2.Size = new System.Drawing.Size(52, 19);
            this.HtextBox2.TabIndex = 21;
            // 
            // BlabelBox2
            // 
            this.BlabelBox2.AutoSize = true;
            this.BlabelBox2.Location = new System.Drawing.Point(165, 27);
            this.BlabelBox2.Name = "BlabelBox2";
            this.BlabelBox2.Size = new System.Drawing.Size(19, 12);
            this.BlabelBox2.TabIndex = 20;
            this.BlabelBox2.Text = "B :";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(744, 519);
            this.Controls.Add(this.ImgPixelColGrp2);
            this.Controls.Add(this.ImgPixelColGrp1);
            this.Controls.Add(this.scrnCapButton2);
            this.Controls.Add(this.pictureBox2);
            this.Controls.Add(this.scrnCapButton1);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "Form1";
            this.Text = "ComparingTool";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            this.ImgPixelColGrp1.ResumeLayout(false);
            this.ImgPixelColGrp1.PerformLayout();
            this.LockGroupBox1.ResumeLayout(false);
            this.LockGroupBox1.PerformLayout();
            this.ImgPixelColGrp2.ResumeLayout(false);
            this.ImgPixelColGrp2.PerformLayout();
            this.LockGroupBox2.ResumeLayout(false);
            this.LockGroupBox2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Button scrnCapButton1;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem FILEToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem OPEN1ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem OPEN2ToolStripMenuItem;
        private System.Windows.Forms.PictureBox pictureBox2;
        private System.Windows.Forms.Button scrnCapButton2;
        private System.Windows.Forms.GroupBox ImgPixelColGrp1;
        private System.Windows.Forms.GroupBox LockGroupBox1;
        private System.Windows.Forms.CheckBox lockCheck1;
        private System.Windows.Forms.Label Vlabel1;
        private System.Windows.Forms.TextBox VtextBox1;
        private System.Windows.Forms.Label Slabel1;
        private System.Windows.Forms.TextBox StextBox1;
        private System.Windows.Forms.Label Hlabel1;
        private System.Windows.Forms.TextBox HtextBox1;
        private System.Windows.Forms.Label Blabel1;
        private System.Windows.Forms.TextBox BtextBox1;
        private System.Windows.Forms.Label Glabel1;
        private System.Windows.Forms.TextBox GtextBox1;
        private System.Windows.Forms.Label Rlabel1;
        private System.Windows.Forms.TextBox RtextBox1;
        private System.Windows.Forms.GroupBox ImgPixelColGrp2;
        private System.Windows.Forms.GroupBox LockGroupBox2;
        private System.Windows.Forms.CheckBox lockCheck2;
        private System.Windows.Forms.Label VlabelBox2;
        private System.Windows.Forms.TextBox RtextBox2;
        private System.Windows.Forms.TextBox VtextBox2;
        private System.Windows.Forms.Label RlabelBox2;
        private System.Windows.Forms.Label SlabelBox2;
        private System.Windows.Forms.TextBox GtextBox2;
        private System.Windows.Forms.TextBox StextBox2;
        private System.Windows.Forms.Label GlabelBox2;
        private System.Windows.Forms.Label HlabelBox2;
        private System.Windows.Forms.TextBox BtextBox2;
        private System.Windows.Forms.TextBox HtextBox2;
        private System.Windows.Forms.Label BlabelBox2;
        private System.Windows.Forms.ToolStripMenuItem SAVEToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem CLOSEToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem VIEWToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem TOPMOSTToolStripMenuItem;
    }
}

