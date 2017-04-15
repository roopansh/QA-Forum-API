#!flask/bin/python
from flask import Flask, jsonify, abort
import random 

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }

]
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/roopansh')
def roopanshHello():
	return str(random.randint(0,10))

@app.route('/task', methods=['GET'])
def task():
	return jsonify({'task' : tasks})

@app.route('/task/get/<int:task_id>', methods=['GET'])
def getTask():
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	return jsonify({'task' : task[0]})

if __name__ == '__main__':
    app.run(debug=True)