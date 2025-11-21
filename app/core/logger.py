import logging
import sys
from app.core.config import settings # Assuming you have a settings module for configuration

LOG_LEVEL = settings.LOGGING_LEVEL.upper() if hasattr(settings, 'LOGGING_LEVEL') else 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'

logger = logging.getLogger("app")
logger.setLevel(LOG_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOG_LEVEL)

formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)