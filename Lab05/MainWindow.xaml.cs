using System;
using System.ComponentModel;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;

namespace Lab5
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Tasks_Button_Click(object sender, RoutedEventArgs e)
        {
            int n = int.Parse(TextBox_N.Text);
            int k = int.Parse(TextBox_K.Text);


            Task<double> numeratorTask = Task.Factory.StartNew(() => CalculateNumerator(n, k));
            Task<double> denominatorTask = Task.Factory.StartNew(() => CalculateDenominator(k));

            Task.WaitAll(numeratorTask, denominatorTask);


            double result = numeratorTask.Result / denominatorTask.Result;


            Tasks_Text.Text = result.ToString();
        }

        private void Delegates_Button_Click(object sender, RoutedEventArgs e)
        {

            int n = int.Parse(TextBox_N.Text);
            int k = int.Parse(TextBox_K.Text);

            Func<int, int, double> numeratorDelegate = CalculateNumerator;
            Func<int, double> denominatorDelegate = CalculateDenominator;

            IAsyncResult numeratorResult = numeratorDelegate.BeginInvoke(n, k, null, null);
            IAsyncResult denominatorResult = denominatorDelegate.BeginInvoke(k, null, null);

            double numerator = numeratorDelegate.EndInvoke(numeratorResult);
            double denominator = denominatorDelegate.EndInvoke(denominatorResult);

            double result = numerator / denominator;

            Delegates_Text.Text = result.ToString();
        }

        private async void AsyncAwait_Button_Click(object sender, RoutedEventArgs e)
        {

            int n = int.Parse(TextBox_N.Text);
            int k = int.Parse(TextBox_K.Text);

            double numerator = await Task.Run(() => CalculateNumerator(n, k));
            double denominator = await Task.Run(() => CalculateDenominator(k));
            double result = numerator / denominator;

            AsyncAwait_Text.Text = result.ToString();
        }


        private static double CalculateNumerator(int n, int k)
        {
            double result = 1;
            for (int i = 0; i < k; i++)
            {
                result *= n - i;
            }
            return result;
        }

        private static double CalculateDenominator(int k)
        {
            double result = 1;
            for (int i = 1; i <= k; i++)
            {
                result *= i;
            }
            return result;
        }

        private void Fib_GetButton_Click(object sender, RoutedEventArgs e)
        {
            BackgroundWorker bw = new BackgroundWorker();
            bw.DoWork += ((object sender, DoWorkEventArgs args) =>
            {
                BackgroundWorker worker = sender as BackgroundWorker;
                int i = (int)args.Argument;

                if (i == 0)
                {
                    args.Result = 0;
                    return;
                }
                else if (i == 1 || i == 2)
                {
                    args.Result = 1;
                    return;
                }
                double fib = 0;
                double prev = 1;
                double prevprev = 1;
                for (int k = 3; k <= i; k++)
                {
                    fib = prev + prevprev;
                    prevprev = prev;
                    prev = fib;
                    worker.ReportProgress(100 * (k - 3) / i);
                    Thread.Sleep(20);
                }
                args.Result = fib;
            });
            bw.ProgressChanged += ((object sender, ProgressChangedEventArgs args) =>
            {
                Fib_ProgressBar.Value = args.ProgressPercentage;
            });

            bw.RunWorkerCompleted += ((object sender, RunWorkerCompletedEventArgs args) =>
            {
                Fib_ResultTextBox.Text = args.Result.ToString();
                Fib_ProgressBar.Value = 100;
            });

            bw.WorkerReportsProgress = true;
            bw.RunWorkerAsync(int.Parse(Fib_TextBox.Text));
        }

        private void Compress_Button_Click(object sender, RoutedEventArgs e)
        {

            var dialog = new FolderBrowserDialog();

            string path;

            if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                path = dialog.SelectedPath;

                Parallel.ForEach(Directory.GetFiles(path), file =>
                {
                    if (Path.GetExtension(file) != ".gz")
                    {
                        CompressFile(file);
                    }
                });

            }

        }

        private void Decompress_Button_Click(object sender, RoutedEventArgs e)
        {

            var dialog = new FolderBrowserDialog();

            string path;

            if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                path = dialog.SelectedPath;

                Parallel.ForEach(Directory.GetFiles(path), file =>
                {
                    if (Path.GetExtension(file) == ".gz")
                        DecompressFile(file);
                });

            }

        }

        private void CompressFile(string path)
        {
            using FileStream originalFileStream = File.Open(path, FileMode.Open);
            using FileStream compressedFileStream = File.Create(path + ".gz");
            using var compressor = new GZipStream(compressedFileStream, CompressionMode.Compress);
            originalFileStream.CopyTo(compressor);

            compressor.Close();
            originalFileStream.Close();
            compressedFileStream.Close();

            File.Delete(path);
        }

        private void DecompressFile(string path)
        {

            using FileStream compressedFileStream = File.Open(path, FileMode.Open);
            using FileStream outputFileStream = File.Create(Path.ChangeExtension(path, ""));
            using var decompressor = new GZipStream(compressedFileStream, CompressionMode.Decompress);
            decompressor.CopyTo(outputFileStream);

            decompressor.Close();
            outputFileStream.Close();
            compressedFileStream.Close();

            File.Delete(path);
        }

        private void Generate_Button_Click(object sender, RoutedEventArgs e)
        {

            var dialog = new FolderBrowserDialog();

            string path;

            if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                path = dialog.SelectedPath;

                string msg = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " +
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " +
                "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris " +
                "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " +
                "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla " +
                "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in " +
                "culpa qui officia deserunt mollit anim id est laborum.";

                string newFileName = $"{path}/sample.txt";

                while (File.Exists(newFileName))
                {
                    newFileName = $"{path}/sample{new Random().Next(1, 1000)}.txt";
                }

                for (int i = 0; i < 1000; i++)
                    File.AppendAllText(newFileName, msg);

            }

        }

        private async void DNS_resolve_Click(object sender, RoutedEventArgs e)
        {
            string[] hostNames = { "www.microsoft.com", "www.apple.com",
            "www.google.com", "www.ibm.com", "cisco.netacad.net",
            "www.oracle.com", "www.nokia.com", "www.hp.com", "www.dell.com",
            "www.samsung.com", "www.toshiba.com", "www.siemens.com",
            "www.amazon.com", "www.sony.com", "www.canon.com", "www.alcatel-lucent.com",
            "www.acer.com", "www.motorola.com" };

            var tasks = hostNames.AsParallel()
                .Select(site => Task.Run(() => resolveIP(site)));

            var results = await Task.WhenAll(tasks);

            string result = string.Join(Environment.NewLine, results);

            DNS_resultBox.Text = result;
        }

        private string resolveIP(string hostName)
        {
            try
            {
                string ip = Dns.GetHostAddresses(hostName).First().ToString();
                return $"{hostName} =>\n{ip}";

            }
            catch
            {
                return $"{hostName} =>\nunknown";
            }
        }

    }
}
