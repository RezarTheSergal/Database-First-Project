# Сюда нужно впихивать создание таблиц с бд (daniildddd)
# - создание схемы БД, пользовательских типов (ENUM), таблиц с перечисленными
# ограничениями. Для этого должна быть реализована кнопка «Создать схему в БД»;

from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date,
    ForeignKey, UniqueConstraint, CheckConstraint, select, insert, delete
)
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError, SQLAlchemyError