""" Archivo principal de la aplicación FastAPI """
import logging
import time
import datetime
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from common_for_services.database.connection import engine, Base
from common_for_services.middleware.db_transaction import DBTransactionMiddleware
from common_for_services.tasks.celery_worker import celery
from app.routers import proveedor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main_app")

# Crear todas las tablas en la base de datos (si no existen)


async def init_db():
    """ Crear todas las tablas en la base de datos (si no existen) """
    start_time = time.time()
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tablas creadas correctamente")
    except Exception as e:
        process_time = time.time() - start_time

        log_data = {
            "package": "middleware",
            "module": "db_transaction.DBTransactionMiddleware",
            "log": "CRITICAL",
            "event": "db_transaction_error",
            "error": str(e),
            "method": None,
            "path": None,
            "response_time": f"Request processed in {process_time:.2f} seconds",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        celery.send_task(
                    "celery_worker.tasks.log_to_logging_service_task", args=[log_data])
        celery.send_task(
            "celery_worker.tasks.send_email_task",
            args=["admin@example.com", "Database Error Alert",
                    json.dumps(log_data, indent=2)]
        )
        logger.critical(
            "La conexión a la base de datos ha fallado al iniciar la aplicación")

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Gestión de Proveedores",
    description="""Una API para manejar proveedores y productos que ofrece un proveedor
                    usando FastAPI y SQLAlchemy.""",
    version="1.0.0"
)

# Configuración de CORS (Permitir acceso desde frontend)
app.add_middleware(
    CORSMiddleware,
    # Cambia esto por los dominios permitidos en producción
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Routers
app.include_router(proveedor.router, prefix="/proveedores",
                   tags=["Proveedores"])


# Health Check Endpoint
@app.get("/documentation", tags=["General"])
async def root():
    """Ruta principal de la API"""
    return {
        "message": "Bienvenido a la API de Proveedores 🚀",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": app.version
    }

app.add_middleware(DBTransactionMiddleware, celery_app=celery)


@app.on_event("startup")
async def on_startup():
    """ Crear la base de datos y las tablas al iniciar la aplicación """
    await init_db()
