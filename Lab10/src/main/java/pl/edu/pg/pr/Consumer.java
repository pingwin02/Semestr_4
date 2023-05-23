package pl.edu.pg.pr;

import static java.lang.Thread.currentThread;
import static java.lang.Thread.sleep;

public class Consumer implements Runnable {
    private Resource resource;
    private String name;

    public Consumer(Resource resource, String name) {
        this.resource = resource;
        this.name = name;
    }

    @Override
    public void run() {
        try {
            while (!currentThread().isInterrupted()) {
                sleep(3000);
                System.out.println("Consumer " + name + " waits ...");
                String product = resource.take();
                System.out.println("Consumer " + name + " consumed: " + product);
            }
        } catch (InterruptedException ex) {
            throw new RuntimeException(ex);
        }
    }
}
