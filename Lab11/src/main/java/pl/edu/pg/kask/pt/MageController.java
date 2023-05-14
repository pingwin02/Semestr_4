package pl.edu.pg.kask.pt;

import java.util.Optional;

public class MageController {
    private final MageRepository repository;

    public MageController(MageRepository repository) {
        this.repository = repository;
    }

    public String find(String name) {
        Optional<Mage> mageOptional = repository.find(name);
        if (mageOptional.isPresent()) {
            Mage mage = mageOptional.get();
            return mage.toString();
        } else {
            return "not found";
        }
    }

    public String delete(String name) {
        try {
            repository.delete(name);
            return "done";
        } catch (IllegalArgumentException e) {
            return "not found";
        }
    }

    public String save(String name, String level) {
        try {
            repository.save(new Mage(name, Integer.parseInt(level)));
            return "done";
        } catch (IllegalArgumentException e) {
            return "bad request";
        }
    }
}
