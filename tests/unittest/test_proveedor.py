"""Test módulo de proveedores"""
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class MockVirtualMemory:
    """ Clase Mock para simular el uso de memoria """

    def __init__(self, percent):
        self.percent = percent


@pytest.mark.asyncio
@patch("psutil.cpu_percent", return_value=30.5)
@patch("psutil.virtual_memory", return_value=MockVirtualMemory(percent=70.0))
async def test_health_check_success(_, __):
    """Debe retornar status OK con métricas de CPU y memoria"""

    response = client.get("/proveedores/health")

    # Verifications
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert json_data["cpu_usage"] == 30.5
    assert json_data["memory_usage"] == 70.0


@pytest.mark.asyncio
@patch("psutil.cpu_percent", return_value=30.5)
@patch("psutil.virtual_memory", return_value=70.0)
async def test_health_check_failure(_, __):
    """Debe manejar excepciones y devolver status ERROR"""

    response= client.get("proveedores/health")

    # Verificaciones
    assert response.status_code == 200
    json_data=response.json()
    assert json_data["status"] == "error"
    assert "Error al verificar la salud de la API" in json_data["message"]
    assert "'float' object has no attribute 'percent'" in json_data["details"]


@ patch("app.repositories.proveedor.RepositorioProveedor.obtener_todos", new_callable=AsyncMock)
def test_obtener_todos_exitoso_sin_registros(mock_obtener_todos):
    """Test obtener todos los proveedores de manera exitosa con 0 registros."""
    mock_obtener_todos.return_value={
        "data": [],
        "totalRows": 0
    }

    response=client.get("/proveedores")

    assert response.status_code == 200
    assert response.json() == mock_obtener_todos.return_value


@ patch("app.repositories.proveedor.RepositorioProveedor.obtener_por_id", new_callable=AsyncMock)
def test_obtener_por_id_no_encontrado(mock_obtener_por_id):
    """Test obtener proveedor por id cuando no existe."""
    mock_obtener_por_id.return_value=None

    response=client.get("/proveedores/8f5c7b3d-2a46-4e8b-8a9c-7e35d2f5b9c1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Proveedor no encontrado"}


@ patch("app.repositories.proveedor.RepositorioProveedor.obtener_por_id", new_callable=AsyncMock)
def test_obtener_por_id(mock_obtener_por_id):
    """Test obtener proveedor por id cuando no existe."""

    mock_obtener_por_id.return_value={
        "nombre": "luis",
        "tipo_identificacion": "Cedula",
        "direccion": "calle 23423",
        "ciudad": "Barranquilla",
        "identificacion": "1287189471",
        "correo": "l.mendoza@uniandes.edu.co",
        "id": "56b1d456-0c4e-4cd0-8c71-95c834c8dbd9",
        "pais": "Colombia",
        "fecha_creacion": "2025-03-22T01:37:32.546822"
    }

    response=client.get("/proveedores/56b1d456-0c4e-4cd0-8c71-95c834c8dbd9")

    assert response.status_code == 200
    assert response.json() == mock_obtener_por_id.return_value


@ patch("app.repositories.proveedor.RepositorioProveedor.crear", new_callable=AsyncMock)
def test_crear_proveedor_exitoso(mock_):
    """ Test crear un proveedor de manera exitosa """
    mock_payload={
        "tipo_identificacion": "NIT",
        "identificacion": "123456789",
        "nombre": "Proveedor 1",
        "correo": "luis@hotmail.com",
        "direccion": "Calle 1 # 1-1",
        "pais": "Colombia",
        "ciudad": "Barranquilla"
    }
    mock_.return_value={
        "tipo_identificacion": "NIT",
        "identificacion": "123456789",
        "nombre": "Proveedor 1",
        "correo": "luis@hotmail.com",
        "direccion": "Calle 1 # 1-1",
        "pais": "Colombia",
        "ciudad": "Barranquilla"
    }

    response=client.post("proveedores", json=mock_payload)

    assert response.status_code == 200
    assert response.json() == mock_.return_value
