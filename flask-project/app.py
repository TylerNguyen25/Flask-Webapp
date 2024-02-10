from flask import Flask, render_template, request, redirect, url_for, abort, g
import sqlite3

app = Flask(__name__)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = 'CREATE TABLE IF NOT EXISTS messages (message TEXT, handle TEXT)' 
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db
    
def insert_message(request):
    db = get_message_db()
    conn = db.cursor()

    msg = request.form['message']
    handle = request.form['name']
    cmd = f"INSERT into messages VALUES ('{msg}','{handle}')"
    conn.execute(cmd)
    db.commit()
    db.close()

def random_messages(n):
    db = get_message_db()
    conn = db.cursor()
    cmd = f'SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}'
    messages = conn.execute(cmd).fetchall()
    db.commit()
    db.close()
    return messages 

def delete_messages():
    db = get_message_db()
    conn = db.cursor()
    cmd = 'DELETE FROM messages'
    conn.execute(cmd)
    db.commit()
    db.close()

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        msg = "Message received"
        insert_message(request)
        return render_template('submit.html', note = msg )

@app.route('/view')
def ask():
    messages = random_messages(5)
    return render_template('ask.html', messages = messages)

@app.route('/delete')
def deleted():
    delete_messages()
    msg = "Database has been cleaned"
    return render_template('delete.html', note = msg)