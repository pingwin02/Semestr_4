package pl.edu.pg.pr;

import static java.lang.Thread.sleep;

public class Producer implements Runnable {
    private Resource resource;
    private static int counter = 1;

    public Producer(Resource resource) {
        this.resource = resource;
    }

    @Override
    public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {
                sleep(2000);
                String product = "Product " + counter++;
                resource.put(product);
                System.out.println("Producer produced: " + product);
            }
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}

