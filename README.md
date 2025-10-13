'''
├── 📁 config/
│   ├── 🔒 .env
│   ├── 🐍 elements.py
│   ├── 🐍 paths.py
│   ├── 🐍 pipeline_config.py
│   └── 🐍 regras_de_negocio.py
├── 📁 pipelines/
│   ├── 📁 specific_analysis/
│   │   ├── 🐍 bottleneck_box.py
│   │   ├── 🐍 bottleneck_salao.py
│   │   ├── 🐍 jornada_pipeline.py
│   │   └── 🐍 time_lead_olpn.py
│   ├── 📁 standard_pipeline/
│       ├── 🐍 cancel_pipeline.py
│       ├── 🐍 expedicao_cd_pipeline.py
│       ├── 🐍 loading_pipeline.py
│       ├── 🐍 olpn_pipeline.py
│       ├── 🐍 packing_pipeline.py
│       ├── 🐍 picking_pipeline.py
│       └── 🐍 putaway_pipeline.py
├── 📁 utils/
│   ├── 🐍 browser_setup.py
│   ├── 🐍 classification.py
│   ├── 🐍 config_logger.py
│   ├── 🐍 get_info.py
│   ├── 🐍 info_system.py
│   └── 🐍 reader.py
├── 📁 web_data_collector/
│   ├── 🐍 cancel.py
│   ├── 🐍 expedicao_cd.py
│   ├── 🐍 loading.py
│   ├── 🐍 login.py
│   ├── 🐍 olpn.py
│   ├── 🐍 packing.py
│   ├── 🐍 picking.py
│   └── 🐍 putaway.py
├── 🐳 Dockerfile
├── 📖 README.md
├── ⚙️ docker-compose.yml
├── 🐍 main.py
├── 📄 requirements.txt
'''

# 🧠 Web Data Collector: Arquitetura Híbrida RPA + ETL Automatizado

Este projeto apresenta uma solução de automação de dados ponta a ponta, unindo RPA e pipelines de ETL para garantir a coleta, tratamento e disponibilização de indicadores estratégicos de forma totalmente
orquestrada.

A iniciativa nasceu da necessidade de eliminar o gargalo na atualização manual de múltiplos indicadores críticos dentro da área. Para resolver esse desafio, foi implementada uma arquitetura híbrida que:

- Extrai dados automaticamente do sistema Manhattan CSI via RPA;
- Organiza e transforma as informações em uma arquitetura de medalhão (Bronze, Silver, Gold);
- Sincroniza os dados com o OneDrive por meio de fluxo no Power Automate;
- Integra os resultados ao Power BI através de Dataflows;
- Executa diariamente às 23h, garantindo a atualização contínua e confiável dos indicadores;

Essa automação reduz esforços operacionais, minimiza erros humanos e entrega governança e escalabilidade ao processo de análise de dados.

## 🚀 Visão Geral

A arquitetura proposta combina **Selenium RPA**, **ETL em Python**, e orquestração via **Power Automate + SharePoint + Power BI**, gerando indicadores atualizados automaticamente com base em arquivos baixados de um sistema legado. O projeto é escalavel para suportar a extração de vários relatório, atualmente 6, e 9 pipelines, e realizar o ETL de forma constante quase que em tempo real

---

## 🎯 Objetivo do Projeto

A arquitetura integra RPA com Selenium, pipelines de ETL em Python e orquestração corporativa via Power Automate + SharePoint + Power BI, garantido que os indicadores sejam atualizados de forma
automática e contínua a partir de extrações de um sistema legado.

Atualmente, a solução comtempla:

- 6 relatórios monitorados via RPA;
- 9 pipelines de ETL em execução;
- Processamento quase em tempo real, assegurando dados consistentes e disponíveis diariamente para consumo analítico.

O desenho arquitetural é escalável e resiliente, permitindo a expansão para novos relatórios e fluxos de dados sem comprometer performance ou governança

---

## 🛠️ Stack Tecnológica

### Linguagens e Plataformas:
- Python 3.12
- Power BI (Dataflows Gen1)
- Power Automate
- SharePoint Online

---

## 🧩 Arquitetura Modular
Link de acesso: https://excalidraw.com/#json=MguHa3ZRbh4GmK8XFeDJc,z8TTvXhE0PbPsNWZRSb5tw
<img width="1046" height="873" alt="image" src="https://github.com/user-attachments/assets/076ff2b1-29e8-4312-a135-6d764a5d10b2" />

## BI

<img width="1531" height="859" alt="image" src="https://github.com/user-attachments/assets/b9d574a3-e333-41eb-8f45-1e687d8910b9" />

---


## ⚙️ Como Usar  

1. Instale as dependências do projeto:  
   ```bash
   pip install -r requirements.txt
   ```

2. Crie o arquivo .env na raiz do projeto e configure as variáveis de ambiente:
    ```bash
    LOGIN_EMAIL=
    LOGIN_PASSWORD=
    CHROME_HEADLESS=true
    ```

3. Configure o settings.py informando o caminho absoluto do seu .env:
    ```ini
    ENV_PATH = Path()
    ```

4. Execute o pipeline principal:
    ```python
    python main.py
    ```

## 👨‍💻 Autor

**Vinicius Giovanni**  
*Analista de Dados Júnior | Foco em Pipelines, ETL, Power BI e Engenharia de Dados*  
[LinkedIn](https://www.linkedin.com/in/vin%C3%ADcius-giovanni-139941297/) · [GitHub](https://github.com/Vinicius-Giovanni)
