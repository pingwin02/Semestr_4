package pl.edu.pg.pr;

public class Main {
    public static void main(String[] args) {
        Magazyn magazyn = new Magazyn(3, 10);

        Producent[] producenci = new Producent[2];
        Konsument[] konsumenci = new Konsument[2];

        for (int i = 0; i < producenci.length; i++) {
            producenci[i] = new Producent(magazyn, i);
            producenci[i].start();
        }

        for (int i = 0; i < konsumenci.length; i++) {
            konsumenci[i] = new Konsument(magazyn, i);
            konsumenci[i].start();
        }

        for (int i = 0; i < producenci.length; i++) {
            try {
                producenci[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}