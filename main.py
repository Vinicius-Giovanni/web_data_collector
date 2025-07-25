from utils.get_info import get_yesterday_date
from utils.config_logger import setup_logger

logger = setup_logger(__name__)

def main():
    data = get_yesterday_date(format='%Q-%W-%Y', logger=logger)
    logger.info(f'resultado retornado: {data}', extra={
        'job': 'main',
        'status': 'completed',
    })


if __name__ == "__main__":
    main()