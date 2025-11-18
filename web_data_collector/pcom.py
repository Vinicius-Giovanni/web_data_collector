import win32com.client as win32
import os
import subprocess
import time

class PCOMSession():

    def __init__(self, session_name="A"):
        self.session_name = session_name
        self.screen = None
        self.oia = None

    @staticmethod
    def open_pcom_ws(ws_path: str):
        """
        Abre o IBM Personal Communications com o workspace especificado.
        """
        if not os.path.exists(ws_path):
            raise FileNotFoundError(F'Arquivo .ws não encontrado: {ws_path}')
        
        print(f'Abrindo PCOM: {ws_path}')

        subprocess.Popen(["cmd","/c","start","",ws_path], shell=True)

        time.sleep(5)

        print("PCOM iniciado")

    def connect(self):
        """
        Conecta à sessão PCOM já aberta (ex: Sessão A).
        """
        try:
            self.screen = win32.Dispatch("PCOMM.autECLPS")
            self.oia = win32.Dispatch("PCOMM.autECLOIA")

            self.screen.SetConnectionByName(self.session_name)
            self.oia.SetConnectionByName(self.session_name)

            # Aguarda terminal ativo
            self.oia.WaitForAppAvailable(10000)

            print(f"Sessão {self.session_name} conectada.")
            return True

        except Exception as e:
            print(f"Falha ao conectar à sessão {self.session_name}: {e}")
            return False

    def send_keys(self, keys, row=None, col=None):
        """
        Envia teclas para o terminal. Se row/col forem informados,
        o cursor é posicionado antes de enviar.
        """
        try:
            if row and col:
                self.screen.SendKeys(keys, row, col)
            else:
                self.screen.SendKeys(keys)
        except Exception as e:
            print(f"Erro ao enviar keys '{keys}': {e}")


