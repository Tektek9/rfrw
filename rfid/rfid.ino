#include <SPI.h>
#include <MFRC522.h>
#include "tag.h"
#include "pins.h"
#include "func.h"

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key defaultKey;

int block = 2;
byte readbackblock[18] = { 0 };
String data;String newblockcontent;

void setup() {
  Serial.begin(9600);
  while (!Serial)
    ;
  SPI.begin();
  mfrc522.PCD_Init();
  delay(4);
  for (byte i = 0; i < 6; i++) {
    defaultKey.keyByte[i] = 0xFF;
  }
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    int tanda = data.indexOf('=');
    if (tanda != -1) {
      String mode = data.substring(0, tanda);
      if (mode == "WRITE") {
        detectCard();
        if (validate(block && isMember())) {
          String newblockcontent = data.substring(tanda + 1);
          writeCard(newblockcontent, block, readbackblock);
          ledSukses();
        } else {
          ledGagal();
          Serial.println("Gagal1");
        }
        stopDetect();
      } else if (mode == "VERIFY") {
        detectCard();
        if (validate(block && isMember())) {
          readCard(block, readbackblock);
          ledSukses();
        } else {
          ledGagal();
          Serial.println("Gagal2");
        }
        stopDetect();
      }
    } else if (data == "TAG") {
      detectCard();
      if (validate(block)) {
        readTag();
        ledSukses();
      } else {
        ledGagal();
        Serial.println("Gagal4");
      }
      stopDetect();
    } else if (data == "READ") {
      detectCard();
      if (validate(block) && isMember()) {
        readCard(block, readbackblock);
        ledSukses();
      } else {
        ledGagal();
        Serial.println("Gagal3");
      }
      stopDetect();
    }
    delay(1000);
  }
}