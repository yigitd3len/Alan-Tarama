import math
import time
import matplotlib.pyplot as plt

class AlanTaramaSimulasyonu:
    def __init__(self, yatay_fov=60, dikey_fov=45):
        self.yatay_fov_yarim = math.radians(yatay_fov) / 2
        self.dikey_fov_yarim = math.radians(dikey_fov) / 2
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def koordinat_bul(self, irtifa, kamera_acisi_derece):
        limit = 90 - math.degrees(self.dikey_fov_yarim)
        if kamera_acisi_derece >= limit:
            return None
        
        theta = math.radians(kamera_acisi_derece)
        aci_yakin = theta - self.dikey_fov_yarim
        aci_uzak  = theta + self.dikey_fov_yarim

        y_yakin = irtifa * math.tan(aci_yakin)
        y_uzak  = irtifa * math.tan(aci_uzak)

        hipotenus_yakin = irtifa / math.cos(aci_yakin)
        hipotenus_uzak  = irtifa / math.cos(aci_uzak)

        w_yakin = 2 * hipotenus_yakin * math.tan(self.yatay_fov_yarim)
        w_uzak  = 2 * hipotenus_uzak  * math.tan(self.yatay_fov_yarim)

        koordinatlar = {
            "sol_on":   (-w_yakin/2, y_yakin),
            "sag_on":   ( w_yakin/2, y_yakin),
            "sag_arka": ( w_uzak/2,  y_uzak),
            "sol_arka": (-w_uzak/2,  y_uzak),
            
            "alt_taban": w_yakin,
            "ust_taban": w_uzak,
            "yukseklik_yer": y_uzak - y_yakin
        }
        return koordinatlar

    
    
    def alan_hesapla(self, veri):
        if veri is None:
            return 0
        
        a = veri["alt_taban"]
        b = veri["ust_taban"]
        h = veri["yukseklik_yer"]

        alan = ((a + b) / 2) * h
        return round(alan, 2)
    
    def gorsellestir(self, veri, alan, irtifa):
        if veri is None: return

        x = [veri["sol_on"][0], veri["sag_on"][0], veri["sag_arka"][0], veri["sol_arka"][0], veri["sol_on"][0]]
        y = [veri["sol_on"][1], veri["sag_on"][1], veri["sag_arka"][1], veri["sol_arka"][1], veri["sol_on"][1]]

        self.ax.clear()
        self.ax.fill(x, y, 'r', alpha=0.3)
        self.ax.plot(x, y, 'b-')

        self.ax.set_title(f"İrtifa: {irtifa}m | Alan: {alan} m²")
        self.ax.set_xlabel("Yatay Genişlik (m)")
        self.ax.set_ylabel("İleri Mesafe (m)")
        self.ax.grid(True)
        self.ax.set_aspect('equal')

        self.ax.plot(0, 0, 'ko', label="Uçak (İzdüşüm)")
        self.ax.legend()

        plt.draw()
        plt.pause(0.1)

    def baslat(self):
        print("Alan Tarama Simülasyonu Başladı.")
        print("Çıkmak için Ctrl+C tuşlarına basın.")

        irtifa = 50
        pitch_acisi = 30

        try:
            while irtifa <= 300:
                koordinatlar = self.koordinat_bul(irtifa, pitch_acisi)
                alan = self.alan_hesapla(koordinatlar)
                print(f"İrtifa: {irtifa}m | Açı: {pitch_acisi}° | Alan: {alan} m²")
                self.gorsellestir(koordinatlar, alan, irtifa)

                irtifa += 2
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Simülasyon durduruldu.")
        print("Simülasyon sona erdi.")
        plt.show(block=True)

if __name__ == "__main__":
    simülasyon = AlanTaramaSimulasyonu()
    simülasyon.baslat()