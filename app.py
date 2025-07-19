from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo"  # necessário para mensagens flash

# Função para conectar no banco
def get_db_connection():
    conn = sqlite3.connect('meu_banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabela se não existir
conn = get_db_connection()
conn.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        email TEXT UNIQUE NOT NULL
    )
''')
conn.commit()
conn.close()

# Página principal (listar)
@app.route('/')
def index():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

# Cadastrar
@app.route('/cadastrar', methods=('POST',))
def cadastrar():
    nome = request.form['nome']
    idade = request.form['idade']
    email = request.form['email']

    if nome and idade and email:
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nome, idade, email) VALUES (?, ?, ?)', (nome, idade, email))
            conn.commit()
            conn.close()
            flash('Usuário cadastrado com sucesso!')
        except sqlite3.IntegrityError:
            flash('Erro: e-mail já cadastrado.')
    else:
        flash('Preencha todos os campos.')
    return redirect(url_for('index'))

# Editar
@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        email = request.form['email']
        conn.execute('UPDATE usuarios SET nome = ?, idade = ?, email = ? WHERE id = ?', (nome, idade, email, id))
        conn.commit()
        conn.close()
        flash('Usuário atualizado!')
        return redirect(url_for('index'))

    conn.close()
    return render_template('editar.html', usuario=usuario)

# Deletar
@app.route('/deletar/<int:id>')
def deletar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Usuário deletado!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
