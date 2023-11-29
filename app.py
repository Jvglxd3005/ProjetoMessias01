import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente
os.environ['FLASK_DEBUG'] = 'True'

# Configurando o modo de depuração com base na variável de ambiente
app.debug = os.environ.get('FLASK_DEBUG') == 'True'

@app.route('/')
def ola():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/adicionar_glossario')
def adicionar_glossario():
    return render_template('adicionar_glossario.html')

@app.route('/fazer_agenda')
def fazer_agenda():
    return render_template('adicionar_agenda.html')

@app.route('/agenda')
def adicionar_agenda():
 #   return render_template('agenda.html')

    itens_agendados = []

    with open(
            'bd_agenda.csv',
            newline='', encoding='utf-8') as arquivo1:
        reader = csv.reader(arquivo1, delimiter=';')
        for l in reader:
            itens_agendados.append(l)

    return render_template('agenda.html',
                           agenda=itens_agendados)


@app.route('/criar_agenda', methods=['POST', ])
def criar_agenda():
    data = request.form['data']
    assunto = request.form['assunto']
    descricao = request.form['descricao']

    with open(
            'bd_agenda.csv', 'a',
            newline='', encoding='utf-8') as arquivo1:
        writer = csv.writer(arquivo1, delimiter=';')
        writer.writerow([data, assunto, descricao])

    return redirect(url_for('adicionar_agenda'))


@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open(
            'bd_glossario.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)

    return render_template('glossario.html',
                           glossario=glossario_de_termos)



@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open(
            'bd_glossario.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))

@app.route('/excluir_agenda/<int:agenda_id>', methods=['POST'])
def excluir_agenda(agenda_id):

    with open('bd_agenda.csv', 'r', newline='') as agd:
        reader = csv.reader(agd)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == agenda_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_agenda.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('adicionar_agenda'))

# @app.route('/pesquisar_termo/<int:termo_id>')
# def pesquisar_termo(termo_id):
#
#     with open('bd_glossario.csv', 'r', newline='') as file:
#         reader = csv.reader(file)
#         linhas = list(reader)
#
#     # Encontrar e excluir o termo com base no ID
#     for i, linha in enumerate(linhas):
#         if i == termo_id:
#             del linhas[i]
#             break



if __name__ == "__main__":
    app.run()