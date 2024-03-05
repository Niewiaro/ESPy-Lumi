# ESPy-Lumi

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![ESP32](https://img.shields.io/badge/ESP32-DevKitC-orange)
![FreeRTOS](https://img.shields.io/badge/FreeRTOS-v10.4.1-green)
![KivyMD](https://img.shields.io/badge/KivyMD-v1.0.0-yellow)

**ESP32** + **Python** + **KivyMD** = **ESPy-Lumi**

Projekt ESPy-Lumi to innowacyjne połączenie Pythona z mikrokontrolerem ESP32, umożliwiające sterowanie paskiem adresowalnego LED (SK6812 RGBW) za pomocą smartfona.

## Zawartość
1. [Opis](#opis)
2. [Funkcjonalności](#funkcjonalności)
3. [Wymagania](#wymagania)
4. [Instalacja](#instalacja)
5. [Użycie](#użycie)
6. [Autor](#autor)
7. [Licencja](#licencja)

## Opis

Ten projekt jest częścią mojej pracy inżynierskiej na Akademii Górniczo-Hutniczej im. Stanisława Staszica w Krakowie.

ESP32 jest używany do sterowania kolorami adresowalnego paska LED (SK6812 RGBW) poprzez protokół Bluetooth. Aplikacja mobilna, napisana w KivyMD, umożliwia użytkownikom wygodne sterowanie oświetleniem z poziomu swojego smartfona. Projekt oparty jest na platformie FreeRTOS, co zapewnia stabilność i niezawodność działania.

## Funkcjonalności

- Sterowanie kolorami RGBW paska LED z poziomu aplikacji mobilnej.
- Wybór dowolnego koloru za pomocą interaktywnego interfejsu.
- Możliwość zapisania ulubionych ustawień kolorów.
- Konfiguracja parametrów paska LED.
- Obsługa wielu efektów świetlnych.
- Obsługa wielu urządzeń ESP32 jednocześnie.

## Wymagania

- Python 3.7 lub nowszy
- Mikrokontroler ESP32 (zalecane: ESP32-DevKitC)
- FreeRTOS w wersji 10.4.1 lub nowszej
- KivyMD w wersji 1.0.0 lub nowszej

## Instalacja

Instrukcja instalacji
W celu uruchomienia projektu ESPy-Lumi na swoim systemie, wykonaj następujące kroki:

1. Sklonuj repozytorium na swoje urządzenie:

```
git clone https://github.com/twoje-username/ESPy-Lumi.git
```

2. Przejdź do katalogu projektu:

```
cd ESPy-Lumi
```

3. Zainstaluj wymagane biblioteki Pythona:

```
pip install -r requirements.txt
```

4. Uruchom plik `setup.py`, aby zainstalować wszystkie niezbędne zależności:

```
python setup.py install
```

5. Wgraj oprogramowanie na mikrokontroler ESP32 zgodnie z instrukcjami znajdującymi się w folderze `ESP32`.

## Użycie

1. Uruchom aplikację mobilną na swoim urządzeniu.
2. Połącz się z urządzeniem ESP32 poprzez interfejs Bluetooth.
3. Wybierz żądany efekt świetlny i dostosuj jego parametry.
4. Ciesz się kolorowymi efektami świetlnymi na pasku LED!

## Autor

Jakub Niewiarowski - [kontakt](mailto:niewiarowski.kuba@gmail.com)

## Licencja

Ten projekt jest objęty licencją MIT - zobacz plik [LICENSE](LICENSE) dla szczegółów.
