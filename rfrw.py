import pyfiglet
import serial.tools
import serial.tools.list_ports
from termcolor import colored
import serial
import time
import sys
import re
import os

textCLI = pyfiglet.figlet_format("RFIDrw")
colorTEXT = colored(textCLI, color="magenta")
arg = len(sys.argv) - 1
defPort = "COM4"
defBaudrate = 9600
defTimeout = 1
optBaudRate = [9600, 15200]
nameAPP = sys.argv[0][2:]
dig16 = "xxxxxxxxxxxxxxxx"
custOPT = f"{defPort} {defBaudrate} {defTimeout}"
dir = os.getcwd()
inpo = "Mohon tempelkan kartu"
done = "Proses selesai, silahkan lepas kartu"
fTag = "tag.h"
lokTag = f"Membuka file {fTag} pada lokasi default"

def fullBantuan():
    print(f"\n{colorTEXT}Untuk bantuan:\n  [16 digit]          - Untuk dikirimkan ke kartu rfid\n  [Port]              - Port komunikasi serial\n  [BaudRate]          - BaudRate komunikasi serial\n  [Timeout]           - Timeout komunikasi serial\n  [-D/--detect]       - Untuk mendeteksi port yang aktif\n  [-R/--read]         - Untuk membaca 16 digit pada kartu rfid\n  [-W/--write]        - Untuk menulis 16 digit pada kartu rfid\n  [-V/--verify]       - Untuk verifikasi 16 digit pada kartu rfid\n  [-T/--tagid]        - Untuk membaca informasi Tag pada kartu rfid\n  [-CM/--checkMember] - Untuk mengecek kartu mana yang memiliki akses member\n  [-UM/--updateMember]  - Untuk mengupdate akses member dari list member yang ada sebelumnya\n\nMode default:\n  python.exe {nameAPP} [-R/--read]\n  python.exe {nameAPP} [-W/--write] [16 digit]\n  python.exe {nameAPP} [-V/--verify] [16 digit]\n  python.exe {nameAPP} [-D/--detect]\n  python.exe {nameAPP} [-T/--tagid]\n  python.exe {nameAPP} [-CM/--checkMember] [Member Lama] [Member Baru]\n  python.exe {nameAPP} [-UM/--updateMember] [Member Lama] [Member Baru]")
    print(f"\nContoh Penggunaan Mode default:\n  python.exe {nameAPP} -R\n  python.exe {nameAPP} --read\n  python.exe {nameAPP} -D\n  python.exe {nameAPP} --detect\n  python.exe {nameAPP} -T\n  python.exe {nameAPP} --tagid\n  python.exe {nameAPP} -W {dig16}\n  python.exe {nameAPP} --write {dig16}\n  python.exe {nameAPP} -V {dig16}\n  python.exe {nameAPP} --verify {dig16}\n  python.exe {nameAPP} -CM\n  python.exe {nameAPP} --checkMember\n  python.exe {nameAPP} -UM '{{0x12, 0x34, 0x56, 0x78}}' '{{0x9E, 0x8D, 0xDE, 0x55}}'\n  python.exe {nameAPP} --updateMember '{{0x12, 0x34, 0x56, 0x78}}' '{{0x9E, 0x8D, 0xDE, 0x55}}'")
    print(f"\nMode custom:\n  python.exe {nameAPP} [-C/--custom] [-R/--read] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-T/--tagid] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-W/--write] [16 digit] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-V/--verify] [16 digit] [Port] [BaudRate] [Timeout]\n")
    print(f"Contoh Penggunaan Mode custom:\n  python.exe {nameAPP} -C -R {custOPT}\n  python.exe {nameAPP} -C --read {custOPT}\n  python.exe {nameAPP} -C -T {custOPT}\n  python.exe {nameAPP} -C --tagid {custOPT}\n  python.exe {nameAPP} -C -W {dig16} {custOPT}\n  python.exe {nameAPP} -C --write {dig16} {custOPT}\n  python.exe {nameAPP} -C -V {dig16} {custOPT}\n  python.exe {nameAPP} -C --verify {dig16} {custOPT}\n  python.exe {nameAPP} --custom -R {custOPT}\n  python.exe {nameAPP} --custom --read {custOPT}\n  python.exe {nameAPP} --custom -T {custOPT}\n  python.exe {nameAPP} --custom --tagid {custOPT}\n  python.exe {nameAPP} --custom -W {dig16} {custOPT}\n  python.exe {nameAPP} --custom --write {dig16} {custOPT}\n  python.exe {nameAPP} --custom -V {dig16} {custOPT}\n  python.exe {nameAPP} --custom --verify {dig16} {custOPT}\n")

def bantuan():
    print(f"\n{colorTEXT}Untuk bantuan:\n  [16 digit]          - Untuk dikirimkan ke kartu rfid\n  [Port]              - Port komunikasi serial\n  [BaudRate]          - BaudRate komunikasi serial\n  [Timeout]           - Timeout komunikasi serial\n  [-D/--detect]       - Untuk mendeteksi port yang aktif\n  [-R/--read]         - Untuk membaca 16 digit pada kartu rfid\n  [-W/--write]        - Untuk menulis 16 digit pada kartu rfid\n  [-V/--verify]       - Untuk verifikasi 16 digit pada kartu rfid\n  [-T/--tagid]        - Untuk membaca informasi Tag pada kartu rfid\n  [-FH/--fullhelp]    - Untuk detail bantuan dan penggunaannya\n  [-CM/--checkMember] - Untuk mengecek kartu mana yang memiliki akses member\n  [-UM/--updateMember]  - Untuk mengupdate akses member dari list member yang ada sebelumnya\n\nMode default:\n  python.exe {nameAPP} [-R/--read]\n  python.exe {nameAPP} [-W/--write] [16 digit]\n  python.exe {nameAPP} [-V/--verify] [16 digit]\n  python.exe {nameAPP} [-D/--detect]\n  python.exe {nameAPP} [-FH/--fullhelp]\n  python.exe {nameAPP} [-T/--tagid]\n  python.exe {nameAPP} [-CM/--checkMember] [Member Lama] [Member Baru]\n  python.exe {nameAPP} [-UM/--updateMember] [Member Lama] [Member Baru]")
    print(f"\nMode custom:\n  python.exe {nameAPP} [-C/--custom] [-R/--read] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-W/--write] [16 digit] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-V/--verify] [16 digit] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-T/--tagid] [Port] [BaudRate] [Timeout]\n")

def info():
    print(f"\nUntuk bantuan:\n  python.exe {nameAPP} -H\n  python.exe {nameAPP} --help\n  python.exe {nameAPP} -FH\n  python.exe {nameAPP} --fullhelp\n")
    
def cekMemberCard(*args):
    if len(args) == 1:
        path = f"{dir}\\rfid\\{args[0]}"
        if os.path.exists(path):
            with open(path, 'r') as file:
                memberFile = file.read()
            
            hasil = re.findall(r'0x[0-9A-Fa-f]{2}',memberFile)
            if hasil != 0:
                print(f"Terdapat data kartu yang sudah mendapatkan akses member\nBerikut list array byte pada file {args[0]}")
                for i in range(0, len(hasil), 4):
                    member = ", ".join([elem for elem in hasil[i:i+4]])
                    print("- {"+member+"}")
                print("")
            else:
                print(f"Tidak ditemukan kartu yang memiliki akses member, silahkan cek pada file {args[0]}\nSelanjutnya cek dibagian memberTag untuk cek detail akses member\n")
        else:
            print(f"File {args[0]} tidak ditemukan\n")
    elif len(args) == 3:
        _doc, _memberLama, _memberBaru = args
        _temp = "tagNew.h"
        defpath = f"{dir}\\rfid\\{_doc}"
        newpath = f"{dir}\\rfid\\{_temp}"
        if os.path.exists(defpath):
            with open(defpath) as r: 
                text = r.read().replace(f"{_memberLama}", f"{_memberBaru}")
            with open(newpath, "w") as w:
                w.write(text)
            os.remove(defpath)
            os.rename(newpath, defpath)
            if os.path.exists(defpath):
                print(f"Berhasil merubah akses member dari {_memberLama} ke {_memberBaru} pada file {_doc}")
                print(f"Silahkan upload file {_doc} ke arduino untuk memperbaharui akses kartu member\n")
            else:
                print(f"Proses merubah akses member dari {_memberLama} ke {_memberBaru} pada file {_doc} gagal, silahkan coba lagi\n")
        else:
            print(f"File {_doc} tidak ditemukan\n")

def kirimData(*args):
    if len(args) == 2:
        _ket = "sedang berjalan, lepas kartu apabila proses sudah selesai"
        conn, command = args
        if "=" in command:
            aa = command.split("=")
            print(f"Mode {aa[0].lower()} {_ket}")
        else:
            print(f"Mode {command[:-1].lower()} {_ket}")
        conn.write(command.encode())
        time.sleep(0.1)

def detectPort():
    detectPORT = serial.tools.list_ports.comports(include_links=False)
    print("\nBerikut list port yang terdeteksi:")
    for port in detectPORT :
        print(f"- {port.device}")
    print("")

def writeCard(*args):
    try:
        _data, _port, _baudRate, _timeOut = args
        serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
        time.sleep(2)
        print(f"{inpo}")
        kirimData(serialComm, f"WRITE={_data}\n")
        while True:
            arduino = serialComm.readline().decode().strip()
            if "Gagal1" in arduino:
                print("Gagal menulis data ke kartu, mohon tunggu sebentar.\nApabila masih belum terdeteksi, silahkan cobalagi")
            elif arduino:
                print(arduino)
            else:
                break
    except serial.serialutil.SerialException:
        print(f"Port default adalah port {defPort} tidak tersedia\nSilahkan gunakan mode custom port dan lakukan pendeteksian port yang tersedia")
    print(f"{done}\n")

def readTag(*args):
    try:
        _port, _baudRate, _timeOut = args
        serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
        time.sleep(2)
        print(f"{inpo}")
        kirimData(serialComm, f"TAG\n")
        while True:
            arduino = serialComm.readline().decode().strip()
            if "=" in arduino:
                temp = re.split(r'=', arduino)
                print(f"{temp[0]}: {temp[1]}")
                print(f"Array Byte {temp[0]}: {temp[2]}")
            elif "Gagal4" in arduino:
                print("Gagal membaca data dari kartu, mohon tunggu sebentar.\nApabila masih belum terdeteksi, silahkan cobalagi")
            elif arduino:
                print(arduino)
            else:
                break
    except serial.serialutil.SerialException:
        print(f"Port default adalah port {defPort} tidak tersedia\nSilahkan gunakan mode custom port dan lakukan pendeteksian port yang tersedia")
    print(f"{done}\n")

def readCard(*args):
    try:
        _port, _baudRate, _timeOut = args
        serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
        time.sleep(2)
        print(f"{inpo}")
        kirimData(serialComm, f"READ\n")
        while True:
            arduino = serialComm.readline().decode().strip()
            if "=" in arduino:
                temp = re.split(r'=', arduino)
                print(temp[0], temp[1])
            elif "Gagal3" in arduino:
                print("Gagal membaca data dari kartu, mohon tunggu sebentar.\nApabila masih belum terdeteksi, silahkan cobalagi")
            elif arduino:
                print(arduino)
            else:
                break
    except serial.serialutil.SerialException:
        print(f"Port default adalah port {defPort} tidak tersedia\nSilahkan gunakan mode custom port dan lakukan pendeteksian port yang tersedia")
    print(f"{done}\n")

def verifyCard(*args):
    try:
        _data, _port, _baudRate, _timeOut = args
        _ket = "Data dari kartu dengan yang diinputkan"
        serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
        time.sleep(2)
        print(f"{inpo}")
        kirimData(serialComm, f"VERIFY={_data}\n")
        while True:
            arduino = serialComm.readline().decode().strip()
            if "=" in arduino:
                temp = re.split(r'=', arduino)
                print(temp[0], temp[1])
                print(f"Data dari inputan {_data}")
                if temp[1] == _data:
                    print(f"{_ket} valid")
                else:
                    print(f"{_ket} tidak valid")
            elif "Gagal2" in arduino:
                print("Gagal verifikasi data dari kartu dan inputan, mohon tunggu sebentar.\nApabila masih belum terdeteksi, silahkan cobalagi")
            elif arduino:
                print(arduino)
            else:
                break
    except serial.serialutil.SerialException:
        print(f"Port default adalah port {defPort} tidak tersedia\nSilahkan gunakan mode custom port dan lakukan pendeteksian port yang tersedia")
    print(f"{done}\n")

def custom(*args):
    if len(args) == 5:
        _mode, _data, _port, _baudrate, _timeout = args
        if _mode in ["-W", "--write"]:
            print(f"\nMode Custom Write")
            writeCard(_data, _port, _baudrate, _timeout)
        elif _mode in ["-V", "--verify"]:
            print(f"\nMode Custom Verify")
            verifyCard(_data, _port, _baudrate, _timeout)
    else:
        _mode, _port, _baudrate, _timeout = args
        if _mode in ["-R", "--read"]:
            print(f"\nMode Custom Read")
            readCard(_port, _baudrate, _timeout)
        elif _mode in ["-T", "--tagid"]:
            print(f"\nMode Custom Tag")
            readTag(_port, _baudrate, _timeout)

if arg == 0:
    info()
elif arg == 1:
    mode = sys.argv[1]
    if mode in ["-R", "--read"]:
        print("\nMode Read")
        readCard(defPort, defBaudrate, defTimeout)
    elif mode in ["-T", "--tagid"]:
        print("\nMode Tag")
        readTag(defPort, defBaudrate, defTimeout)
    elif mode in ["-H", "--help"]:
        bantuan()
    elif mode in ["-FH", "--fullhelp"]:
        fullBantuan()
    elif mode in ["-D", "--detect"]:
        detectPort()
    elif mode in ["-CM", "--checkMember"]:
        print("\nMode CekMember")
        print(f"{lokTag}")
        cekMemberCard(fTag)
    else:
        info()
elif arg > 1 and arg < 7:
    mode = sys.argv[1]
    data = sys.argv[2]
    if mode in ["-W", "--write"] and len(data) == 16:
        print("\nMode Write")
        writeCard(data, defPort, defBaudrate, defTimeout)
    elif mode in ["-UM", "--updateMember"]:
        if arg == 3:
            mLama = sys.argv[2]
            mBaru = sys.argv[3]
            print("\nMode UpdateMember")
            print(f"{lokTag}")
            cekMemberCard(fTag, mLama, mBaru)
    elif mode in ["-V", "--verify"] and len(data) == 16:
        print("\nMode Verify")
        verifyCard(data, defPort, defBaudrate, defTimeout)
    elif mode in ["-C", "--custom"] and arg == 6:
        subMode = sys.argv[2]
        customData = sys.argv[3]
        pOrt = sys.argv[4]
        baudRate = sys.argv[5]
        timeOut = sys.argv[6]
        if subMode in ["-W", "--write", "-V", "--verify"] and len(customData) == 16 and "COM" in pOrt and baudRate.isdigit() and int(baudRate) in optBaudRate and timeOut.isdigit():
            custom(subMode, customData, pOrt, baudRate, timeOut)
        else:
            info()
    elif mode in ["-C", "--custom"] and arg == 5:
        subMode = sys.argv[2]
        pOrt = sys.argv[3]
        baudRate = sys.argv[4]
        timeOut = sys.argv[5]
        if subMode in ["-R", "--read", "-T", "--tagid"] and "COM" in pOrt and baudRate.isdigit() and int(baudRate) in optBaudRate and timeOut.isdigit():
            custom(subMode, pOrt, baudRate, timeOut)
        else:
            info()
    else:
        info()
else:
    info()