package pl.edu.pg.kask.pt;

import java.util.*;

public class Mage implements Comparable<Mage> {
    private String name;
    private int level;
    private double power;
    private Set<Mage> apprentices;

    public Mage(String name, int level, double power) {
        this.name = name;
        this.level = level;
        this.power = power;
    }

    public void addAprentices(Set<Mage> apprentices) {
        this.apprentices = apprentices;
    }

    public String getName() {
        return name;
    }

    public int getLevel() {
        return level;
    }

    public double getPower() {
        return power;
    }

    public Set<Mage> getApprentices() {
        return apprentices;
    }

    public static void printMages(Set<Mage> mages, int depth) {
        for (Mage mage : mages) {
            for (int i = 0; i <= depth; i++) {
                System.out.print("-");
            }
            System.out.println(mage);
            if (mage.getApprentices() != null) {
                printMages(mage.getApprentices(), depth + 1);
            }
        }
    }

    @Override
    public String toString() {
        return "Mage{ name='" + name + "', level=" + level + ", power=" + power + "}";
    }

    @Override
    public int compareTo(Mage o) {
        int result = this.name.compareTo(o.name);
        if (result == 0) {
            result = Integer.compare(this.level, o.level);
        }
        if (result == 0) {
            result = Double.compare(this.power, o.power);
        }
        return result;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Mage mage = (Mage) o;
        return level == mage.level &&
                Double.compare(mage.power, power) == 0 &&
                Objects.equals(name, mage.name) &&
                Objects.equals(apprentices, mage.apprentices);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, level, power, apprentices);
    }
}
