#include <Arduino.h>


// #define LED 2

// void setup() {
//   pinMode(LED,OUTPUT);
// }

// void loop() {
//   digitalWrite(LED,HIGH);
//   delay(500);
//   digitalWrite(LED,LOW);
//   delay(500);
// }



void setup() {
    // Inicjalizacja komunikacji przez Serial
    Serial.begin(115200); // Ustaw prędkość transmisji
    Serial.println("Serial Echo - ESP32"); // Wiadomość startowa
}

void loop() {
    // Sprawdź, czy są dane do odczytania
    if (Serial.available() > 0) {
        // Odczytaj dane
        String receivedData = Serial.readString();

        // Odesłanie odebranych danych
        Serial.println(receivedData);
    }
}





// int incomingByte = 0; // for incoming serial data
 
// void setup() {
//   Serial.begin(115200); // opens serial port, sets data rate to 115200 bps
// }
 
// void loop() {
//   // send data only when you receive data:
//   if (Serial.available() > 0) {
//     // read the incoming byte:
//     incomingByte = Serial.read();
 
//     // say what you got:
//     Serial.print("ESP32 received: ");
//     Serial.println(incomingByte);
//   }
// }





// #include <Adafruit_NeoPixel.h>

// /***************************
//           S E T U P         
// ***************************/

// #define INITIAL_LED_TEST_ENABLED true
// #define INITIAL_LED_TEST_BRIGHTNESS 69  // 0..255
// #define INITIAL_LED_TEST_TIME_MS 500  // 10..
// #define INITIAL_LED_TEST_BLINKS 3  // 1..

// #define MAX_LEDS 144

// // type of your led controller, possible values, see below
// #define LED_TYPE NEO_GRBW
// #define LED_FREQUENCY NEO_KHZ800

// #define LED_PINS 16         // 3 wire leds
// #define BRIGHTNESS 255      // maximum brightness 0-255

// // Define the array of leds
// Adafruit_NeoPixel leds(MAX_LEDS, LED_PINS, LED_TYPE + LED_FREQUENCY);

// // set color to all leds
// void showColor(uint8_t r=0, uint8_t g=0, uint8_t b=0, uint8_t w=0) {
//   #if MAX_LEDS > 1
//     for (int led_pos=0; led_pos < MAX_LEDS; led_pos++) {
//       leds.setPixelColor(led_pos, leds.Color(r, g, b, w));
//     }
//     leds.show();
//   #endif
// }

// // switch of digital and analog leds
// void switchOff() {
//   #if MAX_LEDS > 1
//     leds.clear();
//     leds.show();
//   #endif
// }

// // main function that setups and runs the code
// void setup() {
//   leds.begin();
  
//   // color adjustments
//   leds.setBrightness ( BRIGHTNESS );

//   // initial RGB flash
//   #if INITIAL_LED_TEST_ENABLED == true
//   for (int i=0; i<INITIAL_LED_TEST_BLINKS; i++){
//     for (int v=0;v<INITIAL_LED_TEST_BRIGHTNESS;v++){
//       showColor(v,v,v);  
//       delay(INITIAL_LED_TEST_TIME_MS/2/INITIAL_LED_TEST_BRIGHTNESS);
//     }
//   }
//   #endif
//   showColor(0, 0, 0);
// } // end of setup



// #define RAINBOW_CYCLE_DELAY 50 // Opóźnienie między krokami tęczy


// // Funkcja do generowania koloru tęczy na podstawie wartości
// uint32_t Wheel(byte WheelPos) {
//   WheelPos = 255 - WheelPos;
//   if(WheelPos < 85) {
//     return leds.Color(255 - WheelPos * 3, 0, WheelPos * 3);
//   }
//   if(WheelPos < 170) {
//     WheelPos -= 85;
//     return leds.Color(0, WheelPos * 3, 255 - WheelPos * 3);
//   }
//   WheelPos -= 170;
//   return leds.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
// }

// // Funkcja przesuwająca tęczę przez diody LED
// void rainbowCycle(uint8_t wait) {
//   uint16_t i, j;

//   for(j=0; j<256; j++) { // Jedno przejście tęczy dla każdego koloru
//     for(i=0; i<leds.numPixels(); i++) {
//       leds.setPixelColor(i, Wheel(((i * 256 / leds.numPixels()) + j) & 255));
//     }
//     leds.show();
//     delay(wait);
//   }
// }



// #define WAIT_TIME 10000
// #define WAIT_TIME_STROBE 100

// void loop() {
//   // showColor(255, 15, 5, 5);
//   showColor(255, 0, 0, 10);
//   delay(WAIT_TIME);
//   showColor(150, 180, 255, 10);
//   delay(WAIT_TIME);
//   showColor(255, 0, 0);
//   delay(WAIT_TIME);
//   showColor(0, 255, 0);
//   delay(WAIT_TIME);
//   showColor(0, 0, 255);
//   delay(WAIT_TIME);
//   showColor(0, 0, 0, 255);
//   delay(WAIT_TIME);
//   showColor(255, 255, 255);
//   delay(WAIT_TIME);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);
//   showColor(255, 255, 255, 255);
//   delay(WAIT_TIME_STROBE);
//   switchOff();
//   delay(WAIT_TIME_STROBE);

//   // Kod dla tęczy
//   rainbowCycle(RAINBOW_CYCLE_DELAY);  
// }
