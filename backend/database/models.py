# Сюда нужно впихивать создание таблиц с бд (daniildddd)
# - создание схемы БД, пользовательских типов (ENUM), таблиц с перечисленными
# ограничениями. Для этого должна быть реализована кнопка «Создать схему в БД»;

from typing import List, Optional

from marshmallow import validates
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date,
    ForeignKey, UniqueConstraint, CheckConstraint, select, insert, delete
)
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum
from enum import Enum

from datetime import datetime

class SensorTypeEnum(str, Enum):
    Temperature = 'temperature'
    Vibration = 'vibration'
    Pressure = 'pressure'
    Noise = 'noise'

Base = declarative_base()

class Sensors(Base):
    __tablename__ = "sensors"
    sensor_id  : Mapped[int] = mapped_column(primary_key=True)
    sensor_type : Mapped[SensorTypeEnum] = mapped_column(SAEnum(SensorTypeEnum, name="sensor_type_enum", create_type=True), default=SensorTypeEnum.Temperature, nullable=False)
    unit: Mapped[str] = mapped_column(String(10), nullable=False)
    location: Mapped[str] = mapped_column(String())
    def __repr__(self) -> str:
        return f"Sensors(sensor_id={self.sensor_id!r}, sensor_type={self.sensor_type!r})"

class SensorReadings(Base):
    __tablename__ = "sensor_readings"
    reading_id : Mapped[int] = mapped_column(primary_key=True)
    sensor_id : Mapped[int] = relationship("Sensors", back_populates="sensor_id")
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    value: Mapped[float] = mapped_column()


    __table_args__ = (
        CheckConstraint("value >= 0", name="value_check"),
    )

    def __repr__(self) -> str:
        return f"SensorReadings(id={self.reading_id!r}, name={self.name!r}, fullname={self.fullname!r})"
