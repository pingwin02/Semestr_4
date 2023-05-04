package pl.edu.pg.kask.pt;

import jakarta.persistence.*;
import lombok.*;

@Entity
public class Mage {
    @Id
    @Getter
    @Setter
    private String name;
    @Getter
    @Setter
    private int level;
    @Getter
    @Setter
    @ManyToOne
    private Tower tower;

    @Override
    public String toString() {
        return "Mage{" +
                "name='" + name + '\'' +
                ", level=" + level +
                '}';
    }
}
