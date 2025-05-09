from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string if needed
db = client['mydatabase']  # Replace 'mydatabase' with your database name
todos = db['todos']  # Replace 'todos' with your collection name

@app.route('/')
def index():
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todos.insert_one({'title': title, 'description': description})
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = todos.find_one({'_id': ObjectId(todo_id)})
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todos.update_one({'_id': ObjectId(todo_id)}, {'$set': {'title': title, 'description': description}})
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/delete/<todo_id>')
def delete(todo_id):
    todos.delete_one({'_id': ObjectId(todo_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    from bson.objectid import ObjectId
    app.run(debug=True, port=8000)
