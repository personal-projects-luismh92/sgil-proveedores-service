from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.proveedor import RepositorioProveedor
from app.schemas.proveedor import ProveedorSchema, ProveedorUpdateSchema
from uuid import UUID

class ProveedorService:
    """ Servicio de proveedores """
    @staticmethod
    async def obtener_todos(db: AsyncSession, page: int, per_page: int):
        """ Obtiene todos los proveedores """
        return await RepositorioProveedor.obtener_todos(db, page, per_page)

    @staticmethod
    async def obtener_por_id(db: AsyncSession, proveedor_id: UUID):
        """ Obtiene un proveedor por su ID """
        return await RepositorioProveedor.obtener_por_id(db, proveedor_id)

    @staticmethod
    async def crear(db: AsyncSession, proveedor_data: ProveedorSchema):
        """ Crea un proveedor """
        return await RepositorioProveedor.crear(db, proveedor_data)


 
