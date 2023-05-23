package pl.edu.pg.pr;

import java.util.ArrayList;
import java.util.List;

public class Resource {
    private List<String> buffer = new ArrayList<>();

    public synchronized String take() throws InterruptedException {
        while (buffer.isEmpty()) {
            wait();
        }
        String value = buffer.get(0);
        buffer.remove(0);
        return value;
    }

    public synchronized void put(String value) {
        buffer.add(value);
        notifyAll();
    }
}
