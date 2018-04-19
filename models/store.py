from utils.database import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship("ItemModel", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def create_db(self):
        print(self.json())
        db.session.add(self)
        db.session.commit()

    def delete_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_one_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def json(self):
        return {"id": self.id, "name": self.name, "items": [item.json() for item in self.items.all()]}
