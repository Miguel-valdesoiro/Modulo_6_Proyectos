from sqlalchemy import Column, Integer, String, Boolean, Date
import db
import datetime  # Import the datetime module

class Tarea(db.Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    categoria = Column(String(50))  # Agregamos el campo "categoria"
    fecha_limite = Column(Date)  # Agregamos el campo "fecha_limite"
    hecha = Column(Boolean)

    def __init__(self, contenido, categoria=None, fecha_limite=False, hecha=False):
        self.contenido = contenido
        self.categoria = categoria
        self.fecha_limite = fecha_limite or datetime.date.today()  # Use the current date as the default
        self.hecha = hecha
        print("Tarea creada con éxito")

    def __str__(self):
        return "Tarea {}: {} ({}, {}, {})".format(
            self.id, self.contenido, self.categoria, self.fecha_limite, self.hecha
        )

