from utils.config_logger import setup_logger
from web_data_collector.login import login_csi
from config.settings import PASSWORD, EMAIL

logger = setup_logger(__name__)

def main():
    logger.info('iniciando automacao web_data_collector', extra={
        'job': 'main',
        'status': 'started'
    })
    login_csi()
    logger.info('finalizando automacao web_data_collector', extra={
        'job': 'main',
        'status': 'finished'
    })



if __name__ == "__main__":
    main()