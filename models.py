from flask_sqlalchemy import SQLAlchemy
from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    pedidos = db.relationship('Pedido', back_populates='user')

    def __repr__(self):
        return f"<User {self.name} - {self.email}>"


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    data = db.Column(db.DateTime, nullable=False) 
    status = db.Column(db.String(50), nullable=False, default='Pedido Concluído') 
    user = db.relationship('User', back_populates='pedidos')
    itens = db.relationship('Item', backref='pedido', lazy=True)
    valorPedido = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Pedido {self.id} - {self.status}>"


class Item(db.Model):
    __tablename__ = 'itens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)  
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False) 
    quantidade = db.Column(db.Integer, nullable=False)
    produto = db.relationship('Produto', backref='itens', lazy=True)

    def __repr__(self):
        return f"<Item {self.id} - {self.produto.nome}>"


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Produto {self.nome} - R$ {self.preco}>"
