from sqlalchemy import (
    Column,
    Integer,
    Date,
    Numeric,
    ARRAY,
    Enum,
    ForeignKey,
    CheckConstraint,
    Text,
    TIMESTAMP,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


# ENUM для уровня кофеина
caffeine_level = Enum("low", "medium", "high", "extra_high", name="caffeine_level")


# Таблица продуктов (энергетиков)
class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    flavor = Column(Text)
    volume_ml = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    ingredients = Column(ARRAY(Text))
    caffeine_level = Column(
        caffeine_level, nullable=False, default="medium"
    )  # ENUM для кофеина

    # Ограничения проверки
    __table_args__ = (
        CheckConstraint("volume_ml > 0", name="check_volume_positive"),
        CheckConstraint("price > 0", name="check_price_positive"),
    )

    # Связи
    production_batches = relationship("ProductionBatches", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")
    sales = relationship("Sales", back_populates="product")


# Таблица производственных партий
class ProductionBatches(Base):
    __tablename__ = "production_batches"

    batch_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, 
        ForeignKey('products.product_id'), 
        nullable=False
    )
    production_date = Column(Date, nullable=False)
    quantity_produced = Column(Integer, nullable=False)

    # Ограничение проверки
    __table_args__ = (
        CheckConstraint(
            "quantity_produced > 0", name="check_quantity_produced_positive"
        ),
    )

    # Связи
    product = relationship("Products", back_populates="production_batches")

# Таблица складских запасов
class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity_in_stock = Column(Integer, nullable=False, default=0)
    last_updated = Column(TIMESTAMP, default=func.now())

    # Ограничение проверки
    __table_args__ = (
        CheckConstraint(
            "quantity_in_stock >= 0", name="check_quantity_in_stock_non_negative"
        ),
    )

    # Связи
    product = relationship("Products", back_populates="inventory")


# Таблица продаж
class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    sale_date = Column(Date, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    # Поле client удалено

    # Ограничения проверки
    __table_args__ = (
        CheckConstraint("quantity_sold > 0", name="check_quantity_sold_positive"),
        CheckConstraint("total_price >= 0", name="check_total_price_non_negative"),
    )

    # Связи
    product = relationship("Products", back_populates="sales")
