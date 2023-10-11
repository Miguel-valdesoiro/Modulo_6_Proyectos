from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Define la instancia de Base correctamente
Base = declarative_base()


# Crea un motor SQLAlchemy y una sesión
engine = create_engine('sqlite:///database/tareas.db', connect_args={"check_same_thread": False})

# Crea la tabla 'tarea' en la base de datos
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
