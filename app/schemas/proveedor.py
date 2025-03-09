from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ProveedorSchema(BaseModel):
    """ Esquema de validación para los datos de un proveedor """
    identificacion: str
    nombre: str
    correo: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    sitio_web: Optional[str] = None

    class Config:
        """ Configuración de la clase """
        from_attributes = True


class ProveedorUpdateSchema(BaseModel):
    """ Esquema de validación para los datos de actualización de un proveedor """

    class Config:
        """ Configuración de la clase """
        from_attributes = True
