from app_.config.db import db

class Heladeria(db.Model):
    __tablename__ = 'heladerias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ventas_diarias = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Heladeria {self.nombre}>"
