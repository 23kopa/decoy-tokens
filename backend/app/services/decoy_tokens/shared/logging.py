# backend/app/services/decoy_tokens/shared/logging.py

import logging
from typing import Any, Dict, Optional

class Colors:
    GREY = '\x1b[38;21m'
    BLUE = '\x1b[38;5;39m'
    YELLOW = '\x1b[38;5;226m'
    RED = '\x1b[38;5;196m'
    BOLD_RED = '\x1b[31;1m'
    RESET = '\x1b[0m'


class ColoredFormatter(logging.Formatter):
    """Кастомный форматтер с цветами для уровней логирования"""
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        # Если fmt не указан, используем формат по умолчанию
        if fmt is None:
            fmt = '%(asctime)s UTC | %(levelname)8s | %(name)s | %(message)s'
        super().__init__(fmt, datefmt)
        
        self.FORMATS = {
            logging.DEBUG: Colors.GREY + fmt + Colors.RESET,
            logging.INFO: Colors.BLUE + fmt + Colors.RESET,
            logging.WARNING: Colors.YELLOW + fmt + Colors.RESET,
            logging.ERROR: Colors.RED + fmt + Colors.RESET,
            logging.CRITICAL: Colors.BOLD_RED + fmt + Colors.RESET,
        }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self._fmt)
        # Создаем новый Formatter для каждого уровня
        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)


# Создаем логгер для сервиса
logger = logging.getLogger("decoy_tokens")

# Настраиваем формат
log_format = '%(asctime)s UTC | %(levelname)2s | %(name)s | %(message)s'
formatter = ColoredFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

# Консольный хендлер
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
logger.propagate = False


# Функции для логирования
def log_ip_detection(ip_data: Dict[str, Any]) -> None:
    """Логирование результатов определения IP"""
    logger.info(
        f"IP Detection | "
        f"Method: {ip_data.get('detection_method')} | "
        f"Detected: {ip_data.get('detected_ip')} | "
        f"Direct: {ip_data.get('direct_ip')} | "
        f"Confidence: {ip_data.get('confidence')}"
    )


def log_geo_info(geo_data: Dict[str, Any], ip: str) -> None:
    """Логирование гео-информации"""
    logger.info(
        f"Geo Info | IP: {ip} | "
        f"Country: {geo_data.get('country')} ({geo_data.get('country_code')}) | "
        f"City: {geo_data.get('city')} | "
        f"ASN: {geo_data.get('asn')} | "
        f"Organization: {geo_data.get('as_org')} | "
        f"Source: {geo_data.get('source')}"
    )


def log_token_event(fingerprint: str, ip: str, is_bot: bool, event_type: str = "new") -> None:
    """Логирование событий токена"""
    logger.info(
        f"Token Event | Type: {event_type} | "
        f"Fingerprint: {fingerprint[:16]}... | "
        f"IP: {ip} | "
        f"Bot: {is_bot}"
    )