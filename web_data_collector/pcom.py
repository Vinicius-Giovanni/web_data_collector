import subprocess
from pathlib import Path
import time
import getpass
import ctypes
import sys


# =============================================================================
# Configurações
# =============================================================================

EXE_PATH = Path(r"C:\Program Files\IBM\Personal Communications\pcsws.exe")
DLL_PATH = Path(r"C:\Program Files\IBM\Personal Communications\pcshll32.dll")
SESSION_FILE_TEMPLATE = r"C:\Users\{user}\Desktop\3270(PCOM).ws"
SESSION_LETTER = "A"   # Sessão padrão (A..Z)


# =============================================================================
# Log
# =============================================================================

def log(msg):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)


# =============================================================================
# HLLAPI
# =============================================================================

dll = ctypes.WinDLL(str(DLL_PATH))

def hllapi(func, data, length):
    f = ctypes.c_int(func)

    # Se for string/bytes → cria buffer
    if isinstance(data, (str, bytes)):
        if isinstance(data, str):
            data = data.encode('ascii')
        buf = ctypes.create_string_buffer(data)
    else:
        # Se já for buffer → usa direto
        buf = data

    l = ctypes.c_int(length)
    rc = ctypes.c_int(0)

    dll.hllapi(ctypes.byref(f), buf, ctypes.byref(l), ctypes.byref(rc))
    return buf, rc.value


# =============================================================================
# Operações HLLAPI
# =============================================================================

def connect(session_letter):
    _, rc = hllapi(1, session_letter, len(session_letter))
    return rc

def wait():
    _, rc = hllapi(23, b"", 0)
    return rc

def send_enter():
    _, rc = hllapi(7, b"@E", 2)
    return rc

def send_text(text):
    _, rc = hllapi(7, text, len(text))
    return rc

def read_screen(length=1920):
    buf = ctypes.create_string_buffer(length)
    func = ctypes.c_int(8)
    l = ctypes.c_int(length)
    rc = ctypes.c_int(0)

    dll.hllapi(ctypes.byref(func), buf, ctypes.byref(l), ctypes.byref(rc))
    screen = buf.value.decode('ascii', errors='ignore')
    return screen, rc


# =============================================================================
# Utilidades
# =============================================================================

def print_screen_formatted(screen):
    print("\n" + "=" * 80)
    for i in range(0, len(screen), 80):
        print(screen[i:i+80])
    print("=" * 80 + "\n")


def wait_for_non_empty_screen(timeout=10):
    """
    Mainframes podem devolver tela vazia enquanto PCOMM conecta.
    Este polling garante que somente seguimos com conteúdo real.
    """
    for _ in range(timeout):
        screen, _ = read_screen()
        if not all(c == " " for c in screen):
            return screen
        time.sleep(1)
    return screen


# =============================================================================
# Controle principal
# =============================================================================

def controle():
    user = getpass.getuser()
    session_file = Path(SESSION_FILE_TEMPLATE.format(user=user))

    log(f"Iniciando PCOMM: {session_file}")
    proc = subprocess.Popen([str(EXE_PATH), str(session_file)], shell=False)
    log(f"PID iniciado: {proc.pid}")

    time.sleep(3)  # margem corporativa

    # -------------------------------------------------------------------------
    # Conectar à sessão HLLAPI
    # -------------------------------------------------------------------------
    log(f"Conectando à sessão HLLAPI: {SESSION_LETTER}")

    rc = connect(SESSION_LETTER)
    if rc != 0:
        log(f"ERRO ao conectar na sessão (RC={rc}). Verifique letra da sessão no .WS")
        return

    wait()

    # -------------------------------------------------------------------------
    # Capturar tela inicial
    # -------------------------------------------------------------------------
    log("Lendo tela inicial...")
    screen = wait_for_non_empty_screen()
    print_screen_formatted(screen)

    # -------------------------------------------------------------------------
    # Enviar ENTER
    # -------------------------------------------------------------------------
    log("Enviando ENTER...")
    send_enter()
    wait()

    # -------------------------------------------------------------------------
    # Capturar tela após ENTER
    # -------------------------------------------------------------------------
    log("Lendo tela pós-ENTER...")
    screen, _ = read_screen()
    print_screen_formatted(screen)


# =============================================================================
# Execução
# =============================================================================

if __name__ == "__main__":
    controle()
