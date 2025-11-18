from control_pcom.class_pcom import PCOMSession
import time

def extracao_entrada_de_pedidos():

    p = PCOMSession("A")

    p.open_pcom_ws(r"C:\ProgramData\IBM\Personal Communications\3270.ws")

    if p.connect():
        time.sleep(1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys("1")
        print("Tela 1 escolhida")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(1)
        p.send_keys("J2CD")
        print("Tela J2CD escolhida")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys(keys="21", row=4, col=8)
        print("Empresa preenchida")

        time.sleep(0.1)
        p.send_keys(keys="1200", row=4, col=16)
        print("Flilial preenchida")

        time.sleep(0.1)
        p.send_keys(keys="D", row=4, col=31)
        print("Tipo de atividade preenchida")

        time.sleep(0.1)
        p.send_keys(keys="0516", row=4, col=38)
        print("Deposíto preenchida")

        time.sleep(0.1)
        p.send_keys(keys="29", row=4, col=51)
        print("Matricula 1/2 preenchida")

        time.sleep(0.1)
        p.send_keys(keys="60012828", row=4, col=54)
        print("Matricula 2/2 preenchida")

        time.sleep(0.1)
        p.send_keys(keys="varejo60", row=4, col=70)
        print("Senha preenchida")

        time.sleep(0.1)
        p.send_keys(keys="3", row=7, col=13)
        print("Opção Guia de Controle de Servicos escolhida")

        time.sleep(0.1)
        p.send_keys(keys="6", row=21, col=3)
        print("Opção 1 Consulta")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys(keys="x", row=5, col=7)
        print("Opção S6 ENTREGA AUT. DEPOSITO")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys(keys="x", row=7, col=2)
        print("Opção S6J1357")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys(keys="x", row=3, col=64)
        print("Opção CPD")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys(keys="29 1200 11112025 18112025", row=10, col=3)
        print("Opção Rotina:     RELATORIO WMS ENTRADA DE PEDIDOS")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

        time.sleep(0.1)
        p.send_keys("[pf4]")
        print("PF4 enviado")

        time.sleep(0.1)
        p.send_keys(keys="s", row=20, col=49)
        print("Extraindo entrada de pedidos")

        time.sleep(0.1)
        p.send_keys("[enter]")
        print("ENTER enviado")

    p.close()
