package pl.edu.pg.kask.pt;

import java.util.*;

public class Mage implements Comparable<Mage> {
    private final String name;
    private final int level;
    private final double power;
    private Set<Mage> children;

    public Mage(String name, int level, double power) {
        this.name = name;
        this.level = level;
        this.power = power;
    }

    public void addChildren(Set<Mage> children) {
        this.children = children;
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

    public Set<Mage> getChildren() {
        return children;
    }

    public static void printMages(Set<Mage> mages, int depth) {
        for (Mage mage : mages) {
            for (int i = 0; i <= depth; i++) {
                System.out.print("-");
            }
            System.out.println(mage);
            if (mage.getChildren() != null) {
                printMages(mage.getChildren(), depth + 1);
            }
        }
    }

    public static Map<Mage, Integer> countChildren(Set<Mage> mages, String mode) {
        Map<Mage, Integer> result = null;

        switch (mode) {
            case "-no" -> result = new HashMap<>();
            case "-nat" -> result = new TreeMap<>();
            case "-alt" -> result = new TreeMap<>(new LevelComparator());
            default -> {
                System.out.println("Unknown mode: " + mode);
                System.exit(1);
            }
        }

        for (Mage mage : mages) {
            if (mage.getChildren() != null) {
                result.put(mage, mage.getChildren().size());
                result.putAll(countChildren(mage.getChildren(), mode));
            }
        }
        return result;
    }

    @Override
    public String toString() {
        return "Mage{name='" + name + "', level=" + level + ", power=" + power + "}";
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
                Objects.equals(children, mage.children);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, level, power, children);
    }
}
