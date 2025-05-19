import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app correctly
import psutil

# Create a test client for FastAPI
client = TestClient(app)


class MockVirtualMemory:
    """ Clase Mock para simular el uso de memoria """

    def __init__(self, percent):
        self.percent = percent


class TestHealthCheck:
    """ Clase para probar el endpoint de health check """

    @patch("psutil.cpu_percent", return_value=30.0)  # Mock CPU usage
    @patch("psutil.virtual_memory")
    def test_health_check_exitoso(self, mock_memory, _):
        """Test successful health check response"""
        mock_memory.return_value.percent = 40.0  # Mock Memory usage

        response = client.get("proveedores/health")
        assert response.status_code == 200
        json_response = response.json()

        assert json_response["status"] == "ok"
        assert json_response["message"] == "API proveedores funcionando correctamente"
        assert isinstance(json_response["cpu_usage"], (int, float))
        assert isinstance(json_response["memory_usage"], (int, float))

    @pytest.mark.asyncio
    @patch("psutil.cpu_percent", return_value=30.5)
    @patch("psutil.virtual_memory", return_value=MockVirtualMemory(percent=70.0))
    async def test_health_check_exitoso_con_memoria(self, _, __):
        """Debe retornar status OK con métricas de CPU y memoria"""

        response = client.get("/proveedores/health")

        # Verifications
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["status"] == "ok"
        assert json_data["cpu_usage"] == 30.5
        assert json_data["memory_usage"] == 70.0

    # Simulate an error
    @patch("psutil.cpu_percent", side_effect=Exception("CPU Error"))
    def test_health_check_fallo_sin_memoria(self, _):
        """Test health check when an exception occurs"""
        response = client.get("proveedores/health")
        assert response.status_code == 200  # API should handle errors gracefully
        json_response = response.json()

        assert json_response["status"] == "error"
        assert json_response["message"] == "Error al verificar la salud de la API"
        assert "CPU Error" in json_response["details"]

    @pytest.mark.asyncio
    @patch("psutil.cpu_percent", return_value=30.5)
    @patch("psutil.virtual_memory", return_value=70.0)
    async def test_health_check_fallo_con_memoria(self, _, __):
        """Debe manejar excepciones y devolver status ERROR"""

        response= client.get("proveedores/health")

        # Verificaciones
        assert response.status_code == 200
        json_data=response.json()
        assert json_data["status"] == "error"
        assert "Error al verificar la salud de la API" in json_data["message"]
        assert "'float' object has no attribute 'percent'" in json_data["details"]
