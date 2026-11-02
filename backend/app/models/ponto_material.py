from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base


class PontoMaterial(Base):
    __tablename__ = "pontos_materiais"

    id = Column(Integer, primary_key=True, index=True)

    ponto_id = Column(Integer, ForeignKey("pontos_coleta.id"), nullable=False)

    material_id = Column(Integer, ForeignKey("materiais.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("ponto_id", "material_id", name="uq_ponto_material"),
    )