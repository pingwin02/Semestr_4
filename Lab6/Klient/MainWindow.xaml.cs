using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using Color = System.Drawing.Color;
using MessageBox = System.Windows.MessageBox;
using Point = System.Drawing.Point;
using Window = System.Windows.Window;


namespace Klient
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        bool isConnected = false;
        Color chosenColor;
        short brushSize;
        UdpClient udpClient;
        IPEndPoint endPoint;
        int port;
        Dictionary<byte, ColoredPoint> clientsPoints = new();
        Task task;
        public MainWindow()
        {
            InitializeComponent();
            ChangeStatus(false);
        }

        private void ChangeStatus(bool isConnected)
        {
            this.isConnected = isConnected;
            Board.IsEnabled = isConnected;
            IP_TextBox.IsEnabled = !isConnected;
            Port_TextBox.IsEnabled = !isConnected;
            Connect_Button.IsEnabled = !isConnected;
            Disconnect_Button.IsEnabled = isConnected;
            BrushSize_Slider.IsEnabled = isConnected;
            BrushColor_Rectangle.IsEnabled = isConnected;
            Status_TexBox.Text = isConnected ? "Connected" : "Disconnected";
        }

        private void Connect_Button_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                udpClient = new();
                udpClient.Connect(IP_TextBox.Text, int.Parse(Port_TextBox.Text));
                udpClient.Send(Encoding.ASCII.GetBytes("connect"), 7);

                endPoint = new(IPAddress.Any, 0);
                var data = udpClient.Receive(ref endPoint);
                endPoint.Port = BitConverter.ToInt32(data, 0);

                port = ((IPEndPoint)udpClient.Client.LocalEndPoint).Port;
                udpClient.Close();
                udpClient = new(port);

                udpClient.Connect(endPoint);
                Debug.WriteLine($"Connected to server {endPoint}");

                task = Task.Run(WaitForPaintData);
                ChangeStatus(true);
                Board.Children.Clear();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
                udpClient.Close();
                udpClient = new(port);
            }
        }

        private void Disconnect_Button_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                udpClient.Close();
                udpClient = new(port);

                udpClient.Connect(IP_TextBox.Text, int.Parse(Port_TextBox.Text));
                udpClient.Send(Encoding.ASCII.GetBytes("disconnect"), 10);
                udpClient.Close();

                ChangeStatus(false);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void BrushSize_Slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            brushSize = (short)BrushSize_Slider.Value;
            if (BrushSize_TextBox != null)
                BrushSize_TextBox.Text = brushSize.ToString();

        }

        private void BrushColor_Rectangle_MouseDown(object sender, MouseButtonEventArgs e)
        {
            ColorDialog colorDialog = new();
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
            byte[] bytes = new byte[7];
            bytes[0] = 0x01;
            Buffer.BlockCopy(BitConverter.GetBytes(chosenColor.ToArgb()), 0, bytes, 1, sizeof(int));
            Buffer.BlockCopy(BitConverter.GetBytes(brushSize), 0, bytes, sizeof(int) + 1, sizeof(short));
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
                case 0x01: //color and size
                    {
                        byte[] color = new byte[4];
                        Buffer.BlockCopy(bytes, 2, color, 0, color.Length);
                        byte[] size = new byte[2];
                        Buffer.BlockCopy(bytes, 6, size, 0, size.Length);
                        clientsPoints[id] = new(
                            Color.FromArgb(BitConverter.ToInt32(color, 0)),
                            new(0),
                            BitConverter.ToInt16(size, 0));
                        break;
                    }
                case 0x02: //position
                    {
                        Draw(bytes, id);
                        break;
                    }
                default:
                    {
                        return;
                    }
            }
        }


        private void WaitForPaintData()
        {
            try
            {
                while (isConnected)
                {
                    IPEndPoint endPoint = new(IPAddress.Any, 0);
                    byte[] bytes = udpClient.Receive(ref endPoint);
                    byte id = bytes[0];
                    ManageIncomingMessage(bytes, id);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }


        private void Draw(byte[] bytes, byte id)
        {

            Board.Dispatcher.Invoke(
                new(() =>
                {
                    var client = clientsPoints[id];
                    byte[] position = new byte[4];
                    Buffer.BlockCopy(bytes, 2, position, 0, position.Length);
                    Point point = new(BitConverter.ToInt32(position, 0));
                    client.Point = point;
                    Brush brush = new SolidColorBrush(
                        System.Windows.Media.Color.FromRgb(
                            client.Color.R,
                            client.Color.G,
                            client.Color.B));

                    brushSize = client.Size;

                    Line line = new()
                    {
                        X1 = point.X - brushSize,
                        X2 = point.X,
                        Y1 = point.Y - brushSize,
                        Y2 = point.Y,
                        Stroke = brush,
                        StrokeThickness = brushSize
                    };
                    Board.Children.Add(line);
                }));
        }

    }

    internal class ColoredPoint
    {
        public ColoredPoint(Color color, Point point, short size)
        {
            Color = color;
            Point = point;
            Size = size;

        }
        public Color Color { get; set; }
        public Point Point { get; set; }
        public short Size { get; set; }
    }
}
