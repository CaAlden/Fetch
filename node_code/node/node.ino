#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

#define BAUDRATE 9600
#define DELAY 10000
#define STATUS_LED 12
#define READ 0
#define SEND 1
#define REST 2

SoftwareSerial gpsSerial = SoftwareSerial(6, 5); // RX, TX
Adafruit_NeoPixel statusLed = Adafruit_NeoPixel(1, STATUS_LED, NEO_GRB + NEO_KHZ800);
TinyGPSPlus gps;

String NODE_NUMBER = "1"; //change this manually for each node :(
int gpsCount = 0;

char ledState;
String gpsString;
String xbeeString;

void setup() {
  // open up serial communication
  Serial.begin(BAUDRATE);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  gpsSerial.begin(BAUDRATE);
  
  statusLed.begin();
  triggerLed(0);
}

void loop() {

  triggerLed(REST);
  // read GPS data
  while(gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      if (gpsCount == 0) {
        triggerLed(SEND);
        parseInfo();
        gpsCount = 50;
      } else {
        gpsCount--;
      }
    }
  }
  
}

void parseInfo() {
  String lat;
  String lng;
  String alt;

  if (gps.location.isValid()) {
    lat = String(gps.location.lat(), 6);
    lng = String(gps.location.lng(), 6);
  } else {
    lat = "INVALID";
    lng = "INVALID";
  }

  if (gps.altitude.isValid()) {
    alt = String(gps.altitude.meters(), 6);
  } else {
    alt = "INVALID";
  }
  
  sendGpsData(lat, lng, alt);
}

static void sendGpsData(String lat, String lng, String alt) {
  String msg = "{\"node\":\"" + NODE_NUMBER + "\"";
  msg += ", \"latitude\":\"" + lat + "\"";
  msg += ", \"longitude\":\"" + lng + "\"";
  msg += ", \"altitude\":\"" + alt + "\"}";
  Serial.println(msg);
}

static void readXbee() {
  xbeeString = "";

  if (Serial.available() > 0) {
    char nextChar = Serial.read();
    while(nextChar != '\n' && Serial.available() > 0) {
      xbeeString += nextChar;
      nextChar = Serial.read();
    }
  }
}


static void triggerLed(int state) {
  if (state == READ) {
    setColor(statusLed.Color(0, 255, 0));
  } else if (state == SEND) {
    setColor(statusLed.Color(255, 0, 0));
  } else if (state == REST) {
    setColor(statusLed.Color(0, 0, 0));
  }
}

static void setColor(uint32_t color) {
  statusLed.setPixelColor(0, color);
  statusLed.show();
}
