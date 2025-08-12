'''                        project 1 
     <  -----------------------------------------------------  >
              File Encryption and Decryption Tool '''
              
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        encrypted TEXT,
        key TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/encrypt', methods=['POST'])
def encrypt():
    key = request.form['key']
    message = request.form['message']
    encrypted = "".join(chr(ord(char) ^ int(key)) for char in message)
    
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (encrypted, key) VALUES (?, ?)", (encrypted, key))
    conn.commit()
    conn.close()
    
    return f"<h3>Message Encrypted and Saved.</h3><a href='/'>Back</a>"

@app.route('/decrypt', methods=['POST'])
def decrypt():
    key = request.form['key']
    
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted FROM messages WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()

    if result:
        encrypted = result[0]
        decrypted = "".join(chr(ord(char) ^ int(key)) for char in encrypted)
        return f"<h3>Decrypted Message: {decrypted}</h3><a href='/'>Back</a>"
    else:
        return "<h3>Invalid key. No message found.</h3><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
