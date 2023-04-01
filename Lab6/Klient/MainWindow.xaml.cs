using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Diagnostics.Tracing;
using System.Globalization;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Forms;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;
using Color = System.Drawing.Color;
using Point = System.Drawing.Point;
using Window = System.Windows.Window;


namespace Klient
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        bool isConnected;
        Color chosenColor;
        double brushSize;
        UdpClient udpClient;
        IPEndPoint endPoint;
        int port;
        Dictionary<byte, ColoredPoint> clientsPoints;
        Task task;

        public MainWindow()
        {
            InitializeComponent();
            ChangeStatus(false);
            udpClient = new UdpClient();
            clientsPoints = new Dictionary<byte, ColoredPoint>();
        }

        private void ChangeStatus(bool flag)
        {
            isConnected = flag;
            Board.IsEnabled = flag;
            IP_TextBox.IsEnabled = !flag;
            Port_TextBox.IsEnabled = !flag;
            Connect_Button.IsEnabled = !flag;
            Disconnect_Button.IsEnabled = flag;
            BrushSize_Slider.IsEnabled = flag;
            BrushColor_Rectangle.IsEnabled = flag;
            Status_TexBox.Text = flag ? "Connected" : "Disconnected";

        }

        private void Connect_Button_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                udpClient.Connect(IP_TextBox.Text, int.Parse(Port_TextBox.Text));
                udpClient.Send(Encoding.ASCII.GetBytes("connect"), 7);
                
                endPoint = new IPEndPoint(IPAddress.Any, 0);
                var data = udpClient.Receive(ref endPoint);
                endPoint.Port = BitConverter.ToInt16(data, 0);

                port = ((IPEndPoint)udpClient.Client.LocalEndPoint).Port;
                udpClient.Close();
                udpClient = new UdpClient(port);

                udpClient.Connect(endPoint);
                Debug.WriteLine("Connected to server " + endPoint.ToString());

                task = Task.Run(() => WaitForPaintData());
                ChangeStatus(true);
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
                udpClient.Close();
                udpClient = new UdpClient(port);
            }
        }

        private void Disconnect_Button_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                udpClient.Close();
                udpClient = new UdpClient(port);
                udpClient.Connect(IP_TextBox.Text, int.Parse(Port_TextBox.Text));
                udpClient.Send(Encoding.ASCII.GetBytes("disconnect"), 10);
                
                udpClient.Close();
                udpClient = new UdpClient(port);
                ChangeStatus(false);
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
            }

            
        }

        private void BrushSize_Slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            brushSize = (int)BrushSize_Slider.Value;
            if (BrushSize_TextBox != null)
                BrushSize_TextBox.Text = brushSize.ToString();

        }

        private void BrushColor_Rectangle_MouseDown(object sender, MouseButtonEventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog();
            if (colorDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                chosenColor = colorDialog.Color;

                BrushColor_Rectangle.Fill = new SolidColorBrush(System.Windows.Media.Color.FromRgb(
                    colorDialog.Color.R,
                    colorDialog.Color.G,
                    colorDialog.Color.B));
            }
        }

        private void Board_MouseDown(object sender, MouseButtonEventArgs e)
        {
            byte[] bytes = new byte[5];
            bytes[0] = 0x01;
            Buffer.BlockCopy(BitConverter.GetBytes(chosenColor.ToArgb()), 0, bytes, 1, sizeof(int));
            udpClient.Send(bytes, bytes.Length);

        }

        private void Board_MouseMove(object sender, System.Windows.Input.MouseEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
            {
                byte[] bytes = new byte[5];
                bytes[0] = 0x02;
                Buffer.BlockCopy(BitConverter.GetBytes((short)e.GetPosition(this).X), 0, bytes, 1, 2);
                Buffer.BlockCopy(BitConverter.GetBytes((short)e.GetPosition(this).Y), 0, bytes, 3, 2);
                udpClient.Send(bytes, bytes.Length);
            }
        }

        private void Board_MouseUp(object sender, MouseButtonEventArgs e)
        {
            byte[] bytes = new byte[1];
            bytes[0] = 0x03;
            udpClient.Send(bytes, bytes.Length);
        }

        private void ManageIncomingMessage(byte[] bytes, byte id)
        {
            switch (bytes[1])
            {
                case 0x01:
                    {
                        byte[] color = new byte[4];
                        Buffer.BlockCopy(bytes, 2, color, 0, color.Length);
                        clientsPoints[id] = new ColoredPoint(Color.FromArgb(BitConverter.ToInt32(color, 0)), new Point(0));
                        break;
                    }

                case 0x02:
                    {
                        Draw(bytes, id);
                        break;
                    }

                case 0x03:
                    {
                        StopDraw(id);
                        break;
                    }
            }
        }


        private void WaitForPaintData()
        {
            try
            {
                while (isConnected)
                {
                    IPEndPoint endPoint = new IPEndPoint(IPAddress.Any, 0);
                    byte[] bytes = udpClient.Receive(ref endPoint);
                    byte id = bytes[0];
                    ManageIncomingMessage(bytes, id);
                }
            }
            catch (Exception ex)
            {
                //System.Windows.MessageBox.Show(ex.Message);
            }
        }


        private void Draw(byte[] bytes, byte id)
        {
            try
            {
                Board.Dispatcher.Invoke(DispatcherPriority.Background,
                    new Action(() =>
                    {
                        var client = clientsPoints[id];
                        byte[] position = new byte[4];
                        Buffer.BlockCopy(bytes, 2, position, 0, position.Length);
                        Point point = new Point(BitConverter.ToInt32(position, 0));
                        if (client.Point.IsEmpty)
                        {
                            client.Point = point;
                        }
                        Brush brush = new SolidColorBrush(
                            System.Windows.Media.Color.FromRgb(
                                client.Color.R,
                                client.Color.G,
                                client.Color.B));

                        Line line = new Line()
                        {
                            X1 = point.X - 5.0f,
                            X2 = point.X,
                            Y1 = point.Y - 5.0f,
                            Y2 = point.Y,
                            Stroke = brush,
                            StrokeThickness = brushSize
                        };
                        Board.Children.Add(line);
                    }));

            }
            catch (KeyNotFoundException ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
            }
        }

        private void StopDraw(byte id)
        {
            try
            {
                var client = clientsPoints[id];
                client.Point = new Point(0);
            }
            catch (KeyNotFoundException ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
            }
        }

    }

    internal class ColoredPoint
    {
        public ColoredPoint(Color color, Point point)
        {
            Color = color;
            Point = point;
        }
        public Color Color { get; set; }
        public Point Point { get; set; }
    }
}
