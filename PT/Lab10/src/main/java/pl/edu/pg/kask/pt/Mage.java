package pl.edu.pg.kask.pt;

import jakarta.persistence.*;
import lombok.*;

@Entity
@NoArgsConstructor
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

    public Mage(String name, int level, Tower tower) {
        this.name = name;
        this.level = level;
        this.tower = tower;
    }

    @Override
    public String toString() {
        return "Mage{" +
                "name='" + name + '\'' +
                ", level=" + level +
                '}';
    }
}
