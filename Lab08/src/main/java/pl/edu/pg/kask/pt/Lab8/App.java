package pl.edu.pg.kask.pt.Lab8;

import java.util.*;

public class App {
    private final Queue<Job> tasks = new LinkedList<>();
    private final List<Double> results = new LinkedList<>();
    private final List<Thread> threads = new LinkedList<>();
    private final int numThreads;

    private int taskID = 0;

    public App(int numThreads) {
        this.numThreads = numThreads;
    }

    public synchronized void addTask(Job task) {
        tasks.offer(task);
        notifyAll();
    }

    public synchronized Job getTask() throws InterruptedException {
        while (tasks.isEmpty()) wait();
        return tasks.poll();
    }

    public synchronized void addResult(double result) {
        results.add(result);
    }

    public void start() {
        for (int i = 0; i < numThreads; i++) {
            Thread thread = new Thread(() -> {
                while (!Thread.interrupted()) {
                    try {
                        Job task = getTask();
                        compute(task);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
            thread.start();
            threads.add(thread);
        }

        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print("Enter a number (or type 'q' to exit): ");
            String input = scanner.nextLine();
            if (input.equals("q")) {
                for (Thread thread : threads) {
                    thread.interrupt();
                }
                break;
            }
            try {
                int iter = Integer.parseInt(input);
                addTask(new Job(taskID++, iter));
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

    }

    private void compute(Job task) {
        System.out.println("\nResult of Task " + task.id + ": " + task.calcPi() + " after " + task.count + " iterations");
        addResult(task.result);
    }

    public static void main(String[] args) {
        int numThreads = Integer.parseInt(args[0]);
        App computation = new App(numThreads);
        computation.start();
    }
}