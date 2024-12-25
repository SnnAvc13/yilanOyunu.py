import pygame
import random
import math
import time

# Renk sabitleri
class Renkler:
    SIYAH = (0, 0, 0)
    BEYAZ = (255, 255, 255)
    KIRMIZI = (255, 0, 0)
    YESIL = (0, 255, 0)
    ALTIN = (255, 215, 0)

class YemTipi:
    ELMA = 1      # Normal elma: +1 uzunluk, +10 puan
    ALTIN = 2     # Altın elma: +2 uzunluk, +30 puan

class Yilan:
    def __init__(self, tema_adi='Klasik'):
        self.boyut = 20
        self.hiz = 20
        self.pozisyonlar = [(300, 300)]
        self.yon = [self.hiz, 0]
        self.uzunluk = 1
        self.tema_adi = tema_adi
        self.renkler = [(0, 255, 0)]  # Başlangıç rengi
        self.renk_indeks = 0  # Gökkuşağı teması için

    def yeni_parca_rengi(self):
        if self.tema_adi == 'Klasik':
            # Yeşil tonlarında rastgele renk
            g = random.randint(150, 255)
            return (0, g, 0)
        
        elif self.tema_adi == 'Gökkuşağı':
            # Gökkuşağı renkleri
            renkler = [
                (255, 0, 0),    # Kırmızı
                (255, 127, 0),  # Turuncu
                (255, 255, 0),  # Sarı
                (0, 255, 0),    # Yeşil
                (0, 0, 255),    # Mavi
                (75, 0, 130),   # İndigo
                (148, 0, 211)   # Mor
            ]
            self.renk_indeks = (self.renk_indeks + 1) % len(renkler)
            return renkler[self.renk_indeks]
        
        elif self.tema_adi == 'Altın':
            # Altın tonları
            parlaklik = random.randint(200, 255)
            return (parlaklik, int(parlaklik * 0.85), 0)  # Altın efekti
        
        return (0, 255, 0)  # Varsayılan renk

    def hareket(self):
        yeni_x = self.pozisyonlar[0][0] + self.yon[0]
        yeni_y = self.pozisyonlar[0][1] + self.yon[1]
        self.pozisyonlar.insert(0, (yeni_x, yeni_y))
        
        if len(self.pozisyonlar) > len(self.renkler):
            self.renkler.append(self.yeni_parca_rengi())
        
        if len(self.pozisyonlar) > self.uzunluk:
            self.pozisyonlar.pop()
            self.renkler.pop()

    def yon_degistir(self, yeni_yon):
        if (yeni_yon[0] != -self.yon[0]) or (yeni_yon[1] != -self.yon[1]):
            self.yon = yeni_yon

class Yem:
    def __init__(self, genislik, yukseklik):
        self.boyut = 20
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.tip = YemTipi.ELMA
        self.yeni_konum()

    def yeni_konum(self):
        self.x = random.randrange(0, self.genislik, self.boyut)
        self.y = random.randrange(0, self.yukseklik, self.boyut)
        self.tip = random.choices(
            [YemTipi.ELMA, YemTipi.ALTIN],
            weights=[80, 20]  # %80 normal elma, %20 altın elma
        )[0]

    def ciz(self, ekran):
        if self.tip == YemTipi.ELMA:
            pygame.draw.circle(ekran, Renkler.KIRMIZI, 
                             (self.x + self.boyut//2, self.y + self.boyut//2), 
                             self.boyut//2 - 2)
        else:  # ALTIN
            pygame.draw.circle(ekran, Renkler.ALTIN, 
                             (self.x + self.boyut//2, self.y + self.boyut//2), 
                             self.boyut//2 - 2)

class MenuDurum:
    ANA_MENU = 0
    AYARLAR = 1
    OYUN = 2
    OYUN_SONU = 3

class Tema:
    def __init__(self):
        self.arkaplan_temalar = {
            'Klasik Grid': {
                'isim': 'Klasik Grid',
                'tip': 'grid',
                'renk1': (0, 0, 50),  # Koyu mavi
                'renk2': (20, 20, 50)  # Grid çizgi rengi
            },
            'Gece Modu': {
                'isim': 'Gece Modu',
                'tip': 'gradient',
                'renk1': (20, 0, 30),  # Koyu mor
                'renk2': (60, 0, 90)   # Açık mor
            },
            'Matrix': {
                'isim': 'Matrix',
                'tip': 'grid',
                'renk1': (0, 20, 0),   # Koyu yeşil
                'renk2': (0, 50, 0)    # Açık yeşil
            }
        }
        
        self.yilan_temalar = {
            'Klasik': {
                'isim': 'Klasik',
                'kafa_renk': (0, 200, 0),
                'govde_renk': (0, 255, 0)
            },
            'Gökkuşağı': {
                'isim': 'Gökkuşağı',
                'kafa_renk': (255, 0, 0),
                'govde_renk': 'rainbow'
            },
            'Altın': {
                'isim': 'Altın',
                'kafa_renk': (255, 215, 0),
                'govde_renk': (255, 200, 0)
            }
        }
        
        self.secili_arkaplan = 'Klasik Grid'
        self.secili_yilan = 'Klasik'

class Oyun:
    def __init__(self):
        pygame.init()
        self.genislik = 800
        self.yukseklik = 600
        self.ekran = pygame.display.set_mode((self.genislik, self.yukseklik))
        pygame.display.set_caption("Yılan Oyunu")
        self.saat = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.buyuk_font = pygame.font.Font(None, 72)
        self.grid_boyut = 40
        self.tema = Tema()
        self.menu_durum = MenuDurum.ANA_MENU
        self.butonlar = []
        self.buton_olustur()

    def buton_olustur(self):
        # Ana menü butonları
        self.ana_menu_butonlar = [
            {'text': 'Yeni Oyun', 'rect': pygame.Rect(300, 200, 200, 50)},
            {'text': 'Ayarlar', 'rect': pygame.Rect(300, 300, 200, 50)},
            {'text': 'Çıkış', 'rect': pygame.Rect(300, 400, 200, 50)}
        ]
        
        # Ayarlar menüsü butonları
        self.ayarlar_butonlar = [
            {'text': 'Arkaplan: ' + self.tema.secili_arkaplan, 
             'rect': pygame.Rect(250, 150, 300, 50), 'tip': 'arkaplan'},
            {'text': 'Yılan: ' + self.tema.secili_yilan,
             'rect': pygame.Rect(250, 220, 300, 50), 'tip': 'yilan'},
            {'text': 'Başlat', 'rect': pygame.Rect(300, 290, 200, 50), 'tip': 'baslat'},
            {'text': 'Geri', 'rect': pygame.Rect(300, 360, 200, 50)}
        ]

    def buton_ciz(self, buton, secili=False):
        renk = (100, 100, 255) if secili else (60, 60, 150)
        pygame.draw.rect(self.ekran, renk, buton['rect'])
        pygame.draw.rect(self.ekran, (80, 80, 200), buton['rect'], 2)
        
        text = self.font.render(buton['text'], True, (255, 255, 255))
        text_rect = text.get_rect(center=buton['rect'].center)
        self.ekran.blit(text, text_rect)

    def ana_menu_ciz(self):
        # Başlık
        baslik = self.buyuk_font.render('YILAN OYUNU', True, (0, 255, 0))
        baslik_rect = baslik.get_rect(center=(self.genislik//2, 100))
        self.ekran.blit(baslik, baslik_rect)
        
        # Butonlar
        for buton in self.ana_menu_butonlar:
            self.buton_ciz(buton)

    def ayarlar_menu_ciz(self):
        # Başlık
        baslik = self.buyuk_font.render('AYARLAR', True, (0, 255, 0))
        baslik_rect = baslik.get_rect(center=(self.genislik//2, 100))
        self.ekran.blit(baslik, baslik_rect)
        
        # Butonlar
        for buton in self.ayarlar_butonlar:
            self.buton_ciz(buton)

    def menu_kontrol(self):
        while self.menu_durum != MenuDurum.OYUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.menu_durum == MenuDurum.ANA_MENU:
                        for i, buton in enumerate(self.ana_menu_butonlar):
                            if buton['rect'].collidepoint(pos):
                                if i == 0:  # Yeni Oyun
                                    self.menu_durum = MenuDurum.OYUN
                                    self.oyunu_baslat()
                                    return True
                                elif i == 1:  # Ayarlar
                                    self.menu_durum = MenuDurum.AYARLAR
                                elif i == 2:  # Çıkış
                                    return False
                    
                    elif self.menu_durum == MenuDurum.AYARLAR:
                        for i, buton in enumerate(self.ayarlar_butonlar):
                            if buton['rect'].collidepoint(pos):
                                if buton['tip'] == 'arkaplan':
                                    # Arkaplan temasını değiştir
                                    temalar = list(self.tema.arkaplan_temalar.keys())
                                    curr_idx = temalar.index(self.tema.secili_arkaplan)
                                    self.tema.secili_arkaplan = temalar[(curr_idx + 1) % len(temalar)]
                                    buton['text'] = 'Arkaplan: ' + self.tema.secili_arkaplan
                                elif buton['tip'] == 'yilan':
                                    # Yılan temasını değiştir
                                    temalar = list(self.tema.yilan_temalar.keys())
                                    curr_idx = temalar.index(self.tema.secili_yilan)
                                    self.tema.secili_yilan = temalar[(curr_idx + 1) % len(temalar)]
                                    buton['text'] = 'Yılan: ' + self.tema.secili_yilan
                                elif buton['tip'] == 'baslat':  # Yeni eklenen başlat butonu
                                    self.menu_durum = MenuDurum.OYUN
                                    self.oyunu_baslat()
                                    return True
                                elif i == 3:  # Geri
                                    self.menu_durum = MenuDurum.ANA_MENU

                # Fare üzerinde hover efekti için
                pos = pygame.mouse.get_pos()
                if self.menu_durum == MenuDurum.ANA_MENU:
                    butonlar = self.ana_menu_butonlar
                else:
                    butonlar = self.ayarlar_butonlar

            self.arkaplan_ciz()
            if self.menu_durum == MenuDurum.ANA_MENU:
                self.ana_menu_ciz()
            elif self.menu_durum == MenuDurum.AYARLAR:
                self.ayarlar_menu_ciz()
            
            # Hover efekti
            pos = pygame.mouse.get_pos()
            if self.menu_durum == MenuDurum.ANA_MENU:
                for buton in self.ana_menu_butonlar:
                    self.buton_ciz(buton, buton['rect'].collidepoint(pos))
            else:
                for buton in self.ayarlar_butonlar:
                    self.buton_ciz(buton, buton['rect'].collidepoint(pos))
            
            pygame.display.flip()
            self.saat.tick(60)
        
        return True

    def arkaplan_ciz(self):
        # Gradient arkaplan
        for y in range(self.yukseklik):
            renk_deger = int((y / self.yukseklik) * 50)  # 0-50 arası koyu mavi tonu
            pygame.draw.line(self.ekran, (0, 0, renk_deger), 
                           (0, y), (self.genislik, y))

        # Grid çizgileri
        for x in range(0, self.genislik, self.grid_boyut):
            pygame.draw.line(self.ekran, (20, 20, 50), 
                           (x, 0), (x, self.yukseklik), 1)
        for y in range(0, self.yukseklik, self.grid_boyut):
            pygame.draw.line(self.ekran, (20, 20, 50), 
                           (0, y), (self.genislik, y), 1)

    def oyunu_baslat(self):
        self.yilan = Yilan(self.tema.secili_yilan)
        self.yem = Yem(self.genislik, self.yukseklik)
        self.skor = 0
        self.oyun_devam = True

    def skor_goster(self):
        skor_text = self.font.render(f'Skor: {self.skor}', True, Renkler.BEYAZ)
        self.ekran.blit(skor_text, (10, 10))

    def calistir(self):
        while True:
            if not self.menu_kontrol():
                break
            
            while self.oyun_devam:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.yilan.yon_degistir([0, -self.yilan.hiz])
                        elif event.key == pygame.K_DOWN:
                            self.yilan.yon_degistir([0, self.yilan.hiz])
                        elif event.key == pygame.K_LEFT:
                            self.yilan.yon_degistir([-self.yilan.hiz, 0])
                        elif event.key == pygame.K_RIGHT:
                            self.yilan.yon_degistir([self.yilan.hiz, 0])

                self.yilan.hareket()

                # Sınır kontrolü
                x, y = self.yilan.pozisyonlar[0]
                if x < 0 or x >= self.genislik or y < 0 or y >= self.yukseklik:
                    self.oyun_devam = False
                    continue

                # Kendine çarpma kontrolü
                if self.yilan.pozisyonlar[0] in self.yilan.pozisyonlar[1:]:
                    self.oyun_devam = False
                    continue

                # Yem yeme kontrolü
                if (self.yilan.pozisyonlar[0][0] == self.yem.x and 
                    self.yilan.pozisyonlar[0][1] == self.yem.y):
                    if self.yem.tip == YemTipi.ELMA:
                        self.yilan.uzunluk += 1
                        self.skor += 10
                    else:  # ALTIN
                        self.yilan.uzunluk += 2
                        self.skor += 30
                    self.yem.yeni_konum()

                # Çizim
                self.arkaplan_ciz()
                
                # Yılanı çiz - özel efektlerle
                for i, (pos, renk) in enumerate(zip(self.yilan.pozisyonlar, self.yilan.renkler)):
                    # Yılan kafası
                    if i == 0:
                        # Kafa için özel efekt
                        if self.tema.secili_yilan == 'Altın':
                            # Altın parıltısı efekti
                            parlaklik = abs(math.sin(time.time() * 5)) * 55 + 200
                            kafa_renk = (parlaklik, parlaklik * 0.85, 0)
                        else:
                            kafa_renk = renk
                        
                        pygame.draw.circle(self.ekran, kafa_renk,
                                        (pos[0] + self.yilan.boyut//2,
                                         pos[1] + self.yilan.boyut//2),
                                        self.yilan.boyut//2)
                        
                        # Gözler
                        goz_renk = (0, 0, 0) if self.tema.secili_yilan != 'Altın' else (50, 0, 0)
                        goz_boyut = 3
                        goz_offset = 4
                        
                        # Yön bazlı göz pozisyonları
                        if self.yilan.yon[0] > 0:  # Sağa
                            goz_x = pos[0] + self.yilan.boyut - goz_offset
                            goz_y1 = pos[1] + goz_offset
                            goz_y2 = pos[1] + self.yilan.boyut - goz_offset
                        elif self.yilan.yon[0] < 0:  # Sola
                            goz_x = pos[0] + goz_offset
                            goz_y1 = pos[1] + goz_offset
                            goz_y2 = pos[1] + self.yilan.boyut - goz_offset
                        elif self.yilan.yon[1] < 0:  # Yukarı
                            goz_y = pos[1] + goz_offset
                            goz_x1 = pos[0] + goz_offset
                            goz_x2 = pos[0] + self.yilan.boyut - goz_offset
                        else:  # Aşağı
                            goz_y = pos[1] + self.yilan.boyut - goz_offset
                            goz_x1 = pos[0] + goz_offset
                            goz_x2 = pos[0] + self.yilan.boyut - goz_offset
                        
                        if self.yilan.yon[0] != 0:  # Yatay hareket
                            pygame.draw.circle(self.ekran, goz_renk, (goz_x, goz_y1), goz_boyut)
                            pygame.draw.circle(self.ekran, goz_renk, (goz_x, goz_y2), goz_boyut)
                        else:  # Dikey hareket
                            pygame.draw.circle(self.ekran, goz_renk, (goz_x1, goz_y), goz_boyut)
                            pygame.draw.circle(self.ekran, goz_renk, (goz_x2, goz_y), goz_boyut)
                    
                    else:  # Yılan gövdesi
                        pygame.draw.circle(self.ekran, renk,
                                        (pos[0] + self.yilan.boyut//2,
                                         pos[1] + self.yilan.boyut//2),
                                        self.yilan.boyut//2)
                
                # Yemi çiz
                self.yem.ciz(self.ekran)
                
                self.skor_goster()
                pygame.display.flip()
                self.saat.tick(10)

            self.menu_durum = MenuDurum.ANA_MENU

        pygame.quit()

if __name__ == "__main__":
    oyun = Oyun()
    oyun.calistir() 