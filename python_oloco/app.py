from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

class tarefa:
    def __init__(self,id,titulo,descricao):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao

tarefas = []
tarefas_concluidas = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global tarefas
    if request.method == 'GET':
        return render_template('index.html', tarefas=tarefas, tarefas_concluidas=tarefas_concluidas)
    
    elif request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        id = len(tarefas) + 1
        if id > 1:
            tarefas[0].id = 1
            id = tarefas[-1].id + 1
        nova_tarefa = tarefa(id, titulo, descricao)
        tarefas.append(nova_tarefa)
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    global tarefas
    tarefas = [item for item in tarefas if item.id != item_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:items_id>', methods=['POST'])
def complete(items_id):
        global tarefas, tarefas_concluidas
        tarefas1 = next((item for item in tarefas if item.id == items_id))
        id = len(tarefas_concluidas) + 1
        if id > 1:
            tarefas_concluidas[0].id = 1 
            id = tarefas_concluidas[-1].id + 1
        nova_tarefa = tarefa(id, tarefas1.titulo, tarefas1.descricao)
        tarefas_concluidas.append(nova_tarefa)
        del tarefas[tarefas.index(tarefas1)]
        return redirect(url_for('index'))

@app.route('/delete_concluidas/<int:item_id>', methods=['POST'])
def delete_concluidas(item_id):
    global tarefas_concluidas
    tarefas_concluidas = [item for item in tarefas_concluidas if item.id != item_id]
    return redirect(url_for('index'))

@app.route('/retornar/<int:id_item>', methods=['POST'])
def retornar(id_item):
        global tarefas, tarefas_concluidas
        tarefas1 = next((item for item in tarefas_concluidas if item.id == id_item))
        id = len(tarefas) + 1
        if id > 1:
            id = tarefas[-1].id + 1
            tarefas[0].id = 1
        nova_tarefa = tarefa(id, tarefas1.titulo, tarefas1.descricao)
        tarefas.append(nova_tarefa)
        del tarefas_concluidas[tarefas_concluidas.index(tarefas1)]
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'tarefa'
    with app.app_context():
        app.run(debug=True)