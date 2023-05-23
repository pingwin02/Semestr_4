package pl.edu.pg.pr;

public class Producent extends Thread {
    private final Magazyn magazyn;
    private final int id;

    public Producent(Magazyn magazyn, int id) {
        this.magazyn = magazyn;
        this.id = id;
    }

    public void run() {
        while (true) {
            try {
                int sleepTime = (int) (Math.random() * 5000 + 3000);
                Thread.sleep(sleepTime);
                int indexProduktu = (int) (Math.random() * magazyn.getIloscProduktow());
                int ilosc = (int) (Math.random() * (magazyn.getPojemnosc() / 2)) + 1;
                if (magazyn.dodajProdukt(indexProduktu, ilosc)) {
                    System.out.println("Producent " + id + " wyprodukował " + indexProduktu
                            + ". produkt x" + ilosc);
                    magazyn.wypiszStan();
                } else {
                    System.out.println("Producent " + id + " nie wyprodukował " + indexProduktu
                            + ". produktu x" + ilosc + ".");
                }

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
