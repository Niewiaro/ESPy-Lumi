import serial
import random
import time

# Ustawienia połączenia Bluetooth
BLUETOOTH_PORT = "COM6"  # Zmień na właściwy port Bluetooth
BAUD_RATE = 115200


def generate_intensity_values(min: int = 0, max: int = 255, num_leds: int = 144):
    """Generuje listę 144 losowych wartości intensywności od 0 do 255."""
    return [random.randint(min, max) for _ in range(num_leds)]


def main():
    try:
        # Połączenie z Bluetooth
        ser = serial.Serial(BLUETOOTH_PORT, BAUD_RATE, timeout=1)
        print(f"Połączono z {BLUETOOTH_PORT}")

        while True:
            # Generuj listę losowych wartości intensywności
            values = generate_intensity_values()

            # Konwertuj listę na string oddzielony przecinkami
            data = ",".join(map(str, values)) + "\n"

            # Wyślij dane przez Bluetooth
            ser.write(data.encode())
            print(f"Wysłano: {data.strip()}")

            # Odczekaj 3 sekundy
            time.sleep(3)

    except serial.SerialException as e:
        print(f"Błąd połączenia: {e}")
    except KeyboardInterrupt:
        print("Przerwano przez użytkownika.")
    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()
            print("Zamknięto połączenie Bluetooth.")


if __name__ == "__main__":
    main()
