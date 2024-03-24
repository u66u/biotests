from sqlalchemy import Enum, DateTime, ForeignKey, func, Float, Text, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from enum import Enum as PyEnum


class TestType(PyEnum):
    BLOOD_TEST = "blood_test"
    DNA_TEST = "dna_test"


class BiologicalTest(Base):
    __tablename__ = "biological_test"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False, default=0)
    test_type: Mapped[TestType] = mapped_column(
        Enum(TestType), nullable=False, index=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    __mapper_args__ = {
        "polymorphic_on": test_type,
        "polymorphic_identity": "biological_test",
    }


class BloodTest(BiologicalTest):
    __tablename__ = "blood_test"

    id: Mapped[str] = mapped_column(ForeignKey("biological_test.id"), primary_key=True)
    glucose: Mapped[float] = mapped_column(Float, nullable=True)
    cholesterol: Mapped[float] = mapped_column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": TestType.BLOOD_TEST,
    }


class DNATest(BiologicalTest):
    __tablename__ = "dna_test"

    id: Mapped[str] = mapped_column(ForeignKey("biological_test.id"), primary_key=True)
    gene1: Mapped[str] = mapped_column(String(50), nullable=True)
    gene2: Mapped[str] = mapped_column(String(50), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": TestType.DNA_TEST,
    }
