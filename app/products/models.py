from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(25))
    price: Mapped[int] = mapped_column()


