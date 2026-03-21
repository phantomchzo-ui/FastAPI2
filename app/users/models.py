from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):

    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column(String(125))

