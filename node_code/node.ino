#define BAUDRATE 9600
#define DELAY 1000

void setup() {
	Serial.begin(BAUDRATE);
}

void loop() {
	// TODO read some data and build json to send
	Serial.println("{"test": "Hello World"}");
	delay(DELAY);
}