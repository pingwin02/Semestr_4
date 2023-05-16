package pl.edu.pg.kask.pt;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

public class MageControllerTest {
    private MageController controller;
    private MageRepository repository;

    @BeforeEach
    public void setUp() {
        repository = mock(MageRepository.class);
        controller = new MageController(repository);
    }

    @Test
    public void Should_ReturnDone_When_DeleteExistingEntity() {
        //when
        doNothing().when(repository).delete("ExistingMage");

        //then
        assertEquals("done", controller.delete("ExistingMage"));

    }

    @Test
    public void Should_ReturnNotFound_When_DeleteNonExistingEntity() {
        // when
        doThrow(new IllegalArgumentException()).when(repository).delete("NonExistingMage");

        // then
        assertEquals("not found", controller.delete("NonExistingMage"));
    }

    @Test
    public void Should_ReturnNotFound_When_FindNonExistingEntity() {
        // when
        when(repository.find("NonExistingMage")).thenReturn(Optional.empty());

        // then
        assertEquals("not found", controller.find("NonExistingMage"));
    }

    @Test
    public void Should_ReturnStringRepresentation_When_FindExistingEntity() {
        // when
        when(repository.find("ExistingMage")).thenReturn(Optional.of(new Mage("ExistingMage", 1)));

        // then
        assertEquals("Mage{name='ExistingMage', level=1}", controller.find("ExistingMage"));
    }

    @Test
    public void Should_ReturnDone_When_SaveNewEntity() {
        //when
        doNothing().when(repository).save(any(Mage.class));

        // then
        assertEquals("done", controller.save("NewMage", "1"));
    }

    @Test
    public void Should_ReturnBadRequest_When_SaveExistingEntity() {
        // when
        doThrow(new IllegalArgumentException()).when(repository).save(any(Mage.class));

        // then
        assertEquals("bad request", controller.save("ExistingMage", "1"));
    }


}
