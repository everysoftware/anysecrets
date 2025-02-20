from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from app.base.models import Entity
from app.config import settings
from app.security.encryption import decrypt_aes, encrypt_aes


class Password(Entity):
    __tablename__ = "passwords"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    name: Mapped[str]
    encrypted_username: Mapped[str]
    encrypted_password: Mapped[str]
    url: Mapped[str] = mapped_column(default="")
    note: Mapped[str] = mapped_column(default="")

    @hybrid_property
    def username(self) -> str:
        return decrypt_aes(self.encrypted_username, settings.security.encryption_secret)

    @hybrid_property
    def password(self) -> str:
        return decrypt_aes(self.encrypted_password, settings.security.encryption_secret)

    def set_username(self, value: str) -> None:
        self.encrypted_username = encrypt_aes(value, settings.security.encryption_secret)

    def set_password(self, value: str) -> None:
        self.encrypted_password = encrypt_aes(value, settings.security.encryption_secret)

    def set_sensitive(self, username: str, password: str) -> None:
        self.set_username(username)
        self.set_password(password)

    def update_sensitive(self, username: str | None = None, password: str | None = None) -> None:
        if username is not None:
            self.set_username(username)
        if password is not None:
            self.set_password(password)
