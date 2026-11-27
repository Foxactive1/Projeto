"""Request and response schemas."""
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    sobrenome: str = Field(min_length=1, max_length=120)
    cargo: str = Field(min_length=1, max_length=120)
    salario: float = Field(ge=0, allow_inf_nan=False)
    data_contratacao: date


class EmployeeUpdate(EmployeeCreate):
    pass


class EmployeeRead(EmployeeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
