import logging
from typing import Optional

def setup_logging(
    level: int = logging.INFO,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_file: Optional[str] = None,
    console_log: bool = True
) -> None:
    """Настройка логирования"""
    # Удаляем старые handlers чтобы избежать дублирования
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    # Создаем форматтер
    formatter = logging.Formatter(format_str)
        
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
        
    # Консольный handler
    if console_log:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
    # Файловый handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)