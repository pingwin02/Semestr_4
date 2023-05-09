package pl.edu.pg.kask.pt;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
@NoArgsConstructor
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

    public Tower(String name, int height) {
        this.name = name;
        this.height = height;
    }

    @Override
    public String toString() {
        return "Tower{" +
                "name='" + name + '\'' +
                ", height=" + height +
                '}';
    }
}
