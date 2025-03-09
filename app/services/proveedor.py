from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.proveedor import RepositorioProveedor
from app.schemas.proveedor import ProveedorSchema, ProveedorUpdateSchema


class ProveedorService:
    @staticmethod
    async def obtener_todos(db: AsyncSession, page: int, per_page: int):
        """ Obtiene todos los proveedores """
        return await RepositorioProveedor.obtener_todos(db, page, per_page)

    @staticmethod
    async def obtener_por_id(db: AsyncSession, proveedor_id: int):
        """ Obtiene un proveedor por su ID """
        return await RepositorioProveedor.obtener_por_id(db, proveedor_id)

    @staticmethod
    async def crear(db: AsyncSession, proveedor_data: ProveedorSchema):
        """ Crea un proveedor """
        return await RepositorioProveedor.crear(db, proveedor_data)

    @staticmethod
    async def crear_error_db(db: AsyncSession, proveedor_data: ProveedorSchema):
        """ Crea un proveedor con error en la base de datos """
        return await RepositorioProveedor.crear_error_db(db, proveedor_data)

    @staticmethod
    async def actualizar(db: AsyncSession,
                         proveedor_id: int,
                         proveedor_data: ProveedorUpdateSchema):
        """ Actualiza un proveedor """
        return await RepositorioProveedor.actualizar(db, proveedor_id, proveedor_data)

    @staticmethod
    async def eliminar(db: AsyncSession, proveedor_id: int):
        """ Elimina un proveedor """
        return await RepositorioProveedor.eliminar(db, proveedor_id)
