package pl.edu.pg.kask.pt.Lab8;

import static java.lang.Math.pow;

public class Job {
    public final int id;
    public final int iterations;
    public double result = 0;

    public int count = 0;

    public Job(int id, int iterations) {
        this.id = id;
        this.iterations = iterations;
    }

    public double calcPi() {
        for (int i = 1; i <= iterations; i++) {
            result += 4 * pow(-1, i - 1) / (2*i - 1);
            count++;
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return result;
            }
        }

        return result;
    }
}
