using System.IO;
using System.Text.RegularExpressions;
using System.Windows;

namespace Lab2
{
    /// <summary>
    /// Interaction logic for CreateDialog.xaml
    /// </summary>
    public enum Answer { FILE, DIRECTORY, CANCELED }

    public partial class CreateDialog : Window
    {
        private string root;
        public string destinationPath;
        public Answer answer = Answer.CANCELED;
        public CreateDialog(string root)
        {
            InitializeComponent();
            this.root = root;
        }

        private void OK(object sender, RoutedEventArgs e)
        {
            if (fileName.Text == "" || ((bool)isFile.IsChecked &&
                !Regex.IsMatch(fileName.Text, @"^[a-zA-Z0-9_~-]{1,8}\.(txt|php|html)$")))
            {
                MessageBox.Show("Name is incorrect!", "Error!");
            }
            else
            {
                destinationPath = root + "\\" + fileName.Text;
                FileAttributes attributes = FileAttributes.Normal;
                if ((bool)isReadOnly.IsChecked)
                {
                    attributes |= FileAttributes.ReadOnly;
                }
                if ((bool)isArchive.IsChecked)
                {
                    attributes |= FileAttributes.Archive;
                }
                if ((bool)isSystem.IsChecked)
                {
                    attributes |= FileAttributes.System;
                }
                if ((bool)isHidden.IsChecked)
                {
                    attributes |= FileAttributes.Hidden;
                }
                if ((bool)isFile.IsChecked && !File.Exists(destinationPath))
                {
                    File.Create(destinationPath);
                    answer = Answer.FILE;
                }
                else if ((bool)isDirectory.IsChecked && !Directory.Exists(destinationPath))
                {
                    Directory.CreateDirectory(destinationPath);
                    answer = Answer.DIRECTORY;
                }
                else
                {
                    Close();
                    return;
                }
                File.SetAttributes(destinationPath, attributes);

                Close();

            }

        }

        private void Cancel(object sender, RoutedEventArgs e)
        {
            Close();
        }



    }
}

//Explain what this do
// Regex.IsMatch(fileName.Text, "^[a-zA-Z0-9_~-]{1,8}\\.(txt|php|html)$"))