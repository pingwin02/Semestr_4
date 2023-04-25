package pl.edu.pg.kask.pt.Lab9;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    private static int ClientId = 1;

    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(4444);
            System.out.println("Server started");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client " + ClientId + " connected");
                new Thread(new ClientHandler(clientSocket, ClientId++)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class ClientHandler implements Runnable {
        private final Socket clientSocket;
        private final int clientId;

        public ClientHandler(Socket clientSocket, int clientId) {
            this.clientSocket = clientSocket;
            this.clientId = clientId;
        }

        @Override
        public void run() {
            try {
                ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());
                ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());

                out.writeObject("ready");

                int n = (int) in.readObject();
                System.out.println("Client " + clientId + " wants to send " + n + " messages");

                out.writeObject("ready for messages");

                for (int i = 0; i < n; i++) {
                    Message message = (Message) in.readObject();
                    System.out.println("Received message #" + message.getNumber() + " from client " + clientId + ": " + message.getContent());
                }

                out.writeObject("finished");

                System.out.println("Client " + clientId + " disconnected");

                clientSocket.close();
            } catch (IOException | ClassNotFoundException e) {
                e.printStackTrace();
            }
        }
    }
}
