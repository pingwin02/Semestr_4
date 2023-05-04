using System.Windows.Forms;

namespace Lab4
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
            dataGridView1 = new DataGridView();
            DeleteColumn = new DataGridViewButtonColumn();
            toolStrip1 = new ToolStrip();
            searchForLabel = new ToolStripLabel();
            searchForText = new ToolStripTextBox();
            searchInLabel = new ToolStripLabel();
            searchInText = new ToolStripComboBox();
            findButton = new ToolStripButton();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).BeginInit();
            toolStrip1.SuspendLayout();
            SuspendLayout();
            // 
            // dataGridView1
            // 
            dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView1.Columns.AddRange(new DataGridViewColumn[] { DeleteColumn });
            dataGridView1.Location = new Point(12, 28);
            dataGridView1.Name = "dataGridView1";
            dataGridView1.RowTemplate.Height = 25;
            dataGridView1.Size = new Size(776, 410);
            dataGridView1.TabIndex = 0;
            dataGridView1.CellContentClick += dataGridView1_CellContentClick;
            dataGridView1.CellParsing += dataGridView1_CellParsing;
            dataGridView1.DataError += dataGridView1_DataError;
            // 
            // DeleteColumn
            // 
            DeleteColumn.HeaderText = "";
            DeleteColumn.Name = "DeleteColumn";
            DeleteColumn.ReadOnly = true;
            DeleteColumn.Text = "X";
            DeleteColumn.UseColumnTextForButtonValue = true;
            DeleteColumn.Width = 30;
            // 
            // toolStrip1
            // 
            toolStrip1.Items.AddRange(new ToolStripItem[] { searchForLabel, searchForText, searchInLabel, searchInText, findButton });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Size = new Size(800, 25);
            toolStrip1.TabIndex = 1;
            toolStrip1.Text = "toolStrip1";
            // 
            // searchForLabel
            // 
            searchForLabel.Name = "searchForLabel";
            searchForLabel.Size = new Size(63, 22);
            searchForLabel.Text = "Search for:";
            // 
            // searchForText
            // 
            searchForText.Name = "searchForText";
            searchForText.Size = new Size(100, 25);
            // 
            // searchInLabel
            // 
            searchInLabel.Name = "searchInLabel";
            searchInLabel.Size = new Size(58, 22);
            searchInLabel.Text = "Search in:";
            // 
            // searchInText
            // 
            searchInText.Name = "searchInText";
            searchInText.Size = new Size(121, 25);
            // 
            // findButton
            // 
            findButton.DisplayStyle = ToolStripItemDisplayStyle.Text;
            findButton.ImageTransparentColor = Color.Magenta;
            findButton.Name = "findButton";
            findButton.Size = new Size(34, 22);
            findButton.Text = "Find";
            findButton.Click += findButton_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(toolStrip1);
            Controls.Add(dataGridView1);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)dataGridView1).EndInit();
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private DataGridView dataGridView1;
        private ToolStrip toolStrip1;
        private ToolStripLabel searchForLabel;
        private ToolStripTextBox searchForText;
        private ToolStripLabel searchInLabel;
        private ToolStripComboBox searchInText;
        private ToolStripButton findButton;
        private DataGridViewButtonColumn DeleteColumn;
    }
}