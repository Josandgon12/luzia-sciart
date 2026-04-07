#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NUMPIXELS 24
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#include <SharpIR.h>
SharpIR sensor(SharpIR::GP2Y0A02YK0F, A0);

#define ELEMENTS 15

void setup() {
  Serial.begin(9600);
  pixels.begin();
  pixels.clear();
  pixels.show();

  pinMode(12, OUTPUT);
}

long last = millis();

void loop() {
  long now = millis();
  if (now - last < 200)
    return;
  last = now;

  if (Serial.available() > 0) {
    if (Serial.read() == '1') turnOnLeds(); else clearLeds();
  }

  int distance = sensor.getDistance();
  int button = digitalRead(12);
  Serial.println(distance + String(",") + button);
}

uint8_t status = 0;
void turnOnLeds(){
  if (status == 1)
    return;

  pixels.fill(pixels.Color(127, 150, 180), 0, 24);
  pixels.show();
  status = 1;
}

void clearLeds(){
  if (status == 0)
    return;

  pixels.fill(pixels.Color(0, 0, 0), 0, 24);
  pixels.show();
  status = 0;
}
