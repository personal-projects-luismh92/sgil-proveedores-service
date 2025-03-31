"""Test módulo de proveedores"""
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.repositories.proveedor import RepositorioProveedor

client = TestClient(app)


@patch("app.repositories.proveedor.RepositorioProveedor.obtener_todos", new_callable=AsyncMock)
def test_obtener_todos_exitoso_sin_registros(mock_obtener_todos):
    """Test obtener todos los proveedores de manera exitosa con 0 registros."""
    mock_obtener_todos.return_value = {
        "data": [],
        "totalRows": 0
    }

    response = client.get("/proveedores")

    assert response.status_code == 200
    assert response.json() == mock_obtener_todos.return_value


@patch("app.repositories.proveedor.RepositorioProveedor.obtener_por_id", new_callable=AsyncMock)
def test_obtener_por_id_no_encontrado(mock_obtener_por_id):
    """Test obtener proveedor por id cuando no existe."""
    mock_obtener_por_id.return_value = None

    response = client.get("/proveedores/8f5c7b3d-2a46-4e8b-8a9c-7e35d2f5b9c1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Proveedor no encontrado"}
