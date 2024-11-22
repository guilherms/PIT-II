from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, User, Pedido, Produto, Item
from flask_migrate import Migrate
from db import db, migrate 
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secrect-key-for-session' 


    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def home():
        is_logged_in = 'user_id' in session
        return render_template('indexprodutos.html', is_logged_in=is_logged_in)

    @app.route('/carrinho')
    def carrinho():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('carrinho.html')

    @app.route('/contato')
    def contato():    
        return render_template('contato.html')

    from sqlalchemy.orm import joinedload
    @app.route('/historico', methods=['GET'])
    def historico():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        pedidos = Pedido.query.filter_by(user_id=user_id).options(joinedload(Pedido.itens).joinedload(Item.produto)).all()
        

        for pedido in pedidos:
            print(f"Pedido ID: {pedido.id}, Status: {pedido.status}")
            for item in pedido.itens:
                print(f"Produto: {item.produto.nome}, Preço: {item.produto.preco}, Quantidade: {item.quantidade}")

        return render_template('historico.html', pedidos=pedidos)

    @app.route('/finalizar', methods=['GET', 'POST'])
    def finalizar():
        if request.method == 'GET':
            return render_template('finalizar.html')

        if 'user_id' not in session:
            return redirect(url_for('login'))

        data = request.get_json()
        carrinho = data.get('carrinho', [])

        if not carrinho:
            return jsonify({'error': 'Carrinho vazio'}), 400

        user_id = session['user_id']
        pedido = Pedido(user_id=user_id, data=datetime.utcnow(), status='Pedido Concluído')
        total = 0
        
        db.session.add(pedido)
        db.session.commit() 

        for item in carrinho:
            if item['sabor'] == "chocolate":
                item['sabor'] = "Chocolate"
            if item['sabor'] == "baunilha":
                item['sabor'] = "Baunilha"
            if item['sabor'] == "morango":
                item['sabor'] = "Morango"

            produto = Produto.query.filter_by(nome=item['sabor']).first()
            if produto:
                item_pedido = Item(pedido_id=pedido.id, produto_id=produto.id, quantidade=item['quantidade'])
                total += (float(item['quantidade']) * float(item['preco']))
                db.session.add(item_pedido)

        pedido.valorPedido = total
        db.session.commit()

        return jsonify({'message': 'Pedido finalizado com sucesso!'}), 200


    @app.route('/pedido_confirmado')
    def pedido_confirmado():
        return render_template('pedido_confirmado.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            telefone = request.form['telefone']
            email = request.form['email']
            cpf = request.form['cpf']
            senha = request.form['senha']  
            confirma_senha = request.form['confirm-senha']  
            endereco = request.form['endereco']
            cep = request.form['cep']
            bairro = request.form['bairro']
            cidade = request.form['cidade']
            sexo = request.form['sexo']

            if senha != confirma_senha:
                return "As senhas não coincidem. Tente novamente.", 400 

            try:
                new_user = User(
                    name=name, telefone=telefone, email=email, cpf=cpf, senha=senha,
                    endereco=endereco, cep=cep, bairro=bairro, cidade=cidade, sexo=sexo
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                return f"Ocorreu um erro ao registrar o usuário: {e}", 500  

        return render_template('cadastro.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None 
        if request.method == 'POST':

            email = request.form['email']
            senha = request.form['senha']
            user = User.query.filter_by(email=email).first()

            if user and user.senha == senha:
                session['user_id'] = user.id  
                return redirect(url_for('home'))
            else:
                error = "Credenciais inválidas. Verifique o e-mail ou senha."
        
        return render_template('indexlogin.html', error=error)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0')
