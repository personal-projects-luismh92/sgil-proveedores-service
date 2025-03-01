"""Módulo de modelo de proveedor"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, UUID, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from common_for_services.database.connection import Base

class Proveedor(Base):
    """Modelo de Proveedor en el servicio de proveedores"""
    __tablename__ = "proveedor"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, nullable=False)
    identificacion = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Número de identificación fiscal o comercial (NIT, RFC, RUC, etc.)"
    )
    nombre = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Nombre de la empresa proveedora"
    )
    correo = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
        comment="Correo electrónico de contacto"
    )
    telefono = Column(
        String(20),
        nullable=True,
        comment="Número de teléfono del proveedor"
    )
    direccion = Column(
        Text,
        nullable=True,
        comment="Dirección física del proveedor"
    )
    sitio_web = Column(
        String(255),
        nullable=True,
        comment="Sitio web del proveedor"
    )
    fecha_creacion = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("correo LIKE '%@%.%' OR correo IS NULL",
                        name="check_correo_format"),
        CheckConstraint("LENGTH(telefono) >= 7 OR telefono IS NULL",
                        name="check_telefono_length"),
        CheckConstraint(
            "LENGTH(identificacion) >= 6 AND identificacion NOT LIKE ' %'", name="check_identificacion"),
    )
