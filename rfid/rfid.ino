#include <SPI.h>
#include <MFRC522.h>

#define LED_VALID 2
#define LED_INVALID 3
#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key defaultKey;

int block = 2;
byte readbackblock[18] = { 0 };
String data;
String newblockcontent;

//ISIKAN DIBAWAH INI UNTUK MENDAPATKAN AKSES MEMBER
byte memberTag1[] = {0xD9, 0x3A, 0xE9, 0x56}; //Copy kan disini untuk array byte dari mode tag, dan aktifkan
byte memberTag2[] = {0x9E, 0x8D, 0xDE, 0x55}; //Copy kan disini untuk array byte dari mode tag, dan aktifkan
byte memberTag3[] = {0xAA, 0xFD, 0xDF, 0xFF}; //Copy kan disini untuk array byte dari mode tag, dan aktifkan

void setup() {
  Serial.begin(9600);
  while (!Serial)
    ;
  SPI.begin();
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

void initial() {
  mfrc522.PCD_Init();
  delay(4);
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

//penjaga
bool hanSIP(byte uid[]) {
  if (memcmp(uid, memberTag1, 4) == 0) {
    return true;
  }
  return false;
  if (memcmp(uid, memberTag2, 4) == 0) {
    return true;
  }
  return false;
  if (memcmp(uid, memberTag3, 4) == 0) {
    return true;
  }
  return false;
}

//membaca informasi tag kartu rfid dan mengirim array byte yang nanti bisa digunakan untuk diisikan ulang di kode arduino ini untuk terdaftar sebagai member
void readTag() {
  Serial.print("Tag UID=");
  String tagID = "";
  String spasiID = "";
  String penanda = "";

  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagID += String(mfrc522.uid.uidByte[i], HEX);
  }

  for (int i = 0; i < tagID.length(); i += 2) {
    spasiID += tagID.substring(i, i + 2);
    spasiID += " ";
  }

  for (int i = 0; i < spasiID.length(); i++) {
    spasiID[i] = toupper(spasiID[i]);
  }

  spasiID.trim();
  Serial.print(spasiID);
  Serial.print("={");
  for (int x = 0; x < tagID.length(); x += 2) {
    String byteID = tagID.substring(x, x + 2);

    for (int y = 0; y < byteID.length(); y++) {
      byteID[y] = toupper(byteID[y]);
    }

    if (byteID.length() == 1) {
      byteID = "0" + byteID;
    }

    penanda += "0x" + byteID;

    if (x + 2 < tagID.length()) {
      penanda += ", ";
    }
  }

  Serial.print(penanda);
  Serial.println("}");
}

//Untuk input data ke kartu
void writeCard(String newblockcontent, int blockNumber, byte arrayAddress[]) {
  byte newblockcontentBytes[newblockcontent.length() + 1];
  newblockcontent.getBytes(newblockcontentBytes, sizeof(newblockcontentBytes));
  if (writeBlock(blockNumber, newblockcontentBytes)) {
    Serial.println("Data " + newblockcontent + " berhasil dikirim ke kartu");
  }
}

//Untuk membaca kartu
void readCard(int blockNumber, byte arrayAddress[]) {
  if (readBlock(blockNumber, arrayAddress)) {
    Serial.print("Data dari kartu=");
    for (int j = 0; j < 16; j++) {
      Serial.write(arrayAddress[j]);
    }
    Serial.println("");
  }
}

//Untuk pendeteksian kartu pertama kali
void detectCard() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  Serial.println("Kartu terdeteksi");
  delay(50);
}

//Untuk cek member atau bukan
bool isMember() {
  if (hanSIP(mfrc522.uid.uidByte)) {
    Serial.println("Kartu anda sudah terdaftar sebagai member");
    return true;
  } else {
    Serial.println("Kartu anda belum terdaftar sebagai member");
    Serial.println("Silahkan lakukan mode tag, lalu lakukan mode cek member");
    Serial.println("Selanjutnya lakukan update member, untuk memperbaharui akses member");
    return false;
  }
}

//Validasi deteksi kartu rfid
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