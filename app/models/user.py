from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # full name
    name = Column(String, nullable=False)

    # login email
    email = Column(String, unique=True, index=True, nullable=False)

    # hashed password
    password = Column(String, nullable=False)

    # role → director / pm
    role = Column(String, nullable=False)

    # active or disabled
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)