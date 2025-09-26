from sqlalchemy import (
    Column, Integer, String, Date, Float, Numeric, 
    ARRAY, Enum as SQLEnum, ForeignKey, CheckConstraint, Text, 
    TIMESTAMP, BigInteger
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

# Определение типов ENUM
equipment_status = SQLEnum('working', 'maintenance', 'broken', name='equipment_status')
sensor_type = SQLEnum('temperature', 'vibration', 'pressure', 'noise', name='sensor_type')
maintenance_type = SQLEnum('planned', 'emergency', 'predictive', name='maintenance_type')
risk_level = SQLEnum('low', 'medium', 'high', name='risk_level')

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
        ForeignKey('equipment.equipment_id', ondelete='CASCADE'), 
        nullable=False
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
        Integer, 
        ForeignKey('sensors.sensor_id', ondelete='CASCADE'), 
        nullable=False
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
    
    # Ограничения проверки
    __table_args__ = (
        CheckConstraint('volume_ml > 0', name='check_volume_positive'),
        CheckConstraint('price > 0', name='check_price_positive'),
    )
    
    # Связи
    production_batches = relationship("ProductionBatches", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    sales = relationship("Sales", back_populates="product")


# Таблица производственных партий
class ProductionBatches(Base):
    __tablename__ = 'production_batches'
    
    batch_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, 
        ForeignKey('products.product_id', ondelete='CASCADE'), 
        nullable=False
    )
    equipment_id = Column(
        Integer, 
        ForeignKey('equipment.equipment_id'), 
        nullable=False
    )
    production_date = Column(Date, nullable=False)
    quantity_produced = Column(Integer, nullable=False)
    
    # Ограничение проверки
    __table_args__ = (
        CheckConstraint('quantity_produced > 0', name='check_quantity_produced_positive'),
    )
    
    # Связи
    product = relationship("Products", back_populates="production_batches")
    equipment = relationship("Equipment", back_populates="production_batches")

# Таблица инвентаря
class Inventory(Base):
    __tablename__ = 'inventory'
    
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, 
        ForeignKey('products.product_id', ondelete='CASCADE'), 
        nullable=False
    )
    quantity_in_stock = Column(Integer, nullable=False, default=0)
    last_updated = Column(TIMESTAMP, default=func.now())
    
    # Ограничение проверки
    __table_args__ = (
        CheckConstraint('quantity_in_stock >= 0', name='check_quantity_in_stock_non_negative'),
    )
    
    # Связи
    product = relationship("Products", back_populates="inventory")

# Таблица продаж
class Sales(Base):
    __tablename__ = 'sales'
    
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, 
        ForeignKey('products.product_id'), 
        nullable=False
    )
    sale_date = Column(Date, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    client = Column(Text, nullable=False)
    
    # Ограничения проверки
    __table_args__ = (
        CheckConstraint('quantity_sold > 0', name='check_quantity_sold_positive'),
        CheckConstraint('total_price >= 0', name='check_total_price_non_negative'),
    )
    
    # Связи
    product = relationship("Products", back_populates="sales")

# Таблица журнала технического обслуживания
class MaintenanceLogs(Base):
    __tablename__ = 'maintenance_logs'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(
        Integer, 
        ForeignKey('equipment.equipment_id'), 
        nullable=False
    )
    date = Column(Date, nullable=False)
    type = Column(maintenance_type, nullable=False)
    description = Column(Text)
    technician = Column(Text, nullable=False)
    
    # Связи
    equipment = relationship("Equipment", back_populates="maintenance_logs")

# Таблица прогнозов отказов
class FailurePredictions(Base):
    __tablename__ = 'failure_predictions'
    
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(
        Integer, 
        ForeignKey('equipment.equipment_id'), 
        nullable=False
    )
    sensor_id = Column(
        Integer, 
        ForeignKey('sensors.sensor_id')
    )
    prediction_date = Column(Date, nullable=False)
    failure_date_est = Column(Date)
    risk_level = Column(risk_level, nullable=False)
    recommendation = Column(Text)
    
    # Связи
    equipment = relationship("Equipment", back_populates="failure_predictions")
    sensor = relationship("Sensors", back_populates="failure_predictions")