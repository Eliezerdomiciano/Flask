import secrets
import os
from flask import redirect, render_template, url_for, flash, request, session, current_app


from loja.admin.rotas import categoria, marcas
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto


@app.route('/')
def home():
    pagina = request.args.get('pagina', 1, type=int)
    produtos = Addproduto.query.filter(Addproduto.estoque > 0).pagina(pagina=pagina, per_pagina=1)
    marcas = Marca.query.join(
        Addproduto, (Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(
        Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
    return render_template('/produtos/index.html', produtos=produtos, marcas=marcas, categorias=categorias)


@app.route('/marca/<int:id>')
def get_marca(id):
    marca = Addproduto.query.filter_by(marca_id=id)
    marcas = Marca.query.join(
        Addproduto, (Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(
        Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
    return render_template('/produtos/index.html', marca=marca, marcas=marcas, categorias=categorias)


@app.route('/categorias/<int:id>')
def get_categoria(id):
    get_cat_prod = Addproduto.query.filter_by(categoria_id=id)
    categorias = Categoria.query.join(
        Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
    marcas = Marca.query.join(
        Addproduto, (Marca.id == Addproduto.marca_id)).all()
    return render_template('/produtos/index.html', get_cat_prod=get_cat_prod, categorias=categorias, marcas=marcas)


@app.route('/addmarca', methods=['GET', 'POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Favor fazer login Primeiro', 'success')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')


@app.route('/updatemarca/<int:id>', methods=['GET', 'POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Favor fazer login Primeiro', 'success')
        return redirect(url_for('login'))
    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method == 'POST':
        updatemarca.name = marca
        flash(f'Seu Fabricante foi atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))
    return render_template('/produtos/updatemarca.html', title='Atualizar Fabricantes', updatemarca='updatemarca')


@app.route('/deletemarca/<int:id>', methods=['GET', 'POST'])
def deletemarca(id):
    marca = Marca.query.get_or_404(id)
    if request.method == 'GET':
        db.session.delete(marca)
        db.session.commit()
        flash(f'A Marca {marca.name} Foi deletada com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {marca.name} não foi deletada', 'warning')
    return redirect(url_for('admin'))


@app.route('/deletecategoria/<int:id>', methods=['GET', 'POST'])
def deletecategoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'GET':
        db.session.delete(categoria)
        db.session.commit()
        flash(
            f'A Categoria {categoria.name} Foi deletada com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A categoria {categoria.name} não foi deletada', 'warning')
    return redirect(url_for('admin'))


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Favor fazer login Primeiro', 'success')
        return redirect(url_for('login'))
    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method == 'POST':
        updatecat.name = categoria
        flash(f'Seu Categoria foi atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))

    return render_template('/produtos/updatemarca.html', title='Atualizar Categoria', updatecat='updatecat')


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Favor fazer login Primeiro', 'success')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        cat = Categoria(name=getmarca)
        db.session.add(cat)
        flash(f'A categoria {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html')


@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
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

            addpro = Addproduto(name=name, preco=preco, desconto=desconto, estoque=estoque, cores=cores, descricao=descricao,
                                marca_id=marca, categoria_id=categoria, imagem_1=imagem_1, imagem_2=imagem_2, imagem_3=imagem_3)
            db.session.add(addpro)
            flash(f'Produto {name} foi cadastrada com sucesso', 'success')
            db.session.commit()
            return redirect(url_for('admin'))
        except:
            flash('Tipo de imagem não reconhecida', 'Danger')

    return render_template('/produtos/addproduto.html', title="Cadastrar Produtos", form=form, marcas=marcas, categorias=categorias)


@app.route('/updateproduto/<int:id>', methods=['GET', 'POST'])
def updateproduto(id):
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)
    if request.method == "POST":
        produto.name = form.name.data
        produto.preco = form.preco.data
        produto.desconto = form.desconto.data
        produto.estoque = form.estoque.data
        produto.descricao = form.descricao.data
        produto.cores = form.cores.data

        produto.marca_id = marca
        produto.categoria_id = categoria

        # Salvando Imagem 1
        if request.files.get('imagem_1'):
            try:

                os.unlink(os.path.join(current_app.root_path,
                          "static/imagens/" + produto.imagem_1))
                produto.imagem_1 = photos.save(request.files.get(
                    'imagem_1'), name=secrets.token_hex(10)+".")

            except:
                produto.imagem_1 = photos.save(request.files.get(
                    'imagem_1'), name=secrets.token_hex(10)+".")

        # Salvando Imagem 2
        if request.files.get('imagem_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/imagens/" + produto.imagem_2))
                produto.imagem_2 = photos.save(request.files.get(
                    'imagem_2'), name=secrets.token_hex(10)+".")

            except:
                produto.imagem_2 = photos.save(request.files.get(
                    'imagem_2'), name=secrets.token_hex(10)+".")

        # Salvando Imagem 3
        if request.files.get('imagem_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/imagens/" + produto.imagem_3))
                produto.imagem_3 = photos.save(request.files.get(
                    'imagem_3'), name=secrets.token_hex(10)+".")

            except:
                produto.imagem_3 = photos.save(request.files.get(
                    'imagem_3'), name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'Produto foi atualizado com sucesso', 'success')
        return redirect('/')

    form.name.data = produto.name
    form.preco.data = produto.preco
    form.desconto.data = produto.desconto
    form.estoque.data = produto.estoque
    form.descricao.data = produto.descricao
    form.cores.data = produto.cores

    return render_template('/produtos/updateproduto.html', title='Atualizar Produtos', form=form, marcas=marcas, categorias=categorias, produto=produto)


@app.route('/deleteproduto/<int:id>', methods=['GET', 'POST'])
def deleteproduto(id):
    produto = Addproduto.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('imagem_1'):
            try:

                os.remove(os.path.join(current_app.root_path,
                          "static/imagens/" + produto.imagem_1))
                os.remove(os.path.join(current_app.root_path,
                          "static/imagens/" + produto.imagem_2))
                os.remove(os.path.join(current_app.root_path,
                          "static/imagens/" + produto.imagem_3))
            except Exception as e:
                print(e)
        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f'Produto {produto.name} não foi deletado com sucesso', 'warning')

    return redirect(url_for('admin'))
