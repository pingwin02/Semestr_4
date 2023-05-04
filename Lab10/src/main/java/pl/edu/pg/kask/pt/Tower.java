package pl.edu.pg.kask.pt;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
public class Tower {
    @Id
    @Getter
    @Setter
    private String name;
    @Getter
    @Setter
    private int height;
    @Getter
    @Setter
    @OneToMany(mappedBy = "tower")
    private List<Mage> mages;

    @Override
    public String toString() {
        return "Tower{" +
                "name='" + name + '\'' +
                ", height=" + height +
                '}';
    }
}
