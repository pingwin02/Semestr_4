using System;
using System.ComponentModel;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;

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
                } else if (i == 1 || i == 2)
                {
                    args.Result = 1;
                    return;
                }
                double fib = 0;
                double prev = 1;
                double prevprev = 1;
                for (int k = 3; k <= i ; k++)
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
    }
}
