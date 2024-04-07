import pyfiglet
import serial.tools
import serial.tools.list_ports
from termcolor import colored
import serial
import time
import sys
import re

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

def fullBantuan():
    print(f"\n{colorTEXT}Untuk bantuan:\n  [16 digit]    - Untuk dikirimkan ke kartu rfid\n  [Port]        - Port komunikasi serial\n  [BaudRate]    - BaudRate komunikasi serial\n  [Timeout]     - Timeout komunikasi serial\n  [-D/--detect] - Untuk mendeteksi port yang aktif\n  [-R/--read]   - Untuk membaca 16 digit pada kartu rfid\n  [-W/--write]  - Untuk menulis 16 digit pada kartu rfid\n  [-V/--verify] - Untuk verifikasi 16 digit pada kartu rfid\n\nMode default:\n  python.exe {nameAPP} [-R/--read]\n  python.exe {nameAPP} [-W/--write] [16 digit]\n  python.exe {nameAPP} [-V/--verify] [16 digit]")
    print(f"\nContoh Penggunaan Mode default:\n  python.exe {nameAPP} -R\n  python.exe {nameAPP} --read\n  python.exe {nameAPP} -W {dig16}\n  python.exe {nameAPP} --write {dig16}\n  python.exe {nameAPP} -V {dig16}\n  python.exe {nameAPP} --verify {dig16}")
    print(f"\nMode custom:\n  python.exe {nameAPP} [-C/--custom] [-R/--read] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-W/--write] [16 digit] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-V/--verify] [16 digit] [Port] [BaudRate] [Timeout]\n")
    print(f"Contoh Penggunaan Mode custom:\n  python.exe {nameAPP} -C -R {custOPT}\n  python.exe {nameAPP} -C --read {custOPT}\n  python.exe {nameAPP} -C -W {dig16} {custOPT}\n  python.exe {nameAPP} -C --write {dig16} {custOPT}\n  python.exe {nameAPP} -C -V {dig16} {custOPT}\n  python.exe {nameAPP} -C --verify {dig16} {custOPT}\n  python.exe {nameAPP} --custom -R {custOPT}\n  python.exe {nameAPP} --custom --read {custOPT}\n  python.exe {nameAPP} --custom -W {dig16} {custOPT}\n  python.exe {nameAPP} --custom --write {dig16} {custOPT}\n  python.exe {nameAPP} --custom -V {dig16} {custOPT}\n  python.exe {nameAPP} --custom --verify {dig16} {custOPT}\n")
    
def bantuan():
    print(f"\n{colorTEXT}Untuk bantuan:\n  [16 digit]       - Untuk dikirimkan ke kartu rfid\n  [Port]           - Port komunikasi serial\n  [BaudRate]       - BaudRate komunikasi serial\n  [Timeout]        - Timeout komunikasi serial\n  [-D/--detect]    - Untuk mendeteksi port yang aktif\n  [-R/--read]      - Untuk membaca 16 digit pada kartu rfid\n  [-W/--write]     - Untuk menulis 16 digit pada kartu rfid\n  [-V/--verify]    - Untuk verifikasi 16 digit pada kartu rfid\n  [-FH/--fullhelp] - Untuk detail bantuan dan penggunaannya\n\nMode default:\n  python.exe {nameAPP} [-R/--read]\n  python.exe {nameAPP} [-W/--write] [16 digit]\n  python.exe {nameAPP} [-V/--verify] [16 digit]\n  python.exe {nameAPP} [-FH/--fullhelp]")
    print(f"\nMode custom:\n  python.exe {nameAPP} [-C/--custom] [-R/--read] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-W/--write] [16 digit] [Port] [BaudRate] [Timeout]\n  python.exe {nameAPP} [-C/--custom] [-V/--verify] [16 digit] [Port] [BaudRate] [Timeout]\n")

def kirimData(*args):
    if len(args) == 2:
        conn, command = args
        if "=" in command:
            aa = command.split("=")
            print(f"Mode {aa[0].lower()} sedang berjalan, lepas kartu apabila proses sudah selesai")
        else:
            print(f"Mode {command[:-1].lower()} sedang berjalan, lepas kartu apabila proses sudah selesai")
        conn.write(command.encode())
        time.sleep(0.1)

def detectPort():
    detectPORT = serial.tools.list_ports.comports(include_links=False)
    print("\nBerikut list port yang terdeteksi:")
    for port in detectPORT :
        print(f"- {port.device}")
    print("")

def writeCard(*args):
    _data, _port, _baudRate, _timeOut = args
    serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
    time.sleep(2)
    print("Mohon tempelkan kartu")
    kirimData(serialComm, f"WRITE={_data}\n")
    while True:
        arduino = serialComm.readline().decode().strip()
        if "Gagal1" in arduino:
            print("Gagal menulis data ke kartu, mohon tunggu sebentar.\nApabila masih belum terdeteksi, silahkan cobalagi")
        elif arduino:
            print(arduino)
        else:
            break
    print("Proses selesai, silahkan lepas kartu\n")

def readCard(*args):
    _port, _baudRate, _timeOut = args
    serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
    time.sleep(2)
    print("Mohon tempelkan kartu")
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
    print("Proses selesai, silahkan lepas kartu\n")

def verifyCard(*args):
    _data, _port, _baudRate, _timeOut = args
    serialComm = serial.Serial(port=str(_port), baudrate=int(_baudRate), timeout=int(_timeOut))
    time.sleep(2)
    print("Mohon tempelkan kartu")
    kirimData(serialComm, f"VERIFY={_data}\n")
    while True:
        arduino = serialComm.readline().decode().strip()
        if "=" in arduino:
            temp = re.split(r'=', arduino)
            print(temp[0], temp[1])
            print(f"Data dari inputan {_data}")
            if temp[1] == _data:
                print("Data dari kartu dengan yang diinputkan valid")
            else:
                print("Data dari kartu dengan yang diinputkan tidak valid")
        elif "Gagal2" in arduino:
            print("Gagal verifikasi data dari kartu dan inputan, mohon tunggu sebentar.\nApabila masih belum terdeteksi, silahkan cobalagi")
        elif arduino:
            print(arduino)
        else:
            break
    print("")

def custom(*args):
    if len(args) == 5:
        _mode, _data, _port, _baudrate, _timeout = args
        if _mode in ["-W", "--write"]:
            print(f"\nMode Custom Write")
            writeCard(_data, _port, _baudrate, _timeout)
        else:
            print(f"\nMode Custom Verify")
            verifyCard(_data, _port, _baudrate, _timeout)
    else:
        _mode, _port, _baudrate, _timeout = args
        if _mode in ["-R", "--read"]:
            print(f"\nMode Custom Read")
            readCard(_port, _baudrate, _timeout)

if arg == 0 or (arg == 1 and sys.argv[1] in ["-H", "--help"]):
    bantuan()
elif arg == 1:
    mode = sys.argv[1]
    if mode in ["-R", "--read"]:
        print("\nMode Read")
        readCard(defPort, defBaudrate, defTimeout)
    elif mode in ["-FH", "--fullhelp"]:
        fullBantuan()
    elif mode in ["-D", "--detect"]:
        detectPort()
    else:
        bantuan()
elif arg > 1 and arg < 7:
    mode = sys.argv[1]
    data = sys.argv[2]
    if mode in ["-W", "--write"] and len(data) == 16:
        print("\nMode Write")
        writeCard(data, defPort, defBaudrate, defTimeout)
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
            bantuan()
    elif mode in ["-C", "--custom"] and arg == 5:
        subMode = sys.argv[2]
        pOrt = sys.argv[3]
        baudRate = sys.argv[4]
        timeOut = sys.argv[5]
        if subMode in ["-R", "--read"] and "COM" in pOrt and baudRate.isdigit() and int(baudRate) in optBaudRate and timeOut.isdigit():
            custom(subMode, pOrt, baudRate, timeOut)
        else:
            bantuan()
    else:
        bantuan()
else:
    bantuan()