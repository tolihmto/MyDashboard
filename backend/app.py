import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# WIDGET ENDPOINTS

WIDGETS_FILE = 'widgets.json'

# 🔁 Charge les widgets depuis le fichier
def read_widgets():
    if not os.path.exists(WIDGETS_FILE):
        return []
    with open(WIDGETS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# 💾 Sauvegarde les widgets dans le fichier
def write_widgets(widgets):
    with open(WIDGETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(widgets, f, indent=2)

# 🔁 Endpoint GET
@app.route('/api/widgets', methods=['GET'])
def get_widgets():
    return jsonify(read_widgets())

# 💾 Endpoint POST (remplace tous les widgets)
@app.route('/api/widgets', methods=['POST'])
def save_widgets():
    data = request.get_json()
    with open('widgets.json', 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({'status': 'success'})


@app.route('/api/widgets/<int:widget_id>', methods=['PUT'])
def update_widget_config(widget_id):
    widgets = read_widgets()
    for widget in widgets:
        if widget['id'] == widget_id:
            widget['config'] = request.get_json()
            break
    write_widgets(widgets)
    return jsonify({'status': 'updated'})



# WEATHER ENDPOINTS

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'city parameter is required'}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fr"
    res = requests.get(url)
    if res.status_code != 200:
        return jsonify({'error': 'City not found'}), 404

    data = res.json()
    return jsonify({
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    })

# TODOLIST ENDPOINTS

DATA_FILE = 'todos.json'

def read_todos():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE) as f:
        return json.load(f)

def write_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(read_todos())

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todos = read_todos()
    data = request.get_json()
    new_todo = {
        'id': len(todos) + 1,
        'text': data['text'],
        'done': False
    }
    todos.append(new_todo)
    write_todos(todos)
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todos = read_todos()
    data = request.get_json()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['text'] = data.get('text', todo['text'])
            todo['done'] = data.get('done', todo['done'])
            break
    write_todos(todos)
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = read_todos()
    todos = [todo for todo in todos if todo['id'] != todo_id]
    write_todos(todos)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
