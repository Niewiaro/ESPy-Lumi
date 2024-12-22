DATA = """
„Audio Reactive WLED”, kno.wled.ge, 2024-12-08

Piecuch A., PROGRAMOWANIE MOŻE BYĆ INTERESUJĄCE – PLATFORMA ARDUINO, Dydaktyka Informatyki, 2017
Nano V3.0 z USB mini zgodny z Arduino®, sklep.msalamon.pl, 2024-12-09
Nano, docs.arduino.cc, 2024-12-09

4.2.2. ESP32 important features
El-Khozondar H.J., Mtair S.Y. Qoffa K.O., Qasem O.I., Munyarawi A.H., Nassar Y.F. et al., A smart energy monitoring system using ESP32 microcontroller, e-Prime - Advances in Electrical
Engineering, Electronics and Energy, 2024
ESP32-DevKitC-VIE, www.mouser.pl, 2024-12-09

ESP32-DevKitC V4, docs.espressif.com, 2024-12-09

Upton E., Halfacree G.: Raspberry Pi. Przewodnik użytkownika, Helion S.A. 2013
Raspberry Pi 4, www.raspberrypi.com, 2024-12-09

Pasek LED SMD5050 IP20 14,4W, 60 diod/m, 10mm, RGB - 5m, botland.com.pl, 2024-12-09

Elastyczna matryca 16x16 - 256 LED RGB - WS2812B indywidualnie adresowane, botland.com.pl, 2024-12-09

Pasek LED RGB WS2812B - cyfrowy, adresowany - IP65 144 LED/m, 43W/m, 5V - 1m, botland.com.pl, 2024-12-09

Pasek LED RGBW SK6812 - cyfrowy, adresowany - IP65 144 LED/m, 43,2W/m, 5V - 1m, botland.com.pl, 2024-12-09

Taśma LED COB RGBW 896 chips 24V 16W + zimna 6500K CRI90+, www.eled.pl, 2024-12-09

,,FastLED-HSV-Colors”, github.com/FastLED/FastLED/wiki, 2024-12-19
Kłopotowska A., Architektura a dźwięk  – interdyscyplinarne badania naukowe na temat wykorzystania sygnałów fonicznych w percepcji  i projektowaniu przestrzeni architektonicznej, Budownictwo i Architektura, 2019 grudzień
Graf M., Opara H.C., Barthet M., An Audio-Driven System For Real-Time Music Visualisation, Queen Mary University of London, 2021 maj
,, Cyfrowe przetwarzanie sygnałów w praktycznych zastosowaniach (2)”, ep.com.pl, 2024-12-21

,, Rozwój oprogramowania audio dla systemów embedded”, sii.pl, 2024-12-21
,,Fast, easy LED library for Arduino”, fastled.io, 2024-12-21

,,Adafruit NeoPixel Überguide”, learn.adafruit.com, 2024-12-21

,,WLED Project”,  kno.wled.ge, 2024-12-22

,,Welcome to LedFx”, github.com/LedFx, 2024-12-22

,, Audio Reactive LED Strip”, github.com/scottlawsonbc, 2024-12-21

"""

def main() -> None:
    books = DATA.splitlines()
    books = list(filter(('').__ne__, books))
    books = sorted(books)
    print(books)

if __name__ == "__main__":
    main()
