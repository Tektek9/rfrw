#ifndef TAG_H
#define TAG_H

class Tags {
  public:
    static const byte memberTag1[4];
    static const byte memberTag2[4];
    static const byte memberTag3[4];
};

//ISIKAN DIBAWAH INI UNTUK MENDAPATKAN AKSES MEMBER
const byte Tags::memberTag1[4] = {0xFF, 0xFF, 0xFF, 0xFF}; //Copy kan disini untuk array byte dari mode tag, dan aktifkan
const byte Tags::memberTag2[4] = {0x9E, 0x8D, 0xDE, 0x55}; //Copy kan disini untuk array byte dari mode tag, dan aktifkan
const byte Tags::memberTag3[4] = {0x52, 0x40, 0x85, 0xED}; //Copy kan disini untuk array byte dari mode tag, dan aktifkan

#endif