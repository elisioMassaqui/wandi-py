from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_file():
    code = request.form['code']
    file_name = 'code.ino'
    folder_name = file_name.split('.')[0]

    # Cria o diretório se ele não existir
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Caminho completo para salvar o arquivo
    file_path = os.path.join(folder_name, file_name)

    # Escreve o conteúdo no arquivo
    with open(file_path, 'w') as f:
        f.write(code)

    # Mensagem de sucesso
    message = f'Arquivo "{file_name}" criado com sucesso na pasta "{folder_name}".'

    # Retorna a mensagem como uma resposta
    return message

@app.route('/open', methods=['POST'])
def open_file():
    file_path = request.form['file_path']

    # Lê o conteúdo do arquivo
    with open(file_path, 'r') as f:
        content = f.read()

    return content

if __name__ == '__main__':
    app.run(debug=True)
