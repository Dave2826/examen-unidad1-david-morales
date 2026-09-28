from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import Laptop, LaptopCreate


app = FastAPI(title="API del laboratorio de cómputo")


def cargar_datos_iniciales():
    db = SessionLocal()

    try:
        if db.query(Laptop).count() == 0:
            laptops = [
                Laptop(
                    marca="Dell",
                    modelo="Latitude 5440",
                    ram_gb=16,
                    disponible=True
                ),
                Laptop(
                    marca="Lenovo",
                    modelo="ThinkPad E14",
                    ram_gb=8,
                    disponible=False
                ),
                Laptop(
                    marca="HP",
                    modelo="ProBook 450",
                    ram_gb=16,
                    disponible=True
                )
            ]

            db.add_all(laptops)
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    cargar_datos_iniciales()


@app.get("/")
def inicio():
    return {"mensaje": "API del laboratorio de cómputo"}


@app.get("/laptops")
def listar_laptops(db: Session = Depends(get_db)):
    return db.query(Laptop).all()


@app.get("/laptops/disponibles")
def listar_laptops_disponibles(db: Session = Depends(get_db)):
    return db.query(Laptop).filter(Laptop.disponible == True).all()


@app.get("/laptops/{laptop_id}")
def obtener_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()

    if not laptop:
        raise HTTPException(
            status_code=404,
            detail="Laptop no encontrada"
        )

    return laptop


@app.post("/laptops")
def crear_laptop(
    laptop: LaptopCreate,
    db: Session = Depends(get_db)
):
    nueva_laptop = Laptop(
        marca=laptop.marca,
        modelo=laptop.modelo,
        ram_gb=laptop.ram_gb,
        disponible=True
    )

    db.add(nueva_laptop)
    db.commit()
    db.refresh(nueva_laptop)

    return nueva_laptop