import sqlalchemy as sa
import sqlalchemy.orm as so

from app.extensions import db


class DataPoint(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    weight: so.Mapped[float] = so.mapped_column(sa.Float)
    height: so.Mapped[float] = so.mapped_column(sa.Float)
    category: so.Mapped[int] = so.mapped_column(sa.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'weight': self.weight,
            'height': self.height,
            'category': self.category
        }
