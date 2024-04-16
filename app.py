from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os
import uuid
from datetime import datetime

app = Flask(__name__)

connection_string = 'mongodb+srv://amelia045:mongomell@cluster0.pjx2hyv.mongodb.net/'
client = MongoClient(connection_string)
db = client.dbDiary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    file = request.files["file_give"]
    profile = request.files["profile_give"]  # Mengambil file gambar profil

    # Lakukan sesuatu dengan file yang diunggah, seperti menyimpannya di server
    # Misalnya, menyimpan file di direktori 'static'
    file.save(f'static/{file.filename}')
    profile.save(f'static/{profile.filename}')  # Menyimpan gambar profil di direktori 'static'

    doc = {
        'title': title_receive,
        'content': content_receive,
        'image_path': f'/static/{file.filename}',  # Menyimpan jalur gambar
        'profile': f'/static/{profile.filename}'  # Menyimpan jalur gambar profil
    }
    db.diary.insert_one(doc)

    return jsonify({'message': 'Upload complete!'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
