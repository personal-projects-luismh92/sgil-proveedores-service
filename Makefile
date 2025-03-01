# Variables
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# Crear y activar el entorno virtual
venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip --extra-index-url https://pypi.org/simple

# Instalar dependencias
install: venv
	$(PIP) install -r requirements.txt --extra-index-url https://pypi.org/simple

# Ejecutar la API en local con recarga automática
run:
	export DB_HOST_URL="127.0.0.1:5432"; \
	export DB_NAME="sgil-proveedores"; \
	export DB_USER="postgres"; \
	export DB_PASSWORD="123456"; \
	. $(VENV_DIR)/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload

# Ejecutar pruebas con pytest
test:
	pytest -v

# Formatear código con Black
format:
	black .

# Revisar errores con Flake8
lint:
	flake8 .

# Eliminar el entorno virtual
clean:
	rm -rf $(VENV_DIR) __pycache__

# Regenerar el entorno virtual y reinstalar dependencias
reset: clean venv install

# Ejecutar migraciones con Alembic (si usas migraciones)
migrate:
	alembic upgrade head

# Crear un nuevo archivo de migración (si usas Alembic)
makemigrations:
	alembic revision --autogenerate -m "Nueva migración"
