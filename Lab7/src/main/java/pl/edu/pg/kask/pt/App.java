package pl.edu.pg.kask.pt;

import java.util.*;

public class App {


    public static void main(String[] args) {

        if (args.length != 1) {
            System.out.println("Usage: -no|-nat|-alt");
            System.exit(1);
        }
        String mode = args[0];
        Set<Mage> mages = null;
        Set<Mage> children1 = null;
        Set<Mage> children2 = null;
        Set<Mage> children3 = null;

        switch (mode) {
            case "-no" : {  //no sorting
                mages = new HashSet<>();
                children1 = new HashSet<>();
                children2 = new HashSet<>();
                children3 = new HashSet<>();
                break;
            }
            case "-nat" : {  //default sorting
                mages = new TreeSet<>();
                children1 = new TreeSet<>();
                children2 = new TreeSet<>();
                children3 = new TreeSet<>();
                break;
            }
            case "-alt" : {  //alternative sorting
                mages = new TreeSet<>(new LevelComparator());
                children1 = new TreeSet<>(new LevelComparator());
                children2 = new TreeSet<>(new LevelComparator());
                children3 = new TreeSet<>(new LevelComparator());
                break;
            }
            default : {
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

        children1.add(mage1);
        children1.add(mage2);
        children1.add(mage3);

        children2.add(mage4);
        children2.add(mage6);

        children3.add(mage8);
        children3.add(mage9);
        children3.add(mage10);

        mage5.addChildren(children2);
        mage6.addChildren(children1);
        mage7.addChildren(children3);

        mages.add(mage5);
        mages.add(mage7);

        Mage.printMages(mages, 0);

        System.out.println();

        Mage.countChildren(mages, mode).forEach((mage, integer)
                -> System.out.println(mage + " : " + integer));

    }
}
