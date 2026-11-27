from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, build_engine, get_session
from .models import Employee
from .schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate


def create_app(database_url: str | None = None) -> FastAPI:
    app_engine = build_engine(database_url) if database_url else None

    def session_dependency():
        if app_engine is None:
            yield from get_session()
        else:
            from sqlalchemy.orm import sessionmaker
            factory = sessionmaker(bind=app_engine, autoflush=False, expire_on_commit=False)
            with factory() as session:
                yield session

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        if app_engine is not None:
            Base.metadata.create_all(bind=app_engine)
        else:
            from .database import engine
            Base.metadata.create_all(bind=engine)
        yield

    app = FastAPI(
        title="Employee Manager API",
        description="API REST para gerenciamento de funcionários.",
        version="2.0.0",
        lifespan=lifespan,
    )

    @app.get("/health", tags=["Sistema"])
    def health():
        return {"status": "ok", "service": "employee-manager-api"}

    @app.get("/employees", response_model=list[EmployeeRead], tags=["Funcionários"])
    def list_employees(session: Session = Depends(session_dependency)):
        return session.scalars(select(Employee).order_by(Employee.id)).all()

    @app.post("/employees", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED, tags=["Funcionários"])
    def create_employee(payload: EmployeeCreate, session: Session = Depends(session_dependency)):
        employee = Employee(**payload.model_dump())
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee

    @app.get("/employees/{employee_id}", response_model=EmployeeRead, tags=["Funcionários"])
    def get_employee(employee_id: int, session: Session = Depends(session_dependency)):
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        return employee

    @app.put("/employees/{employee_id}", response_model=EmployeeRead, tags=["Funcionários"])
    def update_employee(employee_id: int, payload: EmployeeUpdate, session: Session = Depends(session_dependency)):
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        for field, value in payload.model_dump().items():
            setattr(employee, field, value)
        session.commit()
        session.refresh(employee)
        return employee

    @app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Funcionários"])
    def delete_employee(employee_id: int, session: Session = Depends(session_dependency)):
        employee = session.get(Employee, employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        session.delete(employee)
        session.commit()
        return None

    return app


app = create_app()
