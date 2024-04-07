#include <SPI.h>
#include <MFRC522.h>

#define LED_VALID 2
#define LED_INVALID 3
#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key defaultKey;

int block = 2;
byte readbackblock[18] = {0};
String data;
String newblockcontent;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  SPI.begin();
  mfrc522.PCD_Init();
  delay(4);
  initial();
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    int tanda = data.indexOf('=');
    if (tanda != -1) {
      String mode = data.substring(0, tanda); 
      if (mode == "WRITE") {
        detectCard();
        if (validate(block)) {
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
        if (validate(block)) {
          readCard(block, readbackblock);
          ledSukses();
        } else {
          ledGagal();
          Serial.println("Gagal2");
        }
        stopDetect();
      }
    } else {
      detectCard();
      if (validate(block)) {
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

void initial() {
  for (byte i = 0; i < 6; i++) {
    defaultKey.keyByte[i] = 0xFF;
  }
}

//untuk mematikan pendeteksian
void stopDetect() {
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

//menyalakan led gagal
void ledGagal() {
  digitalWrite(LED_INVALID, HIGH);
  delay(2000);
  digitalWrite(LED_INVALID, LOW);
}

//menyalakan led sukses
void ledSukses() {
  digitalWrite(LED_VALID, HIGH);
  delay(2000);
  digitalWrite(LED_VALID, LOW);
}

//untuk input data ke kartu
void writeCard(String newblockcontent, int blockNumber, byte arrayAddress[]) {
  byte newblockcontentBytes[newblockcontent.length() + 1];
  newblockcontent.getBytes(newblockcontentBytes, sizeof(newblockcontentBytes));
  if (writeBlock(blockNumber, newblockcontentBytes)) {
    Serial.println("Data " + newblockcontent + " berhasil dikirim ke kartu");
  }
}

//untuk membaca kartu
void readCard(int blockNumber, byte arrayAddress[]) {
  if (readBlock(blockNumber, arrayAddress)) {
    Serial.print("Data dari kartu=");
    for (int j = 0; j < 16; j++) {
      Serial.write(arrayAddress[j]);
    }
    Serial.println("");
  }
}

//untuk pendeteksian kartu pertama kali
void detectCard() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  Serial.println("Kartu terdeteksi");
  delay(50);
}

//hansip rfid
bool validate(int blockNumber) {
  int largestModulo4Number = blockNumber / 4 * 4;
  int trailerBlock = largestModulo4Number + 3;
  byte status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &defaultKey, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    return false;
  } else {
    return true;
  }
}

//Write specific block
bool writeBlock(int blockNumber, byte arrayAddress[]) {
  byte status2 = mfrc522.MIFARE_Write(blockNumber, arrayAddress, 16);
  if (status2 != MFRC522::STATUS_OK) {
    Serial.print("MIFARE_Write() failed: ");
    Serial.println(mfrc522.GetStatusCodeName(status2));
    return false;
  } else {
    return true;
  }
}

//Read specific block
bool readBlock(int blockNumber, byte arrayAddress[]) {
  byte buffersize = 18;                         
  byte status2 = mfrc522.MIFARE_Read(blockNumber, arrayAddress, &buffersize);
  if (status2 != MFRC522::STATUS_OK) {
    Serial.print("MIFARE_read() failed: ");
    Serial.println(mfrc522.GetStatusCodeName(status2));
    return false;
  } else {
    Serial.println("Membaca data dari kartu");
    return true;
  }
}