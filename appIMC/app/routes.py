from flask import Flask, render_template, request, redirect, json
from app.mongo import MongoAPI
import socket
from prometheus_flask_exporter import PrometheusMetrics

# dataMongo = {
#         "url": "mongodb://localhost:50027/admin",
#         "database": "flaskDB",
#         "collection": "IMC",
#     }

dataMongo = {
    "url": "mongodb://mongodb-service:27017/admin",
    "database": "flaskDB",
    "collection": "IMC"}


app = Flask(__name__)
# METRICS
metrics = PrometheusMetrics(app)
versao = "v1.0.1"
contador_por_path = metrics.counter(
    'url', 'Requests count by url', labels={'url': lambda: request.path, 'versao': versao}
)
# END METRICS - ITALO

meuhost = socket.gethostname()

@app.route('/')
@app.route('/index')
@contador_por_path
def index():

    entries = MongoAPI(dataMongo).read()
    return render_template('index.html',
                           entries=entries, 
                           meuhost=meuhost)


@app.route('/add', methods=['POST'])
def add():
    form = request.form
    fn = form.get('Nome')
    fp = float(form.get('Peso'))
    fa = float(form.get('Altura'))
    imc = round(fp/(fa*fa), 2)
    if imc < 18.6:
        cl = 'MAGREZA'
    elif imc < 25:
        cl = 'NORMAL'
    elif imc < 30:
        cl = 'SOBREPESO'
    elif imc < 40:
        cl = 'OBESIDADE'
    else:
        cl = 'OBESIDADE GRAVE'

    if fn and fp and fa:
        person = {'Nome': fn,
                  'Peso': fp,
                  'Altura': fa,
                  'Imc': imc,
                  'Classificacao': cl}
        MongoAPI(dataMongo).insertOne(person)

    entries = MongoAPI(dataMongo).read()

    return render_template('index.html', entries=entries, 
                           meuhost=meuhost)


@app.route('/action/<updel>/<person>', methods=['GET'])
def get_person(updel=None, person=None):
    entries = MongoAPI(dataMongo).readOne(str(person))
    if str(updel) == 'update':
        return render_template('update.html', entries=entries, 
                           meuhost=meuhost)
    elif str(updel) == 'delete':
        return render_template('delete.html', entries=entries, 
                           meuhost=meuhost)
    else:
        entries = MongoAPI(dataMongo).read()
        return render_template('index.html', entries=entries, 
                           meuhost=meuhost)


@app.route('/save', methods=['POST'])
def save():
    form = request.form
    oid = form.get('oid')
    fn = form.get('Nome')
    fp = float(form.get('Peso'))
    fa = float(form.get('Altura'))
    imc = round(fp / (fa * fa), 2)
    if imc < 18.6:
        cl = 'MAGREZA'
    elif imc < 25:
        cl = 'NORMAL'
    elif imc < 30:
        cl = 'SOBREPESO'
    elif imc < 40:
        cl = 'OBESIDADE'
    else:
        cl = 'OBESIDADE GRAVE'

    if fn and fp and fa:
        person = {'Nome': fn,
                  'Peso': fp,
                  'Altura': fa,
                  'Imc': imc,
                  'Classificacao': cl}
        MongoAPI(dataMongo).updateOne(oid, person)
    entries = MongoAPI(dataMongo).read()
    return render_template('index.html', entries=entries, 
                           meuhost=meuhost)


@app.route('/delete', methods=['POST'])
def delete():
    form = request.form
    oid = form.get('oid')
    if oid:
        MongoAPI(dataMongo).deleteOne(oid)
    entries = MongoAPI(dataMongo).read()
    return render_template('index.html', entries=entries, 
                           meuhost=meuhost)

@app.route('/metrics')
def mymetrics():
    PrometheusMetrics(app, group_by='path')
