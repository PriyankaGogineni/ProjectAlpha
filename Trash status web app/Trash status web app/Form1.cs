namespace Trash_Status_web_app
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            label2.Text = "Recayable - 20%";

            detailedview_btn.Text = "Detailed View";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            label2.Text = "Recayable - 100%";

        }

        string[] product = { "Glass : 40%", "Wood", "Paper", "Cardboard" };

        private void detailedview_btn_Click(object sender, EventArgs e)
        {
            label1.Text = product[0];
            label1.Text = product[0];
        }
    }
}