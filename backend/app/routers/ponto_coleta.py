from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.ponto_coleta import PontoColeta
from app.schemas.ponto_coleta import (
    PontoColetaCreate,
    PontoColetaUpdate,
    PontoColetaResponse,
    PontoColetaDetalhe
)
from app.models.material import Material
from app.models.ponto_material import PontoMaterial


router = APIRouter(
    prefix="/pontos-coleta",
    tags=["Pontos de Coleta"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PontoColetaResponse)
def criar_ponto(
    ponto: PontoColetaCreate,
    db: Session = Depends(get_db)
):
    novo_ponto = PontoColeta(
        **ponto.model_dump()
    )

    db.add(novo_ponto)
    db.commit()
    db.refresh(novo_ponto)

    return novo_ponto

@router.get("/", response_model=list[PontoColetaResponse])
def listar_pontos(db: Session = Depends(get_db)):
    pontos = db.query(PontoColeta).all()

    return pontos

@router.get("/{ponto_id}", response_model=PontoColetaResponse)
def buscar_ponto(
    ponto_id: int,
    db: Session = Depends(get_db)
):
    ponto = (
        db.query(PontoColeta)
        .filter(PontoColeta.id == ponto_id)
        .first()
    )

    if not ponto:
        raise HTTPException(
            status_code=404,
            detail="Ponto de coleta não encontrado"
        )

    return ponto

@router.put("/{ponto_id}", response_model=PontoColetaResponse)
def atualizar_ponto(
    ponto_id: int,
    dados_ponto: PontoColetaUpdate,
    db: Session = Depends(get_db)
):
    ponto = (
        db.query(PontoColeta)
        .filter(PontoColeta.id == ponto_id)
        .first()
    )

    if not ponto:
        raise HTTPException(
            status_code=404,
            detail="Ponto de coleta não encontrado"
        )

    for campo, valor in dados_ponto.model_dump().items():
        setattr(ponto, campo, valor)

    db.commit()
    db.refresh(ponto)

    return ponto

@router.delete("/{ponto_id}")
def excluir_ponto(
    ponto_id: int,
    db: Session = Depends(get_db)
):
    ponto = (
        db.query(PontoColeta)
        .filter(PontoColeta.id == ponto_id)
        .first()
    )

    if not ponto:
        raise HTTPException(
            status_code=404,
            detail="Ponto de coleta não encontrado"
        )

    db.delete(ponto)
    db.commit()

    return {
        "message": "Ponto de coleta excluído com sucesso"
    }

@router.get("/{ponto_id}")

@router.get("/{ponto_id}/detalhes", response_model=PontoColetaDetalhe)
def buscar_ponto_com_detalhes(
    ponto_id: int,
    db: Session = Depends(get_db)
):
    ponto = (
        db.query(PontoColeta)
        .filter(PontoColeta.id == ponto_id)
        .first()
    )

    if not ponto:
        raise HTTPException(
            status_code=404,
            detail="Ponto de coleta não encontrado"
        )

    materiais = (
        db.query(Material)
        .join(
            PontoMaterial,
            Material.id == PontoMaterial.material_id
        )
        .filter(PontoMaterial.ponto_id == ponto_id)
        .all()
    )

    return {
        "id": ponto.id,
        "nome": ponto.nome,
        "descricao": ponto.descricao,
        "endereco": ponto.endereco,
        "bairro": ponto.bairro,
        "latitude": ponto.latitude,
        "longitude": ponto.longitude,
        "horario": ponto.horario,
        "ativo": ponto.ativo,
        "materiais": materiais
    }