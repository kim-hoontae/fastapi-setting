from sqlalchemy     import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from model.database import Base
from datetime import datetime

class BaseMixin:
    id         = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class User(Base, BaseMixin):
    __tablename__ = 'users'

    email        = Column(String(length=200), unique=True, index=True, nullable=False)
    password     = Column(String(length=300), nullable=False)
    name         = Column(String(length=50), nullable=False)
    is_active    = Column(Boolean, default=True)
