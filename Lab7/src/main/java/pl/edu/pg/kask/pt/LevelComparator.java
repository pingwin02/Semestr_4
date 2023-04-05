package pl.edu.pg.kask.pt;

import java.util.Comparator;

public class LevelComparator implements Comparator<Mage> {
    @Override
    public int compare(Mage o1, Mage o2) {
        //level then name then power
        int result = Integer.compare(o1.getLevel(), o2.getLevel());
        if (result == 0) {
            result = o1.getName().compareTo(o2.getName());
        }
        if (result == 0) {
            result = Double.compare(o1.getPower(), o2.getPower());
        }
        return result;
    }
}
