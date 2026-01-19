int ldrPin = 12;   
int irPins[] = {A0, A1, A2, A3, A4, A5, 10, 11};
int leds[] = {2, 3, 4, 5, 6, 7, 8, 9};
int totalSensors = 8;

unsigned long ledOffTime[8];      
const long interval = 15000;      

int irCounts[8] = {0,0,0,0,0,0,0,0};
bool lastIrState[8] = {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};
bool lastLedState[8] = {false,false,false,false,false,false,false,false};
int lastLdr = -1;

void setup() {
  Serial.begin(9600);
  pinMode(ldrPin, INPUT);
  
  for (int i = 0; i < totalSensors; i++) {
    pinMode(irPins[i], INPUT);
    pinMode(leds[i], OUTPUT);
    ledOffTime[i] = 0;
  }
}

void loop() {
  int ldrState = digitalRead(ldrPin);
  unsigned long currentTime = millis();

  if (ldrState != lastLdr) {
    Serial.print("LDR:"); Serial.println(ldrState == HIGH ? "DAY" : "NIGHT"); 
    lastLdr = ldrState;
  }

  if (ldrState == HIGH) { 
    for (int i = 0; i < totalSensors; i++) {
      digitalWrite(leds[i], LOW);
      ledOffTime[i] = 0;
      if (lastLedState[i]) {
         Serial.print("LED:"); Serial.print(i); Serial.println(":OFF");
         lastLedState[i] = false;
      }
    }
  } else { 
    for (int pos = 0; pos < totalSensors; pos++) {
      int reading = digitalRead(irPins[pos]);
      
      if (reading == LOW && lastIrState[pos] == HIGH) {
        irCounts[pos]++;
        Serial.print("IR_COUNT:"); Serial.print(pos); Serial.print(":"); Serial.println(irCounts[pos]);
        
        if (pos - 1 >= 0)           ledOffTime[pos - 1] = currentTime + interval;
        ledOffTime[pos]             = currentTime + interval;
        if (pos + 1 < totalSensors) ledOffTime[pos + 1] = currentTime + interval;
        if (pos + 2 < totalSensors) ledOffTime[pos + 2] = currentTime + interval;
      }
      lastIrState[pos] = reading;
    }

    for (int i = 0; i < totalSensors; i++) {
      bool shouldBeOn = (currentTime < ledOffTime[i]);
      digitalWrite(leds[i], shouldBeOn ? HIGH : LOW);
      
      if (shouldBeOn != lastLedState[i]) {
        Serial.print("LED:"); Serial.print(i); Serial