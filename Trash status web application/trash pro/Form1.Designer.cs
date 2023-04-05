namespace trash_pro
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            this.Dailybtn = new System.Windows.Forms.Button();
            this.Weeklybtn = new System.Windows.Forms.Button();
            this.label_data = new System.Windows.Forms.Label();
            this.detailedview_btn = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.backgroundWorker2 = new System.ComponentModel.BackgroundWorker();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.label1.Location = new System.Drawing.Point(339, 27);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(149, 28);
            this.label1.TabIndex = 0;
            this.label1.Text = "Trash Statctics";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // Dailybtn
            // 
            this.Dailybtn.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.Dailybtn.Location = new System.Drawing.Point(50, 111);
            this.Dailybtn.Name = "Dailybtn";
            this.Dailybtn.Size = new System.Drawing.Size(140, 41);
            this.Dailybtn.TabIndex = 1;
            this.Dailybtn.Text = "Daily Status";
            this.Dailybtn.UseVisualStyleBackColor = true;
            this.Dailybtn.Click += new System.EventHandler(this.Dailybtn_Click);
            // 
            // Weeklybtn
            // 
            this.Weeklybtn.Font = new System.Drawing.Font("Segoe UI", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.Weeklybtn.Location = new System.Drawing.Point(50, 189);
            this.Weeklybtn.Name = "Weeklybtn";
            this.Weeklybtn.Size = new System.Drawing.Size(154, 36);
            this.Weeklybtn.TabIndex = 2;
            this.Weeklybtn.Text = "Weekly Status";
            this.Weeklybtn.UseVisualStyleBackColor = true;
            this.Weeklybtn.Click += new System.EventHandler(this.Weeklybtn_Click);
            // 
            // label_data
            // 
            this.label_data.AutoSize = true;
            this.label_data.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.label_data.Location = new System.Drawing.Point(69, 272);
            this.label_data.Name = "label_data";
            this.label_data.Size = new System.Drawing.Size(0, 28);
            this.label_data.TabIndex = 3;
            // 
            // detailedview_btn
            // 
            this.detailedview_btn.Location = new System.Drawing.Point(292, 271);
            this.detailedview_btn.Name = "detailedview_btn";
            this.detailedview_btn.Size = new System.Drawing.Size(146, 29);
            this.detailedview_btn.TabIndex = 4;
            this.detailedview_btn.UseVisualStyleBackColor = true;
            this.detailedview_btn.Click += new System.EventHandler(this.detailedview_btn_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(75, 335);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(0, 20);
            this.label2.TabIndex = 5;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 428);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.detailedview_btn);
            this.Controls.Add(this.label_data);
            this.Controls.Add(this.Weeklybtn);
            this.Controls.Add(this.Dailybtn);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private Label label1;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private Button Dailybtn;
        private Button Weeklybtn;
        private Label label_data;
        private Button detailedview_btn;
        private Label label2;
        private System.ComponentModel.BackgroundWorker backgroundWorker2;
    }
}