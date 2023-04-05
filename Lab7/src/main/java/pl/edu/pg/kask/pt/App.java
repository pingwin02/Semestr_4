package pl.edu.pg.kask.pt;

import java.util.*;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) {

        if (args.length != 1) {
            System.out.println("Usage: App <mode>");
            System.exit(1);
        }
        String mode = args[0];
        Set<Mage> mages = null;

        switch (mode) {
            case "0" -> mages = new HashSet<>(); //no sorting
            case "1" -> mages = new TreeSet<>(); //default sorting
            case "2" -> mages = new TreeSet<>(new LevelComparator()); //alternative sorting
            default -> {
                System.out.println("Unknown mode: " + mode);
                System.exit(1);
            }
        }

        Mage mage1 = new Mage("Harry", 10, 999);
        Mage mage2 = new Mage("Hermiona", 8, 14);
        Mage mage3 = new Mage("Ron", 9, 45);
        Mage mage4 = new Mage("Draco", 11, 15);
        Mage mage5 = new Mage("Voldemort", 10, 97);
        Mage mage6 = new Mage("Dumbledore", 50, 15);
        Mage mage7 = new Mage("Snape", 15, 41);
        Mage mage8 = new Mage("Hagrid", 20, 50);
        Mage mage9 = new Mage("Dobby", 24, 54);
        Mage mage10 = new Mage("Bellatrix", 21, 12);

        mage5.addAprentices(new HashSet<>(Arrays.asList(mage4, mage6)));
        mage6.addAprentices(new HashSet<>(Arrays.asList(mage1, mage2, mage3)));
        mage7.addAprentices(new HashSet<>(Arrays.asList(mage9, mage10)));

        mages.add(mage5);
        mages.add(mage7);

        Mage.printMages(mages, 0);
    }
}
