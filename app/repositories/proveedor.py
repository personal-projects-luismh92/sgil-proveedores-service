""" Módulo que contiene la clase RepositorioProveedor """
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import Query
from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorSchema
from uuid import UUID


class RepositorioProveedor:
    """  Repositorio de proveedores """
    @staticmethod
    async def obtener_todos(db: AsyncSession,
                            page: Optional[int] = Query(
                                None, alias="page", ge=0),
                            size: Optional[int] = Query(None, alias="size", ge=1, le=100)):
        """Obtiene todos los proveedores de forma asíncrona"""

        # Count total records before pagination
        # Count the rows by the 'id' column
        count_query = select(func.count(Proveedor.id))
        result = await db.execute(count_query)
        total_rows = result.scalar()

        # Base query for getting rows
        query = select(Proveedor)

        # Apply pagination if both page and size are provided
        if page is not None and size is not None:
            query = query.offset(page * size).limit(size)
            total_pages = (total_rows + size - 1) // size  # Ceiling division
        else:
            total_pages = None  # No pagination

        # Execute the query to fetch the results
        result = await db.execute(query)
        data = result.scalars().all()

        # Prepare the response
        response = {
            "data": data,
            "totalRows": total_rows,
            "totalPages": total_pages
        }

        if total_pages is None:
            del response["totalPages"]

        return response

    @staticmethod
    async def obtener_por_id(db: AsyncSession, proveedor_id: UUID):
        """Obtiene un proveedor por su ID de forma asíncrona"""
        result = await db.execute(select(Proveedor).filter_by(id=proveedor_id))
        return result.scalars().first()

    @staticmethod
    async def crear(db: AsyncSession, proveedor_data: ProveedorSchema):
        """Crea un nuevo proveedor de forma asíncrona"""
        nuevo_proveedor = Proveedor(**proveedor_data.model_dump())
        db.add(nuevo_proveedor)
        await db.commit()
        await db.refresh(nuevo_proveedor)
        return nuevo_proveedor
