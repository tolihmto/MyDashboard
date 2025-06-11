import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# WIDGET ENDPOINTS

WIDGETS_FILE = 'widgets.json'

def read_widgets():
    if not os.path.exists(WIDGETS_FILE):
        with open(WIDGETS_FILE, 'w') as f:
            json.dump([], f)
    with open(WIDGETS_FILE) as f:
        return json.load(f)

def write_widgets(widgets):
    with open(WIDGETS_FILE, 'w') as f:
        json.dump(widgets, f)

@app.route('/api/widgets', methods=['GET'])
def get_widgets():
    return jsonify(read_widgets())

@app.route('/api/widgets', methods=['POST'])
def save_widgets():
    widgets = request.get_json()
    write_widgets(widgets)
    return jsonify({'status': 'ok'}), 200

# WEATHER ENDPOINTS

OPENWEATHER_API_KEY = '1c386c495b48de29a8c3da2173ca9672'

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
