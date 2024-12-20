import numpy as np
import matplotlib.pyplot as plt

# Funkcja VisibleSpectrum
def visible_spectrum(wavelength):
    r, g, b = 0, 0, 0
    if 380 <= wavelength < 440:
        r = -(wavelength - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif 440 <= wavelength < 490:
        r = 0.0
        g = (wavelength - 440) / (490 - 440)
        b = 1.0
    elif 490 <= wavelength < 510:
        r = 0.0
        g = 1.0
        b = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        r = (wavelength - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif 580 <= wavelength < 645:
        r = 1.0
        g = -(wavelength - 645) / (645 - 580)
        b = 0.0
    elif 645 <= wavelength <= 750:
        r = 1.0
        g = 0.0
        b = 0.0

    # Skoryguj intensywność na końcach spektrum
    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 645 <= wavelength <= 750:
        factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
    else:
        factor = 1.0

    r = int((r * factor) * 255)
    g = int((g * factor) * 255)
    b = int((b * factor) * 255)

    return r, g, b

# Generowanie danych
wavelengths = np.linspace(380, 750, 1000)  # Długości fal w zakresie widzialnym
colors = [visible_spectrum(w) for w in wavelengths]

# Składowe R, G, B
r_values = [c[0] for c in colors]
g_values = [c[1] for c in colors]
b_values = [c[2] for c in colors]

# Wykresy
plt.figure(figsize=(15, 10))

# Gradient widzialnego światła
gradient = np.array(colors) / 255
plt.imshow([gradient], extent=[380, 750, 260, 300], aspect='auto', origin='lower')

# Składowe RGB
plt.plot(wavelengths, r_values, label="Czerwona (Red)", color="red")
plt.plot(wavelengths, g_values, label="Zielona (Green)", color="green")
plt.plot(wavelengths, b_values, label="Niebieska (Blue)", color="blue")

# Oznaczenia kluczowych długości fal
key_wavelengths = [380, 440, 490, 510, 580, 645, 750]
key_labels = ['Fiolet (380 nm)', 'Niebieski (440 nm)', 'Cyjan (490 nm)', 'Zielony (510 nm)', 
              'Żółty (580 nm)', 'Czerwony (645 nm)', 'Czerwony (750 nm)']
for w, label in zip(key_wavelengths, key_labels):
    plt.axvline(x=w, color='gray', linestyle='--', alpha=0.5)
    plt.text(w, 10, label, rotation=90, verticalalignment='bottom', horizontalalignment='right', fontsize=10)

# Ustawienia wykresu
plt.title("Mieszanie kolorów w spektrum widzialnym", fontsize=14)
plt.xlabel("Długość fali (nm)", fontsize=12)
plt.ylabel("Intensywność składowych RGB [0-255]", fontsize=12)
plt.ylim(0, 299)
plt.xlim(380, 750)
plt.legend(fontsize=10, loc='center right')
plt.grid(True, linestyle='--', alpha=0.3)

# Wyświetlenie wykresu
plt.tight_layout()
plt.show()
