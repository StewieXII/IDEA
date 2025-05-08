from . import db  # Importar la instancia de db desde __init__.py
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):  # Usa la instancia de db que está en __init__.py
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Usuario {self.email}>'