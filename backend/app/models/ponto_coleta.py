from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database import Base


class PontoColeta(Base):
    __tablename__ = "pontos_coleta"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    horario = Column(String(150), nullable=True)
    ativo = Column(Boolean, default=True)