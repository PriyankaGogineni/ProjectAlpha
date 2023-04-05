namespace trash_pro
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
        
        private void Dailybtn_Click(object sender, EventArgs e)
        {
            label_data.Text = "recayable - 20%";
            
            detailedview_btn.Text = "Detailed View";
        }

        private void Weeklybtn_Click(object sender, EventArgs e)
        {
            label_data.Text = "recayable - 100%";
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
        string[] product = { "glass : 40%", "wood", "paper", "cardboard" };
        private void detailedview_btn_Click(object sender, EventArgs e)
        {

            label2.Text = product[0];
            label2.Text = product[0];
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}