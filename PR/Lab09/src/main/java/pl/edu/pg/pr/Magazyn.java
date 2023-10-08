package pl.edu.pg.pr;

public class Magazyn {
    private int[] produkty;
    private final int pojemnosc;

    public Magazyn(int iloscProduktow, int pojemnosc) {
        produkty = new int[iloscProduktow];
        this.pojemnosc = pojemnosc;
    }

    public boolean dodajProdukt(int index, int ilosc) {
        if (produkty[index] + ilosc > pojemnosc) {
            return false;
        } else {
            produkty[index] += ilosc;
            return true;
        }
    }

    public boolean usunProdukt(int index, int ilosc) {
        if (produkty[index] - ilosc < 0) {
            return false;
        } else {
            produkty[index] -= ilosc;
            return true;
        }
    }

    public synchronized void wypiszStan() {
        for (int i = 0; i < produkty.length; i++) {
            System.out.println("Produkt " + i + ": " + produkty[i] + "/" + pojemnosc);
        }
    }

    public int getIloscProduktow() {
        return produkty.length;
    }

    public int getIloscProduktu(int index) {
        return produkty[index];
    }

    public int getPojemnosc() {
        return pojemnosc;
    }
}
