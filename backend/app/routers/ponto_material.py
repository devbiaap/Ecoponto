from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.material import MaterialResponse
from app.schemas.ponto_coleta import PontoColetaResponse

from app.database import SessionLocal
from app.models.ponto_coleta import PontoColeta
from app.models.material import Material
from app.models.ponto_material import PontoMaterial
from app.schemas.ponto_material import (
    PontoMaterialCreate,
    PontoMaterialResponse
)


router = APIRouter(
    prefix="/pontos-materiais",
    tags=["Pontos e Materiais"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PontoMaterialResponse)
def adicionar_material_ao_ponto(
    dados: PontoMaterialCreate,
    db: Session = Depends(get_db)
):
    ponto = (
        db.query(PontoColeta)
        .filter(PontoColeta.id == dados.ponto_id)
        .first()
    )

    if not ponto:
        raise HTTPException(
            status_code=404,
            detail="Ponto de coleta não encontrado"
        )

    material = (
        db.query(Material)
        .filter(Material.id == dados.material_id)
        .first()
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material não encontrado"
        )

    relacionamento = PontoMaterial(
        ponto_id=dados.ponto_id,
        material_id=dados.material_id
    )

    try:
        db.add(relacionamento)
        db.commit()
        db.refresh(relacionamento)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Este material já está associado a este ponto de coleta"
        )

    return relacionamento

@router.get("/ponto/{ponto_id}", response_model=list[MaterialResponse])
def listar_materiais_do_ponto(
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

    return materiais

@router.get("/material/{material_id}", response_model=list[PontoColetaResponse])
def listar_pontos_do_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    material = (
        db.query(Material)
        .filter(Material.id == material_id)
        .first()
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material não encontrado"
        )

    pontos = (
        db.query(PontoColeta)
        .join(
            PontoMaterial,
            PontoColeta.id == PontoMaterial.ponto_id
        )
        .filter(PontoMaterial.material_id == material_id)
        .all()
    )

    return pontos