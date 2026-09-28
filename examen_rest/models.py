from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Laptop(Base):
    __tablename__ = "laptops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    marca: Mapped[str] = mapped_column(String(100))
    modelo: Mapped[str] = mapped_column(String(100))
    ram_gb: Mapped[int] = mapped_column(Integer)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True)


class LaptopCreate(BaseModel):
    marca: str
    modelo: str
    ram_gb: int