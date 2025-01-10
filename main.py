from cachelib import FileSystemCache
from datetime import timedelta
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_session import Session
import sqlite3
app = Flask(__name__)
app.secret_key = '12345'
app.config['SESSION_TYPE'] = 'cachelib'
app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir='flask_session', threshold=500)
Session(app)
import sqlite3
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()


@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == "GET":
        cursor.execute('SELECT * FROM instagram')
        data = cursor.fetchall()
        return render_template('main.html', data=data)
    elif request.method == "POST":
        cursor.execute('SELECT * FROM instagram')
        data = cursor.fetchall()

@app.route('/autorisation/', methods=['GET', 'POST'])
def autorisation():
    if request.method == 'POST':
        login = request.form['username']           
        password = request.form['password']
        cursor.execute('SELECT * FROM autorisation WHERE username = ? AND password = ?', [login, password])
        data = cursor.fetchall()

        if len(data) != 0:
            flash('Вход выполнен успешно!', 'success')
            session['login'] = True
            session['username'] = login
            session.permanent = False
            app.permanent_session_lifetime = timedelta(minutes=1)
            session.modified = True
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('main_page'))
        else:
            flash('Неправильное имя пользователя или пароль.', 'danger')
            return redirect(url_for('page_login'))
    return render_template('autorisation.html')


@app.route('/add/')
def add_page():
    cursor.execute('SELECT * FROM autorisation')
    data = cursor.fetchall()
    if 'login' not in session:
        flash('Необходимо залогиниться', 'danger')
        return redirect(url_for('page_login'))
    return render_template('add.html')


@app.route('/autorisation/save/', methods=['POST'])
def save_page():
    login = request.form['username']
    password = request.form['password']
    last_name = request.form['last_name']
    name = request.form['name']
    patronymic = request.form['patronymic']
    dender = request.form['dender']
    cursor.execute('SELECT * FROM autorisation WHERE username = ?', [login])
    data = cursor.fetchall()
    print(data)
    if data == []:
        cursor.execute(f'INSERT INTO autorisation (last_name, name, patronymic, gender, username, password) VALUES (?,?,?,?,?,?)', [name, last_name, dender, patronymic, login, password])
        conn.commit()
        flash('зарегался','success')

    else:
        flash('такое имя уже есть, меняй','danger')
        return redirect(url_for('autorisation'))
    return render_template('login.html')


@app.route('/upload/', methods=['POST'])
def save_post():
    image = request.files.get('image')

    title = request.form['title']
    file_name = f'static/uploads/{image.filename}'
    description = request.form['description']
    image.save(file_name)
    cursor.execute(f'INSERT INTO instagram (tittle, file_name, description) VALUES (?,?,?)',
                   [title, file_name, description])
    conn.commit()
    return redirect(url_for('main_page'))


@app.route('/login/', methods=['POST', 'GET'])
def page_login():

    return render_template('login.html')


@app.route('/search/', methods=['POST', 'GET'])
def found_user():

    return render_template('search.html')

@app.route('/search/result/', methods = ['POST,GEYT'])
def result():
    login = request.form['username']
    cursor.execute('SELECT * FROM autorisation WHERE username = ?', [login])
    data = cursor.fetchall()
    if data != []:
        pass



@app.route('/logout/')
def logout():
    session.clear()
    flash('вы вышли из профиля','danger')
    return redirect(url_for('page_login'))


if __name__ == '__main__':
    app.run(debug=True)
