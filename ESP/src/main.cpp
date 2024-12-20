#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <BluetoothSerial.h>


/***************************
         S E T U P
***************************/

// __________LEDS___________
#define INITIAL_LED_TEST_ENABLED true
#define INITIAL_LED_TEST_BRIGHTNESS 100 // 0-255
#define INITIAL_LED_TEST_TIME_MS 100    // 10-
#define INITIAL_LED_TEST_BLINKS 1       // 1-

#define NUM_LEDS 144 // Number of LEDs
#define LED_TYPE NEO_GRBW
#define LED_FREQUENCY NEO_KHZ800
#define LED_PINS 12    // 3 wire leds
#define BRIGHTNESS 255 // maximum brightness 0-255

#define BAUD_RATE 115200 // Serial transmission speed

// Define the array of leds
Adafruit_NeoPixel leds(NUM_LEDS, LED_PINS, LED_TYPE + LED_FREQUENCY);

// _______Bluetooth________
BluetoothSerial SerialBT;


/***************************
          C O D E
***************************/

// set color to all leds
void showColor(uint8_t r = 0, uint8_t g = 0, uint8_t b = 0, uint8_t w = 0)
{
#if NUM_LEDS > 1
    for (int led_pos = 0; led_pos < NUM_LEDS; led_pos++)
    {
        leds.setPixelColor(led_pos, leds.Color(r, g, b, w));
    }
    leds.show();
#endif
}

// rainbow
uint32_t Wheel(byte WheelPos)
{
    WheelPos = 255 - WheelPos;
    if (WheelPos < 85)
    {
        return leds.Color(255 - WheelPos * 3, 0, WheelPos * 3); // Red -> Blue
    }
    if (WheelPos < 170)
    {
        WheelPos -= 85;
        return leds.Color(0, WheelPos * 3, 255 - WheelPos * 3); // Blue -> Green
    }
    WheelPos -= 170;
    return leds.Color(WheelPos * 3, 255 - WheelPos * 3, 0); // Green -> Red
}

// light visible spectrum rainbow
uint32_t VisibleSpectrum(int index, int totalLEDs)
{
    float position = (float)index / (float)totalLEDs;  // normalize 0–1
    float wavelength = 380 + (position * (750 - 380)); // scale to wavelength 380–750 nm

    // wavelength to RGB (aproxyamt spectrum)
    float r, g, b;
    if (wavelength >= 380 && wavelength < 440)
    {
        r = -(wavelength - 440) / (440 - 380);
        g = 0.0;
        b = 1.0;
    }
    else if (wavelength >= 440 && wavelength < 490)
    {
        r = 0.0;
        g = (wavelength - 440) / (490 - 440);
        b = 1.0;
    }
    else if (wavelength >= 490 && wavelength < 510)
    {
        r = 0.0;
        g = 1.0;
        b = -(wavelength - 510) / (510 - 490);
    }
    else if (wavelength >= 510 && wavelength < 580)
    {
        r = (wavelength - 510) / (580 - 510);
        g = 1.0;
        b = 0.0;
    }
    else if (wavelength >= 580 && wavelength < 645)
    {
        r = 1.0;
        g = -(wavelength - 645) / (645 - 580);
        b = 0.0;
    }
    else if (wavelength >= 645 && wavelength <= 750)
    {
        r = 1.0;
        g = 0.0;
        b = 0.0;
    }
    else
    {
        r = 0.0;
        g = 0.0;
        b = 0.0; // out of spectrum range
    }

    float intensity;
    if (wavelength >= 380 && wavelength < 420)
    {
        intensity = 0.3 + 0.7 * (wavelength - 380) / (420 - 380);
    }
    else if (wavelength >= 645 && wavelength <= 750)
    {
        intensity = 0.3 + 0.7 * (750 - wavelength) / (750 - 645);
    }
    else
    {
        intensity = 1.0;
    }

    r = pow(r * intensity, 0.8); // Gamma correction
    g = pow(g * intensity, 0.8);
    b = pow(b * intensity, 0.8);

    return leds.Color((int)(r * 255), (int)(g * 255), (int)(b * 255));
}

// main function that setups and runs the code
void setup()
{
    Serial.begin(BAUD_RATE);
    if (!SerialBT.begin("ESP32_LED_Control"))
    {
        Serial.println("Bluetooth initialization failed!");
        while (true)
            ;
    }
    Serial.println("Bluetooth ready. Connect to 'ESP32_LED_Control'.");

    leds.begin();
    leds.clear();
    leds.show();
    leds.setBrightness(BRIGHTNESS);

// initial RGB flash
#if INITIAL_LED_TEST_ENABLED == true
    for (int i = 0; i < INITIAL_LED_TEST_BLINKS; i++)
    {
        for (int v = 0; v < INITIAL_LED_TEST_BRIGHTNESS; v++)
        {
            showColor(v);
            delay(INITIAL_LED_TEST_TIME_MS / 2 / INITIAL_LED_TEST_BRIGHTNESS);
        }
        for (int v = 0; v < INITIAL_LED_TEST_BRIGHTNESS; v++)
        {
            showColor(0, v);
            delay(INITIAL_LED_TEST_TIME_MS / 2 / INITIAL_LED_TEST_BRIGHTNESS);
        }
        for (int v = 0; v < INITIAL_LED_TEST_BRIGHTNESS; v++)
        {
            showColor(0, 0, v);
            delay(INITIAL_LED_TEST_TIME_MS / 2 / INITIAL_LED_TEST_BRIGHTNESS);
        }
        for (int v = 0; v < INITIAL_LED_TEST_BRIGHTNESS; v++)
        {
            showColor(0, 0, 0, v);
            delay(INITIAL_LED_TEST_TIME_MS / 2 / INITIAL_LED_TEST_BRIGHTNESS);
        }
        for (int v = 0; v < INITIAL_LED_TEST_BRIGHTNESS; v++)
        {
            showColor(v, v, v, v);
            delay(INITIAL_LED_TEST_TIME_MS / 2 / INITIAL_LED_TEST_BRIGHTNESS);
        }
    }
#endif
    showColor(0, 0, 0);
} // end of setup

void loop()
{
    if (SerialBT.available())
    {
        String receivedData = SerialBT.readStringUntil('\n'); // read BT data
        receivedData.trim(); // remove white space

        Serial.println(receivedData);
        Serial.println(receivedData.length());

        int intensities[NUM_LEDS];
        int index = 0;
        int start = 0;

        for (int i = 0; i < receivedData.length(); i++)
        {
            if (receivedData[i] == ',' || i == receivedData.length() - 1)
            {
                String value = receivedData.substring(start, (i == receivedData.length() - 1) ? i + 1 : i);
                intensities[index++] = value.toInt();
                start = i + 1;
            }
        }

        // rainbow
        // if (index == NUM_LEDS) {
        //     for (int i = 0; i < NUM_LEDS; i++) {
        //         uint32_t color = Wheel((i * 256 / NUM_LEDS) % 256);

        //         uint8_t r = (color >> 16) & 0xFF;
        //         uint8_t g = (color >> 8) & 0xFF;
        //         uint8_t b = color & 0xFF;

        //         r = (r * intensities[i]) / 255;
        //         g = (g * intensities[i]) / 255;
        //         b = (b * intensities[i]) / 255;

        //         leds.setPixelColor(i, leds.Color(r, g, b));
        //     }
        //     leds.show();

        // visible spectrum rainbow
        if (index == NUM_LEDS)
        {
            for (int i = 0; i < NUM_LEDS; i++)
            {
                uint32_t spectrumColor = VisibleSpectrum(i, NUM_LEDS);

                uint8_t r = (spectrumColor >> 16) & 0xFF;
                uint8_t g = (spectrumColor >> 8) & 0xFF;
                uint8_t b = spectrumColor & 0xFF;

                r = (r * intensities[i]) / 255;
                g = (g * intensities[i]) / 255;
                b = (b * intensities[i]) / 255;

                leds.setPixelColor(i, leds.Color(r, g, b));
            }
            leds.show();
            Serial.println("Colors of LEDs updated.");
        }
        else
        {
            Serial.println("ERROR: Invalid data.");
        }

        SerialBT.flush(); // clear RX buffer after data read
    }
}
