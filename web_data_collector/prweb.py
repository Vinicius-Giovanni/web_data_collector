from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
from utils.config_logger import log_with_context
from config.pipeline_config import logger, LINKS
from config.paths import TEMP_DIR
from config.elements import ELEMENTS
from utils.browser_setup import create_authenticated_driver
import time
from utils.get_info import today, yesterday

todays = today(format='%d%m%Y')
yesterdays = yesterday(format='%d%m%Y')

@log_with_context(job='prweb', logger=logger)
def prweb(cookies: list[dict],
          download_dir: Path) -> None:

    driver = create_authenticated_driver(cookies, download_dir=download_dir)

    wait = WebDriverWait(driver, 30)
    driver.get(LINKS['LOGIN_PRWEB'])
    
    # === Verificação de carregamento da página ===
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/table/tbody/tr/td[2]/table/tbody/tr[2]/td/font/b')
    ))

    print('Aplicações WEB carregado')

    empresa = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[1]/tbody/tr[1]/td[1]/input[1]')
    ))

    empresa.clear()
    empresa.send_keys('29')

    print('Empresa preenchida')
    time.sleep(1.5)

    matricula = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[1]/tbody/tr[1]/td[2]/input[1]')
    ))

    matricula.clear()
    matricula.send_keys('3892735')

    print('Matricula preenchida')
    time.sleep(1.5)

    senha = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[1]/tbody/tr[1]/td[3]/b[1]/input')
    ))

    senha.clear()
    senha.send_keys('varejo90')

    print('Senha preenchida')
    time.sleep(1.5)

    processa = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[2]/tbody/tr/td[2]/input')
    ))
    processa.click()

    # === Escolha de Programa ===
    escolha_programa = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[1]/tbody/tr[2]/td/select')
    ))
    if escolha_programa:
            Select(escolha_programa).select_by_value('5')

    print('Escolha de programa feita')
    time.sleep(1.5)

    processa_2 = wait.until(EC.element_to_be_clickable(
          (By.XPATH, '/html/body/form[1]/table[2]/tbody/tr/td[2]/input')
    ))
    processa_2.click()

    print('Processado')
    time.sleep(1.5)

    # # === Cabeçalho ===
    # Empresa
    empresa_2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[2]/tbody/tr/td[2]/input[1]')
    ))
    empresa_2.clear()
    empresa_2.send_keys('21')

    print('Empresa preenchida')
    time.sleep(1.5)

    # Matricula
    filial = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form[1]/table[2]/tbody/tr/td[3]/input[1]')
    ))
    filial.clear()
    filial.send_keys('1200')

    print('Matricula preenchida')
    time.sleep(1.5)

    # Tipo ativ
    tipo_ativ = wait.until(EC.element_to_be_clickable(  
        (By.XPATH, '/html/body/form[1]/table[2]/tbody/tr/td[4]/input[1]')
    ))
    tipo_ativ.clear()
    tipo_ativ.send_keys('d')

    print('Tipo atividade preenchida')
    time.sleep(1.5)

    documentos_carga = wait.until(EC.element_to_be_clickable(  
        (By.XPATH, '/html/body/form[1]/table[3]/tbody/tr/td[1]/table/tbody/tr[13]/td[1]/input')
    ))
    documentos_carga.click()

    print('Escolhendo documentos de carga')
    time.sleep(1.5)

    transfere = wait.until(EC.element_to_be_clickable(  
        (By.XPATH, '//*[@id="NM_BOT_TRA"]')
    ))
    transfere.click()

    print('Transfere')
    time.sleep(1.5)

    transportadora_sku = wait.until(EC.element_to_be_clickable(
          (By.XPATH, '/html/body/form[1]/table[3]/tbody/tr[3]/td[1]/input')
    ))
    transportadora_sku.click()

    print('Transportadora e SKU selecionados')
    time.sleep(1.5)

    processa_3 = wait.until(EC.element_to_be_clickable(
          (By.XPATH, '//*[@id="NM_BOT_PRC"]')
    ))
    processa_3.click()

    # === Puxando por SKU ===

    # Empresa
    empresa_4 = wait.until(EC.element_to_be_clickable(
          (By.XPATH, '/html/body/form/table[3]/tbody/tr/td[5]/input[1]')
    ))
    empresa_4.clear()
    empresa_4.send_keys('29')

    print('Empresa selecionada')
    time.sleep(1.5)

    matricula_3 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/form/table[3]/tbody/tr/td[6]/input[1]')
        ))
    matricula_3.clear()
    matricula_3.send_keys('3892735')

    print('Maticula preenchida')
    time.sleep(1.5)

    senha_2 = wait.until(EC.element_to_be_clickable(
          (By.XPATH, '/html/body/form/table[3]/tbody/tr/td[7]/b[1]/input')
    ))
    senha_2.clear()
    senha_2.send_keys('varejo90')

    print('Senha preenchida')
    time.sleep(1.5)

    modalidade_da_rota = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form/table[4]/tbody/tr[2]/td[2]/select')
    ))
    if modalidade_da_rota:
            Select(modalidade_da_rota).select_by_value('5')
        
    print('Modalidade da rota selecionada')
    time.sleep(1.5)

    data_retroativa = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form/table[4]/tbody/tr[6]/td[2]/input[1]')
    ))
    data_retroativa.clear()
    data_retroativa.send_keys(yesterdays)

    data_entrega = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/form/table[4]/tbody/tr[10]/td[2]/input[1]')
    ))
    data_entrega.clear()
    data_entrega.send_keys(todays)

    print('Cabeçalho preenchido')
    time.sleep(1.5)

    processa_4 = wait.until(EC.element_to_be_clickable(
          (By.XPATH, '//*[@id="NM_BOT_PRC"]')
    ))
    processa_4.click()

    print('Processado')
    time.sleep(1.5)


 # Documento



    
    


def prweb_from_file(cookies_path: str,
                     download_dir: Path) -> None:
    """
    Extract data from prweb using cookies from a file
    """

    with open(cookies_path, 'r') as file:
        cookies = json.load(file)

    prweb(cookies=cookies,
          download_dir=download_dir)