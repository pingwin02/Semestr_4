using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Forms;

namespace Lab2
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : System.Windows.Window
    {
        private string startingPath;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Open(object sender, RoutedEventArgs e)
        {
            var dlg = new FolderBrowserDialog() { Description = "Select directory to open" };

            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                tree.Items.Clear();
                startingPath = dlg.SelectedPath;
                tree.Items.Add(GenerateTree(new DirectoryInfo(startingPath)));
            }

        }

        private void Close(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private TreeViewItem CreateTreeFileItem(FileInfo file)
        {
            TreeViewItem item = new TreeViewItem
            {
                Header = file.Name,
                Tag = file.FullName,
                ContextMenu = new ContextMenu()
            };
            MenuItem openButton = new MenuItem { Header = "Open" };
            openButton.Click += new RoutedEventHandler(OpenEvent);
            MenuItem deleteButtonFile = new MenuItem { Header = "Delete" };
            deleteButtonFile.Click += new RoutedEventHandler(DeleteEvent);
            item.ContextMenu.Items.Add(openButton);
            item.ContextMenu.Items.Add(deleteButtonFile);

            return item;
        }

        private TreeViewItem GenerateTree(DirectoryInfo selectedDir)
        {
            TreeViewItem root = new TreeViewItem
            {
                Header = selectedDir.Name,
                Tag = selectedDir.FullName,
                ContextMenu = new ContextMenu()
            };
            MenuItem createButton = new MenuItem { Header = "Create" };
            createButton.Click += new RoutedEventHandler(CreateEvent);
            MenuItem deleteButton = new MenuItem { Header = "Delete" };
            deleteButton.Click += new RoutedEventHandler(DeleteEvent);
            root.ContextMenu.Items.Add(createButton);
            root.ContextMenu.Items.Add(deleteButton);

            foreach (DirectoryInfo subDir in selectedDir.GetDirectories())
            {
                root.Items.Add(GenerateTree(subDir));
            }
            foreach (FileInfo file in selectedDir.GetFiles())
            {
                root.Items.Add(CreateTreeFileItem(file));
            }
            root.Selected += new RoutedEventHandler(StatusEvent);
            return root;
        }

        private void OpenEvent(object sender, RoutedEventArgs e)
        {
            TreeViewItem item = (TreeViewItem)tree.SelectedItem;
            if (item != null)
            {
                viewer.Text = File.ReadAllText((string)item.Tag);
            }
        }

        private void CreateEvent(object sender, RoutedEventArgs e)
        {
            TreeViewItem root = (TreeViewItem)tree.SelectedItem;
            if (root != null)
            {
                string path = (string)root.Tag;
                CreateDialog dialog = new CreateDialog(path);

                dialog.ShowDialog();

                if (dialog.answer == Answer.FILE)
                {
                    root.Items.Add(CreateTreeFileItem(new FileInfo(dialog.destinationPath)));
                }
                else if (dialog.answer == Answer.DIRECTORY)
                {
                    root.Items.Add(GenerateTree(new DirectoryInfo(dialog.destinationPath)));
                }
            }
        }

        private void DeleteEvent(object sender, RoutedEventArgs e)
        {
            TreeViewItem selected = (TreeViewItem)tree.SelectedItem;
            if (selected != null)
            {
                string selectedPath = (string)selected.Tag;

                if (selectedPath == startingPath)
                {
                    tree.Items.Clear();
                }
                else
                {
                    TreeViewItem parent = (TreeViewItem)selected.Parent;
                    parent.Items.Remove(selected);
                }

                FileAttributes attributes = File.GetAttributes(selectedPath);
                File.SetAttributes(selectedPath,
                   attributes & ~FileAttributes.ReadOnly);

                if (attributes.HasFlag(FileAttributes.Directory))
                {
                    var directory = new DirectoryInfo(selectedPath);
                    foreach (var info in directory.GetFileSystemInfos("*", SearchOption.AllDirectories))
                    {
                        info.Attributes &= ~FileAttributes.ReadOnly;
                    }
                    Directory.Delete(selectedPath, true);
                }
                else
                {
                    File.Delete(selectedPath);
                }

            }
        }

        private void StatusEvent(object sender, RoutedEventArgs e)
        {
            string rahs = "";

            TreeViewItem selected = (TreeViewItem)tree.SelectedItem;
            string selectedPath = (string)selected.Tag;
            FileAttributes attributes = File.GetAttributes(selectedPath);

            if ((FileAttributes.ReadOnly & attributes) == FileAttributes.ReadOnly)
            {
                rahs += 'r';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.Archive & attributes) == FileAttributes.Archive)
            {
                rahs += 'a';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.System & attributes) == FileAttributes.System)
            {
                rahs += 's';
            }
            else
            {
                rahs += '-';
            }
            if ((FileAttributes.Hidden & attributes) == FileAttributes.Hidden)
            {
                rahs += 'h';
            }
            else
            {
                rahs += '-';
            }

            status.Text = rahs;
        }

    }
}
