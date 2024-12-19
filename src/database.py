from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Integer, DateTime
from datetime import datetime

# Create a class Base of SQLAlchemy (na versão 2.x)
Base = declarative_base()

class BitcoinPrice(Base):
    """Defines the table in the database."""
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    cryptocurrency = Column(String(50), nullable=False)  # until 50 caracteres
    currency = Column(String(10), nullable=False)        # until 10 caracteres
    timestamp = Column(DateTime, default=datetime.now)