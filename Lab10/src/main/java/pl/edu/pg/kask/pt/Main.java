package pl.edu.pg.kask.pt;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;

import java.util.List;
import java.util.Scanner;

public class Main {

    private static final EntityManagerFactory emf = Persistence.createEntityManagerFactory("Lab10PU");

    public static void main(String[] args) {
        initializeTestData();

        Scanner input = new Scanner(System.in);
        boolean exit = false;

        while (!exit) {
            System.out.println("Choose an option:");
            System.out.println("1. Add mage");
            System.out.println("2. Add tower");
            System.out.println("3. Remove mage");
            System.out.println("4. Remove tower");
            System.out.println("5. Show all database");
            System.out.println("6. Advanced queries");
            System.out.println("7. Exit");

            try {
                int option = input.nextInt();
                input.nextLine();
                switch (option) {
                    case 1 -> addMage(input);
                    case 2 -> addTower(input);
                    case 3 -> deleteMage(input);
                    case 4 -> deleteTower(input);
                    case 5 -> showAllDatabase();
                    case 6 -> advancedQueries(input);
                    case 7 -> exit = true;
                    default -> System.out.println("ERROR: Invalid option, try again.");
                }
            } catch (Exception e) {
                System.out.println("ERROR: Input error, try again.");
                input.nextLine();
            }
        }
        emf.close();
    }

    private static void initializeTestData() {
        try (EntityManager em = emf.createEntityManager()) {

            em.getTransaction().begin();

            Tower tower1 = new Tower("Black Tower", 100);
            Tower tower2 = new Tower("White Tower", 200);

            Mage mage1 = new Mage("Gandalf", 20, tower1);
            Mage mage2 = new Mage("Sauron", 30, tower1);
            Mage mage3 = new Mage("Harry Potter", 205, tower2);

            em.persist(tower1);
            em.persist(tower2);
            em.persist(mage1);
            em.persist(mage2);
            em.persist(mage3);

            em.getTransaction().commit();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }


    private static void addTower(Scanner input) {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("Enter tower name:");
            String towerName = input.nextLine();
            System.out.println("Enter tower height:");
            int towerHeight = input.nextInt();
            em.getTransaction().begin();
            Tower tower = new Tower(towerName, towerHeight);
            em.persist(tower);
            em.getTransaction().commit();
            System.out.println("SUCCESS: Tower added");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

    }

    private static void addMage(Scanner input) {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("Enter mage name:");
            String mageName = input.nextLine();
            System.out.println("Enter mage level:");
            int mageLevel = input.nextInt();
            input.nextLine();
            System.out.println("Enter tower name (optional):");
            String towerName = input.nextLine();
            em.getTransaction().begin();
            Tower tower = em.find(Tower.class, towerName);
            if (tower == null && !towerName.isEmpty()) {
                System.out.println("ERROR: Tower not found");
                return;
            }
            Mage mage = new Mage(mageName, mageLevel, tower);
            em.persist(mage);
            em.getTransaction().commit();
            System.out.println("SUCCESS: Mage added");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static void deleteMage(Scanner input) {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("Enter mage name:");
            String mageName = input.nextLine();
            em.getTransaction().begin();
            Mage mage = em.find(Mage.class, mageName);
            em.remove(mage);
            em.getTransaction().commit();
            System.out.println("SUCCESS: Mage deleted");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static void deleteTower(Scanner input) {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("Enter tower name:");
            String towerName = input.nextLine();
            em.getTransaction().begin();
            em.createQuery("UPDATE Mage m SET m.tower = NULL WHERE m.tower.name = :towerName")
                    .setParameter("towerName", towerName)
                    .executeUpdate();
            Tower tower = em.find(Tower.class, towerName);
            em.remove(tower);
            em.getTransaction().commit();
            System.out.println("SUCCESS: Tower deleted");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }


    private static void showAllDatabase() {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("---");
            List<Tower> towers = em.createQuery("SELECT t FROM Tower t", Tower.class).getResultList();
            for (Tower tower : towers) {
                System.out.println(tower);
                for (Mage mage : tower.getMages()) {
                    System.out.println("- " + mage);
                }
            }
            List<Mage> mages = em.createQuery("SELECT m FROM Mage m WHERE m.tower IS NULL", Mage.class).getResultList();
            for (Mage mage : mages) {
                System.out.println(mage);
            }
            System.out.println("---");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static void advancedQueries(Scanner input) {
        boolean exit = false;

        while (!exit) {
            System.out.println("Choose an option:");
            System.out.println("1. Show all mages with level higher than");
            System.out.println("2. Show all towers with height lower than");
            System.out.println("3. Show all mages with level higher than tower height");
            System.out.println("4. Exit");

            try {
                int option = input.nextInt();
                input.nextLine();
                switch (option) {
                    case 1 -> showMagesWithLevelHigherThan(input);
                    case 2 -> showTowersWithHeightLowerThan(input);
                    case 3 -> showMagesWithLevelHigherThanTowerHeight();
                    case 4 -> exit = true;
                    default -> System.out.println("ERROR: Invalid option, try again.");
                }
            } catch (Exception e) {
                System.out.println("ERROR: Input error, try again.");
                input.nextLine();
            }


        }

    }

    private static void showMagesWithLevelHigherThan(Scanner input) {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("Enter level:");
            int level = input.nextInt();
            input.nextLine();
            List<Mage> mages = em.createQuery("SELECT m FROM Mage m WHERE m.level > :level", Mage.class)
                    .setParameter("level", level)
                    .getResultList();
            System.out.println("---");
            for (Mage mage : mages) {
                System.out.println(mage);
            }
            System.out.println("---");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static void showTowersWithHeightLowerThan(Scanner input) {
        try (EntityManager em = emf.createEntityManager()) {
            System.out.println("Enter height:");
            int height = input.nextInt();
            input.nextLine();
            List<Tower> towers = em.createQuery("SELECT t FROM Tower t WHERE t.height < :height", Tower.class)
                    .setParameter("height", height)
                    .getResultList();
            System.out.println("---");
            for (Tower tower : towers) {
                System.out.println(tower);
            }
            System.out.println("---");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static void showMagesWithLevelHigherThanTowerHeight() {
        try (EntityManager em = emf.createEntityManager()) {
            List<Mage> mages = em.createQuery("SELECT m FROM Mage m WHERE m.level > m.tower.height", Mage.class)
                    .getResultList();
            System.out.println("---");
            for (Mage mage : mages) {
                System.out.println(mage + " - " + mage.getTower());
            }
            System.out.println("---");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}