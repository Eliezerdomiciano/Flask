import secrets
import os
from flask import redirect, render_template, url_for, flash, request, session, current_app


# from loja.admin.rotas import categoria, marcas
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto


@app.route('/addpedido', methods=['GET', 'POST'])
def addpedido():
    if 'email' not in session:
        flash(f'Favor fazer login Primeiro', 'success')
        return redirect(url_for('login'))

    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":
        name = form.name.data
        preco = form.preco.data
        desconto = form.desconto.data
        estoque = form.estoque.data
        cores = form.cores.data
        descricao = form.descricao.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')
        try:
            imagem_1 = photos.save(request.files.get(
                'imagem_1'), name=secrets.token_hex(10) + ".")
            imagem_2 = photos.save(request.files.get(
                'imagem_2'), name=secrets.token_hex(10) + ".")
            imagem_3 = photos.save(request.files.get(
                'imagem_3'), name=secrets.token_hex(10) + ".")

            addpedido = Addproduto(name=name, preco=preco, desconto=desconto, estoque=estoque, cores=cores, descricao=descricao,
                                   marca_id=marca, categoria_id=categoria, imagem_1=imagem_1, imagem_2=imagem_2, imagem_3=imagem_3)
            db.session.add(addpedido)
            flash(f'Produto {name} foi cadastrada com sucesso', 'success')
            db.session.commit()
            return redirect(url_for('cliente'))
        except:
            flash('Tipo de imagem não reconhecida', 'Danger')

    return render_template('/cliente/addpedido.html', title="Cadastrar Produtos", form=form, marcas=marcas, categorias=categorias)



