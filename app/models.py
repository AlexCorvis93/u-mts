from datetime import datetime
from app import db


class Product(db.Model):
    """Б/У оборудование"""
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float())
    description = db.Column(db.Text(), nullable=True)
    image = db.relationship('ProductImage', backref='product')

    def __repr__(self):
        return f"{self.id}"


class ProductImage(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f"{self.prod_id}"


class Proposal(db.Model):
    """Заявка от клиента"""
    __tablename__ = 'proposal'
    id = db.Column(db.Integer(), primary_key=True)
    customer = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"Заявка от: {self.customer}+{self.email}+{self.date}"


class CompletedProposal(db.Model):
    """Отработанная заявка от клиента"""
    __tablename__ = 'completed'
    id = db.Column(db.Integer(), primary_key=True)
    customer = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"Заявка от: {self.customer}+{self.email}+{self.date}"


