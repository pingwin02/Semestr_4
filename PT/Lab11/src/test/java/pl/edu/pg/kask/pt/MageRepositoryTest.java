package pl.edu.pg.kask.pt;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

public class MageRepositoryTest {
    private MageRepository repository;

    @BeforeEach
    public void setUp() {
        repository = new MageRepository();
    }

    @Test
    public void Should_ThrowIllegalArgumentException_When_DeletingNonExistingEntity() {
        // then
        assertThrows(IllegalArgumentException.class, () -> repository.delete("NonExistingMage"));
    }

    @Test
    public void Should_ReturnEmptyOptional_When_FindingNonExistingEntity() {
        // when
        Optional<Mage> found = repository.find("NonExistingMage");

        // then
        assertFalse(found.isPresent());
    }

    @Test
    public void Should_ReturnOptionalWithEntity_When_FindingExistingEntity() {
        // given
        Mage mage = new Mage("ExistingMage", 5);
        repository.save(mage);

        // when
        Optional<Mage> found = repository.find("ExistingMage");

        // then
        assertTrue(found.isPresent());
        assertEquals(mage, found.get());
    }

    @Test
    public void Should_ThrowIllegalArgumentException_When_SavingExistingEntity() {
        // given
        repository.save(new Mage("ExistingMage", 5));

        // then
        assertThrows(IllegalArgumentException.class, () -> repository.save(new Mage("ExistingMage", 1)));
    }


    @Test
    public void Should_DeleteExistingEntity_When_DeleteExistingEntity() {
        // given
        Mage mage = new Mage("ExistingMage", 5);
        repository.save(mage);

        // when
        repository.delete("ExistingMage");

        // then
        assertFalse(repository.find("ExistingMage").isPresent());
    }

    @Test
    public void Should_SaveNewEntity_When_SaveNewEntity() {
        // given
        Mage mage = new Mage("NewMage", 1);

        // when
        repository.save(mage);

        // then
        Optional<Mage> found = repository.find("NewMage");
        assertTrue(found.isPresent());
        assertEquals(mage, found.get());
    }
}
