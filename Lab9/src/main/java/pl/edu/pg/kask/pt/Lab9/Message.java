package pl.edu.pg.kask.pt.Lab9;

import java.io.Serializable;

public class Message implements Serializable {
    private final int number;
    private final String content;

    public Message(int number, String content) {
        this.number = number;
        this.content = content;
    }

    public int getNumber() {
        return number;
    }

    public String getContent() {
        return content;
    }
}