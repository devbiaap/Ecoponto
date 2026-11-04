from pydantic import BaseModel, Field


class MaterialBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str | None = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(MaterialBase):
    pass


class MaterialResponse(MaterialBase):
    id: int

    model_config = {
        "from_attributes": True
    }