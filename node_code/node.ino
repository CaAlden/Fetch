#include <SoftwareSerial.h>

#define BAUDRATE 9600
#define DELAY 1000
#define LED_PIN 10
#define STATUS_LED 12

SoftwareSerial gpsSerial(5, 6); // RX, TX
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

	pinMode(LED_PIN, OUTPUT); // red LED
	pinMode(STATUS_LED, OUTPUT);
}

void loop() {

	triggerLed();
	readXbee();	
	triggerLed();
	readGPS();
	triggerLed();
	sendXbeeMessage();
	triggerLed();
	delay(DELAY);
}

void sendXbeeMessage() {
	# send json with node number and gpscoordinates
	Serial.println("{\"node\":\"" + NODE_NUMBER + "\", \"gps\":\"" + gpsString + "\"}");
}

void readXbee() {
	xbeeString = "";
	Serial.listen()

	if (Serial.available() > 0) {
		char nextChar = Serial.read();
		xbeeString += nextChar;
	}
}

void readGPS() {
	gpsString = "";
	gpsSerial.listen()

	if (gpsSerial.available() > 0) {
		char nextChar = gpsSerial.read();
		if (char != '\n') {
			gpsString += nextChar;
		}
	}
	
}

void triggerLed() {
	digitalWrite(STATUS_LED,(ledState) ? HIGH : LOW);
	ledState = !ledState;
}