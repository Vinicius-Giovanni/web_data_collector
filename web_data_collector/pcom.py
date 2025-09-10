import subprocess
from pathlib import Path
import time
import getpass
import ctypes

# Importe de usuario atual
user = getpass.getuser()
print(f'Usuario atual: {user}')

# Iniciando o PCOMM com o arquivo de sessao especifico
exe_path = Path(r'C:\Program Files\IBM\Personal Communications\pcsws.exe')
session_file = Path(fr'C:\Users\{user}\Desktop\3270(PCOM).ws')
print(f'Arquivo de sessao: {session_file}')

proc =subprocess.Popen([exe_path, session_file], shell=False)
time.sleep(2)
print(f'PCOMM inciado com PID {proc.pid}')

# Carregando DLL do PCOM (EHLLAPI)
dll = ctypes.WinDLL(r'C:\Program Files\IBM\Personal Communications\pcshll32.dll')

def hllapi(function, data):
    func = ctypes.c_int(function)
    if isinstance(data, str):
        data = data.encode('ascii')
    buf = ctypes.create_string_buffer(data)
    lenght = ctypes.c_int(len(data))
    rc = ctypes.c_int(0)
    dll.hllapi(ctypes.byref(func), buf, ctypes.byref(lenght), ctypes.byref(rc))
    return rc.value

def wait():
    func = ctypes.c_int(23)
    buf = ctypes.create_string_buffer(b"")
    lenght = ctypes.c_int(0)
    rc = ctypes.c_int(0)
    dll.hllapi(ctypes.byref(func), buf, ctypes.byref(lenght), ctypes.byref(rc))
    return rc.value

def connect(session='A'):
    return hllapi(1, session)

def send_string(text):
    return hllapi(3, text)

def send_enter():
    return hllapi(7, '@E')

connect('A')
wait()

send_enter()
wait()

send_string('1')
send_enter()
wait()

send_string('J2CD')
wait()
