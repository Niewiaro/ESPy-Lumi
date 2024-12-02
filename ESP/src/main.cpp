#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

/***************************
          S E T U P
***************************/

#define INITIAL_LED_TEST_ENABLED true
#define INITIAL_LED_TEST_BRIGHTNESS 69 // 0..255
#define INITIAL_LED_TEST_TIME_MS 500   // 10..
#define INITIAL_LED_TEST_BLINKS 3      // 1..

#define MAX_LEDS 144

// type of your led controller, possible values, see below
#define LED_TYPE NEO_GRBW
#define LED_FREQUENCY NEO_KHZ800

#define LED_PINS 12    // 3 wire leds
#define BRIGHTNESS 100 // maximum brightness 0-255

// Define the array of leds
Adafruit_NeoPixel leds(MAX_LEDS, LED_PINS, LED_TYPE + LED_FREQUENCY);

// set color to all leds
void showColor(uint8_t r = 0, uint8_t g = 0, uint8_t b = 0, uint8_t w = 0)
{
#if MAX_LEDS > 1
    for (int led_pos = 0; led_pos < MAX_LEDS; led_pos++)
    {
        leds.setPixelColor(led_pos, leds.Color(r, g, b, w));
    }
    leds.show();
#endif
}

// switch off digital and analog leds
void switchOff()
{
#if MAX_LEDS > 1
    leds.clear();
    leds.show();
#endif
}

// main function that setups and runs the code
void setup()
{
    // Inicjalizacja komunikacji przez Serial
    Serial.begin(115200);                  // Ustaw prędkość transmisji
    Serial.println("Serial Echo - ESP32"); // Wiadomość startowa

    leds.begin();

    // color adjustments
    leds.setBrightness(BRIGHTNESS);

// initial RGB flash
#if INITIAL_LED_TEST_ENABLED == true
    for (int i = 0; i < INITIAL_LED_TEST_BLINKS; i++)
    {
        for (int v = 0; v < INITIAL_LED_TEST_BRIGHTNESS; v++)
        {
            showColor(v, v, v);
            delay(INITIAL_LED_TEST_TIME_MS / 2 / INITIAL_LED_TEST_BRIGHTNESS);
        }
    }
#endif
    showColor(0, 0, 0);
} // end of setup

#define RAINBOW_CYCLE_DELAY 50 // Opóźnienie między krokami tęczy

// Funkcja do generowania koloru tęczy na podstawie wartości
uint32_t Wheel(byte WheelPos)
{
    WheelPos = 255 - WheelPos;
    if (WheelPos < 85)
    {
        return leds.Color(255 - WheelPos * 3, 0, WheelPos * 3);
    }
    if (WheelPos < 170)
    {
        WheelPos -= 85;
        return leds.Color(0, WheelPos * 3, 255 - WheelPos * 3);
    }
    WheelPos -= 170;
    return leds.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

// Funkcja przesuwająca tęczę przez diody LED
void rainbowCycle(uint8_t wait)
{
    uint16_t i, j;

    for (j = 0; j < 256; j++)
    { // Jedno przejście tęczy dla każdego koloru
        for (i = 0; i < leds.numPixels(); i++)
        {
            leds.setPixelColor(i, Wheel(((i * 256 / leds.numPixels()) + j) & 255));
        }
        leds.show();
        delay(wait);
    }
}

#define WAIT_TIME 10000
#define WAIT_TIME_STROBE 100

void loop()
{
    // Sprawdź, czy są dane do odczytania
    if (Serial.available() > 0)
    {
        // Odczytaj dane
        String receivedData = Serial.readString();

        // Odesłanie odebranych danych
        Serial.printf("echo:\t%s\n", receivedData.c_str()); // Konwersja String na C-string

        // Sprawdzenie komendy
        if (receivedData == "r")
        {
            Serial.println("Turning LEDs red");
            showColor(255, 0, 0); // Ustaw kolor czerwony
        }
        else if (receivedData == "g")
        {
            Serial.println("Turning LEDs green");
            showColor(0, 255, 0); // Ustaw kolor zielony
        }
        else if (receivedData == "b")
        {
            Serial.println("Turning LEDs blue");
            showColor(0, 0, 255); // Ustaw kolor niebieski
        }
        else if (receivedData == "w")
        {
            Serial.println("Turning LEDs white");
            showColor(0, 0, 0, 255); // Ustaw kolor niebieski
        }
        else if (receivedData == "full")
        {
            Serial.println("Turning LEDs white");
            showColor(255, 255, 255, 255); // Ustaw kolor niebieski
        }
        else if (receivedData == "off")
        {
            Serial.println("Turning LEDs off");
            switchOff(); // Wyłączenie LED
        }
        else if (receivedData == "rainbow")
        {
            Serial.println("Starting rainbow effect");
            rainbowCycle(RAINBOW_CYCLE_DELAY); // Efekt tęczy
        }
        else
        {
            Serial.println("Unknown command");
        }
    }
}
