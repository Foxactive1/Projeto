from fastapi.testclient import TestClient
from employee_manager.api import create_app


def test_employee_crud(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'test.db'}")
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        payload = {"nome": "Maria", "sobrenome": "Silva", "cargo": "Analista", "salario": 4500.0, "data_contratacao": "2024-01-15"}
        created = client.post("/employees", json=payload)
        assert created.status_code == 201
        employee_id = created.json()["id"]
        assert client.get(f"/employees/{employee_id}").json()["nome"] == "Maria"
        updated = {**payload, "cargo": "Engenheira"}
        assert client.put(f"/employees/{employee_id}", json=updated).json()["cargo"] == "Engenheira"
        assert client.delete(f"/employees/{employee_id}").status_code == 204
        assert client.get(f"/employees/{employee_id}").status_code == 404
