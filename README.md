# rfrw
RFID 
- read data
- write data
- verify data
- read tag
- rfid auth
- detection port
- custom serial configuration
- check member
- update member

Langkah installasi
```
pip install -r requirements.txt
```
Untuk bantuan
```
Untuk bantuan:
  [16 digit]            - Untuk dikirimkan ke kartu rfid
  [Port]                - Port komunikasi serial
  [BaudRate]            - BaudRate komunikasi serial
  [Timeout]             - Timeout komunikasi serial
  [-D/--detect]         - Untuk mendeteksi port yang aktif
  [-R/--read]           - Untuk membaca 16 digit pada kartu rfid
  [-W/--write]          - Untuk menulis 16 digit pada kartu rfid
  [-V/--verify]         - Untuk verifikasi 16 digit pada kartu rfid
  [-T/--tagid]          - Untuk membaca informasi Tag pada kartu rfid
  [-FH/--fullhelp]      - Untuk detail bantuan dan penggunaannya
  [-CM/--checkMember]   - Untuk mengecek kartu mana yang memiliki akses member
  [-UM/--updateMember]  - Untuk mengupdate akses member dari list member yang ada sebelumnya

Mode default:
  python.exe rfrw.py [-R/--read]
  python.exe rfrw.py [-W/--write] [16 digit]
  python.exe rfrw.py [-V/--verify] [16 digit]
  python.exe rfrw.py [-D/--detect]
  python.exe rfrw.py [-FH/--fullhelp]
  python.exe rfrw.py [-T/--tagid]
  python.exe rfrw.py [-CM/--checkMember] [Member Lama] [Member Baru]
  python.exe rfrw.py [-UM/--updateMember] [Member Lama] [Member Baru]

Mode custom:
  python.exe rfrw.py [-C/--custom] [-R/--read] [Port] [BaudRate] [Timeout]
  python.exe rfrw.py [-C/--custom] [-W/--write] [16 digit] [Port] [BaudRate] [Timeout]
  python.exe rfrw.py [-C/--custom] [-V/--verify] [16 digit] [Port] [BaudRate] [Timeout]
  python.exe rfrw.py [-C/--custom] [-T/--tagid] [Port] [BaudRate] [Timeout]
```

Untuk bantuan yang lebih detail
```
Untuk bantuan:
  [16 digit]            - Untuk dikirimkan ke kartu rfid
  [Port]                - Port komunikasi serial
  [BaudRate]            - BaudRate komunikasi serial
  [Timeout]             - Timeout komunikasi serial
  [-D/--detect]         - Untuk mendeteksi port yang aktif
  [-R/--read]           - Untuk membaca 16 digit pada kartu rfid
  [-W/--write]          - Untuk menulis 16 digit pada kartu rfid
  [-V/--verify]         - Untuk verifikasi 16 digit pada kartu rfid
  [-T/--tagid]          - Untuk membaca informasi Tag pada kartu rfid
  [-CM/--checkMember]   - Untuk mengecek kartu mana yang memiliki akses member
  [-UM/--updateMember]  - Untuk mengupdate akses member dari list member yang ada sebelumnya

Mode default:
  python.exe rfrw.py [-R/--read]
  python.exe rfrw.py [-W/--write] [16 digit]
  python.exe rfrw.py [-V/--verify] [16 digit]
  python.exe rfrw.py [-D/--detect]
  python.exe rfrw.py [-T/--tagid]
  python.exe rfrw.py [-CM/--checkMember] [Member Lama] [Member Baru]
  python.exe rfrw.py [-UM/--updateMember] [Member Lama] [Member Baru]

Contoh Penggunaan Mode default:
  python.exe rfrw.py -R
  python.exe rfrw.py --read
  python.exe rfrw.py -D
  python.exe rfrw.py --detect
  python.exe rfrw.py -T
  python.exe rfrw.py --tagid
  python.exe rfrw.py -W xxxxxxxxxxxxxxxx
  python.exe rfrw.py --write xxxxxxxxxxxxxxxx
  python.exe rfrw.py -V xxxxxxxxxxxxxxxx
  python.exe rfrw.py --verify xxxxxxxxxxxxxxxx
  python.exe rfrw.py -CM
  python.exe rfrw.py --checkMember
  python.exe rfrw.py -UM '{0x12, 0x34, 0x56, 0x78}' '{0x9E, 0x8D, 0xDE, 0x55}'
  python.exe rfrw.py --updateMember '{0x12, 0x34, 0x56, 0x78}' '{0x9E, 0x8D, 0xDE, 0x55}'

Mode custom:
  python.exe rfrw.py [-C/--custom] [-R/--read] [Port] [BaudRate] [Timeout]
  python.exe rfrw.py [-C/--custom] [-T/--tagid] [Port] [BaudRate] [Timeout]
  python.exe rfrw.py [-C/--custom] [-W/--write] [16 digit] [Port] [BaudRate] [Timeout]
  python.exe rfrw.py [-C/--custom] [-V/--verify] [16 digit] [Port] [BaudRate] [Timeout]

Contoh Penggunaan Mode custom:
  python.exe rfrw.py -C -R COM4 9600 1
  python.exe rfrw.py -C --read COM4 9600 1
  python.exe rfrw.py -C -T COM4 9600 1
  python.exe rfrw.py -C --tagid COM4 9600 1
  python.exe rfrw.py -C -W xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py -C --write xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py -C -V xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py -C --verify xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py --custom -R COM4 9600 1
  python.exe rfrw.py --custom --read COM4 9600 1
  python.exe rfrw.py --custom -T COM4 9600 1
  python.exe rfrw.py --custom --tagid COM4 9600 1
  python.exe rfrw.py --custom -W xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py --custom --write xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py --custom -V xxxxxxxxxxxxxxxx COM4 9600 1
  python.exe rfrw.py --custom --verify xxxxxxxxxxxxxxxx COM4 9600 1
```

