from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.products.models import Post


class User(Base):

    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column(String(125))

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")


class Profile(Base):

    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    bio: Mapped[str | None]
    user_id: Mapped["User"] = mapped_column(ForeignKey("users.id"), unique=True)
