#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

#define BAUDRATE 9600
#define DELAY 1000
#define STATUS_LED 12
#define REST 0
#define READ_XBEE 1
#define READ_GPS 2
#define SEND_XBEE 3

SoftwareSerial gpsSerial = SoftwareSerial(5, 6); // RX, TX
Adafruit_NeoPixel statusLed = Adafruit_NeoPixel(1, STATUS_LED, NEO_GRB)

char ledState;
String gpsString;
String xbeeString;

#define NODE_NUMBER 1 //change this manually for each node :(

void setup() {
	// open up serial communication
	Serial.begin(BAUDRATE);

	while (!Serial) {
		; // wait for serial port to connect. Needed for native USB port only
	}

	gpsSerial.begin(BAUDRATE);
	gpsSerial.write(0xFF);

	statusLed.begin()
	triggerLed(0)
}

void loop() {

	triggerLed(1);
	readXbee();	
	triggerLed(2);
	readGPS();
	triggerLed(3);
	sendXbeeMessage();
	triggerLed(0);
	delay(DELAY);
}

static void sendXbeeMessage() {
	# send json with node number and gpscoordinates
	Serial.println("{\"node\":\"" + NODE_NUMBER + "\", \"gps\":\"" + gpsString + "\"}");
}

static void readXbee() {
	xbeeString = "";
	Serial.listen()

	if (Serial.available() > 0) {
		char nextChar = Serial.read();
		while(nextChar != '\n' && Serial.available() > 0) {
			xbeeString += nextChar;
			nextChar = Serial.read();
		}
	}
}

static void readGPS() {
	gpsString = "";
	gpsSerial.listen()

	if (gpsSerial.available() > 0) {
		char nextChar = gpsSerial.read();
		while (nextChar != '\n' && gpsSerial.available() > 0) {
			gpsString += nextChar;
			nextChar = gpsSerial.read();
		}
	}
	
}

static void triggerLed(int state) {
	if (state == REST) {
		setColor(statusLed.Color(0, 0, 0));
	} else if (state == READ_XBEE) {
		setColor(statusLed.Color(0, 255, 0));
	} else if (state == READ_GPS) {
		setColor(statusLed.Color(0, 255, 100));
	} else if (state == SEND_XBEE) {
		setColor(statusLed.Color(255, 0, 0));
	}
}

static void setColor(uint32_t color) {
    for (uint16_t i = 0; i < triangle.numPixels()+4; i++) {
      statusLed.setPixelColor(i, color);
    }
    statusLed.show();
}
