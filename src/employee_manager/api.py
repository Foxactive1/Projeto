"""FastAPI application factory and employee CRUD endpoints."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, build_database
from .models import Employee
from .schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate


def create_app(database_url: str | None = None) -> FastAPI:
    engine, session_factory = build_database(database_url)
    Base.metadata.create_all(bind=engine)

    def get_session():
        with session_factory() as session:
            yield session

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        engine.dispose()

    app = FastAPI(title="Employee Manager API", version="2.0.0", lifespan=lifespan)
    app.state.engine = engine

    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok", "service": "employee-manager"}

    @app.post("/employees", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED, tags=["employees"])
    def create_employee(payload: EmployeeCreate, session: Session = Depends(get_session)):
        employee = Employee(**payload.model_dump())
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee

    @app.get("/employees", response_model=list[EmployeeRead], tags=["employees"])
    def list_employees(session: Session = Depends(get_session)):
        return session.scalars(select(Employee).order_by(Employee.id)).all()

    @app.get("/employees/{employee_id}", response_model=EmployeeRead, tags=["employees"])
    def get_employee(employee_id: int, session: Session = Depends(get_session)):
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        return employee

    @app.put("/employees/{employee_id}", response_model=EmployeeRead, tags=["employees"])
    def update_employee(employee_id: int, payload: EmployeeUpdate, session: Session = Depends(get_session)):
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        for key, value in payload.model_dump().items():
            setattr(employee, key, value)
        session.commit()
        session.refresh(employee)
        return employee

    @app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["employees"])
    def delete_employee(employee_id: int, session: Session = Depends(get_session)):
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        session.delete(employee)
        session.commit()
        return None

    return app


app = create_app()
