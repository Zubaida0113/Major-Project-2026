from flask import Flask, request, render_template, jsonify
import sqlite3, os
import model

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect('complaints.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        trust REAL,
        priority REAL,
        triage REAL,
        category TEXT
    )''')
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('complaints.db')
    data = conn.execute("SELECT * FROM complaints").fetchall()
    conn.close()
    return render_template('admin.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['audio']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = model.process_audio(path)

    conn = sqlite3.connect('complaints.db')
    conn.execute("INSERT INTO complaints (text, trust, priority, triage, category) VALUES (?, ?, ?, ?, ?)",
                 (result['text'], result['trust'], result['priority'], result['triage'], result['category']))
    conn.commit()
    conn.close()

    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)