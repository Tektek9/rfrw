#include <SPI.h>
#include "pins.h"
#include "handler.h"

Pins pins;
Handlers handler;
MFRC522 mfrc522(pins.SS_PIN, pins.RST_PIN);

int block = 2;
byte readbackblock[18] = { 0 };
String data;
String newblockcontent;

void setup() {
  Serial.begin(9600);
  while (!Serial)
    ;
  SPI.begin();
  mfrc522.PCD_Init();
  delay(4);
  for (byte i = 0; i < 6; i++) {
    handler.defaultKey.keyByte[i] = 0xFF;
  }
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    int tanda = data.indexOf('=');
    if (tanda != -1) {
      String mode = data.substring(0, tanda);
      if (mode == "WRITE") {
        handler.detectCard();
        if (handler.validate(block && handler.isMember())) {
          String newblockcontent = data.substring(tanda + 1);
          handler.writeCard(newblockcontent, block, readbackblock);
          handler.ledSukses();
        } else {
          handler.ledGagal();
          Serial.println("Gagal1");
        }
        handler.stopDetect();
      } else if (mode == "VERIFY") {
        handler.detectCard();
        if (handler.validate(block && handler.isMember())) {
          handler.readCard(block, readbackblock);
          handler.ledSukses();
        } else {
          handler.ledGagal();
          Serial.println("Gagal2");
        }
        handler.stopDetect();
      }
    } else if (data == "TAG") {
      handler.detectCard();
      if (handler.validate(block)) {
        handler.readTag();
        handler.ledSukses();
      } else {
        handler.ledGagal();
        Serial.println("Gagal4");
      }
      handler.stopDetect();
    } else if (data == "READ") {
      handler.detectCard();
      if (handler.validate(block) && handler.isMember()) {
        handler.readCard(block, readbackblock);
        handler.ledSukses();
      } else {
        handler.ledGagal();
        Serial.println("Gagal3");
      }
      handler.stopDetect();
    }
    delay(1000);
  }
}