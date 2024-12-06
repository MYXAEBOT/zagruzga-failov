from flask import Flask, render_template, request, flash

app = Flask(__name__)
import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)

cursor = conn.cursor()


@app.route('/')
def main():
    cursor.execute('SELECT * FROM instagram')
    data = cursor.fetchall()
    return render_template('main.html', data=data)

@app.route('/add/')
def add():
    return render_template('add.html')

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
    return 'Выполнено'


if __name__ == '__main__':
    app.run(debug=True)
