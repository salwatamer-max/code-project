from flask import Flask, request, render_template_string
import mysql.connector
from datetime import datetime

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="noteuser",
    password="notepass",
    database="notesdb"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form['note']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO notes (content, timestamp) VALUES (%s, %s)", (note, timestamp))
        db.commit()

    cursor.execute("SELECT content, timestamp FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()

    return render_template_string('''
        <form method="post">
            <textarea name="note" placeholder="Write your note here..." rows="4" cols="50"></textarea><br>
            <input type="submit" value="Save Note">
        </form>
        <hr>
        {% for note in notes %}
            <p>🕒 {{ note[1] }}<br>📌 {{ note[0] }}</p>
        {% endfor %}
    ''', notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

