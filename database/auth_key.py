from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


# Auth Key model
class AuthKey(Base):
    __tablename__ = "auth_key"

    id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def to_dict(self):
        return self.__dict__
