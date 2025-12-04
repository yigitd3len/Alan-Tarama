import math

class AlanHesaplayici:
    def __init__(self, yatay_fov_derece=60, dikey_fov_derece=45):
        """
        Kamera özelliklerini burada tanımlıyoruz.
        Örnek: Standart bir drone kamerası 60 derece yatay, 45 derece dikey görür.
        """
        # Dereceleri Radyana çeviriyoruz (Bilgisayar dereceden anlamaz, radyan sever)
        self.yatay_fov_yarim = math.radians(yatay_fov_derece) / 2
        self.dikey_fov_yarim = math.radians(dikey_fov_derece) / 2

    def hesapla(self, irtifa, kamera_acisi):
        """
        PARAMETRELER:
        irtifa (h): Uçağın yerden yüksekliği (Metre cinsinden)
        kamera_acisi (theta): Kameranın dikeyle yaptığı açı.
             0 derece = Tam aşağı bakıyor (Nadir)
             90 derece = Tam karşıya (ufka) bakıyor
        """

        # --- GÜVENLİK KONTROLÜ ---
        # Eğer kamera ufka veya gökyüzüne bakıyorsa alan sonsuz olur, hesaplayamayız.
        # Sınır açısı: 90 dereceden dikey görüş açısının yarısını çıkar.
        limit_acisi = math.degrees(math.pi/2 - self.dikey_fov_yarim)
        
        if kamera_acisi >= limit_acisi:
            return {"hata": "Kamera ufka bakıyor, alan hesaplanamaz (Sonsuz)!"}

        # Açıyı radyana çevir (Hesaplamalar için şart)
        egim_radyan = math.radians(kamera_acisi)

        # --- ADIM 1: İLERİ UZAKLIKLARI HESAPLA (Y EKSENİ) ---
        # Kameranın gördüğü en yakın nokta ve en uzak noktanın uçağın altına olan uzaklığı.
        # Formül: Mesafe = İrtifa * tan(Açı)
        
        aci_yakin = egim_radyan - self.dikey_fov_yarim
        aci_uzak  = egim_radyan + self.dikey_fov_yarim

        # math.tan() içine negatif açı girerse sorun olmaz, arkaya baktığını anlarız.
        dist_yakin = irtifa * math.tan(aci_yakin) 
        dist_uzak  = irtifa * math.tan(aci_uzak)
        
        # Yerdeki şeklin uzunluğu (Trapezoid Height)
        yerdeki_uzunluk = dist_uzak - dist_yakin

        # --- ADIM 2: GENİŞLİKLERİ HESAPLA (X EKSENİ) ---
        # Yamuğun alt (yakın) ve üst (uzak) taban genişlikleri.
        # Uzaktaki kenar her zaman daha geniştir.
        # Formül: Genişlik = 2 * Hipotenüs * tan(Yatay_FOV_Yarim)
        
        # Hipotenüsleri bul (Kameradan o noktaya olan kuş bakışı mesafe değil, gerçek ışın mesafesi)
        # Cosinüs formülü: h / cos(alpha) = hipotenüs
        hipotenus_yakin = irtifa / math.cos(aci_yakin)
        hipotenus_uzak  = irtifa / math.cos(aci_uzak)

        genislik_yakin = 2 * hipotenus_yakin * math.tan(self.yatay_fov_yarim)
        genislik_uzak  = 2 * hipotenus_uzak  * math.tan(self.yatay_fov_yarim)

        # --- ADIM 3: ALAN HESABI (Madde 4.3) ---
        # Yamuk Alanı = (Alt Taban + Üst Taban) / 2 * Yükseklik
        alan_m2 = ((genislik_yakin + genislik_uzak) / 2) * yerdeki_uzunluk

        # Sonuçları paketleyip gönderelim
        return {
            "irtifa": irtifa,
            "kamera_egim": kamera_acisi,
            "alan_m2": round(alan_m2, 2),  # 4.3 Talebi: Alan hesabı
            "yerdeki_uzunluk_m": round(yerdeki_uzunluk, 2),
            "genislik_yakin_m": round(genislik_yakin, 2),
            "genislik_uzak_m": round(genislik_uzak, 2),
            "koordinatlar": { # Görselleştirme ekibi için köşe noktaları
                "yakin_sol": (-genislik_yakin/2, dist_yakin),
                "yakin_sag": ( genislik_yakin/2, dist_yakin),
                "uzak_sag":  ( genislik_uzak/2,  dist_uzak),
                "uzak_sol":  (-genislik_uzak/2,  dist_uzak)
            }
        }

# --- TEST KODU (Projeyi çalıştırmak için burayı kullan) ---
if __name__ == "__main__":
    # Hesaplayıcıyı başlat
    hesap = AlanHesaplayici()

    print("--- SENARYO 1: Uçak 100m'de, Kamera Tam Aşağı Bakıyor ---")
    sonuc1 = hesap.hesapla(irtifa=100, kamera_acisi=0)
    print(f"Alan: {sonuc1['alan_m2']} m² (Beklenen: Dikdörtgen)")

    print("\n--- SENARYO 2: Uçak 100m'de, Kamera 30 Derece İleri Bakıyor ---")
    sonuc2 = hesap.hesapla(irtifa=100, kamera_acisi=30)
    print(f"Alan: {sonuc2['alan_m2']} m² (Beklenen: Daha büyük, Yamuk)") # Madde 4.2 Kanıtı

    print("\n--- SENARYO 3: Uçak 200m'ye Yükseldi (Açı aynı) ---")
    sonuc3 = hesap.hesapla(irtifa=200, kamera_acisi=30)
    print(f"Alan: {sonuc3['alan_m2']} m² (Beklenen: İrtifa artınca alan büyümeli)") # Madde 4.2 Kanıtı