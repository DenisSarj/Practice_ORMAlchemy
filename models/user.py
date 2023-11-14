from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from .address import Address

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    username: Mapped[str | None] = mapped_column(String(20), unique=True)

    addresses: Mapped[list['Address']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __str__(self):
        return f'User(id={self.id!r}, name={self.name!r}, username={self.username!r} '

    def __repr__(self):
        return str(self)
