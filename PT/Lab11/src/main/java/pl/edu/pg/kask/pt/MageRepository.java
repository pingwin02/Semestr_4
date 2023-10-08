package pl.edu.pg.kask.pt;

import java.util.Collection;
import java.util.HashSet;
import java.util.Optional;

public class MageRepository {
    private Collection<Mage> collection = new HashSet<>();

    public Optional<Mage> find(String name) {
        return collection.stream()
                .filter(mage -> mage.getName().equals(name))
                .findFirst();
    }

    public void delete(String name) {
        boolean removed = collection.removeIf(mage -> mage.getName().equals(name));
        if (!removed) {
            throw new IllegalArgumentException("No such mage with name: " + name);
        }
    }

    public void save(Mage mage) {
        if (find(mage.getName()).isPresent()) {
            throw new IllegalArgumentException("Mage with name " + mage.getName() + " already exists in the repository");
        }
        collection.add(mage);
    }
}