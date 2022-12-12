/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;

void request(String path, char out[256]){
  if ((WiFiMulti.run() != WL_CONNECTED)) return;
  HTTPClient http;
  WiFiClient client;
  if (http.begin(client, "http://192.168.137.20:1234" + path)) {  // HTTP

    int httpCode = http.GET();
    if (httpCode > 0) {
      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
        String payload = http.getString();
        strcpy(out, payload.c_str());
      }
    } else {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  } else {
    Serial.printf("[HTTP] Unable to connect\n");
  }
}

int b_light_on = true;
int id = 0;
int pot=A0;
int ledpin=D3;
int photo=D6;

void setup() {

  Serial.begin(115200);
  //Serial.setDebugOutput(true);

  pinMode(ledpin,OUTPUT);
  pinMode(photo,OUTPUT);
  pinMode(pot, INPUT);

  digitalWrite(photo, LOW);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("cheloo", "croibossu");

  char resp[256];
  request("/add_room", resp);

  request("/getid", resp);
  id = String(resp).toInt() + 1;
  
}

void should_turn_off(){
  char res[256];
  request("/get_close_list", res);
  String sid(id);
  Serial.println(sid);
  String sres(res);
  Serial.println(res);
  Serial.println(sid.toInt() == sres.toInt());
  if(sid.toInt() == sres.toInt()){
    b_light_on = false;
    request("/clear_rooms", res);
  }else{
    b_light_on = true;
  }
}


int pot_val;

void control_loop(){
  should_turn_off();
  // Serial.println(b_light_on);

  pot_val = analogRead(pot);
  pot_val = map(pot_val,0,1023,0,2);

  

  if(b_light_on){
    digitalWrite(ledpin, HIGH);
    // digitalWrite(photo, HIGH);
  }else{
    digitalWrite(ledpin, LOW);
    // digitalWrite(photo, HIGH);
    Serial.println("ROOM SHUT DOWN");
  }
}

void loop(){

  if(pot_val == 2)
  {
    pot_val = analogRead(pot);
    //digitalWrite(ledpin,HIGH);
    Serial.print(pot_val);
    Serial.print(' ');
    pot_val = map(pot_val,0,1023,0,2);
    Serial.println(pot_val);
    digitalWrite(ledpin,HIGH);

    b_light_on = true;
  }
  else if(pot_val == 0)
  {
    pot_val = analogRead(pot);
    //digitalWrite(ledpin,HIGH);
    Serial.print(pot_val);
    Serial.print(' ');
    pot_val = map(pot_val,0,1023,0,2);
    Serial.println(pot_val);
    digitalWrite(ledpin,LOW);

    b_light_on = false;
  }
  else if(pot_val == 1)
  {
    control_loop();
  }
  

  delay(100);
}
