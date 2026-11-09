from pydantic import BaseModel


class PontoMaterialCreate(BaseModel):
    ponto_id: int
    material_id: int


class PontoMaterialResponse(BaseModel):
    id: int
    ponto_id: int
    material_id: int

    model_config = {
        "from_attributes": True
    }