import uuid
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.user import User
from app.models.biological_test import BiologicalTest


class Order(Base):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("user.id"), nullable=False, index=True
    )
    test_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("biological_test.id"),
        nullable=False,
        index=True,
    )
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    user: Mapped[User] = relationship("User", back_populates="orders")
    test: Mapped[BiologicalTest] = relationship("BiologicalTest")
