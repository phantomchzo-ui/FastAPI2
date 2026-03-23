from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.products.models import Post

if TYPE_CHECKING:
    from app.products.models import Post


class User(Base):
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column(String(125))

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.name!r})"


class Profile(Base):

    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    bio: Mapped[str | None]
    user: Mapped["User"] = relationship(back_populates="profile")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
