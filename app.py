'''

Pequeno exemplo de uso do Flask-Bootstrap

https://pythonhosted.org/Flask-Bootstrap/

https://pythonhosted.org/flask-nav/


Exemplos com Bootstrap - https://getbootstrap.com/docs/3.3/getting-started/#examples

Veja mais detalhes nesse tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-facelift

'''
import sys
from datetime import datetime, date

import sqlalchemy
from flask import Flask, render_template, request, url_for, session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from meusforms import LoginForm, RegisterForm, AgendaForm, EventoForm

SECRET_KEY = 'aula de BCD - string aleatória'

app = Flask(__name__)
app.secret_key = SECRET_KEY

boostrap = Bootstrap(app)  # isso habilita o template bootstrap/base.html
nav = Nav()
nav.init_app(app)  # isso habilita a criação de menus de navegação do pacote Flask-Nav
user_mysql = sys.argv[1]
pass_mysql = sys.argv[2]
engine = create_engine("mysql+mysqlconnector://" + user_mysql + ":" + pass_mysql +"@localhost:3306/mydb")
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Usuario = Base.classes.Usuario
Evento = Base.classes.Evento
Agenda = Base.classes.Agenda
Inscricao = Base.classes.Inscricao


@nav.navigation()
def meunavbar():
    menu = Navbar('')
    menu.items = [View('Home', 'inicio'), View('Gerenciar Agendas', 'autenticar'), View('Pessoas', 'pessoas')]
    return menu


@app.route('/pessoas')
def pessoas():
    sessionSQL = Session()
    if (session.get("login") is not None):
        pessoas = sessionSQL.query(Usuario).filter(Usuario.nome != session.get("login")).all()
    else:
        pessoas = sessionSQL.query(Usuario).all()
    sessionSQL.close()
    return render_template('pessoas.html', pessoas=pessoas)


@app.route('/agendas', methods=['GET', 'POST'])
def agendas():
    if request.method == 'GET':
        autenticado = False
        usuario = session.get('id')
        id = str(request.args.get('id'))
        if usuario is not None and usuario == id:
            autenticado = True
        sessionSQL = Session()
        if autenticado:
            agendas = sessionSQL.query(Agenda).filter(Agenda.idUsuario == id).all()
        else:
            agendas = sessionSQL.query(Agenda).filter(Agenda.idUsuario == id, Agenda.estado == 1).all()
        sessionSQL.close()
        return render_template('agendas.html', agendas=agendas, autenticado=autenticado)
    else:
        if session.get('id') is not None:
            sessionSQL = Session()
            agenda = sessionSQL.query(Agenda)
            idU = request.form['idU']
            idA = request.form['idA']
            estado = request.form['estado']
            agenda = sessionSQL.query(Agenda) \
                .filter(Agenda.idUsuario == idU, Agenda.idAgenda == idA).first()
            agenda.estado = int(estado)
            sessionSQL.commit()
            agendas = sessionSQL.query(Agenda).filter(Agenda.idUsuario == idU).all()
            sessionSQL.close()
            return render_template('agendas.html', agendas=agendas, autenticado=True)
        else:
            return redirect(url_for("autenticar"))


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
    return redirect(url_for("eventos", idA=idA, idU=idU))


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
    return render_template('inscritos.html', evento=evento, inscritos=inscritos)


@app.route('/eventos',  methods=['GET'])
def eventos():
    if request.method == 'GET':
        idA = str(request.args.get('idA'))
        idU = str(request.args.get('idU'))

        autenticado = False
        usuario = session.get('id')
        if usuario is not None and usuario == idU:
            autenticado = True

        sessionSQL = Session()
        if autenticado:
            eventos = sessionSQL.query(Evento).filter(Evento.idAgenda == idA, Evento.idUsuario == idU).all()
        else:
            eventos = sessionSQL.query(Evento).filter(Evento.idAgenda == idA,
                                                      Evento.idUsuario == idU, Evento.vagas > 0).all()
        sessionSQL.close()

        return render_template('eventos.html', eventos=eventos, autenticado=autenticado, idA=idA)


@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    form = RegisterForm()
    form.idA = str(request.args.get('idA'))
    form.idU = str(request.args.get('idU'))
    form.idE = str(request.args.get('idE'))

    if form.validate_on_submit():
        sessionSQL = Session()
        evento = sessionSQL.query(Evento).filter(
            Evento.idAgenda == form.idA, Evento.idUsuario == form.idU, Evento.idEvento == form.idE).first()
        evento.vagas -= 1
        inscricao = Inscricao()
        inscricao.idUsuario = form.idU
        inscricao.idAgenda = form.idA
        inscricao.idEvento = form.idE
        inscricao.idInscricao = form.name.data
        try:
            sessionSQL.add(inscricao)
            sessionSQL.commit()
            sessionSQL.close()
        except sqlalchemy.exc.IntegrityError:
            return render_template('inscricao.html', form=form, message="Erro: Nome já inscrito nesta agenda")

        return render_template('index.html')

    return render_template('inscricao.html', form=form, message=None)


@app.route('/login', methods=['GET', 'POST'])
def autenticar():
    if session.get("id") is not None:
        return redirect(url_for("agendas", id=session.get("id")))
    form = LoginForm()
    message = None
    if form.validate_on_submit():
        login = form.username.data
        sessionSQL = Session()
        usuario = sessionSQL.query(Usuario).filter(Usuario.nome == login).first()
        if usuario is not None:
            if check_password_hash(usuario.senha, form.password.data):
                session["id"] = str(usuario.idUsuario)
                sessionSQL.close()
                return redirect(url_for("agendas", id=usuario.idUsuario))
        else:
            message = "Nome ou senha incorretos"
        sessionSQL.close()
    return render_template('login.html', title='Autenticação de usuários', form=form, message = message)


@app.route('/registro_agenda', methods=['GET', 'POST'])
def registro_agenda():
    if session.get("id") is not None:
        form = AgendaForm()
        if form.validate_on_submit():
            sessionSQL = Session()
            agenda = Agenda()
            agenda.idUsuario = session.get("id")
            agenda.descricao = form.desc.data
            estado = form.status.data
            if estado == 'en':
                agenda.estado = 1
            else:
                agenda.estado = 0
            sessionSQL.add(agenda)
            sessionSQL.commit()
            sessionSQL.close()
            return redirect(url_for("agendas", id=session.get("id")))

        return render_template('registro_agenda.html', form=form)
    else:
        return redirect(url_for("autenticar"))


@app.route('/registro_evento', methods=['GET', 'POST'])
def registro_evento():
    if session.get("id") is not None:
        form = EventoForm()
        if form.validate_on_submit():

            if form.inicio.data > form.fim.data:
                message = "Erro: Hora de início posterior a hora de término"
                return render_template('registro_evento.html', form=form, message=message)
            elif form.date.data < date.today():
                message = "Erro: Data anterior a data atual"
                return render_template('registro_evento.html', form=form, message=message)

            evento = Evento()
            evento.idUsuario = session.get("id")
            evento.descricao = form.desc.data
            evento.idAgenda = request.args.get('idA')
            evento.dia = str(form.date.data)
            evento.inicio = str(form.inicio.data)
            evento.fim = str(form.fim.data)
            evento.vagas = form.vagas.data

            sessionSQL = Session()
            sessionSQL.add(evento)
            sessionSQL.commit()
            sessionSQL.close()

            return redirect(url_for("agendas", id=session.get("id")))

        return render_template('registro_evento.html', form=form, message=None)

    else:
        return redirect(url_for("autenticar"))


@app.route('/')
def inicio():
    return render_template('index.html')

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
