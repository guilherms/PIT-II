from app import create_app, db
from models import Produto

app = create_app()

with app.app_context():
    produtos = [
        {"nome": "Chocolate", "preco": 12.00},
        {"nome": "Morango", "preco": 12.00},
        {"nome": "Baunilha", "preco": 10.00}
    ]

    for produto in produtos:
        novo_produto = Produto(nome=produto['nome'], preco=produto['preco'])
        db.session.add(novo_produto)

    db.session.commit()
    print("Produtos cadastrados com sucesso!")

