from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.material import Material
from app.schemas.material import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse
)


router = APIRouter(
    prefix="/materiais",
    tags=["Materiais"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MaterialResponse)
def criar_material(
    material: MaterialCreate,
    db: Session = Depends(get_db)
):
    novo_material = Material(
        **material.model_dump()
    )

    db.add(novo_material)
    db.commit()
    db.refresh(novo_material)

    return novo_material


@router.get("/", response_model=list[MaterialResponse])
def listar_materiais(
    db: Session = Depends(get_db)
):
    return db.query(Material).all()


@router.get("/{material_id}", response_model=MaterialResponse)
def buscar_material(
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

    return material


@router.put("/{material_id}", response_model=MaterialResponse)
def atualizar_material(
    material_id: int,
    dados_material: MaterialUpdate,
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

    for campo, valor in dados_material.model_dump().items():
        setattr(material, campo, valor)

    db.commit()
    db.refresh(material)

    return material


@router.delete("/{material_id}")
def excluir_material(
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

    db.delete(material)
    db.commit()

    return {
        "message": "Material excluído com sucesso"
    }