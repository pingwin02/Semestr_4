package pl.edu.pg.pr;

public class App {

    public static void main(String[] args) throws InterruptedException {
        Resource resource = new Resource();
        Thread producer = new Thread(new Producer(resource));
        Thread consumer1 = new Thread(new Consumer(resource, "1"));
        Thread consumer2 = new Thread(new Consumer(resource, "2"));

        producer.start();
        consumer1.start();
        consumer2.start();

        producer.join();
        consumer1.join();
        consumer2.join();
    }
}
