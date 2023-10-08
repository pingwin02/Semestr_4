using System.Collections.Concurrent;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Serwer
{
    internal class Program
    {
        UdpClient _connectionServer;
        UdpClient _paintServer;
        List<IPEndPoint> _clients;
        BlockingCollection<(byte, byte[])> _paintCollection;
        List<(byte, byte[])> _paintCollectionBackup;

        IPEndPoint _connectionEndPoint;
        IPEndPoint _paintEndPoint;

        private static void Main()
        {
            new Program().Start();
        }

        private void Start()
        {
            _connectionServer = new(0);
            _paintServer = new(0);

            _connectionEndPoint = (IPEndPoint)_connectionServer.Client.LocalEndPoint;
            _paintEndPoint = (IPEndPoint)_paintServer.Client.LocalEndPoint;

            _clients = new();
            _paintCollection = new();
            _paintCollectionBackup = new();

            Console.WriteLine($"Server available at: {_connectionEndPoint.Port}");

            Task.WaitAll(
                Task.Factory.StartNew(MainThread),
                Task.Factory.StartNew(SecondThread),
                Task.Factory.StartNew(ThirdThread)
            );

        }
        private void MainThread()
        {
            try
            {
                while (true)
                {
                    IPEndPoint endPoint = new(IPAddress.Any, 0);
                    byte[] bytes = _connectionServer.Receive(ref endPoint);
                    string message = Encoding.ASCII.GetString(bytes);
                    if (message.Equals("connect"))
                    {
                        Console.WriteLine($"{endPoint} connected");
                        _clients.Add(endPoint);
                        byte[] paintPort = BitConverter.GetBytes(_paintEndPoint.Port);
                        _connectionServer.Send(paintPort, paintPort.Length, endPoint);
                        RestoreBoard(endPoint);
                    }
                    else if (message.Equals("disconnect"))
                    {
                        Console.WriteLine($"{endPoint} disconnected");
                        _clients.Remove(endPoint);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }

        }


        private void SecondThread()
        {
            try
            {
                while (true)
                {
                    IPEndPoint endPoint = new(IPAddress.Any, 0);
                    byte[] bytes = _paintServer.Receive(ref endPoint);
                    int clientIndex = _clients.FindIndex(x => x.Equals(endPoint));
                    if (clientIndex == -1)
                    {
                        Console.WriteLine($"Unknown client {endPoint} wants to draw something. Connection terminated.");
                    }
                    else
                    {
                        switch (bytes[0])
                        {
                            case 0x01:
                                Console.WriteLine($"{endPoint} has started drawing");
                                break;
                            case 0x03:
                                Console.WriteLine($"{endPoint} has stopped drawing");
                                break;
                            default:
                                break;
                        }
                        _paintCollection.Add(((byte)clientIndex, bytes));
                        _paintCollectionBackup.Add(((byte)clientIndex, bytes));
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }

        }
        private void ThirdThread()
        {
            try
            {
                while (true)
                {
                    var data = _paintCollection.Take();
                    byte[] message = new byte[1 + data.Item2.Length];
                    message[0] = data.Item1;
                    Buffer.BlockCopy(data.Item2, 0, message, 1, data.Item2.Length);
                    _clients.ForEach(client => _paintServer.Send(message, message.Length, client));
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }

        }

        private void RestoreBoard(IPEndPoint client)
        {
            try
            {
                Thread.Sleep(100);
                Console.WriteLine($"Begin restoring board for {client}");
                foreach (var data in _paintCollectionBackup)
                {
                    byte[] message = new byte[1 + data.Item2.Length];
                    message[0] = data.Item1;
                    Buffer.BlockCopy(data.Item2, 0, message, 1, data.Item2.Length);
                    _paintServer.Send(message, message.Length, client);
                }
                Console.WriteLine($"End restoring board for {client}");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }


        }

    }
}
