using System.Security.Cryptography.X509Certificates;

namespace trash_data
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void submit_btn_Click(object sender, EventArgs e)
        {
            string[] product = {"glass","wood","paper","cardboard"};
            string ToLower(string st) 
            {
                string result = "";
                int len = st.Length;
                int j;
                for(int i=0; i<len; i++)
                {
                    j= st[i];
                    if (j >= 65 && j<97)
                    {
                        j += 32;
                        result += (char)j;
                    }
                    else
                        result += (char)j;
                }
                return result;
            }

            string Final = "Non Recyclable";
            for (int k = 0; k < 3; k++)
            {
                string ans = ToLower(product_tb.Text);
                if (ans == product[k])
                {
                    Final = "Recyclable";
                    break;
                }   
            }

            label3.Text = Final;

        }

       
    }
}