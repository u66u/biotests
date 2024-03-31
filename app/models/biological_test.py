from datetime import date
from sqlalchemy import (
    Date,
    Enum,
    DateTime,
    ForeignKey,
    func,
    Float,
    Text,
    String,
    DECIMAL,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base
from enum import Enum as PyEnum


class TestType(PyEnum):
    DNA_M_PHENO_AGE_LEVINE_TEST = "dna_m_pheno_age_levine_2018_test"
    BLOODMARKER_BA_ESTIMATION_TEST = "bloodmarker_ba_estimation_test"


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
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __mapper_args__ = {
        "polymorphic_on": test_type,
        "polymorphic_identity": "biological_test",
    }


class DNAmPhenoAgeLevine2018Test(BiologicalTest):
    __tablename__ = "dna_m_pheno_age_levine_2018_test"

    id: Mapped[str] = mapped_column(ForeignKey("biological_test.id"), primary_key=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    albumin: Mapped[float] = mapped_column(Float, nullable=True)
    creatinine: Mapped[float] = mapped_column(Float, nullable=True)
    glucose: Mapped[float] = mapped_column(Float, nullable=True)
    c_reactive_protein: Mapped[float] = mapped_column(Float, nullable=True)
    lymphocytes_percentage: Mapped[float] = mapped_column(Float, nullable=True)
    mean_corpuscular_volume: Mapped[float] = mapped_column(Float, nullable=True)
    red_blood_cell_distribution_width: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    alkaline_phosphatase: Mapped[float] = mapped_column(Float, nullable=True)
    white_blood_cell_count: Mapped[float] = mapped_column(Float, nullable=True)
    result: Mapped[float] = mapped_column(Float, nullable=True)

    __mapper_args__ = {"polymorphic_identity": TestType.DNA_M_PHENO_AGE_LEVINE_TEST}


class BloodMarketBAEstimationTest(BiologicalTest):
    __tablename__ = "bloodmarker_ba_estimation_test"

    id: Mapped[str] = mapped_column(ForeignKey("biological_test.id"), primary_key=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    albumin: Mapped[float] = mapped_column(Float, nullable=True)
    alkaline_phosphatase: Mapped[float] = mapped_column(Float, nullable=True)
    urea: Mapped[float] = mapped_column(Float, nullable=True)
    cholesterol: Mapped[float] = mapped_column(Float, nullable=True)
    creatinine: Mapped[float] = mapped_column(Float, nullable=True)
    cystatin_c: Mapped[float] = mapped_column(Float, nullable=True)
    glycated_haemoglobin: Mapped[float] = mapped_column(Float, nullable=True)
    log_c_reactive_protein: Mapped[float] = mapped_column(Float, nullable=True)
    log_gamma_glutamyltransf: Mapped[float] = mapped_column(Float, nullable=True)
    red_blood_cell_erythrocyte_count: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    mean_corpuscular_volume: Mapped[float] = mapped_column(Float, nullable=True)
    red_blood_cell_erythrocyte_distribution_width: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    monocyte_count: Mapped[float] = mapped_column(Float, nullable=True)
    neutrophill_count: Mapped[float] = mapped_column(Float, nullable=True)
    lymphocyte_percentage: Mapped[float] = mapped_column(Float, nullable=True)
    mean_sphered_cell_volume: Mapped[float] = mapped_column(Float, nullable=True)
    log_alanine_aminotransfe: Mapped[float] = mapped_column(Float, nullable=True)
    log_shbg: Mapped[float] = mapped_column(Float, nullable=True)
    log_vitamin_d: Mapped[float] = mapped_column(Float, nullable=True)
    high_light_scatter_reticulocyte_percentage: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    glucose: Mapped[float] = mapped_column(Float, nullable=True)
    platelet_distribution_width: Mapped[float] = mapped_column(Float, nullable=True)
    mean_corpuscular_haemoglobin: Mapped[float] = mapped_column(Float, nullable=True)
    platelet_crit: Mapped[float] = mapped_column(Float, nullable=True)
    apolipoprotein_a: Mapped[float] = mapped_column(Float, nullable=True)
    result: Mapped[float] = mapped_column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": TestType.BLOODMARKER_BA_ESTIMATION_TEST,
    }
