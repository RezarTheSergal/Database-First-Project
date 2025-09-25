from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    Numeric,
    ARRAY,
    Enum,
    ForeignKey,
    CheckConstraint,
    Text,
    TIMESTAMP,
    BigInteger,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

# Определение типов ENUM
equipment_status = Enum('working', 'maintenance', 'broken', name='equipment_status')
sensor_type = Enum('temperature', 'vibration', 'pressure', 'noise', name='sensor_type')
maintenance_type = Enum('planned', 'emergency', 'predictive', name='maintenance_type')
risk_level = Enum('low', 'medium', 'high', name='risk_level')

# Таблица оборудования
class Equipment(Base):
    __tablename__ = 'equipment'
    equipment_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    install_date = Column(Date, nullable=False)
    last_service = Column(Date)
    status = Column(equipment_status, nullable=False, default='working')

    # Связи
    sensors = relationship("Sensors", back_populates="equipment", cascade="all, delete-orphan")
    production_batches = relationship("ProductionBatches", back_populates="equipment")
    maintenance_logs = relationship("MaintenanceLogs", back_populates="equipment")
    failure_predictions = relationship("FailurePredictions", back_populates="equipment")

# Таблица датчиков
class Sensors(Base):
    __tablename__ = 'sensors'
    sensor_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(
        Integer,
        ForeignKey("equipment.equipment_id", ondelete="CASCADE"),
        nullable=False,
    )
    type = Column(sensor_type, nullable=False)
    unit = Column(String(10), nullable=False)
    location = Column(Text)

    # Связи
    equipment = relationship("Equipment", back_populates="sensors")
    sensor_readings = relationship("SensorReadings", back_populates="sensor", cascade="all, delete-orphan")
    failure_predictions = relationship("FailurePredictions", back_populates="sensor")

# Таблица показаний датчиков
class SensorReadings(Base):
    __tablename__ = 'sensor_readings'
    reading_id = Column(BigInteger, primary_key=True, autoincrement=True)
    sensor_id = Column(
        Integer, ForeignKey("sensors.sensor_id", ondelete="CASCADE"), nullable=False
    )
    timestamp = Column(TIMESTAMP, nullable=False, default=func.now())
    value = Column(Float, nullable=False)

    # Ограничение проверки
    __table_args__ = (
        CheckConstraint('value >= 0', name='check_value_non_negative'),
    )

    # Связи
    sensor = relationship("Sensors", back_populates="sensor_readings")

# Таблица продуктов
class Products(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    flavor = Column(Text)
    volume_ml = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    ingredients = Column(ARRAY(Text))

    # Ограничения проверки
    __table_args__ = (
        CheckConstraint('volume_ml > 0', name='check_volume_positive'),
        CheckConstraint('price > 0', name='check_price_positive'),
    )

    # Связи
    production_batches = relationship("ProductionBatches", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    sales = relationship("Sales", back_populates="product")
