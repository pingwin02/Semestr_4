package pl.edu.pg.kask.pt.Lab9;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Socket clientSocket = new Socket("localhost", 4444);
        ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());
        ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());
        Scanner scanner = new Scanner(System.in);
        String userInput;

        String ready1 = (String) in.readObject();
        System.out.println(ready1);

        System.out.println("Type an integer:");
        userInput = scanner.nextLine();
        out.writeObject(Integer.parseInt(userInput));

        String ready2 = (String) in.readObject();
        System.out.println(ready2);

        System.out.println("Type " + userInput + " messages:");
        for (int i = 0; i < Integer.parseInt(userInput); i++) {
            System.out.println("Message " + (i + 1) + ":");
            String message = scanner.nextLine();
            out.writeObject(new Message(i + 1, message));
        }

        String finished = (String) in.readObject();

        System.out.println(finished);

        clientSocket.close();
    }
}
