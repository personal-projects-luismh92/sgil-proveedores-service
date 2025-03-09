""" Rutas para el CRUD de proveedores """
import asyncio
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from common_for_services.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.proveedor import ProveedorService
from app.schemas.proveedor import ProveedorSchema, ProveedorUpdateSchema
import psutil
router = APIRouter()

# Health Check Endpoint


@router.get("/health")
async def health_check():
    """Verifica que la API esté funcionando correctamente"""
    try:

        # Call the function
        cpu_usage = await asyncio.to_thread(psutil.cpu_percent)
        # Wrap in lambda
        memory_usage = await asyncio.to_thread(lambda: psutil.virtual_memory().percent)

        return {
            "status": "ok",
            "message": "API proveedores funcionando correctamente",
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }

    except Exception as e:
        return {"status": "error",
                "message": "Error al verificar la salud de la API",
                "details": str(e)}


@router.get("")
async def obtener_proveedores(request: Request, db: AsyncSession = Depends(get_db)):
    """ Obtiene todos los proveedores """

    params = request.query_params
    per_page = int(params.get("size", 10))
    page = params.get("page", 1)
    if page is not None:
        page = int(page) - 1
    return await ProveedorService.obtener_todos(db,  page, per_page)


@router.get("/{proveedor_id}")
async def obtener_proveedor(proveedor_id: UUID, db: AsyncSession = Depends(get_db)):
    proveedor = await ProveedorService.obtener_por_id(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.post("")
async def crear_proveedor(proveedor_data: ProveedorSchema,
                          db: AsyncSession = Depends(get_db)):
    """Crea un proveedor"""
    return await ProveedorService.crear(db, proveedor_data)


@router.post("error-database")
async def crear_proveedor_error_db(proveedor_data: ProveedorSchema,
                                   db: AsyncSession = Depends(get_db)):
    """Crea un proveedor con error en la base de datos"""
    return await ProveedorService.crear_error_db(db, proveedor_data)


@router.put("/{proveedor_id}")
async def actualizar_proveedor(proveedor_id: int,
                               proveedor_data: ProveedorUpdateSchema,
                               db: AsyncSession = Depends(get_db)):
    """ Actualiza un proveedor """
    proveedor_actualizado = await ProveedorService.actualizar(
        db, proveedor_id, proveedor_data)
    if not proveedor_actualizado:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor_actualizado


@router.delete("/{proveedor_id}")
async def eliminar_proveedor(proveedor_id: int,
                             db: AsyncSession = Depends(get_db)):
    """ Elimina un proveedor """
    if not await ProveedorService.eliminar(db, proveedor_id):
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return {"message": "Proveedor eliminado"}
