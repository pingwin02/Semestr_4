package pl.edu.pg.pr;

public class Konsument extends Thread {

    private final Magazyn magazyn;
    private final int id;

    public Konsument(Magazyn magazyn, int id) {
        this.magazyn = magazyn;
        this.id = id;
    }

    public void run() {
        while (true) {
            try {
                int sleepTime = (int) (Math.random() * 5000 + 3000);
                Thread.sleep(sleepTime);
                int indexProduktu = (int) (Math.random() * magazyn.getIloscProduktow());
                int ilosc = (int) (Math.random() * (magazyn.getIloscProduktu(indexProduktu) / 2)) + 1;
                if (magazyn.usunProdukt(indexProduktu, ilosc)) {
                    System.out.println("Konsument " + id + " kupił produkt " + indexProduktu
                            + ". produkt x" + ilosc);
                    magazyn.wypiszStan();
                } else {
                    System.out.println("Konsument " + id + " nie kupił produktu " + indexProduktu
                            + ". produktu x" + ilosc);
                }

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
