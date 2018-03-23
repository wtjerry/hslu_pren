void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop() {

//  Serial.println("hi");
  
  // send data only when you receive data:
  if (Serial.available() > 0) {
    //sendMsg(readMsg());
    Serial.println("hi");
    sendMsg(readMsg());
  }
}

String readMsg(){
  String msg = "";
  char c = Serial.read();
  msg += c;/*
  c = Serial.read();
  msg += c;
  c = Serial.read();
  msg += c;
  c = Serial.read();
  msg += c;*/
  return msg;
}

void sendMsg(String msg) {
  Serial.println(msg);
}
