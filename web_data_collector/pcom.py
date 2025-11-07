import subprocess
from pathlib import Path
import time
import getpass
import ctypes
import sys

EXE_PATH = Path(r'C:\Program Files\IBM\Personal Communications\pcsws.exe')
DLL_PATH = Path(r'C:\Program Files\IBM\Personal Communications\pcshll32.dll')
SESSION_FILE_TEMPLATE = r'C:\Users\{user}\Desktop\3270(PCOM).ws'

def log(msg):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", file=sys.stdout)

def print_screen_formatted(text):
    print("\n" + "=" * 50)
    for i in range(0, len(text), 80):
        print(text[i:i+80])
    print("=" * 50 + "\n")

dll = ctypes.WinDLL(str(DLL_PATH))

def hllapi(func, data, length):
    f = ctypes.c_int(func)
    buf = ctypes.create_string_buffer(data)
    l = ctypes.c_int(length)
    rc = ctypes.c_int(0)
    dll.hllapi(ctypes.byref(f), buf, ctypes.byref(l), ctypes.byref(rc))
    return rc.value

def connect(session='A'):
    return hllapi(1, session.encode('ascii'), len(session))

def wait():
    return hllapi(23, b'', 0)

def read_screen(length=1920):
    buf = ctypes.create_string_buffer(length)
    func = ctypes.c_int(8)
    l = ctypes.c_int(length)
    rc = ctypes.c_int(0)
    dll.hllapi(ctypes.byref(func), buf, ctypes.byref(l), ctypes.byref(rc))
    screen = buf.value.decode('ascii', errors='ignore')
    return screen, rc.value

def send_enter():
    # função 7 = SendKey
    return hllapi(7, b'@E', 2)

if __name__ == "__main__":
    user = getpass.getuser()
    session_file = Path(SESSION_FILE_TEMPLATE.format(user=user))
    log(f"Iniciando PCOMM com sessão: {session_file}")

    proc = subprocess.Popen([str(EXE_PATH), str(session_file)], shell=False)
    log(f"PCOMM iniciado com PID {proc.pid}")

    log("Aguardando 7 segundos para inicialização completa...")
    time.sleep(7)

    rc = connect('A')
    log(f"Retorno connect: {rc}")

    if rc != 0:
        log("❌ Não foi possível conectar. Verifique o ID da sessão ('A', 'B', etc).")
        sys.exit()

    log("✅ Sessão conectada. Aguardando resposta do host...")
    log("🔹 Enviando tecla ENTER...")
    send_enter()

    for i in range(10):
        wait()
        screen, rc_screen = read_screen()
        non_empty = len(screen.strip())
        log(f"Tentativa {i+1}: tela tem {non_empty} caracteres não vazios")
        if non_empty > 0:
            print_screen_formatted(screen)
            break
        time.sleep(2)
    else:
        log("⚠️ Mesmo após várias tentativas, a tela continua vazia.")
