from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# In-memory task storage (store tasks temporarily)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_data = request.form
    task = {
        'id': str(uuid.uuid4()),  # Unique ID for each task
        'task': task_data['task'],
        'completed': False
    }
    tasks.append(task)
    
    # Log the task addition
    print(f"Task added: {task['task']} with ID: {task['id']}")
    
    return jsonify(tasks=tasks)

@app.route('/toggle/<task_id>', methods=['POST'])
def toggle_task(task_id):
    task = next(t for t in tasks if t['id'] == task_id)
    task['completed'] = not task['completed']
    
    # Log the task toggle
    print(f"Task toggled: {task['task']} with ID: {task['id']} - Completed: {task['completed']}")
    
    return jsonify(tasks=tasks)

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    
    # Log the task deletion
    print(f"Task deleted with ID: {task_id}")
    
    return jsonify(tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
