package pl.edu.pg.kask.pt.Lab8;

import java.util.*;

public class App {
    private final Queue<Integer> tasks = new LinkedList<>();
    private final Map<Integer, Integer> results = new HashMap<>();
    private final List<Thread> threads = new LinkedList<>();
    private final int numThreads;
    private volatile boolean isRunning = true;

    public App(int numThreads) {
        this.numThreads = numThreads;
    }

    public synchronized void addTask(int task) {
        tasks.offer(task);
        notifyAll();
    }

    public synchronized Integer getTask() throws InterruptedException {
        wait();
        return tasks.poll();
    }

    public synchronized void addResult(int task, int result) {
        results.put(task, result);
    }

    public void start() {
        for (int i = 0; i < numThreads; i++) {
            Thread thread = new Thread(() -> {
                while (isRunning) {
                    try {
                        Integer task = getTask();
                        if (task != null) {
                            addResult(task, compute(task));
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                System.out.println(Thread.currentThread().getName() + " finished");
            });
            thread.start();
            threads.add(thread);
        }

        Scanner scanner = new Scanner(System.in);
        while (isRunning) {
            System.out.print("Enter a number (or type 'q' to exit): ");
            String input = scanner.nextLine();
            if (input.equals("q")) {
                isRunning = false;
                synchronized (this) {
                    notifyAll();
                }
                break;
            }
            try {
                int task = Integer.parseInt(input);
                addTask(task);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input, please enter an integer or 'q'");
            }
        }

        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        System.out.println("Results:");
        for (Map.Entry<Integer, Integer> entry : results.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }
    }

    private Integer compute(int task) throws InterruptedException {
        //find the first prime number greater than the given number
        int prime = task + 1;
        while (!isPrime(prime)) {
            Thread.sleep(300);
            prime++;
        }
        return prime;
    }

    private boolean isPrime(int prime) {
        for (int i = 2; i < prime; i++) {
            if (prime % i == 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        int numThreads = Integer.parseInt(args[0]);
        App computation = new App(numThreads);
        computation.start();
    }
}