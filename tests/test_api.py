from fastapi.testclient import TestClient

from employee_manager.api import create_app


def test_health():
    with TestClient(create_app("sqlite://")) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_employee_crud():
    with TestClient(create_app("sqlite://")) as client:
        payload = {
            "nome": "Ana", "sobrenome": "Exemplo", "cargo": "Analista",
            "salario": 4500.0, "data_contratacao": "2024-01-15",
        }
        created = client.post("/employees", json=payload)
        assert created.status_code == 201
        employee_id = created.json()["id"]
        assert client.get(f"/employees/{employee_id}").status_code == 200
        assert len(client.get("/employees").json()) == 1
        assert client.put(f"/employees/{employee_id}", json={**payload, "cargo": "Especialista"}).json()["cargo"] == "Especialista"
        assert client.delete(f"/employees/{employee_id}").status_code == 204
        assert client.get(f"/employees/{employee_id}").status_code == 404
