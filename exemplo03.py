'''

Pequeno exemplo de uso do Flask-Bootstrap

https://pythonhosted.org/Flask-Bootstrap/

https://pythonhosted.org/flask-nav/


Exemplos com Bootstrap - https://getbootstrap.com/docs/3.3/getting-started/#examples

Veja mais detalhes nesse tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-facelift

'''

from flask import Flask, render_template, request, url_for,session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json

from werkzeug.utils import redirect

from meusforms import LoginForm, FormDeRegistro, RegisterForm

from dadostabela import *

SECRET_KEY = 'aula de BCD - string aleatória'

app = Flask(__name__)
app.secret_key = SECRET_KEY

boostrap = Bootstrap(app)  # isso habilita o template bootstrap/base.html
nav = Nav()
nav.init_app(app)  # isso habilita a criação de menus de navegação do pacote Flask-Nav

engine = create_engine("mysql+mysqlconnector://guilherme:56205340@localhost:3306/mydb")
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Usuario = Base.classes.Usuario
Evento = Base.classes.Evento
Agenda = Base.classes.Agenda
Inscricao = Base.classes.Inscricao


@nav.navigation()
def meunavbar():
    menu = Navbar('Gerenciador de Agenda')
    menu.items = [View('Home', 'inicio'), View('Gerenciar Agendas', 'autenticar'), View('Pessoas', 'pessoas')]
    return menu


@app.route('/pessoas')
def pessoas():
    sessionSQL = Session()
    if(session.get("login") is not None):
        pessoas = sessionSQL.query(Usuario).filter(Usuario.nome != session.get("login")).all()
    else:
        pessoas = sessionSQL.query(Usuario).all()
    sessionSQL.close()
    # pessoasJ = []
    # columnsJ = []
    # for p in pessoas:
    #     d: object = p.__dict__
    #     d2 = {"id": d.get('idUsuario'), "Nome": d.get('nome')}
    #     print(d2)
    #     pessoasJ.append(d2)
    # for p in pessoasJ[0].keys():
    #     columnsJ.append({"field": p, "title": p, "sortable": True})
    # for c in columnsJ:
    #     print(c)

    #return render_template('pessoas.html', data=pessoasJ, columns=columnsJ)
    return render_template('pessoas.html',pessoas = pessoas)


@app.route('/agendas')
def agendas():
    autenticado = False
    usuario = session.get('id')
    id = str(request.args.get('id'))
    if usuario is not None and usuario == id:
        autenticado = True
    sessionSQL = Session()
    agendas = sessionSQL.query(Agenda).filter(Agenda.idUsuario == id).all()
    sessionSQL.close()
    print(autenticado)
    return render_template('agendas.html', agendas=agendas, autenticado = autenticado)

@app.route('/excluir')
def excluir():
    idA = str(request.args.get('idA'))
    idU = str(request.args.get('idU'))
    idE = str(request.args.get('idE'))

    sessionSQL = Session()
    evento = sessionSQL.query(Evento).filter(
        Evento.idAgenda == idA, Evento.idUsuario == idU, Evento.idEvento == idE).first()

    sessionSQL.delete(evento)
    sessionSQL.commit()
    sessionSQL.close()
    return redirect(url_for("eventos", idA=idA,idU=idU))


@app.route('/inscritos')
def inscritos():
    idA = str(request.args.get('idA'))
    idU = str(request.args.get('idU'))
    idE = str(request.args.get('idE'))

    sessionSQL = Session()
    evento = sessionSQL.query(Evento).filter(
        Evento.idAgenda == idA, Evento.idUsuario == idU, Evento.idEvento == idE).first()

    inscritos = evento.inscricao_collection

    sessionSQL.close()
    return render_template('inscritos.html', evento=evento, inscritos = inscritos)

@app.route('/desativar')
def desativar():
 pass

@app.route('/eventos')
def eventos():
    idA = str(request.args.get('idA'))
    idU = str(request.args.get('idU'))

    autenticado = False
    usuario = session.get('id')
    if usuario is not None and usuario == idU:
        autenticado = True

    sessionSQL = Session()
    eventos = sessionSQL.query(Evento).filter(Evento.idAgenda == idA, Evento.idUsuario == idU).all()
    sessionSQL.close()

    return render_template('eventos.html', eventos=eventos,autenticado=autenticado)

@app.route('/inscricao', methods=['GET','POST'])
def inscricao():
    form = RegisterForm()
    form.idA = str(request.args.get('idA'))
    form.idU = str(request.args.get('idU'))
    form.idE = str(request.args.get('idE'))

    if form.validate_on_submit():
        sessionSQL = Session()
        evento = sessionSQL.query(Evento).filter(
            Evento.idAgenda == form.idA,Evento.idUsuario == form.idU,Evento.idEvento == form.idE).first()
        evento.vagas -= 1
        inscricao = Inscricao()
        inscricao.idUsuario = form.idU
        inscricao.idAgenda = form.idA
        inscricao.idEvento = form.idE
        inscricao.nome = form.name.data
        sessionSQL.add(inscricao)
        sessionSQL.commit()
        sessionSQL.close()
        return render_template('index.html')

    return render_template('inscricao.html', form=form)


@app.route('/registro', methods=['GET', 'POST'])
def cadastro():
    form = FormDeRegistro()
    if form.validate_on_submit():
        return render_template('index.html', title="Usuário registrado")
    return render_template('registro.html', title='Cadastro de usuário', form=form)


@app.route('/login', methods=['GET', 'POST'])
def autenticar():
    if(session.get("id") is not None):
        return redirect(url_for("agendas", id = session.get("id")))
    form = LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        senha = form.password.data
        sessionSQL = Session()
        usuario = sessionSQL.query(Usuario).filter(Usuario.nome == login).first()
        if (senha == usuario.senha):
            session["id"] = str(usuario.idUsuario)
            sessionSQL.close()
            return redirect(url_for("agendas", id = usuario.idUsuario))
        sessionSQL.close()
    return render_template('login.html', title='Autenticação de usuários', form=form)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/professor')
def professor():
    return render_template('index.html')


@app.route('/aluno')
def aluno():
    '''
    Ilustra um exemplo de como exibir tabelas. Também mostrado um exemplo do flask-bootstrap-table
    As estuturas de dados 'data'e 'columns' estão no script dadostabela.py
    :return:
    '''
    return render_template('alunos.html', data=data, columns=columns)


@app.errorhandler(404)
def page_not_found(e):
    '''
    Para tratar erros de páginas não encontradas - HTTP 404
    :param e:
    :return:
    '''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
