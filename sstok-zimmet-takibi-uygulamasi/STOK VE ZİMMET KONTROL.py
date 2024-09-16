import json
import os

class Urun:
    def __init__(self, urun_kodu='', urun_adi='', kategori='', fiyat=0, stok_miktari=0, min_stok=0):
        self.urun_kodu = urun_kodu
        self.urun_adi = urun_adi
        self.kategori = kategori
        self.fiyat = fiyat
        self.stok_miktari = stok_miktari
        self.min_stok = min_stok
        self.satis_gecmisi = []

    def stok_ekle(self, miktar):
        self.stok_miktari += miktar
        print(f"{self.urun_adi} stoğu güncellendi. Yeni stok: {self.stok_miktari}")

    def stok_azalt(self, miktar):
        if miktar > self.stok_miktari:
            print(f"Yeterli stok yok! Mevcut stok: {self.stok_miktari}")
        else:
            self.stok_miktari -= miktar
            self.satis_gecmisi.append(miktar)
            print(f"{miktar} adet {self.urun_adi} satıldı. Kalan stok: {self.stok_miktari}")

    def stok_durumunu_kontrol_et(self):
        if self.stok_miktari <= self.min_stok:
            print(f"UYARI: {self.urun_adi} stok seviyesi kritik! (Stok: {self.stok_miktari})")

    def to_dict(self):
        return {
            "urun_kodu": self.urun_kodu,
            "urun_adi": self.urun_adi,
            "kategori": self.kategori,
            "fiyat": self.fiyat,
            "stok_miktari": self.stok_miktari,
            "min_stok": self.min_stok,
            "satis_gecmisi": self.satis_gecmisi
        }

    @staticmethod
    def from_dict(data):
        urun = Urun(
            data.get('urun_kodu', ''),
            data.get('urun_adi', ''),
            data.get('kategori', ''),
            data.get('fiyat', 0),
            data.get('stok_miktari', 0),
            data.get('min_stok', 0)
        )
        urun.satis_gecmisi = data.get('satis_gecmisi', [])
        return urun

class Depo:
    def __init__(self, depo_adi):
        self.depo_adi = depo_adi
        self.urunler = {}

    def urun_ekle(self, urun):
        self.urunler[urun.urun_kodu] = urun
        print(f"{urun.urun_adi} {self.depo_adi} deposuna eklendi.")

    def stok_guncelle(self, urun_kodu, miktar):
        if urun_kodu in self.urunler:
            self.urunler[urun_kodu].stok_ekle(miktar)
            self.kaydet()
        else:
            print(f"{urun_kodu} {self.depo_adi} deposunda bulunmuyor.")

    def stok_azalt(self, urun_kodu, miktar):
        if urun_kodu in self.urunler:
            self.urunler[urun_kodu].stok_azalt(miktar)
            self.kaydet()
        else:
            print(f"{urun_kodu} {self.depo_adi} deposunda bulunmuyor.")

    def urun_listele(self):
        if not self.urunler:
            print(f"\n{self.depo_adi} deposunda ürün bulunmuyor.")
            return
        print(f"\n{self.depo_adi} deposundaki ürünler:")
        for urun in self.urunler.values():
            print(f"- {urun.urun_adi}: {urun.stok_miktari} adet ({urun.fiyat} TL)")

    def kritik_stok_kontrol(self):
        if not self.urunler:
            print(f"\n{self.depo_adi} deposunda kontrol edilecek ürün bulunmuyor.")
            return
        print(f"\n{self.depo_adi} deposundaki kritik stok seviyesindeki ürünler:")
        for urun in self.urunler.values():
            urun.stok_durumunu_kontrol_et()

    def urun_arama(self, urun_adi):
        bulunan_urunler = [urun for urun in self.urunler.values() if urun_adi.lower() in urun.urun_adi.lower()]
        if bulunan_urunler:
            for urun in bulunan_urunler:
                print(f"{urun.urun_adi} bulundu: {urun.stok_miktari} adet stokta.")
            return bulunan_urunler
        print(f"{urun_adi} {self.depo_adi} deposunda bulunamadı.")
        return None

    def to_dict(self):
        return {
            "depo_adi": self.depo_adi,
            "urunler": {k: v.to_dict() for k, v in self.urunler.items()}
        }

    @staticmethod
    def from_dict(data):
        depo = Depo(data['depo_adi'])
        depo.urunler = {k: Urun.from_dict(v) for k, v in data['urunler'].items()}
        return depo

    def kaydet(self):
        with open(f'{self.depo_adi}.json', 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @staticmethod
    def yukle(depo_adi):
        if os.path.exists(f'{depo_adi}.json'):
            with open(f'{depo_adi}.json', 'r') as file:
                data = json.load(file)
                return Depo.from_dict(data)
        return Depo(depo_adi)

class Tedarikci:
    def __init__(self, tedarikci_adi='', urunler=[]):
        self.tedarikci_adi = tedarikci_adi
        self.urunler = urunler

    def tedarikci_bilgisi(self):
        print(f"\nTedarikçi: {self.tedarikci_adi}")
        print("Sağlanan ürünler:")
        for urun in self.urunler:
            print(f"- {urun}")

    def to_dict(self):
        return {
            "tedarikci_adi": self.tedarikci_adi,
            "urunler": self.urunler
        }

    @staticmethod
    def from_dict(data):
        return Tedarikci(data.get('tedarikci_adi', ''), data.get('urunler', []))

class Siparis:
    def __init__(self, musteri_adi='', urun=None, miktar=0, durum="Hazırlanıyor"):
        self.musteri_adi = musteri_adi
        self.urun = urun
        self.miktar = miktar
        self.durum = durum

    def siparis_bilgisi(self):
        print(f"\nSipariş Bilgisi: {self.musteri_adi} - {self.miktar} adet {self.urun.urun_adi} ({self.durum})")

    def to_dict(self):
        return {
            "musteri_adi": self.musteri_adi,
            "urun": self.urun.to_dict() if self.urun else {},
            "miktar": self.miktar,
            "durum": self.durum
        }

    @staticmethod
    def from_dict(data):
        urun = Urun.from_dict(data.get('urun', {}))
        return Siparis(data.get('musteri_adi', ''), urun, data.get('miktar', 0), data.get('durum', 'Hazırlanıyor'))

class StokYonetimSistemi:
    def __init__(self):
        self.depolar = {}
        self.tedarikciler = []
        self.siparisler = []

    def depo_ekle(self, depo):
        self.depolar[depo.depo_adi] = depo
        print(f"{depo.depo_adi} başarıyla eklendi.")

    def tedarikci_ekle(self, tedarikci):
        self.tedarikciler.append(tedarikci)
        print(f"{tedarikci.tedarikci_adi} başarıyla eklendi.")

    def siparis_ekle(self, siparis):
        self.siparisler.append(siparis)
        print(f"Sipariş başarıyla oluşturuldu: {siparis.musteri_adi} - {siparis.urun.urun_adi} ({siparis.miktar} adet)")

    def tum_urunleri_listele(self):
        if not self.depolar:
            print("\nSistemde depo bulunmuyor.")
            return
        for depo in self.depolar.values():
            depo.urun_listele()

    def kritik_stoklari_kontrol_et(self):
        if not self.depolar:
            print("\nSistemde depo bulunmuyor.")
            return
        for depo in self.depolar.values():
            depo.kritik_stok_kontrol()

    def tum_siparisleri_listele(self):
        if not self.siparisler:
            print("\nSipariş bulunmuyor.")
            return
        print("\nTüm Siparişler:")
        for siparis in self.siparisler:
            siparis.siparis_bilgisi()

    def menu(self):
        while True:
            print("\nStok Yönetim Sistemi Menüsü:")
            print("1. Depo Ekle")
            print("2. Ürün Ekle")
            print("3. Stok Güncelle")
            print("4. Stok Azalt")
            print("5. Ürün Listele")
            print("6. Kritik Stokları Kontrol Et")
            print("7. Sipariş Ekle")
            print("8. Siparişleri Listele")
            print("9. Çıkış")
            
            secim = input("Bir seçenek girin (1-9): ")
            
            if secim == '1':
                depo_adi = input("Depo adı: ")
                depo = Depo(depo_adi)
                self.depo_ekle(depo)
            elif secim == '2':
                depo_adi = input("Ürünü ekleyeceğiniz depo adı: ")
                urun_kodu = input("Ürün kodu: ")
                urun_adi = input("Ürün adı: ")
                kategori = input("Kategori: ")
                fiyat = float(input("Fiyat: "))
                stok_miktari = int(input("Stok miktarı: "))
                min_stok = int(input("Minimum stok: "))
                urun = Urun(urun_kodu, urun_adi, kategori, fiyat, stok_miktari, min_stok)
                depo = self.depolar.get(depo_adi)
                if depo:
                    depo.urun_ekle(urun)
                else:
                    print("Depo bulunamadı.")
            elif secim == '3':
                depo_adi = input("Stok güncelleyeceğiniz depo adı: ")
                urun_kodu = input("Ürün kodu: ")
                miktar = int(input("Eklemek istediğiniz miktar: "))
                depo = self.depolar.get(depo_adi)
                if depo:
                    depo.stok_guncelle(urun_kodu, miktar)
                else:
                    print("Depo bulunamadı.")
            elif secim == '4':
                depo_adi = input("Stok azaltacağınız depo adı: ")
                urun_kodu = input("Ürün kodu: ")
                miktar = int(input("Azaltmak istediğiniz miktar: "))
                depo = self.depolar.get(depo_adi)
                if depo:
                    depo.stok_azalt(urun_kodu, miktar)
                else:
                    print("Depo bulunamadı.")
            elif secim == '5':
                depo_adi = input("Ürünleri listelemek istediğiniz depo adı: ")
                depo = self.depolar.get(depo_adi)
                if depo:
                    depo.urun_listele()
                else:
                    print("Depo bulunamadı.")
            elif secim == '6':
                self.kritik_stoklari_kontrol_et()
            elif secim == '7':
                musteri_adi = input("Müşteri adı: ")
                depo_adi = input("Ürünü alacağınız depo adı: ")
                urun_kodu = input("Ürün kodu: ")
                miktar = int(input("Sipariş miktarı: "))
                depo = self.depolar.get(depo_adi)
                if depo:
                    urun = depo.urunler.get(urun_kodu)
                    if urun:
                        siparis = Siparis(musteri_adi, urun, miktar)
                        self.siparis_ekle(siparis)
                    else:
                        print("Ürün bulunamadı.")
                else:
                    print("Depo bulunamadı.")
            elif secim == '8':
                self.tum_siparisleri_listele()
            elif secim == '9':
                print("Çıkış yapılıyor...")
                break
            else:
                print("Geçersiz seçenek. Lütfen 1-9 arasında bir seçim yapın.")

if __name__ == "__main__":
    sistem = StokYonetimSistemi()
    
    while True:
        sistem.menu()