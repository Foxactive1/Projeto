from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    sobrenome: str = Field(min_length=1, max_length=120)
    cargo: str = Field(min_length=1, max_length=120)
    salario: float = Field(ge=0)
    data_contratacao: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
